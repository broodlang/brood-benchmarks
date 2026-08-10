# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the interpretation of the [benchmark data](BENCHMARKS.md). **Current position
only** — what is fast, what is slow, what would close it, what is ruled out. History lives in the
Brood repo's `docs/devlog.md`.

No gap here is architectural; they are implementation headroom. ~60% of an interpreted row's time
is in the bytecode dispatch loop, so the broad levers are **dispatch cost** and **JIT coverage**.

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

- **`spawn-live` (1.75 s, 1.60 GB — 2.5× slower, 1.8× heavier than the BEAM).** ~5.5 KB per live
  process against ~3.1 KB. Moved 2026-08-05 (−16% wall, −26% CPU, A/B-corroborated): the previous
  entry claimed compiled code was no longer the cause, which was true of the mechanism and false in
  practice — sharing was keyed by the closure *handle*, and a no-capture closure is promoted afresh
  per creation, so 300k `spawn` thunks and 300k `receive` matchers each compiled their own copy
  (100,154 compiles per 100,000 units, 8.1 µs each). Keyed by AST now (ADR-215).
  Moved again 2026-08-06 (−9% wall, −11% CPU): `fold` now walks a vector by index, where coercing
  through `seq` and `first`/`rest` made `(rest v)` materialise the tail as a list — 27.7 → 15.0
  allocations per unit. And again 2026-08-10 (−8% wall, **−16% CPU**): the vector fold moved into a
  native counted loop that resolves a passthrough reducer like `+` once instead of per element, and
  `fold` now tests a vector first in its type dispatch instead of last. **The receive machinery was
  named here as what came next and has since been measured and retired** — worth ~1.8% of this row,
  inside the noise (see ruled-out). What is left is the process floor, which none of the four wins
  touched, and which wants a real allocation profile.
- **`nbody` (~11× Node, ~25× .NET)** — was ~23×/~54× until 2026-07-30; now 4/7, within 1.2× of
  Elixir. The cause was not the immutable rebuild this entry once blamed: the tier-time profile
  types an arm's *parameters* only, so a function whose floats arrive from a `def`'d constant read
  as non-float context, lowered its float multiply onto the integer path, and deopted on every
  activation until the sixteen-deopt rule bailed it to the interpreter — silent interpretation, no
  error, no failing test. Fixed by unboxing float-valued global reads behind the existing tag guard.
  What is left *is* the rebuild (a fresh 7-element vector per body per step), needing escape
  analysis or a native float array. A standing check fell out of it: **the JIT-vs-no-JIT ratio per
  row** — `fib` 54×, `collatz` 40×, but nbody 3.2×, which is what exposed the bail; `bintree` (3.5×)
  and `nqueens` (3.4×) are still in that band.
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
- **Message latency (`pingpong`, `ring` — Elixir leads ~2.7–3.3×)** — the widest honest gap, with
  its three large levers already taken: direct handoff (1.9×), the HOF matcher fast path (3.0×), and
  the leading-keyword receive filter that removed an O(rounds × backlog) rescan (backlog 500:
  ~420 ms → 34 ms). What is left per message is a mailbox mutex, a `wake_parked`, a re-enqueue and
  one matcher activation, over a floor of per-message copies and heap-captured migratable
  continuations — that floor is design. Brood beats every thread/queue language here; Node's `ring`
  is cooperative single-thread async.
  **Do not extend this to `latency`** — measured 2026-08-02, that row was never per-message cost
  (a send + receive is 1.1 µs); it was spawn placement.
- **Text codecs (`json`, `regex`, `base64` — all 6/7, ahead of Clojure)** — pure-Brood
  `std/` libraries against native codecs, by design. The next structural lever is a
  bytes/codepoint fast path shared by all three.
- **`sort`** — do not re-optimise the comparator (already unboxed). Still the suite's
  heaviest row for memory; the allocation volume is the cost, not collection.
- **`primes`, `loop`** — raw dispatch overhead, both already closed hard.

**Memory is not a frontier row.** Base RSS ~20 MB: 3rd-lightest of the seven and the
lightest of the compiled-class runtimes.

## Levers (rough priority)

1. **The green-process floor (~5.5 KB live vs the BEAM's ~3.1 KB)** — now the top lever on
   `spawn-live`, by elimination. Attributed: IC tables ~536 B, `Box<Process>` (the inline `Heap` is
   1376 B), `Arc<Mailbox>` 184 B, `Suspended` 128 B. **Working state, not slack** — three tunings
   were measured and reverted (see ruled-out). Closing needs it *smaller*, not dropped: shrink
   `CallIcEntry`, or share IC entries for frozen callees (sound — a sealed binding resolves
   process-independently). It is also the piece none of the last four wins touched: the row's peak
   RSS has sat near 1.6 GB throughout.

2. **The cold call into `fold` itself** — the largest remaining piece of the payload work, and
   already sized. After moving the vector fold into a native counted loop (`%vector-reduce`) and
   testing vectors first in the dispatch, `(fold + 0 p)` costs **27.1 µs/unit** against
   **23.9 µs** for calling `%vector-reduce` directly — so ~3.2 µs/unit is the cold call into the
   Brood-level `fold` wrapper, more than the reduce it performs (2.3 µs). Making `fold` native is
   the lever; it is a real change, not a reorder, because it must keep map-as-pairs, seq-view
   fusion (which calls a Brood transducer back), and the exact error/promotion behaviour.

3. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — structure-walkers
   don't tier and some heap reads go through per-op FFI callbacks. Extending the proven
   inline small-vector read template to variable-index reads and in-arm alloc (blocked by
   non-tail-call safepoints) is the win toward Elixir. `pipeline` additionally wants the
   capturing-closure fast-link.
4. **True call inlining / bounded unroll** — removes calls rather than cheapening them;
   the remaining `fib`/`bintree`-class lever.
5. **Interpreter dispatch** — the ~60% `vm_run_bc` share bounds every un-JIT'd row.
6. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values.
7. **`matmul`/`nbody` unboxed storage** — boxed 24-byte `Value` vs a register
   `long`/`double`; any design must not violate the immutability invariant.

## Measured and ruled out — don't re-attempt

- **The receive machinery / the matcher's missing native fast frame — was lever 1, retired
  2026-08-10.** The finding itself stands: a `receive` whose pattern **compares a literal** —
  `[:go v]`, `[:reply ^r v]`, i.e. essentially every real one — generates a matcher that lowers to
  native, deopts, is latched off, and thereafter pays the interpreter's call trampoline instead of
  the JIT's fast frame. What was wrong was its *size* on this row. Measured directly, by running
  the `spawn-live` unit with three receive patterns doing identical work, interleaved, three
  rounds: `[:go p]` (bails) **28.0 µs/unit**, `[t p] :when (%eq t :go)` (also bails) **27.8**,
  `[_t p]` (stays native) **27.5**. That is ~1.8% with overlapping spreads. The guard row is the
  control that makes it readable — it bails like the tag row, so the small gap is the native frame
  and not the skipped comparison. The compiled arm is shared process-wide, so 16 deopts bail it
  for all 300k units, and it *still* buys nothing.

  Two corrections worth keeping. The matcher does **not** deopt per activation: it deopts exactly
  **16** times, `jit_deopt_feedback` latches it `BAILED`, and the remaining ~284k calls are
  declined before running — the old "~282k deopts" came from `jit_deopt`, which counts `jit_tier`'s
  outcome-1 only and is blind to the HOF fast frame the matcher uses. That also dissolves the
  standing puzzle "an arm that no longer deopts still fails to link": `BAILED` is sticky, so
  removing the deopt source does not un-bail an arm that already bailed. It may still be worth
  something on a long-lived message row (`latency`, `pingpong`, `supervisor`) — untested, and the
  only remaining reason to look.

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
- **Per-process inline caches — withdrawn as a lever (2026-08-05).** This list's top item for two
  revisions, on the strength of a counter: a fresh unit misses ~half its call sites. The counter was
  true and the inference wrong. Sized against the `ns_*` timers it is ~2 µs of a 33 µs unit, and a
  purpose-built A/B found a *cached* callee no faster than re-resolving one on the VM — the computed
  head measured slightly **faster**, because the global path pays an IC probe and validation while
  the computed path reads a slot. On a short-lived process the IC arm is worse still, since it pays
  install and tiering cost it never amortises. A high miss *rate* is unavoidable on a process that
  makes five calls; it is not the same as a high cost.
- **Splitting shared compiled code from per-process JIT-tier state.** The `collatz`/
  `nqueens` regression that motivated it is an artifact of `make ab`'s single-core pin —
  the background JIT compiler competes with the benchmark for that core. Unpinned, and
  under this harness's own pinning, there is no regression. Sharing deliberately makes
  more prelude arms tier up (18 lowered vs 7); splitting the state would undo `spawn`
  −14.8% to fix nothing.

See [`results/report.md`](results/report.md) for the current numbers and
[`results/positioning.svg`](results/positioning.svg) for the compute-vs-memory map.
