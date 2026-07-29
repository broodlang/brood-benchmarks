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
arm's native code *and* its bytecode — compiled once per runtime, not once per process; a
`def` deopts affected code, so hot reload holds.

## Where the gaps are

Ratios are Brood's compute vs the fastest language on that row.

- **`spawn-live` (3.03 s, 1.97 GB — last of five).** ~6.6 KB per live process against the
  BEAM's ~3 KB. Compiled code is no longer the cause: every shared-region closure
  (prelude *and* user code) compiles once per runtime. What is left is the process itself
  — mailbox, isolated heap, captured continuation — and roughly half of it is
  **unattributed**. Attributing it wants a real allocation profile; whole-program
  differencing has been taken as far as it goes (per-phase `live_bytes()` deltas are
  invalid — the counter is process-wide across workers).
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

1. **The green-process floor (~6.6 KB RSS / ~4.5 KB allocated, vs the BEAM's ~3 KB).**
   Now that compiled code is shared per runtime, this is the whole of the `spawn-live`
   gap. Attributed per structure: the **inline-cache tables are 664 B** (`vm_call_ics`
   384, `vm_fast_links` 160, `arm_ic_blocks` 120) of ~1144 B of per-process tables, on
   top of `Box<Process>` 1840 B, `Arc<Mailbox>` 184 B and `Suspended` 128 B.

   **It is working state, not slack** — three tunings were measured and all reverted (see
   the ruled-out list). Closing on the BEAM needs the state to be *smaller*, not dropped:
   shrink `CallIcEntry` (96 B, of which the `fast` memo is 32), or share IC entries for
   frozen callees across processes (ADR-175 Stage 3 — sound because a sealed binding's
   resolution is process-independent). Both are design changes; cost them before starting.

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
- **Three tunings of the green-process floor.** (a) Park-trim threshold at 0 (always
  trim): no change at all. (b) Capacity-1 first touch for the slab `Vec`s — predicted
  ~700 B/proc, delivered 110 B, and cost `bintree` +4.8% in extra reallocs. (c) Dropping
  the inline-cache tables when a process parks: safe and effective on memory (floor 4.53
  → 3.89 KB/proc, `spawn-live` 2.00 → 1.75 GB) but **`pingpong` +26% / `ring` +18%**, and
  restricting it to the first park barely helped (+11.5% / +16.9%) — the cost is a process
  losing caches it built at startup and rebuilding them entering its hot loop, not the
  frequency of dropping.
- **Splitting shared compiled code from per-process JIT-tier state.** The `collatz`/
  `nqueens` regression that motivated it is an artifact of `make ab`'s single-core pin —
  the background JIT compiler competes with the benchmark for that core. Unpinned, and
  under this harness's own pinning, there is no regression. Sharing deliberately makes
  more prelude arms tier up (18 lowered vs 7); splitting the state would undo `spawn`
  −14.8% to fix nothing.

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
