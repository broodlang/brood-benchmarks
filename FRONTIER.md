# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the *interpretation* of the [benchmark data](BENCHMARKS.md). The
[README](README.md) stays a plain "where we stand" for everyone else; the Brood repo's
`docs/devlog.md` and `docs/compute-frontier.md` hold the working notes and the history of
how each item got here. **This file states the current position only** — what is fast,
what is slow, what would close it, and what has already been measured and ruled out.

None of the gaps are architectural; they are implementation headroom. Profiling puts
~60% of an interpreted row's time in the bytecode dispatch loop (`vm_run_bc`), so the two
broad levers are **interpreter-dispatch cost** and **widening JIT coverage**. Numbers are
from the current run in [`results/report.md`](results/report.md).

## What runs native

The tier-1 JIT covers integer self-tail loops (`loop`, `collatz`), float-comparison loops
(`mandelbrot`), indexed array reads (`matmul`'s inner `dot`, via loop-invariant hoisting —
sound without alias analysis because Brood data is immutable), non-tail and tail-position
recursion (`fib`, `ackermann`), inline small-vector reads (`bintree`), and the JIT-lowered
`table-*` ops (`sieve`). Int/float recursion uses an unboxed i64/f64 register calling
convention with an overflow deopt. A JIT'd caller links straight to a JIT'd callee through
an epoch-guarded in-IR fast-link; processes of a runtime share one compiled copy of an
arm's native code and (for prelude closures) its bytecode; a `def` deopts affected code,
so hot reload holds.

## Where the gaps are

Ratios are Brood's compute vs the fastest language on that row.

- **`spawn-live` (3.47 s, 2.80 GB — last of five).** ~9 KB per live process against the
  BEAM's ~3 KB. Two known causes, in priority order: **user-code arms still compile
  per-process** (only prelude closures are shared — see lever 1), and the process floor
  itself is ~6 KB (mailbox, heap, captured continuation), of which ~2.9 KB is
  unattributed and wants a real allocation profile.
- **`nbody` (~23× Node, ~54× .NET)** — float physics rebuilding immutable body vectors
  every step. The residual *is* the rebuild. Closing it needs escape analysis that reuses
  the per-step vectors, or a native float-array primitive (philosophically fraught — see
  the immutability invariant). More a known immutable-cost data point than a target.
- **`bintree` (~103 ms, 6th; the BEAM is unusually fast here at ~12 ms)** — drifts in the
  95–115 ms band, trading places with Python/Ruby. The cost is the call protocol: ~77 ns
  per node over four non-tail calls. That is the X-register/call-convention redesign, not
  a tuning knob. The open watch-item.
- **`nqueens` (~12×)** — backtracking recursion; the `reduce`-over-`range` per node and
  the non-tail `solve`/`safe?` recursion dominate.
- **`mandelbrot` (~8×)** — `esc` is JIT'd with register-carried f64 params; the residual is
  boxed 24-byte `Value` tagging in the arithmetic plus loop overhead. Near the JIT floor.
- **`pipeline` (~8×)** — lazy-seq/transducer composition the JIT doesn't cover; allocation
  churn dominates. Blocker: `eduction`'s step closures capture, and the fast-link bails on
  captures.
- **`matmul` (the ~32× ratio is inflated by .NET's 4 ms denominator)** — inner loop is
  native; residual is the one read LICM can't hoist plus boxed `Value` array storage.
- **Message latency (`pingpong`, `ring` — Elixir leads ~2.8–3.5×)** — the widest honest
  gap. What remains is the per-candidate `vm_apply` in the mailbox scan over an
  irreducible floor of per-message immutable copies and heap-captured migratable
  continuations. That floor is design, not something traded away. Brood beats every
  thread/queue language here; Node's `ring` result is cooperative single-thread async.
- **Text codecs (`json`, `regex`, `base64` — all 6/7, ahead of Clojure)** — pure-Brood
  `std/` libraries against native codecs, by design. The next structural lever is a
  bytes/codepoint fast path shared by all three.
- **`sort`** — do not re-optimise the comparator (already unboxed). Still the suite's
  heaviest row for memory; the allocation volume is the cost, not collection.
- **`primes`, `loop`** — raw dispatch overhead, both already closed hard.

**Memory is not a frontier row.** Base RSS ~20 MB: 3rd-lightest of the seven and the
lightest of the compiled-class runtimes.

## Levers (rough priority)

1. **Share user-code arms across processes.** Prelude closures are shared per runtime
   (ADR-175); RUNTIME-keyed user arms are not, because those handles are freed and
   recycled (ADR-091) and the shared map would need free-epoch discipline. This is most of
   the residual `spawn-live` gap — a 40-arm user body still costs ~37 KB/proc. Paired
   sub-item: **split shared code from per-process JIT-tier state**, since a shared arm
   currently shares `jit_calls`/`jit_deopts`/`compile_epoch` (costs `collatz` ~8%, wins
   `sort` ~5%).
2. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — structure-walkers
   don't tier and some heap reads go through per-op FFI callbacks. Extending the proven
   inline small-vector read template to variable-index reads and in-arm alloc (blocked by
   non-tail-call safepoints) is the win toward Elixir. `pipeline` additionally wants the
   capturing-closure fast-link.
3. **True call inlining / bounded unroll** — removes calls rather than cheapening them;
   the remaining `fib`/`bintree`-class lever.
4. **Interpreter dispatch** — the ~60% `vm_run_bc` share bounds every un-JIT'd row.
5. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values.
6. **`matmul`/`nbody` unboxed storage** — boxed 24-byte `Value` vs a register
   `long`/`double`; any design must not violate the immutability invariant.

## Measured and ruled out — don't re-attempt

- **GC tuning for `bintree` / `nbody`.** Neither is GC-bound (45k and 798 objects copied
  per run; ~4% and ~2% of the row) and neither bails to the VM. Nursery sizing does
  nothing — flat across an 8K→128K sweep, and larger floors make both *worse*.
- **Float back-edge store elision** — ~0, absorbed by the store buffer.
- **In-IR call frame-setup** — measured regression, reverted. The FFI boundary is not the
  bottleneck.
- **Always-on native-call timing** — 8–22% on the message rows.
- **Comparator work in `sort`** — already unboxed.

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
