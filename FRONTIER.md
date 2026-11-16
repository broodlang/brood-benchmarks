# Optimization frontier — where the gaps are and what would move them

The interpretation of the [benchmark data](BENCHMARKS.md), for contributors: what is slow, why,
what would close it and what has been ruled out. **Current position only.** History is in git
and in brood's `docs/devlog.md`; current numbers are in the [tables](BENCHMARKS.md).

No gap here is architectural; they are implementation headroom. On an interpreted row about 60%
of the time is the bytecode dispatch loop, so the broad levers are **dispatch cost** and
**JIT coverage**.

## What runs native

The tier-1 JIT covers:
- integer self-tail loops (`loop`, `collatz`);
- float loops (`mandelbrot`);
- indexed vector reads, hoisted out of loops (`matmul`; sound without alias analysis because data
  is immutable);
- tail and non-tail recursion over unboxed `i64`/`f64` with an overflow deopt (`fib`,
  `ackermann`);
- inline small-vector reads (`bintree`);
- `table-*` ops (`sieve`).

JIT'd callers link straight to JIT'd callees through an epoch-guarded link. Processes share one
compiled copy of each arm. A `def` deopts the code it affects, so hot reload holds.

## Where the gaps are

- **`spawn-live`** (Brood's weakest row, against the BEAM). The cost is the process floor: ~5.5 KB
  per live process against the BEAM's ~3.1 KB (inline caches, the `Process` box, mailbox,
  continuation). See levers 1–2.
- **`bintree`.** The call protocol: four non-tail calls per node. C loses this row to the
  garbage-collected runtimes, so "native allocation" is not the target. Lever 5.
- **`nqueens`.** Backtracking recursion: a `reduce` over `range` per node, `solve` still on the
  VM, a closure captured per node. C's margin is partly structural (it reuses a stack array), so
  Node is the fairer target.
- **`nbody`.** A fresh 7-element vector per body per step. Closing it needs escape analysis or a
  native float array. Lever 8.
- **`mandelbrot`, `matmul`.** Near the JIT floor; what remains is boxed 24-byte `Value` cells. Both
  rows are a few milliseconds in the fast columns, so read Brood's absolute time.
- **`pipeline`.** Lazy-seq and transducer composition the JIT doesn't cover. It does not allocate
  per element; about half the row is call plumbing for computed-head calls (lever 3).
- **`pingpong`, `ring`.** Per-message fixed cost: a mailbox lock, a wake, a re-enqueue and a
  matcher activation, over a floor of copied messages and migratable continuations (design). A
  `receive` loop cannot JIT. This is not what `latency` measures; that row's tail was spawn
  placement.
- **`json`.** The one codec still written in Brood (`regex` and `base64` run natively, so those
  rows no longer measure the interpreter). Profile parse and encode separately before optimising:
  the two halves are far from equal.
- **`sort`.** The comparator is already unboxed; the allocation volume is the cost.

## Measurement traps

- **A stale binary measures the old code without failing.** `std/` is compiled into the binary.
  Append garbage to the module and rerun: a success means you measured nothing.
- **A row that errors fast looks fast.** The published harness checks every checksum;
  `ab-bench` does not.
- **The first run in a process measures tiering.** Discard one run before timing.
- **Pinning charges you for the JIT.** `taskset` puts the background compiler on the benchmark's
  core, so extra compilation reads as a slowdown.
- **Equal instructions with different cycles is code layout**, not a regression; compare
  `perf stat` instructions before bisecting. (`mandelbrot` at 0.52.0 was this.)
- **A ramp below the gate has no culprit commit.** Five +2% changes make a real regression no
  bisect can find. Sample a few points first: a step means bisect, a ramp means a sweep.
- **`compute = wall − startup` miscorrects.** The `startup` row loads `io` and tiers nothing, so
  short rows partly measure module loading and warm-up, and a change to startup alone moves
  every row's compute.
- Use `(mem-bytes)` / `(mem-peak)` for allocation questions and RSS only for what the OS mapped.
  `release-fast` strips symbols; rebuild with `CARGO_PROFILE_RELEASE_FAST_STRIP=none
  CARGO_PROFILE_RELEASE_FAST_DEBUG=1` for `perf`.

## Levers (rough priority)

1. **Shrink the green-process floor** (`spawn-live`). The bytes are working state, not slack:
   shrink `CallIcEntry` (64 → ~48 B), or share inline-cache entries for frozen callees across
   processes. Measure at the parked state, which sets peak memory.
2. **A native `fold`** (~11% of `spawn-live`). It must keep map-as-pairs, seq fusion and exact
   error behaviour, and it is the prelude's most-used function.
3. **The computed-head call protocol** (`nqueens`, `pipeline`, `sort`, callbacks). Resolution is
   ruled out (below); what is left is frame setup and dispatch.
4. **Heap-walking code**: extend the inline small-vector read to variable indexes and in-arm
   allocation (blocked by safepoints at non-tail calls).
5. **Call inlining / bounded unroll**: the remaining `fib`/`bintree` lever.
6. **Interpreter dispatch**, which bounds every row the JIT doesn't cover.
7. **Wider LINMAP coverage**: `reduce`-style folds over non-integer values.
8. **Unboxed storage** for `matmul`/`nbody`, without breaking immutability.

## Measured and ruled out — don't re-attempt

- **Memoizing computed-head resolution.** Parity at the default ceiling and +7% `spawn-live`
  RSS: the memo costs more than the lookups it replaces.
- **Dropping the capture bail for `pipeline`.** That path is 0% of the row.
- **The `receive` matcher's missing native frame.** ~1.8% of `spawn-live`, inside the noise.
- **GC tuning for `bintree`/`nbody`.** Neither row is GC-bound, and larger nurseries make both
  worse.
- **Per-process inline caches as a speed lever.** On the VM a cached callee is no faster.
- **Three process-floor tunings.** Park-trim at 0 did nothing; capacity-1 slabs cost `bintree`
  +4.8%; dropping caches on park cost `pingpong` +26%.
- **Splitting shared compiled code from per-process tier state.** It would undo `spawn` −15%.
- Float back-edge store elision, in-IR call frame setup, always-on native-call timing, and
  `sort` comparator work.
