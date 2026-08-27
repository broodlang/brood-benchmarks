# Optimization frontier — where the gaps are and what would move them

Core-dev notes: the interpretation of the [benchmark data](BENCHMARKS.md). **Current position
only** — what is fast, what is slow, what would close it, what is ruled out. History lives in the
Brood repo's `docs/devlog.md`.

No gap here is architectural; they are implementation headroom. ~60% of an interpreted row's time
is in the bytecode dispatch loop, so the broad levers are **dispatch cost** and **JIT coverage**.

## What runs native

The tier-1 JIT covers integer self-tail loops (`loop`, `collatz`), float-comparison loops
(`mandelbrot`), indexed array reads (`matmul`'s inner `dot`, via loop-invariant hoisting — sound
without alias analysis because Brood data is immutable), non-tail and tail recursion (`fib`,
`ackermann`), inline small-vector reads (`bintree`), and the JIT-lowered `table-*` ops (`sieve`).
Int/float recursion uses an unboxed i64/f64 register calling convention with an overflow deopt. A
JIT'd caller links straight to a JIT'd callee through an epoch-guarded in-IR fast-link; processes
of a runtime share one compiled copy of an arm's native code *and* its bytecode; a `def` deopts
affected code, so hot reload holds.

## Where the gaps are

Ratios are Brood's compute vs the fastest language on that row — **usually C**, a machine-floor
reference, so these read "vs roughly the hardware", not "vs the fastest managed runtime".

- **`spawn-live` (1.58 s, 1.73 GB — 1.9× slower and 1.9× heavier than the BEAM).** ~5.5 KB per
  live process against ~3.1 KB. Four wins landed here (ADR-215 AST-keyed code sharing, `fold`
  walking a vector by index, a native counted fold, dispatch reorder) and **none touched the
  process floor**, which is what is left — the row's peak RSS sat flat throughout. See levers 1
  and 2b.
- **`nbody`** — the immutable rebuild (a fresh 7-element vector per body per step) is what
  remains; it needs escape analysis or a native float array. A standing check fell out of the
  earlier bug here: **the JIT-vs-no-JIT ratio per row** — `fib` 54×, `collatz` 40×, but `nbody`
  3.2×, which is what exposed a silent bail. `bintree` (3.5×) and `nqueens` (3.4×) are in that
  same suspicious band.
- **`bintree` (7.8×; the BEAM is unusually fast here and beats C)** — the one row C does not lead:
  malloc/free on ~819k short-lived nodes loses to a generational collector, worth knowing before
  treating "native allocation" as the target. The cost is the call protocol: ~77 ns per node over
  four non-tail calls. That is the X-register/call-convention redesign, not a tuning knob. **The
  open watch-item.**
- **`nqueens` (36× C, 12× Node)** — backtracking recursion; the `reduce`-over-`range` per node and
  the non-tail `solve`/`safe?` recursion dominate. C's margin is partly structural (it pushes onto
  a stack array where Node and .NET copy the placed-columns list per node), so **12× against Node
  is the fairer target**.
- **`mandelbrot` (9.6× C)** — `esc` is JIT'd with register-carried f64 params; the residual is
  boxed 24-byte `Value` tagging plus loop overhead. Near the JIT floor — C is only 1.2× ahead of
  .NET here, so the row is close to its arithmetic limit for everyone.
- **`matmul` (59× C)** — inner loop is native; residual is the one read LICM can't hoist plus boxed
  `Value` array storage. Both denominators are ~2–4 ms, so read the absolute, not the multiple.
- **`pipeline` (8.7×)** — lazy-seq/transducer composition the JIT doesn't cover; allocation churn
  dominates. Re-profiled at N=10M (self time):

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

  **~50% of this row is call plumbing.** But see the ruled-out list: memoizing the *resolution*
  half was implemented and measured at ~0 where users run. The cost is the **call protocol**, not
  the bookkeeping.
- **Message latency (`pingpong` 3.0×, `ring` 2.5×, `supervisor` 2.9× vs Elixir)** — the widest
  honest gap, with its three large levers already taken: direct handoff (1.9×), the HOF matcher
  fast path (3.0×), and the receive-mark that removed an O(rounds × backlog) rescan. What is left
  per message is a mailbox mutex, a `wake_parked`, a re-enqueue and one matcher activation, over a
  floor of per-message copies and heap-captured migratable continuations — that floor is design.
  Brood beats every thread/queue language here; Node's `ring` is cooperative single-thread async.
  **Do not extend this to `latency`** — that row was never per-message cost (a send + receive is
  1.1 µs); it was spawn placement.
- **Text codecs (`json`, `regex`, `base64`)** — pure-Brood `std/` libraries against native codecs,
  by design. **The shared-fast-path lever was taken on 2026-08-26 and it was two of the three,
  not all three** (published 2026-08-27):
  - `json` **−20.8%** (0.7% floor). `string/->codepoints` is a native that had **no native
    inverse**, so every parser rebuilt its result with `(apply str (map int->char cs))` — a
    closure call and a one-character string per code point, then an N-way concat.
    `%codepoints->string` is that inverse (brood ADR-249); parse ~85 → ~45 ms.
  - `base64` **−9.5%** (0.0% floor). Decode read a CHAMP map for the reverse alphabet and
    indexed through `nth`, a closure that re-checks `int?`/`vector?`/length before reaching
    `%vector-ref` — eight per output triple. A dense codepoint-indexed vector plus direct
    `%vector-ref`: 29.4 → 15.5 ms, of which the dense vector was only ~7%.
  - `regex` **unchanged, and it has no such gap** — its hot path is a memoised DFA whose steady
    state is one `table/get`, not string assembly. The "shared by all three" framing was wrong
    about which rows shared the problem.

  **Split a codec row before optimising it.** Both movers are two-directional and the halves are
  nowhere near equal — `base64` decode was 4× its encode, `json` parse 2.4× its encode — so
  optimising the wrong half is invisible at the row level. The *encoders* are deliberately
  untouched: the symmetric change needs a range check per element, and a call per element in
  these loops cost `base64` encode **4×**.
- **`sort`** — do not re-optimise the comparator (already unboxed). The suite's heaviest row for
  memory; the allocation volume is the cost, not collection.
- **`primes`, `pipeline` regressions — both CLOSED.** Kept only for the methodology below.

**Memory and startup: KI-61 is FIXED and published (2026-08-27).** Startup **31 → 18 ms** (5th of
eight to 4th, within 0.5 ms of Node) and base RSS **56 → 52 MB**; prelude boot itself is ~7.5 ms
against 22.8 ms. The cause was a per-wave namespacing tax — each wave that moved prelude names into
a module forced that module to load from source at every boot — and the fix was not the std-image
registration replay recorded here, it was to stop loading them at boot: the prelude's references are
**autoload stubs** that load on first call (brood ADR-246), plus moving prelude def-sites into the
boot cache instead of a second positioned read of the prelude (ADR-247).

**It also moved almost every compute row −12% to −20%, and that needs saying plainly because the
obvious prediction was wrong.** `compute = wall − startup` should cancel a saving that appears in
both — but the `startup` row is `(io/puts 0)`, which loads `io` and through it `string`, while most
rows load neither. Those rows keep the whole lazy-load saving while only ~13 ms is subtracted away
(`fib`'s wall fell 29 ms against `startup`'s 13). So the broad improvement is **one boot change
counted once per row**, not twenty wins — and the under-subtraction already recorded at the end of
this section is the reason.

**What is left on startup** is no longer prelude building: a program that touches `io` pays `io`'s
own dependency chain (`string`, `file`, `path`) — 15.4 ms measured, against a ~15 ms bare boot. The
std image plus a registration replay is exactly the lever for that, and it is now purely additive.

## The Brood column pays a per-run cost no other compiled column pays

Measured 2026-08-27, and it is the one standing *methodology* handicap rather than a runtime gap.

Elixir and .NET run as prebuilt artifacts; C is a binary. Brood runs from source, and pays for it
twice per run: compiling the benchmark program (~1.7 ms) and **re-evaluating every `std/` module the
program requires** — `json` 4.6 ms, `regex` 4.9 ms, `seq` 3.2 ms, `encoding` 2.1 ms, `os` 0.8 ms.
None of it is subtracted, because `compute = wall − startup` and the `startup` row loads only `io`.
Against the 2026-08-27 compute figures that is **~2–4% on the codec rows, ~1% elsewhere** — never
enough to move an ordering, always in the same direction.

**The fix landed 2026-08-27 (brood ADR-256) and the handicap is now optional rather than
structural.** The stdlib image restores a module's bindings instead of re-evaluating its source:
`json` 6.5 → 1.7 ms, `http` 12.0 → 3.6 ms, `regex` 4.7 → 1.1 ms, `datetime` 3.2 → 1.0 ms, and the
`json` row measures **−5.6% end to end**. Brood's suite is 4917/4917 with it installed at boot,
against 4917/4917 without.

**Two claims made here on 2026-08-27 were wrong and are withdrawn.** That `datetime/now` came back
unbound: that name has never existed — the module defines `utc-now`, which works. And that the suite
"fails 150 of ~4900": that figure, and the 170-of-4888 and 131-of-4873 before it, were all taken by
installing the image from a *program*, which cannot exercise it — a qualified name auto-requires its
module at compile time, so the test framework loads the whole library from source before the first
line runs. Instrumented, that configuration materialises **zero** modules while reporting 99 sections
installed. Measured properly (installed at boot) the gap was 157 of 4917, and its largest part — 112
of them — was not a registration gap at all but a concurrency race in the loader.

The image is now **on by default** in the runtime (`BROOD_NO_STDIMAGE=1` opts out), and the harness
builds it in `build_brood()` — the fair analog of Elixir's `elixirc` step, and for the same reason:
the runtime installs an image whenever one exists but never spends ~1 s *building* one, so a
benchmark host that had never run `nest` would have measured the source path while a developer's
machine measured the image. Numbers published before 2026-08-27 still carry the per-run library
cost described above.

**Warming the JIT across runs is not the answer and should not be attempted.** Every JIT column
cold-starts per process — V8, RyuJIT, BeamAsm, HotSpot — which is why Clojure carries a caveat
instead of a warm-up. The harness's discarded run per language already warms what carries across
processes; for Brood that is the build-id-keyed boot cache (~1.2 s cold vs ~18 ms warm). Warming
Brood's tiering between measured runs would favour Brood alone.

## Measurement traps found the hard way

Six ways to get a confident wrong number on this runtime, each of which produced one:

- **A stale binary reports the old code and does not fail.** `std/*.blsp` is `include_str!`'d
  into the binary, so editing a module and re-running the existing build measures nothing —
  silently. That produced three "results" (40.2 → 37.5 → 44.1 ms) around an unchanged build in
  2026-08-26's codec session. One command settles it: append garbage to the module and see
  whether the run still succeeds.
- **A row that errors fast looks exactly like a row that is fast.** `persistent-map` died at
  compile when a namespace wave renamed `map-int-add`, and kept appearing in `ab-bench` sweeps
  with plausible times *and plausible deltas* until someone ran it by hand. A harness that
  times a column should assert the column's answer, which the published harness does and
  `ab-bench` does not.

- **Pinning charges you for the JIT.** `taskset` puts the background compiler on the benchmark's
  core, so anything that increases compilation volume reads as a slowdown. The same loop measured
  **+68% pinned and +28% unpinned** — both sides inflate, so the regression inflates too.
- **First-run timing measures tiering, not the code.** A 20M loop reads ~50 ms on its first run in
  a process and ~24 ms on its second, regardless of anything else. Run once and discard before
  timing. Skipping this produced a whole retracted finding (brood KI-63), including a clean
  "threshold at 2000 functions" that does not exist. It is not even stable against program
  *shape*: the identical loop read 25 ms alone in a file and 40–51 ms as the first of three sites.
- **Differencing two programs breaks when the non-loop part is big.** `wall(with) − wall(without)`
  cancels setup exactly, then reports the loop taking 4 ms once both walls are dominated by
  compiling 2000 `defn`s.
- **A sub-gate ramp has no culprit commit.** The A/B gate rejects anything under `max(5%, 2×floor)`,
  so five changes worth +2–3% each are a real 6% regression that no gate ever saw and no bisect can
  localise — a bisect must return *something*, so it returns whatever sat past the threshold
  (once: a Brood test file). Use a per-commit sweep recording absolutes for trend, not pass/fail.

And one about this repo specifically: **`compute = wall − startup` under-subtracts.** The `startup`
row is `(io/puts 0)`, which loads `io` but not `os`/`string`, and has no hot function to tier — so
it does not carry the per-run module-load or JIT-warm-up cost every real row pays. Rows in the tens
of milliseconds are substantially measuring those.

Method notes: use **`(mem-bytes)` / `(mem-peak)`** for an allocation question and RSS only for
"what did the OS map". Ladder numbers on `spawn-live` are **CPU** µs/unit, not wall (the row
spreads across workers). `release-fast` sets `strip = true`, so `perf` gives raw addresses until
you rebuild with `CARGO_PROFILE_RELEASE_FAST_STRIP=none CARGO_PROFILE_RELEASE_FAST_DEBUG=1`. The
`perf-stats` `ns_*` accumulators are useless for close comparisons — every one read *lower* for the
slower variant, the atomics' own perturbation swamping the signal.

## Levers (rough priority)

1. **The green-process floor (~5.5 KB live vs the BEAM's ~3.1 KB)** — top lever on `spawn-live`, by
   elimination. Attributed: **IC tables 896 B** (after the lazy `FastLink` mirror, 2b),
   `Box<Process>` (inline `Heap` 1376 B), `Arc<Mailbox>` 184 B, `Suspended` 128 B. **Working state,
   not slack** — three tunings were measured and reverted (see ruled-out). Closing needs it
   *smaller*, not dropped: shrink `CallIcEntry`, or share IC entries for frozen callees (sound — a
   sealed binding resolves process-independently).

2. **Make `fold` native — worth ~11% of `spawn-live`.** `(fold + 0 p)` costs **26.6 µs/unit**
   against **23.7 µs** calling `%vector-reduce` straight from the unit body; trivial forwarders
   isolate it (23.7 → 24.3 → 25.4 → 26.6 for zero/one/two forwarders and `fold`). So **a bare
   Brood-level call costs ~0.85 µs**, and `fold`'s 2.9 µs is that plus its `vector?` predicate call
   plus argument handling.

   **"First call in a process" is the wrong framing — measured false.** Calling the same arm again
   in the same process costs the same as the first; nesting an identity forwarder 1/2/3 deep costs
   **+2.21 / +2.15 / +1.40 µs** — flat, not front-loaded. There is no warm-up to remove.
   Compilation is not it either (`BROOD_TRACE_COMPILE` counts a constant ~142 compiles whether the
   run spawns 100 or 400 processes). Converted to absolute ns/unit, the added cost is
   `Heap::env_get` **+560**, kernel page faults **+274**, `value::is_dynamic` **+232**,
   `code_gen_pinned` **+170**, `GlobalAlloc::alloc` **+164**, `RwLock::read_contended` **+128** —
   **memory traffic in a 1.2 GB working set, not dispatch bookkeeping.**

   It is a real change, not a reorder: `fold` must keep map-as-pairs, seq-view fusion (which
   applies a Brood transducer and recurses), and exact error/promotion behaviour — and `seq` is not
   a Rust builtin, so the generic path calls back into Brood. It is the most-used function in the
   prelude, so the regression surface is the whole library.

2b. **Per-process inline-cache tables — half of each is never touched.** Instrumenting teardown on
   a real `spawn-live` gives an identical shape for every unit: **14 call-IC sites allocated, 6–7
   ever populated**, 4 arms entered. `vm_arm_block` allocates an arm's block whole on first entry,
   sized by the arm's *total* `nsites`, whether or not this process will execute them.

   - ~~Allocate the `FastLink` mirror lazily~~ — **DONE.** 19,968 of 20,001 unit processes now
     publish into no slot and allocate no mirror: **−192.6 B/process**, RSS 6364 → 6093 B/process
     (−4.3%), time-neutral at both ceilings. (`fib` is the load-bearing check — the in-IR fast-link
     is worth ~20% there, so +0.0% proves linking still happens.)
   - **Shrink `CallIcEntry`** 64 → ~48 B: `epoch` u64→u32, `callee: Value` narrowed,
     `callee_bases: (u32, u32)` packed. ~224 B/process per 14 sites.
   - **Share entries for frozen callees** across processes — biggest of the three, and the most
     design.

   Read the per-process saving at the **parked** state, not the fully-run one: peak memory is set
   by the state all N processes are in at once.

3. **The computed-head call protocol.** A computed head takes no inline cache, so `nqueens`,
   `pipeline`, `sort` and every callback/message-handler workload re-derive the callee per call.
   The *resolution* half is ruled out (below); what is left is frame setup and dispatch — a fast
   frame skipping `push_frame` (6.3%).
4. **Heap-walking / allocation-heavy code** (`nqueens`, `pipeline`) — structure-walkers don't tier
   and some heap reads go through per-op FFI callbacks. Extend the proven inline small-vector read
   template to variable-index reads and in-arm alloc (blocked by non-tail-call safepoints).
5. **True call inlining / bounded unroll** — removes calls rather than cheapening them; the
   remaining `fib`/`bintree`-class lever.
6. **Interpreter dispatch** — the ~60% `vm_run_bc` share bounds every un-JIT'd row.
7. **LINMAP wider coverage** — next target is `reduce`-style folds over non-integer values.
8. **`matmul`/`nbody` unboxed storage** — boxed 24-byte `Value` vs a register `long`/`double`; any
   design must not violate the immutability invariant.

## Measured and ruled out — don't re-attempt

- **Memoizing computed-head resolution per `(closure, argc)`** — implemented, measured, reverted.
  Sized at ~18% of `pipeline` from the profile above; delivered −4.3%/−4.9% on `nqueens` at
  ceiling 1, **parity at the default ceiling**, and **`spawn-live` peak RSS +7.0%** — a memory
  regression on the row lever 1 is about. Two lessons: **the profile over-promised because the
  derivations are cheaper than the memo that replaces them** (a closure deref plus a `max_by_key`
  over a single-arm closure costs less than a `HashMap` probe — a share in a profile is not a share
  you can collect); and an intermediate version cost `reduce` +5.0% by resolving an arm even for
  thin wrappers, i.e. *compiling* every `+` just to memoize it.
- **The capturing-closure fast-link as `pipeline`'s blocker.** `perf` puts the elided free-global
  fast-link (the path that bails on captures) at **0% of pipeline** — transducer steps are
  computed-head, so they never reach it — and both JIT fast frames fill capture slots anyway. Do
  not spend a session dropping a capture bail for this row.
- **The receive machinery / the matcher's missing native fast frame.** The finding stands — a
  `receive` matching a literal generates a matcher that lowers, deopts, is latched off, and pays
  the interpreter's trampoline — but on `spawn-live` it is worth **~1.8%, inside the noise**
  (`[:go p]` 28.0 µs/unit, an equivalent guard 27.8, the bind-only `[_t p]` that stays native
  27.5). The matcher deopts exactly **16** times, then `jit_deopt_feedback` latches it `BAILED` and
  declines the rest; `BAILED` is sticky, so removing a deopt source does not un-bail an arm. May
  still be worth something on a long-lived message row — untested, the only reason left to look.
- **GC tuning for `bintree` / `nbody`.** Neither is GC-bound (45k and 798 objects copied per run;
  ~4% and ~2%) and neither bails. Nursery sizing is flat across an 8K→128K sweep; larger floors
  make both *worse*.
- **Per-process inline caches as a lever.** A fresh unit misses ~half its call sites — true counter,
  wrong inference. It is ~2 µs of a 33 µs unit, and a *cached* callee is no faster than
  re-resolving one on the VM (the computed head measured slightly **faster**: the global path pays
  an IC probe and validation while the computed path reads a slot). A high miss *rate* on a process
  that makes five calls is unavoidable, and is not a high cost.
- **Three tunings of the green-process floor.** (a) Park-trim threshold at 0: no change. (b)
  Capacity-1 first touch for the slab `Vec`s: predicted ~700 B/proc, delivered 110 B, cost
  `bintree` +4.8% in reallocs. (c) Dropping IC tables when a process parks: effective on memory
  (floor 4.53 → 3.89 KB/proc) but **`pingpong` +26% / `ring` +18%** — the cost is a process losing
  caches it built at startup and rebuilding them, not the frequency of dropping.
- **Splitting shared compiled code from per-process JIT-tier state.** The `collatz`/`nqueens`
  regression that motivated it is an artifact of `make ab`'s single-core pin. Sharing deliberately
  makes more prelude arms tier up (18 lowered vs 7); splitting would undo `spawn` −14.8% to fix
  nothing.
- **Float back-edge store elision** (~0, absorbed by the store buffer); **in-IR call frame-setup**
  (measured regression — the FFI boundary is not the bottleneck); **always-on native-call timing**
  (8–22% on the message rows); **comparator work in `sort`** (already unboxed).

See [`results/report.md`](results/report.md) for the current numbers and
[`results/overview.svg`](results/overview.svg) for the ranked overall-speed chart.
