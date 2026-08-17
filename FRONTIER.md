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
- **`nbody` (~12× Node, ~27× .NET) — READ THIS BEFORE PUBLISHING AN `nbody` NUMBER.** The row was
  **dead** from 2026-08-14 to 2026-08-17 (`unbound symbol: sqrt` — brood ADR-227 moved `sqrt` into
  `std/math.blsp` and this repo was never migrated; a full harness run would have failed on it),
  and fixing it correctly costs **~1.8×**: the kernel's `sqrt` call-site JIT inline requires a
  **bare** head resolving to a **PRELUDE** closure, and post-move neither spelling qualifies, so
  every `sqrt` now pays a closure call plus the wrapper's two `cond` comparisons. Measured, pinned:
  **0.38–0.40 s with the inlined native vs 0.66–0.74 s through `math/sqrt`** (microbench: 406 vs
  754 ms). So **an `nbody` figure measured now is ~1.8× off its pre-2026-08-14 self and is NOT a
  runtime regression** — see brood `docs/known-issues.md` KI-44, whose performance half is open.
  Was ~23×/~54× until 2026-07-30; then 4/7, within 1.3× of
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
- **`pipeline` (9.0×) — the +9.3% regression is RECOVERED (ADR-228, 2026-08-14), and it was not
  the unavoidable price this entry priced it as.** Lazy-seq/transducer composition the JIT
  doesn't cover; allocation churn dominates. A/B measured against **two** bases, and the runs
  disagree by more than a couple of points, so the range is what is claimed: **−9.1% vs
  `26b04e36` and −5.6% vs `a57cc573`** (both best-of-15, default ceiling), **−6.2% then −4.7%**
  at ceiling 1. It improves on every run and at both ceilings — the direction is settled and
  ADR-224's +9.3% is substantially recovered — but the **size is uncertain within ~5–9%**, and
  the `floor` column read 0.0% on several of these, which at integer-millisecond output means
  "below the resolution", not "no noise". Pinning it wants a fixed baseline binary plus a
  base-vs-base control at higher N. Not yet in a published harness run — the ratio above is the
  last published one. `nqueens` came with it at **−6.2% then −4.4%** (ceiling 1), which
  *straddles* the `max(5%, 2×floor)` gate and so is not claimed as certified either.

  **What ADR-224 actually cost, and why the diagnosis below stopped one step short.** The entry
  was right that a closure-per-element row pays ADR-224 per element, and wrong that the cost was
  "pure indirection". `exec_chunk`'s call arm states that a **computed head takes no inline
  cache** — and ADR-224 creates its handle at *IC-fill*. So on this row there was no IC to fill:
  every element allocated a fresh `Arc<ArmHandle>` **and** cloned the shared
  `Arc<CompiledArm>`, an atomic RMW on the very cross-process cache line KI-40 is about.
  Memoizing the handle per `(closure, argc)` in the `vm_cache` entry the path already consults
  removes both. `pfib` at ceiling 1 is unchanged (−1.9% against a 0.7% floor), so ADR-224's
  3.19× is intact — a `vm_cache` is per-process, so no handle is shared across processes.
  `nqueens` improves with it too (see above) — a new win rather than a recovery, though not one
  that clears the gate on both runs.

  The lesson worth carrying: "the commit working as designed, so the cost is the price" was a
  *plausible* reading of a clean bisect, and it closed the question one level above the
  mechanism. The bisect was correct; the conclusion drawn from it was not.

  **The blocker named here for two revisions — "`eduction`'s step closures capture, and the
  fast-link bails on captures" — is wrong, and was killed by profiling on 2026-07-03 (the
  correction now lives with the lever it retired, in the brood repo's
  `docs/compute-frontier.md` — the 2026-07-02 block's "Next levers", item 1). It is restated
  here because this file is what a contributor reads first.** Two independent reasons:
  the bail is on the **elided free-global in-IR fast-link**, and `perf` measured that path at
  **0% of pipeline** — a transducer step is a **computed head** (a captured `rf`/`f`), so it never
  reaches the elided fast-link at all; and separately, both JIT fast frames now **fill** capture
  slots from the captured env rather than refusing the arm (`jit_runtime.rs`'s native→native
  link and `hof_apply_native`, verified present on 2026-08-14). Do not spend a session dropping
  a capture bail for this row.

  **What actually dominates — re-profiled 2026-08-14 at N=10M, post-ADR-228** (`perf` works on
  the dev box again; self time). This supersedes the 2026-07-03 figures (`dispatch` 19.7%,
  `push_frame` 11.5%), which pointed at the same place:

  | share | symbol | what it is |
  |---|---|---|
  | 15.1% | `dispatch::dispatch` | the computed-head branch |
  | 8.1% | `jit_dispatch_call` | |
  | 6.3% | `dispatch::push_frame` | |
  | 5.3% | `eval::passthrough_arm` | per-call thin-wrapper predicate |
  | 5.0% | `Heap::closure` | handle deref, per call |
  | 4.8% | `Heap::vm_cache_arm_handle` | the memo's own hash lookup |
  | 3.1% | `compiled_arm_for` | |
  | 2.0% | `Closure::select_arm` | `max_by_key` over arms, per call |
  | 1.2% | `Heap::vm_arm_block` | |
  | ~8% | SmallVec `extend`/`from_iter` | argument staging |

  So **~50% of this row is call plumbing**, and the lever follows from the root cause rather than
  from a guess: give computed heads a **one-way monomorphic IC keyed on closure identity**,
  caching `(passthrough?, handle, cenv, bases)` together — `exec_chunk` already performs exactly
  that identity check for *staged* heads, so the pattern exists. That collapses
  `passthrough_arm` + `select_arm` + `vm_arm_block` + the memo lookup + much of `Heap::closure`
  into one guarded slot read, and it reaches every callback / message-handler workload, not just
  this row. A fast frame for the path (skipping `push_frame`) is the separate, deeper half.

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

  **Partial update 2026-08-14: ADR-228 gives some of it back, and that is consistent with the
  ramp reading rather than against it.** The handle memo (see `pipeline`) measures **−4.3% here
  against a 1.4% floor** at best-of-15 — real in direction, but it does **not** clear the
  `max(5%, 2×floor)` gate, so it is recorded as unconfirmed, not as a fix. (An earlier
  best-of-7 sweep read −7.0%; the disagreement between the two sample sizes is exactly why the
  gate exists.) The useful inference: a ramp made of several sub-gate contributions can also be
  *un*-made a piece at a time, so "no culprit commit" does not mean "nothing to recover" — it
  means no single commit will show up as the recovery either. Still do not spend a bisect here.

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

3. **The computed-head call path — now the best-measured lever on the board, and it is one
   mechanism serving many rows.** A computed head takes no inline cache, so `nqueens`,
   `pipeline`, `sort` and every callback / message-handler workload re-derive the whole
   callee resolution per call. ADR-228 took the allocation out of it (`pipeline` −9.1%,
   `nqueens` −6.2% at ceiling 1); the per-call *work* is still there and profiled — see the
   `pipeline` entry's table, where `passthrough_arm` + `select_arm` + `vm_arm_block` + the
   memo lookup + much of `Heap::closure` sum to ~18% of the row. **Next: a one-way monomorphic
   IC keyed on closure identity**, caching `(passthrough?, handle, cenv, bases)` together.
   Then, separately and deeper, a fast frame for that path (skipping `push_frame`, 6.3%).

4. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — structure-walkers
   don't tier and some heap reads go through per-op FFI callbacks. Extending the proven
   inline small-vector read template to variable-index reads and in-arm alloc (blocked by
   non-tail-call safepoints) is the win toward Elixir. *Not* the capturing-closure fast-link,
   which is measured dead for `pipeline` (see the ruled-out list).
5. **True call inlining / bounded unroll** — removes calls rather than cheapening them;
   the remaining `fib`/`bintree`-class lever.
6. **Interpreter dispatch** — the ~60% `vm_run_bc` share bounds every un-JIT'd row.
7. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values.
8. **`matmul`/`nbody` unboxed storage** — boxed 24-byte `Value` vs a register
   `long`/`double`; any design must not violate the immutability invariant.

## Measured and ruled out — don't re-attempt

- **The capturing-closure fast-link as `pipeline`'s blocker — retired 2026-07-03, and it had
  been this file's stated blocker for two revisions after that.** `perf` puts the elided
  free-global fast-link (the path that bails on captures) at **0% of pipeline** — transducer
  steps are computed-head — and both JIT fast frames fill capture slots anyway. The HOF native
  fast frame that *did* ship from this line of attack left the row flat while buying `nqueens`
  ~18%. Full reasoning in the `pipeline` entry above.

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
[`results/overview.svg`](results/overview.svg) for the ranked overall-speed chart
(base RSS per language is in the README standings table).
