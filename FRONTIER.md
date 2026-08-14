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

Ratios are Brood's compute vs the fastest language on that row. **From 2026-08-14 that is usually
C**, which now runs the 16 compute rows as a machine-floor reference and leads 14 of the 15 it
shares with the aggregate. Ratios on those rows therefore got larger without Brood moving —
they are now "vs roughly the hardware" rather than "vs the fastest managed runtime". Where the
old denominator is the more useful one it is named explicitly below.

- **`spawn-live` (1.76 s, 1.62 GB — 2.5× slower, 1.8× heavier than the BEAM).** ~5.5 KB per live
  process against ~3.1 KB. **Flat 2026-08-13** (0.3.9 → 0.3.11), and flat by measurement rather
  than by silence: a fixed-baseline A/B reads CPU **+1.1%** (per-side spreads 5.5% / 7.0%) and wall
  −0.6% against a 0.9% floor. That ends a run of four consecutive moves; nothing in the 56 commits
  of that range touched this row, which is consistent with the standing diagnosis that what is left
  is the process floor. Moved 2026-08-05 (−16% wall, −26% CPU, A/B-corroborated): the previous
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
- **`nbody` (~12× Node, ~27× .NET)** — was ~23×/~54× until 2026-07-30; now 4/7, within 1.3× of
  Elixir. The 2026-08-13 harness read it **−7.1%, which an A/B did not confirm** (−0.9%, verdict
  noise) — a reminder that a single harness row is one best-of-3 sample, not a result; do not
  bank this as a win. The cause was not the immutable rebuild this entry once blamed: the
  tier-time profile
  types an arm's *parameters* only, so a function whose floats arrive from a `def`'d constant read
  as non-float context, lowered its float multiply onto the integer path, and deopted on every
  activation until the sixteen-deopt rule bailed it to the interpreter — silent interpretation, no
  error, no failing test. Fixed by unboxing float-valued global reads behind the existing tag guard.
  What is left *is* the rebuild (a fresh 7-element vector per body per step), needing escape
  analysis or a native float array. A standing check fell out of it: **the JIT-vs-no-JIT ratio per
  row** — `fib` 54×, `collatz` 40×, but nbody 3.2×, which is what exposed the bail; `bintree` (3.5×)
  and `nqueens` (3.4×) are still in that band.
- **`bintree` (7.4×; the BEAM is unusually fast here at ~15 ms — and beats C)** — the one row C
  does not lead: malloc/free on ~819k short-lived nodes loses to a generational collector, which
  is worth knowing before treating "native allocation" as the target. Drifts in the
  95–115 ms band, trading places with Python/Ruby. The cost is the call protocol: ~77 ns
  per node over four non-tail calls. That is the X-register/call-convention redesign, not
  a tuning knob. The open watch-item.
- **`nqueens` (31.4× C, 12.0× Node)** — backtracking recursion; the `reduce`-over-`range` per node
  and the non-tail `solve`/`safe?` recursion dominate. Note C's margin here is partly structural:
  it pushes onto a stack array where Node and .NET copy the placed-columns list per node, so the
  12× against Node is the fairer number to optimise against.
- **`mandelbrot` (10.6× C, 8.9× .NET)** — `esc` is JIT'd with register-carried f64 params; the
  residual is boxed 24-byte `Value` tagging in the arithmetic plus loop overhead. Near the JIT
  floor. That C is only 1.2× ahead of .NET here says the row is close to its arithmetic limit
  for everyone, which is the useful reading.
- **`pipeline` (9.0×) — REGRESSED +9.3%, bisected to `98e97308` (ADR-224).** Lazy-seq/transducer
  composition the JIT doesn't cover; allocation churn dominates. Blocker: `eduction`'s step
  closures capture, and the fast-link bails on captures.

  The regression bisects cleanly to **`98e97308` "reach a shared compiled arm through a
  process-local handle"**, confirmed against its own parent: **+5.8%** in a sweep and **+5.7%**
  re-run alone against a 1.9% floor. The mechanism is the commit working as designed. It removes
  multi-core contention — three `Arc` clones per call on one shared refcount cache line, which had
  `pfib` stalled at 769% cores — by routing every call through a process-local `ArmHandle` created
  per (process, call site) at IC-fill. That is a 3.19× multi-core win. **Single-threaded there is
  no contention to relieve, so the indirection is pure cost**, and a row that calls a closure per
  element pays it per element.

  Not a diligence failure: the commit ran an 8-row `make ab` and explicitly accepted a known +1.8%
  on `spawn-live`. The 8 rows just did not include this one. If the trade is worth keeping — and
  on the `pfib` numbers it probably is — this row's ~6% is the price, and should be recorded as
  such rather than chased.

  The remaining ~3.5% (bisected step +5.7%, end-to-end +9.3%) is not attributed; see `primes`
  below for why that is expected rather than a loose end.
- **`matmul` (49.5× C, 29.3× .NET)** — inner loop is native; residual is the one read LICM can't
  hoist plus boxed `Value` array storage. Both denominators are small (2.6 ms and 4.4 ms), so the
  ratio is dramatic on a row where everyone is fast; read the absolute, not the multiple.
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
- **`primes` (7.1× C, 5.4× .NET) — REGRESSED ~+6%, and it does NOT bisect. Read this before
  hunting it.** Raw dispatch overhead, previously closed hard, which is what made it worth a look.
  The regression is real and reproduces on demand: +7.2% one day and +5.8% the next, each against
  a 1.4% floor, end to end across 0.3.9 → 0.3.11.

  **But there is no culprit commit.** A bisect over the range landed on `69b03dcb`, which changes
  exactly one file — `tests/tcp_test.blsp`, a Brood test that cannot touch the compiled runtime —
  and A/B'ing that commit against its parent reads +1.4% against a 1.4% floor, i.e. nothing. The
  bisect had to return *something*, so it returned the commit that happened to sit on the far side
  of the threshold. Intermediate points bear this out: 69 → 68 → 70 → 74 ms across the range is a
  ramp, not a step. `98e97308` contributes ~+2.9% of it (measured, and correctly called noise at
  the time).

  **The methodological point is the finding, and it generalises.** The A/B gate rejects anything
  under 5% or twice the row's floor, so a change worth +2–3% passes as noise — correctly, on its
  own evidence. Five such changes are a real 6% regression that no individual gate ever saw and no
  bisect can localise, because no single step crosses the line. Do not spend another bisect on this
  row. If it matters, the tools that fit are a per-commit sweep recording absolutes for trend
  rather than pass/fail verdicts, or profiling 0.3.11 directly against 0.3.9 to find where the time
  went. `loop` stayed flat (+0.9%) throughout, so it is not general dispatch cost.

**Memory is not a frontier row.** Base RSS ~23 MB: 4th-lightest of the eight and the lightest of
the *managed* runtimes. C's 1.6 MB is the new floor and is not a target — it is a process with no
runtime in it; the meaningful comparison stays Python 9.8, Ruby 19.0, .NET 25.9, Node 42.7.

## Levers (rough priority)

1. **The green-process floor (~5.5 KB live vs the BEAM's ~3.1 KB)** — now the top lever on
   `spawn-live`, by elimination. Attributed: IC tables ~536 B, `Box<Process>` (the inline `Heap` is
   1376 B), `Arc<Mailbox>` 184 B, `Suspended` 128 B. **Working state, not slack** — three tunings
   were measured and reverted (see ruled-out). Closing needs it *smaller*, not dropped: shrink
   `CallIcEntry`, or share IC entries for frozen callees (sound — a sealed binding resolves
   process-independently). It is also the piece none of the last four wins touched: the row's peak
   RSS has sat near 1.6 GB throughout.

2. **The cold call into `fold` — worth ~11% of `spawn-live`, and the number is now
   decomposed.** After the native vector reduce and the dispatch reorder, `(fold + 0 p)` costs
   **26.6 µs/unit** against **23.7 µs** for calling `%vector-reduce` straight from the unit
   body. Measured 2026-08-10 by inserting trivial forwarders to separate "fold" from "a call":

   | unit body | µs/unit |
   |---|---|
   | `(%vector-reduce + 0 p)` | 23.7 |
   | one trivial Brood fn forwarding to it | 24.3 |
   | two nested forwarders | 25.4 |
   | `(fold + 0 p)` | 26.6 |

   So **a bare Brood-level call in a freshly spawned process costs ~0.85 µs**, and `fold`'s
   2.9 µs is that call *plus* its own `vector?` predicate call plus argument handling. Making
   `fold` native removes all of it, which is ~11% of this row — worth doing, and worth knowing
   it is 11% and not more before starting.

   **It is a real change, not a reorder.** `fold` must keep map-as-pairs, seq-view fusion
   (which applies a Brood transducer and recurses), and exact error/promotion behaviour — and
   note `seq` is *not* a Rust builtin, so the generic path has to call back into Brood. It is
   also the most-used function in the prelude, so the regression surface is the whole library.

   **The per-call tax generalises and may be the bigger lever.** ~0.85 µs for one call in a
   cold process is a tax every prelude call in this row pays, not just `fold`'s. Whatever makes
   a first-call-in-a-process cheap would pay out across `spawn-live` far more broadly than
   nativising one function. That is unmeasured and is the thing to look at first.

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
