# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the *interpretation* of the [benchmark data](BENCHMARKS.md). This is where
implementation suggestions live — the [README](README.md) stays a plain "where we stand" for
everyone else. (The Brood repo's `docs/compute-frontier.md` holds the deeper working notes and
play-by-play; this file is the current benchmark-suite read.)

None of the gaps below are architectural — they are implementation headroom in a young runtime.
Profiling puts ~60 % of an interpreted benchmark's time in the bytecode dispatch loop (`vm_run_bc`),
so the two broad levers are **interpreter-dispatch cost** and **widening JIT coverage**.
Numbers below are from the 2026-07-27 run unless dated otherwise.

## What runs native vs interpreted

The tier-1 JIT covers: integer self-tail loops (`loop`, `collatz`), float-comparison loops
(`mandelbrot`), indexed array reads (`matmul`'s inner `dot`, via loop-invariant hoisting — sound
with no alias analysis because Brood data is immutable), **non-tail and tail-position recursion**
(`fib`, `ackermann`), inline small-vector reads (`bintree`), and the JIT-lowered `table-*` ops
(`sieve`). For int-/float-only recursion an **unboxed-i64/f64 register calling convention**
(2026-07-02) carries args/results in registers with an overflow deopt — the lever that took `fib`
227 → 58 ms and `pfib` 847 → 188 ms. A JIT'd caller links straight to a JIT'd callee through an
epoch-guarded in-IR fast-link; workers share one compiled copy of an arm's native code; a `def`
deopts affected code, so hot reload holds.

**The native-stack guard now costs a call (2026-07-27, brood `f11f4cb`) — the newest recoverable
item on this list.** Deep recursion through JIT'd code could run the *native* stack into its guard
page: an abort, so it killed the OS process rather than the green one, and `try`/`catch` never saw
it. The fix stamps `Heap::jit_stack_limit` from the live remaining stack before entering native
code, checks it in every lowered arm's prologue (three instructions), and — because
`jit_native_depth` under-counts recursion that re-enters Rust through `brood_rt_call_slow` — makes
`jit_dispatch_call`'s headroom probe **unconditional** instead of skipping it below depth 64.
Measured cost, three-binary A/B (`26939e2` / `f11f4cb` / `1a3fc1c`, best-of-7, same build flags):
`fib` wall 70 → 86 ms, `pfib` 183 → 239 ms — ~+30% of compute on the two call-bound rows, and
nothing after `f11f4cb` moves them further. Correctness worth paying for; the *price* is not
obviously irreducible:

- The prologue check is 3 instructions against a preloaded absolute address — cheap by
  construction, and it is the part that cannot be dropped.
- The suspicious half is `stamp_stack_limit`, which calls `stacker::remaining_stack()` on **every**
  `jit_run_fast_link` — and the fast link is the ~26 ns Brood→Brood path `fib` lives on. The limit
  is an absolute address valid for the whole thread stack, so re-deriving it per link is redundant:
  stamping only at the *outermost* native entry (`jit_native_depth == 0`, plus wherever a green
  process is (re)scheduled onto a worker, since stack bases differ) should keep the guard sound
  while taking the probe off the hot path. Unmeasured — the obvious next experiment.
- The unconditional probe in `jit_dispatch_call` is the other candidate; that one is on the slow
  call path, which the commit notes already does far more work than a thread-local read.

Still interpreted (or only partly JIT'd) — the weak rows; ratios are Brood's compute vs the fastest
language on that row:

- **`nbody` (327 ms; ~25× Node, ~53× .NET's 6 ms)** — float physics rebuilding immutable body
  vectors every step. Vector + float-JIT work took it from 5.9 s; the residual is the rebuild
  itself. Closing further needs escape analysis that reuses the per-step vectors, or a native
  float-array primitive (philosophically fraught — see the immutability invariant). A known
  immutable-cost data point more than a target.
- **`bintree` (113 ms, 6th — the BEAM is unusually fast here at ~10 ms)** — inline small-vector
  storage closed it to 90 ms once; it has since drifted in the 95–115 ms band run-to-run,
  trading places with Python/Ruby. **The one open watch-item.** Remaining known headroom: the
  non-tail-call safepoints in `check`/`make` block the in-arm alloc inline.
- **`nqueens` (83 ms, ~12×)** — backtracking recursion; the `reduce`-over-`range` per node and the
  non-tail `solve`/`safe?` recursion dominate.
- **`mandelbrot` (173 ms, ~9×)** — `esc` is JIT'd with register-carried f64 params (verified via
  CLIF); the residual is the boxed 24-byte `Value` tagging in the arithmetic itself plus loop
  overhead. Eliding back-edge slot stores was prototyped → ~0 (absorbed by the store buffer;
  don't re-attempt). Near the current JIT floor.
- **`pipeline` (32 ms, ~8×)** — lazy-seq / transducer composition the JIT doesn't cover;
  allocation churn dominates. The known blocker: `eduction`'s step closures capture, and the
  fast-link bails on captures.
- **`sort` (194 ms, ~3.0×)** — `(sort nums)` is native `%sort-asc`, and **the sorting is no longer
  the expensive part of it.** Phase-isolated at 375k ints (best-of-11, same binary): building the
  input list ~99 ms, the `sort` call ~79 ms, the checksum walk ~14 ms. Of that sort call, comparison
  is now a few ms — brood `1749307` unboxes the all-`Int` case to a raw `Vec<i64>` (106 → 79 ms,
  −25%), so what remains is `seq_items` walking the cons spine in and `heap.list` allocating a fresh
  375k-cell list out. That is allocation, the same frontier as `bintree`/`nbody`, and it is also why
  this row is the suite's heaviest for memory (188 MB, 7/7). Do not re-optimise the comparator.
  (Earlier editions of this file said the cost was "building the input list"; that was measured
  wrong — the sort call was the larger half.)
- **`matmul` (134 ms; the ~33× ratio is inflated by .NET's 4 ms denominator)** — the inner loop is
  native; the residual is the one read LICM can't hoist plus boxed `Value` array storage.
- **`primes` (46 ms, ~5×), `loop` (42 ms, ~4×)** — raw dispatch overhead; both already closed
  hard (loop was 304 ms before the 2026-07-16 match-lowering + call-gate round).

**Memory is not a frontier row.** Base RSS is **20 MB** — 3rd-lightest of the seven, a megabyte
behind Ruby, and the lightest of the compiled-class runtimes. (The ~28 MB carried until 2026-07-26 was the
pre-boot-cache source boot: the harness took min wall but max RSS across runs, so the post-rebuild
cache populate kept landing in the memory column alone. Fixed with a warmup run. Methodology lesson
worth keeping — an asymmetric best-of/worst-of aggregation hides improvements as readily as it
manufactures regressions.)

Closed rows worth remembering when reading ratios: `wordcount` (~13× → 1.1×, LINMAP + dense-Table),
`errors`/`errors-deep` (2nd–3rd — .NET is *worst* at deep error recovery at ~670 ms, a reminder
that compute-loop-only views mislead), `pfib` (2nd, ~93 % of the machine's parallel-scaling
ceiling, ahead of Elixir).

## Wider-range findings (2026-07-12 additions, updated)

Ranked by what's left, not by history — the war-story details live in the Brood repo devlog:

1. **Message-passing latency (`pingpong` 188 ms, `ring` 716 ms — Elixir leads ~2.8–3.5×).** Still
   the widest honest gap, but the smallest it has been — closed from ~14× by four rounds, most
   recently ADR-155 (emit `receive` clause bodies at the call site instead of wrapping each in a
   thunk, which also made the matcher arm JIT-lowerable): `ring` −48%, `pingpong` −21%.

   What is left is the per-candidate `vm_apply` in the mailbox scan (`BROOD_NO_HOF=1` is
   197 → 509 ms, so that protocol still does real work) over an irreducible floor of per-message
   immutable copies and heap-captured migratable continuations — design, not traded away. Brood
   beats every thread/queue language soundly; Node's `ring` "win" is cooperative single-thread
   async.
2. **Text codecs (`json` 148 ms, `regex` 88 ms, `base64` 107 ms — all 6/7, ahead of Clojure).**
   Pure-Brood `std/` libraries vs native codecs, by design. The residual ~10–40× is honest
   interpreted-library cost; next structural lever would be a bytes/codepoint fast path shared by
   all three.
3. **`sieve` 36 ms (3rd) and `persistent-map` 63 ms (4th)** — largely closed by the lock-free
   dense int-key `Table` + JIT-lowered `table-*` ops (+ the fused `map-int-add` idiom). What's
   left is the expected floor of a Table standing in for a mutable bool array, and CHAMP
   path-copy under read-modify-write.
4. **`ackermann` 360 ms (3rd)** — was 4.1 s dead last; the i64 register worker now recognises
   tail self-calls and the stale depth cap is gone. Any mixed tail+non-tail int recursion rides
   registers.

## Candidate levers (rough priority)

0. **Hoist `stamp_stack_limit` out of `jit_run_fast_link`** — the cheapest known win on the board,
   because it is recovering a cost we just measured (~30% of `fib`/`pfib`) rather than finding a
   new one. Stamp at the outermost native entry and at green-process (re)scheduling, not per fast
   link. Must keep the KI-14 guarantee intact: `tests/jit_deep_recursion_test.blsp` aborts the
   process if the guard regresses, so it is a self-checking change.
1. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — the structure-walkers still
   don't tier and some heap reads go through per-op FFI callbacks. The inline small-vector
   storage + read template is proven; extending it to variable-index reads and in-arm alloc
   (blocked by non-tail-call safepoints) is the remaining win toward Elixir. `pipeline`
   additionally wants the capturing-closure fast-link (fill capture slots in the fast frame).
2. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the
   remaining `fib`-class lever. (A measured attempt to move call frame-setup into JIT IR
   regressed and was reverted — the FFI boundary is not the bottleneck.)
3. **Interpreter dispatch** — the ~60 % `vm_run_bc` share bounds every un-JIT'd row.
4. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values
   (needs Tables holding non-serialisable `Value`s, or a type-directed variant).
5. **`matmul`/`nbody` unboxed storage** — a boxed 24-byte `Value` vs a register `long`/`double`;
   any unboxed-array design must not violate the immutability invariant.

Dead ends (measured; don't re-attempt): float back-edge store elision (~0 — store buffer),
in-IR call frame-setup (reverted), always-on native-call timing (8–22 % on message rows).

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
