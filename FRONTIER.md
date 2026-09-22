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

- **`spawn-live` (1.13 s, 1.49 GB — 1.7× slower and 1.7× heavier than the BEAM).** ~5.2 KB per
  live process against ~3.1 KB. Four wins landed here (ADR-215 AST-keyed code sharing, `fold`
  walking a vector by index, a native counted fold, dispatch reorder) and **none touched the
  process floor** — the row's peak RSS sat flat at 1.69–1.75 GB throughout — until 2026-09-21,
  when three commits on the floor itself (no ColdHeap per spawn, SmallMaps for the per-process
  maps, a root stack that grows by four) took it 1.75 → 1.56 GB (−11%) with the wall −6.6%. The
  floor is still what is left. See levers 1
  and 2b.
- **`nbody`** — the immutable rebuild (a fresh 7-element vector per body per step) is what
  remains; it needs escape analysis or a native float array. A standing check fell out of the
  earlier bug here: **the JIT-vs-no-JIT ratio per row** — `fib` 54×, `collatz` 40×, but `nbody`
  3.2×, which is what exposed a silent bail. `bintree` (3.5×) and `nqueens` (3.4×) are in that
  same suspicious band.
- **`bintree` (6.1×; the BEAM is unusually fast here and beats C)** — the one row C does not lead:
  malloc/free on ~819k short-lived nodes loses to a generational collector, worth knowing before
  treating "native allocation" as the target. The cost is the call protocol: ~77 ns per node over
  four non-tail calls. That is the X-register/call-convention redesign, not a tuning knob. **The
  open watch-item.**
- **`nqueens` (35× C, 7.5× Node; was 53× / 12× before the db98f7cd refresh)** — backtracking
  recursion; the `reduce`-over-`range` per node and the non-tail `solve`/`safe?` recursion
  dominate. **A quarter of the row was one unary minus** (2026-09-20): `safe?`'s `(- dist)` was
  a generic call to the variadic wrapper — a non-tail call, hence a GC safepoint, hence no
  hoisted pair-slab bases — so the list walk read every pair through `brood_rt_car`/`_cdr`
  callbacks. Unary `-`/`/` lower to the 2-arg primitive now: 1 507M → 1 111M instructions,
  −29% wall. What is left: the native entry per `reduce` element (~12%), `solve` on the VM
  (~15%), a closure captured per node. C's margin is partly structural (it pushes onto
  a stack array where Node and .NET copy the placed-columns list per node), so **the Node
  ratio is the fairer target**.
- **`mandelbrot` (3.8× C; was 9.3× until the 422c92a5 refresh)** — `esc` is JIT'd with
  register-carried f64 params; the residual is boxed 24-byte `Value` tagging plus loop overhead.
  The 2026-09-21 halving (161 → 77 ms wall, 0.5% spread over three invocations) is brood
  ADR-378: an arm whose floats arrive through vector reads used to lower onto the integer path,
  deopt on every activation and latch BAILED — and the latch never cleared its callers' fast
  links, so the interpreted arm was entered natively forever. Deopt feedback now re-tiers it in
  float context, and untyped comparisons dispatch by tag. Near the JIT floor now — C is only
  1.2× ahead of .NET here, so the row is close to its arithmetic limit for everyone.
- **`matmul` (51× C)** — inner loop is native; residual is the one read LICM can't hoist plus boxed
  `Value` array storage. Both denominators are ~2–4 ms, so read the absolute, not the multiple.
- **`pipeline` (6.2× Node)** — lazy-seq/transducer composition the JIT doesn't cover. **The
  "allocation churn dominates" half of this entry was withdrawn 2026-08-28: it does not.**
  Scoped counters (`perf/measure`, size-swept 100k → 1M so only work-proportional counters
  count) put `alloc` at **15, flat** — `alloc_slot!` is the one macro behind every LOCAL heap
  allocation, so the lazy `lfilter`/`lmap` form really does stream without allocating per
  element. What scales is **1.48 `jit-link-done` and 1.40 `env-get` per element**: the cost is
  the call path, ~1.5 fast-linked calls an element. The profile below (call plumbing ~50%) is
  the half that stands. Re-profiled at N=10M (self time):

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
- **Message latency (`pingpong` 3.2×, `ring` 3.0× vs Elixir; `supervisor`'s 2026-09-14 spike
  was the type checker, below)** — the widest
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
- **A variadic wrapper called in a loop costs ~36%; the fixed-arity ones cost nothing.** Isolated
  on `collatz`, one binary, same program shape:

  | variant | time |
  |---|---|
  | `math/rem`, `math/quot`, `math/max` all qualified | 223 ms |
  | the same, but `%max` called directly | **142 ms** |
  | all three primitives directly | **142 ms** |

  The middle row equals the bottom row, which settles it: **`math/rem` and `math/quot` are free**
  and the whole delta is **`math/max`**, called once per `sweep` iteration. The reason is visible
  in the JIT dump — `steps` lowers to native with **no `Call` instruction at all**
  (`Prim2SlotInt JumpIfFalse … SelfCall`), because a fixed-arity one-primitive body is inlined
  into its caller and disappears. `math/max` lowers to `GlobalIc Local Call`: it is
  `(apply %max xs)` over `& xs`, so it allocates an argument list and cannot be inlined.

  So the lever is **variadic dispatch, not wrappers in general** — which is precisely the worked
  example in brood's CLAUDE.md ("variadic `+`/`-`/`=` … cost ~40× a direct call") and its
  prescribed fix: efficient **multi-arity dispatch in the evaluator**, keeping the functions in
  Brood. `math/max`/`math/min` are the two `math` entries in that shape; `collatz` and `latency`
  are the rows that call them in a loop.

  Qualification itself is free: `math/rem` bare via `(:use math)` measured 204 ms against 205 ms
  qualified, so the module system costs nothing at a call site.

  **`collatz` 95 → 185 ms between the 2026-08-27 and 2026-08-28 published runs is this**, not a
  runtime regression: the port had to migrate off the retired bare names, and one of the three it
  moved to is variadic.

  **Closed at 0.18.1 (2026-08-30 Brood-column refresh): `collatz` is back to 92 ms** — the
  variadic call-shape cost above was fixed in the brood runtime during the 0.16–0.18 window,
  so the row recovered without the port changing. The multi-arity-dispatch prescription this
  entry pointed at is no longer collatz's gap; what remains of the row is the tier-1 JIT's
  ordinary integer-loop story (3/8, +2.8× vs C).

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

**Startup and base RSS moved again 2026-09-01 (brood ADR-313): 22.5 → 20.2 ms and base RSS
72.6 → 60.1 MB (−17%).** The default crash reporter was armed by calling into
`std/proc/crash-report.blsp`, and by brood's load-by-inference that pulled ten stdlib modules
into *every* run — `io/puts` bringing `io`/`file`/`path`/`string`/`reflect`/`math` behind it.
Arming now happens in the prelude and the reporter loads on the first crash. The RSS figure is
the striking one: 12.5 MB of this runtime's resident set was modules no program had asked for.

It moved the compute rows too (`bintree` −4.6%, `fib` −4.5%, `primes` −4.1%, `loop` −5.2%), and
for a reason worth recording beside the under-subtraction note above: nine fewer modules is
**~13% fewer JIT-lowered arms** (bintree 108 → 94, fib 95 → 84), which is brood KI-100's
instruction-fetch mechanism — fewer arms carrying native code means a smaller hot footprint.
Note also that the `startup` row itself now loads **7 modules rather than 10**, so it subtracts
*less* from every other row than it used to: the under-subtraction described above got slightly
worse, and the compute improvements here are, if anything, understated.

**RETRACTED 2026-09-02, same day: brood ADR-314 shipped default-on and was reverted to
opt-in.** An imaged boot restored a stale stdlib-image section directory, and still does not
carry the module-level names the prelude's own evaluation binds (`file/list-files` came back
unbound). The column has been re-measured on the restored default: **startup is 19.6 ms**,
not the 16.0 ms published for a few hours, and the short rows return with it —
`reduce` +17.7%, `strings` +14.1%, `pipeline` +8.5% against that briefly-published column.
Those are not regressions; they are the correction of numbers taken with a feature that is
no longer on. Everything below about the *mechanism* still holds and is what ADR-314 will be
worth once it is correct; the figures are the achievable ones, not the shipped ones.

**Startup 20.2 -> 16.0 ms and base RSS 60.1 -> 57.3 MB (ACHIEVABLE, not currently on):** Boot went
9.36 -> 5.32 ms and a whole empty `brood` run 13.5 -> 8.3 ms; the `startup` row shows less
than that because it is `(io/puts 0)`, which still loads `io`'s module chain on top of boot.

**Read the per-row `compute` column carefully this time, because it moves the wrong way.**
Every row got faster in WALL — the number a user actually waits for — by 0.3% to 21%. But
`compute = wall - startup`, and the subtracted constant just fell by 4.2 ms, so any row whose
wall fell by *less* than that reports worse compute:

| row | wall | compute |
|---|---|---|
| `loop` | +2.4% (inside its 3.9% spread) | **+11.9%** |
| `sort` | +0.3% | +4.8% |
| `fib` | -5.3% | -1.0% |
| `mandelbrot` | -3.6% | -1.8% |

That is arithmetic, not a regression: a 49 ms row cannot show the benefit of a 4.2 ms
saving it also had subtracted from it. It carried through to the aggregate — the field-wide
geomean reads 10.4x -> 10.6x and Brood's rank 4th -> 5th — so the published headline
understates this release while the wall column overstates nothing.

This is the **mirror image** of the effect recorded above for KI-61, where a boot saving the
`startup` row did *not* fully absorb inflated every compute row instead. Same mechanism, same
row, opposite sign, and worth deciding about rather than rediscovering a third time: as the
runtime's fixed costs shrink, subtracting a `startup` row that itself loads modules
over-corrects for rows that load none. Changing it is a methodology decision, not a bug fix,
so nothing here has been adjusted.

**Startup 12.9 → 13.6 ms at the 422c92a5 refresh (2026-09-21), and it is real: +6.2% against
a 0.0% floor under `ab-bench`, 74.4M → 81.3M instructions on `(io/puts 0)`.** Attributed on
unstripped binaries (brood KI-182). The largest piece is the JIT compiling at boot: brood
ADR-381 offers every declared `def` to the Brood contract hook even when contracts are
unarmed, the hook's `(not (or (%contracts-armed?) …))` runs once per declared name as `io`'s
sections materialise, `not` crosses the tier threshold, and every `brood file` run now
instantiates Cranelift to compile it (`BROOD_JIT_DUMP_IR=1`: one arm, `not`, on the new
binary; none on the old; none on an empty file; `BROOD_NO_JIT=1` gives 1.55M of it back).
The rest is diffuse and expected: the prelude image carries def sites now (brood ADR-382,
802 → 1328 entries, +0.6M in position-table inserts) and the prelude itself grew by the
contracts policy and the ADR-377/379 additions (+0.3M freeze, +0.4M image load). The number
is published as measured; the fix is brood's, not this repo's.

**Startup at the 653d41d9 refresh (2026-09-22): 13.6 → 13.1 ms, and the mechanism above is
closed.** brood KI-182's fixes — the kernel no longer consults the contract policy unarmed,
the `defability` op function carries the armed test inline, the image replay registers impls
without re-running their arity diagnostic, and `nth`'s index guard no longer calls `not` —
leave no arm lowering on any module load; `(io/puts 0)` reads 78.3M instructions against the
136b14d7 column's 75.0M (was 81.3M), the remainder being the prelude image's def sites and a
larger prelude. Every other row moved inside its spread; like-for-like 7.20 → 7.12.

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

## An unmeasured column hides a real regression (2026-09-01)

A refresh at 0.22.0 found **every compute row 4–10% slower** than the published 0.19.1
column. It is real, not a coin flip — the whole chain was checked before it was believed:

- min-of-3 interleaved harness invocations (the per-row minimum landed on all three
  invocations, 18/9/4, which is what a healthy min-of-3 looks like);
- build-parity A/B (`make ab`, both arms built by the same target, interleaved, pinned,
  std-image **live on both arms**): mandelbrot **+8.1%** against a **0.9%** floor, solo
  re-run at N=11;
- **unpinned** re-measurement, because `make ab` pins to one core and would charge the
  benchmark for background JIT compilation — and the new binary lowers *more* arms (97 vs
  85). It survived: **+6.8%** unpinned, precisely timed and interleaved;
- an output check: all three binaries print checksum `6129302`, so the arms do equal work.

**Shape.** Boot **+2.8 ms (+14.5%)**, and JIT'd compute **~+5.5%** — at tier 1 compute
moves only +1.1%, so the compute half lives on the native path, not the interpreter. The
boot half tracks the stdlib growing (the startup image went 5199 → 5332 bindings), which is
feature cost rather than a defect; the compute half is not explained.

**Attribution so far** (mandelbrot, same treatment, base times): `8a2aaa01` 223 ms,
`6589e74b` 221 ms, `2c822875` 226 ms — all still fast; `80bb25d8` (v0.21.0) 242 ms and
`2210d922` (ADR-310) 242 ms — already slow. So it landed in **`2c822875..80bb25d8`**, and
three plausible suspects are *excluded*: the Cranelift `*_imm` → `_s` migration, the JIT
hot-admission commit, and ADR-310. Everything after v0.21.0 measures as noise (+0.8%).

**Why it went unnoticed for three releases, and what now catches it.** Nothing in this repo
measures timing except a hand-run harness. The daily gate checks that rows *run* and that
checksums *agree* — both stayed green the whole time. `bench/staleness.py` (wired into the
daily job) now compares the commit the column was measured at against the commit under test
and fails on a version boundary. It deliberately measures nothing: a perf gate on a shared
runner would be a flake generator, and a gate nobody trusts is worse than none.

## `supervisor` +50% at the 2026-09-14 field run — the checker, not the supervisor (2026-09-15)

The full seven-language refresh at `c9d6c1a1` found every row inside drift except one:
**`supervisor` 886 → 1330 ms**, the row measuring 20,000 supervised children with a quarter
retired and restarted. It clears the verification bar the rest of this file insists on, in both
directions:

| | run 1 | run 2 | run 3 | spread |
|---|---|---|---|---|
| `5c913fe3` (the 0.27.2 column), rebuilt + its own std image, PATH-overridden | 888.6 ms | 892.1 ms | 891.4 ms | 0.4% |
| `c9d6c1a1` (this column) | 1342.0 ms | 1344.7 ms | 1349.8 ms | 0.6% |

Both sides are best-of-7 within the invocation (`supervisor` is in `NOISY`), and three whole
invocations per side — the min-of-3 treatment that exists because one invocation is a coin flip
on this box. A row that normally wanders is holding still here, on both binaries, 50% apart.

**Peak RSS did not move with it** (626 → 644 MB, inside this row's own RSS drift), so the cost is
time, not allocation volume: something on the per-child path got slower, not bigger. Nothing else
in the run moved beyond drift, which argues against a broad dispatch or boot cause and for
something on the link/monitor/restart path specifically.

**Resolved to a cause the next day, and it was none of the four candidates above.** A `BENCH_N`
sweep put the cost at a flat ~520 ms — N=100 read 625 ms against 104 — so it was load time, and
cutting the program form by form put it on one line: `(def sup (supervisor/start []))`, which
checked in 463 ms where it had cost 41. `brood file.blsp` runs the advisory type checker before the
program, and the checker's call-site specializer returned a `None` through `?` *before* its memo
write, so a negative answer that cost a full body walk was re-asked at every call site and every
enclosing level: the prelude's `get` re-typed 1864 times for 52 distinct questions. Latent since
call-site specialization landed; reachable once ADR-341 gave module-private parameters types
(brood KI-138, fixed at `0148a3a5`, guarded by a test that bounds the walks).

| | run 1 | run 2 | run 3 | min |
|---|---|---|---|---|
| `d99fea7e` (this refresh, KI-138 fixed) | 1087.2 ms | 1102.3 ms | 1101.0 ms | **1087 ms** |

**Then the other half, the same afternoon (KI-139).** The fix above left the probe's check at
240 ms against 10 ms on the 0.27.2 column's binary, and the row at 1.09 s. Timing each specialized
walk put 249 of those milliseconds on ONE 239-node body (`supervisor-group-restart`); counting
expression visits during it read 78 910 — 330× the body; per-form entry counts laid the ladder out
(1 → 2 → 4 → 7 → 11 → … → 2464 down the nesting, each `(do …)` re-entering its single form twice);
backtraces at the doubled entry named the caller. A `let`/`do`/`if` whose body the inferencer
could not type returned unknown from the control-flow path and then **fell through to the call
path**, which typed `(let (b) body)` as a call to a function named `let` — bindings and body
re-typed as its arguments. One guard (a special-form head that cannot be typed is unknown, never a
call): probe check 290 → 65 ms, visits 288 408 → 20 979.

| | run 1 | run 2 | run 3 | min |
|---|---|---|---|---|
| `c813ce1a` (KI-138 + KI-139 fixed, that refresh) | 875.9 ms | 879.3 ms | 861.0 ms | **861 ms** |
| `5c913fe3` (the 0.27.2 column's binary), same day, image rebuilt | | | | 975 ms |
| `b092e62b` (0.28.0, the current column), same day, later | 839.2 ms | 836.0 ms | 836.8 ms | **836 ms** |

Under where it started, on a day the control says is ~7% slower than that column's. Two lessons
this file already teaches, restated by the day: a flat profile plus a per-walk count that "looks
about right" is not attribution (three measurements were needed, each contradicting the previous
theory); and the signal came from this column, not from a test — the argument for keeping it fresh.

## The v0.31.0 refresh: the release column, and it is the db98f7cd column (2026-09-20, night)

Min of three interleaved brood-only invocations at the tagged release `136b14d7`
(brood 0.31.0). No row moved past its spread but `json` −3.1% and `ring` −3.6% (both inside
the day's codegen-class swing on those rows); like-for-like 7.54, still ahead of Node. The
release carries, beyond the db98f7cd runtime, KI-170's direct-load frame with its two
follow-up fixes, a relower that fires per sixteen entry deopts, and the checker's docstring
fix — none on a benchmark path, which is what this column confirms. Published so the
staleness gate reads the release version.

## The db98f7cd refresh: `nqueens` −29% from a unary minus, and the like-for-like score passes Node (2026-09-20, evening)

Min of three interleaved brood-only invocations (spreads 0.2–3.5%), the runtime at brood
`db98f7cd`. One row moved on purpose — **`nqueens` 135.3 → 96.1 ms (−29.0%, spread 1.1%)**,
rank 8/9 → 7/9 — and it is the `make ab --floor` reading the change landed on (−28.5%, 0.7%
floor). The mechanism is in the `nqueens` bullet above: `(- dist)` was a call, the call was a
safepoint, the safepoint kept `safe?` from reading its list inline. **The like-for-like
score is 7.55, ahead of Node's 7.62 for the first time** (rank 6/9 → 5/9); aggregate
compute vs the field's average 0.84× → 0.80×.

Also in this column, unasked: `ring` −4.3% and `pingpong` −4.1% against the 1b9befd0
numbers — the same rows the previous refresh read +3.6% / +0.8% and attributed to
release-fast codegen partitioning. This binary partitioned differently and they came back.
Two consecutive columns moving the message rows ±4% with the VM's counters identical is the
argument, made twice now, for measuring on a deterministic-codegen build.

## The 1b9befd0 refresh: the whole column moves, from four brood fixes and a verdict cache (2026-09-20)

Min of three interleaved brood-only invocations (spreads 0.2–3.9% except `sieve` 7.7%), the
runtime at brood `1b9befd0`. Every compute row is faster, most by 5–10%, and the moves have
names (brood's devlog 2026-09-20, three entries):

- **Short rows, −14% to −21%: `reduce` 21.2 → 16.7 ms, `strings` 28.5 → 23.5, `pipeline`
  23.9 → 20.6.** Brood ADR-371: `brood file` now replays its pre-flight type-check verdict
  for an unchanged program instead of walking it on every run — the walk was 34M of
  `pipeline`'s 217M instructions (18.7%), 20M of `reduce`'s 166M. This is the structural
  close of brood KI-150 (the "short rows carry today's checker cost" note two refreshes
  above): the checker's per-run tax is gone from the column, and a checker feature can no
  longer move a benchmark row. It is exactly the class of per-run artifact the boot cache
  and the stdlib image already are — the harness's discarded warm-up run warms it — so it
  is measured the same way. **It cost one thing on the way:** the first column at `4fb3e1cd`
  read base RSS 42.6 → 49.3 MB, because a hit skipped the walk's eager module loads and the
  run's lazy load recompiled the top-level form (brood ADR-366's stale mark); a hit replays
  the walk's loads now and the column reads 45.1 MB — the residual is the day's other
  changes (KI-166's per-thread symbol-hash table among them), not the cache.
- **`spawn` −22% (47.7 → 37.1 ms), `supervisor` −10% (553 → 498 ms), `nbody` −14%
  (196.6 → 169.9 ms).** Brood KI-167: a loop handed to its recompiled body after a lazy
  module load (ADR-366) ran the rest of its life NESTED — every `receive` in it parked the
  OS worker dirty, and a native preempt with no driver to yield to interpreted up to 256
  iterations. Now a frame-level tail transition. `nbody`'s share is ADR-372 beside it: a
  register-carried param profiled `Int` on one activation deopted on every other, forever
  (a `SelfCall` arm had no deopt feedback); sixteen entry deopts now re-lower the arm with
  that slot boxed. And the inline `empty?` deopted for anything but nil or a pair, so every
  `(cond (empty? coll) …)` prelude loop handed a vector ran on the VM — `json`'s
  `needs-escape?` 7 910 times per run — which is `json` −7.8% and part of `wordcount` −8%.
- **`mandelbrot` −6.7%.** §7.9 of brood's compute frontier closed: the float-slot veto in the
  profitability gate refused exactly one arm in this corpus (`row-sum`) and protected none.
- **The like-for-like score 8.90 → 7.75**, within 0.13 of Node's 7.62 (the rank stays 6/9);
  aggregate compute vs the field's average 0.91× → 0.84×.

**Read with the usual care.** `ring` +3.6% on a 2.0% spread with `pingpong` +0.8% — **settled
the same evening with fixed baselines, and it is the release-fast codegen class, not the
message path.** Interleaved best-of-9 of the morning's brood commit (`2c1596c0`) against
this column's (`1b9befd0`), both images live, base-vs-base floor 0.2–0.7%: `ring` +9.5%,
`pingpong` +7.9%, and the same with `BROOD_NO_CHECK=1`, so the verdict cache is not it.
Bisected over the four commits between with `perf stat`: `pingpong` **instructions +1.4%
then +0.2%, cycles +4%, L1-icache misses 67M → 75M (+11%)**, and the VM's own work counters
(`BROOD_PERF_STATS`: activations, IC hits, allocs, env hops, native entries) are **identical
to the last few hundred** across the commits. No message-path code changed; the day's
commits added Rust in the tooling and gated three dev-tools items out of the lean build, and
the release-fast profile (no LTO) re-partitioned the hot dispatch code around them — the
`strings` +8.8%-on-+1.4%-instructions class two refreshes above. The wall number is real
and published as measured; the code did not slow down. The lever, if this class is to stop
moving the message rows, is a deterministic-codegen build for measurement (LTO, one codegen
unit — what `nest release` ships), which is a harness decision, not a runtime one. `sieve`'s −9.3% carries a 7.7% spread. `startup` −2.3% is inside its 2.4%
spread. Nothing else in the column is within its spread of the previous number.

## The a6a0d934 refresh: `supervisor` −5% again, from the multi-pair `assoc` unroll (2026-09-18, midday)

Min of three interleaved brood-only invocations (spreads 0.2–2.5%), the runtime at brood
`a6a0d934` (`fe8633ba`'s code; the last commit is a docs line). **`supervisor` 584 → 553 ms
(−5.3%, spread 0.6%)** — the `make ab --floor` reading the change landed on (−5.8% against
its base, −4.6% against this column's), 2.2× Elixir → 2.1×: a literal multi-pair
`(assoc st :n i :children xs :ids ids)` now unrolls at compile time into nested single-pair
`MapAssoc` instructions, no rest list and no `%assoc-map-pairs` loop (1.28 → 0.53 µs on a
three-pair loop). The rest of the column is the pre-flight type check, attributed the way the
morning's was: every `BROOD_NO_CHECK=1` run of the moved rows is flat against the previous
column's binary (+0.1–1% instructions) while `brood --check` alone grew **4–7M instructions
per file** — today's checker work (KI-164's guard narrowing, KI-165's runtime enforcement of
`deftype` aliases, C13, C14) — which is 3–4% on a 20–30 ms row and nothing on a long one. Of
the rows past the gate: `strings` +8.8% wall on **+1.4% instructions** (checked run, both
binaries) is the release-fast codegen-partitioning class, not code (brood's CLAUDE.md,
2026-09-17 afternoon), `pipeline` +3.5% is the checker's, `ring` +3.6% on a 1.3% spread with
`pingpong` flat and no message-path change is drift. Nothing in the runtime moved up.
Also in this runtime and not visible in any row: a map literal in a hot arm no longer bails
the arm (`MakeMap` joined the JIT subset). The checker's per-run cost is brood KI-150, and
today's +5M is another data point for its structural option.

## The 04958398 refresh: `supervisor` −5% from the 3-arity `get` and `assoc` primitives (ADR-368) (2026-09-18)

Min of three interleaved brood-only invocations (spreads 0.2–4.7%), the runtime at brood
`04958398`. One row moved: **`supervisor` 614 → 584 ms (−4.9%, spread 0.4%)**, which is the
`make ab --floor` reading the change was landed on (−4.6% against its base, −4.5% at the VM
ceiling) — the 2.3× against Elixir is 2.2×. The mechanism is ADR-362's continued: `(get m k
default)` (every record read-with-default) and `(assoc m k v)` (every record update) were full
calls through the prelude wrapper's `cond`; they are `PrimOp3` instructions now, one VM arm
and one JIT callback each, with rules as narrow as the 2-arity read's — a record's nil result
still reaches `%lookup-miss`, a vector `assoc` still goes through the wrapper. In isolation a
2M-iteration loop of two reads went 1124 → 172 ms (281 → 43 ns a read) and an `assoc` loop
921 → 590 ms (460 → 295 ns); on the supervisor's ~16 µs per child that is the ~1.5 µs the
decomposition below priced the map wrappers at. Everything else read inside its spread:
`ring` −3.3% on a 4.7% spread, `errors` −3.3% on 0.3% (real but small; the recompile of
lazily-loaded bodies, ADR-366, is the only runtime change that could touch it), `sort` +2.7%
on 0.9% (a `sort` reading is the row's own bimodality — see the 2026-09-10 note). Also in this
runtime and NOT visible here, because the harness runs every row with the pre-flight check:
brood ADR-366 — a body compiled before its module lazily loaded kept its pre-load compile shape
for the whole process, 2.8× the instructions on `pipeline` under `BROOD_NO_CHECK=1`; the row's
unchecked path is now the cheapest one. What remains of `supervisor`'s gap is the per-message
floor and the call protocol, unchanged.

## The 0.30.1 refresh: `supervisor` −30% with no edit to the supervisor — the VM got the instructions process code dispatches on (2026-09-17, afternoon)

`supervisor` **879 → 613 ms** (min of 3, spread 0.8%; Elixir 256). Every earlier move on this
row was a supervisor fix; this one changed nothing in `supervisor.blsp`. One `start-child` was
decomposed by layer — a bare send/receive round trip 1.9 µs, `gen/call` 5.0, a `gen/call` that
`spawn-link`s inside the server 7.4, the real `start-child` 22.5 — and the supervisor's own
~15 µs bisected by deletion under a copied module name: nine `get`s and six `assoc`s on the
state map were prelude *wrappers* (5 µs — the wrapper's call and its own `map?`/`vector?`
dispatch, each a Brood call on the VM, cost more than the CHAMP op under it), and the
7-clause loop's `receive` matcher allocated five fail-continuation closures per message and
called one per failing clause (2.2 µs, `ns_match_run` at 19% of the isolated run). None of it
is the supervisor: it is the shape of every `gen` server and every `match` over a message,
which the JIT's profitability gate rightly refuses (`call-mediated-boxed`), so it runs on the
VM interpreter, where a Brood→Brood call is ~70 ns. Four general changes (brood ADR-362): the
`receive` matcher chains clauses as an `or` where `match` would build a thunk; the type
predicates are one instruction (`PrimOp1::TypeIs`, recognised by the `(%eq (type-of x) :kw)`
shape — `vector?` 168 → 67 ns on the VM, 1 ns native); `%vector-ref`/`%vector-length` inline
(the `VectorRef` prim entry had named the native by its pre-`seq/` spelling and was dead
since that rename); and the 2-arity map read is a primitive by default (ADR-296's opt-in,
with a plain map's miss answered inline: a hit 322 → 66 ns, a 100% miss 519 → 123).

The same instructions land everywhere a map or a tagged tuple is read, which is what the
rest of the column shows: `json` **138 → 111 ms** (−19.5%), `nbody` −12.6%, `pingpong` −11.9%,
`spawn-live` −9.1%, `persistent-map` −7.8%, `spawn` −7.1%, `regex` −6.4%, `pipeline` −6%;
nothing moved up beyond its spread. `start-child` is now 16.4 µs against Elixir's ~3, and the
remaining split is recorded in brood's handoff: the messaging floor (~6 µs — `pingpong`'s
class), the VM call protocol (~70 ns per call, ~30 calls per child — the general lever), the
3-arity `get` and `assoc` wrappers (~1.5 µs), `gen/call`'s own interpreted body (1.2 µs).

A trap the sweep set on the way, recorded because it will recur: brood's `make ab` read
`ring` +6% and `pingpong` +7% against sub-1% floors, with instruction counts equal at one
worker, every VM counter identical, and a bisect by variant build blaming a compile-time-only
change. Under `release-lean` (LTO, one codegen unit — what `nest release` and this column's
`make install` ship) the same trees read `pingpong` 182 vs 181 ms and `ring` inside its 2%
spread: `release-fast` has no LTO, and the Rust additions moved the inliner's partition of
the kernel's message path (`copy_cross_heap_rec`, called per message, stopped inlining). A
kernel-path row that moves a few percent with no counter moving is a build-profile question
before it is a code question.

## The 0.30.0 refresh: `pipeline` −52% from fusion, and two loops that were never loops (2026-09-17)

`pipeline` **48 → 23 ms** (min of 3, spread 0.9%): the `(-> (range n) (seq/lfilter …)
(seq/lmap …) (reduce 0 +))` the row is written as now compiles to one native counted loop —
the stage literals substituted in, the range's bounds read once — instead of a transducer
closure per stage called per element through a Rust→native gateway (brood ADR-360 §7:
3 735 → 460 instructions per element; what is left is the `mult35?` call). `bintree` **79 →
75 ms**: the callee nils its own frame, so the inline native call stopped looping over the
callee's slots (call-convention rung A4, first half).

Two things this refresh does NOT show, because no row writes them, and that user code does:
a `letrec`-bound local loop had never compiled to a `SelfCall` — 100 ns per iteration against
a `defn` loop's 2.3 ns, every named local loop in the language (KI-156, fixed the same day)
— and a `fold` with a passthrough-shaped reducer, `(fn (acc x) (+ acc x))`, took the generic
dispatch at 137 ns per element where a non-passthrough body of the same fold took 25 (now the
same 25). A `fold` over a range with any literal is the counted loop: `(fold (range 3M) 0 (fn
(acc x) (+ acc x)))` 410 → 21 ms. The rest of the column is inside the ±3% the box drifts.

## The 2026-09-16 field run: Go joins, and the tally a user writes is the fast one (v0.30.0)

Two things changed at once, and they are separate.

**Go is a full column** (`bench/go/`, one static binary per row, `bench/go/README.md` for the
judgement calls). It lands where the field had a hole — between C and .NET: 1.8× the C floor on
the 15-row aggregate, 1.4× on the single-threaded compute rows, at C's memory (1.8 MB base RSS,
2.3 ms startup). It is the column to read Brood's concurrency rows against now that the BEAM is
not the only scheduler in the field: goroutines are not isolated processes (shared heap, no
mailbox — `spawn-live` copies its payload explicitly and sits in the coroutine table), but they
are preemptively scheduled across cores, and `pingpong` at 24 ms against Brood's 178 and the
BEAM's 58 says what a channel handoff costs against a mailbox with a copying send. `latency`
is the exception: Go's p99 sits with Brood's, not below it — a goroutine that runs for 500 µs
is not preempted (Go's tick is 10 ms), so the requests queued on its P wait, which is the row's
question asked of a third scheduler. Go's aggregate against Brood's is 5.9×; the row set the
overview aggregates did not change (Go runs every `all` row), so this run's overall figures ARE
comparable with the previous ones — unlike the C landing.

**`wordcount` and `persistent-map` are now written as a user writes them.** The review of every
port for idiom found one Brood finding: both called `%map-int-add`, an undocumented kernel
primitive that only the compiler's linear-map rewrite recognised — the idiomatic
`(assoc m k (+ 1 (get m k 0)))` was 8× slower on the same loop. The ports were changed to the
idiom, and brood was changed to recognise it (ADR-360, KI-151 there: `%table-add`, and
`%map-int-add` made exactly the same `+`). The published rows are the idiom: `wordcount` 42 ms
and `persistent-map` 56 ms against 39 / 55 for the primitive spelling at the last refresh —
the same figure, from code nobody has to know a `%` name to write. What is left on those rows
is what was left before: the immutable map against Go's `m[k] += v` (6 ms) is 7–9×, which is
the CHAMP-in-a-table build against a mutating hash map, not the loop.

Everything else in the Brood column is inside the ±10% field drift of the 0.29.2 refresh.

## The 0.29.2 refresh: `bintree` −8% from the call convention's first rungs, `base64` +7% from a checker cost (2026-09-16, evening)

`bintree` **84 → 77 ms** (min of 3, spread 0.1%): brood's call convention work (rungs A0/A1,
`docs/call-convention.md` there) took the inline native→native call from 237 to 213
instructions by moving the per-call save/restore of six activation fields into the callbacks
that read them. The fixed-baseline A/B predicted −7.4%.

`base64` **65 → 70 ms** (+6.6%, spread 1.4%) — over the veto line, so it was bisected before
publishing, with instruction counts because the row's wall is bimodal at 76–80 ms across
binaries: ~5% of it is brood `1a8759fb`, which removed nine declared sigs from `std/encoding`;
`brood file` type-checks a program before running it, and the pre-flight now INFERS those
functions' types on every run (~30 M instructions, ~8 ms) where a declaration was a lookup.
Skip the check and the wave's delta is +1%. Filed as brood **KI-150** for the wave's owner —
the KI-138/139 class, a checker cost paid by every short-lived program. The convention's own
share on this row is +1.6%.

## The 0.29.0 refresh: `regex` −34% from a JIT fix the row had been asking for (2026-09-16)

`regex` **113 → 75 ms** (min of 3, spread 1.2%), and it is a lowering change, not a regex one:
brood ADR-353 (KI-132). Two deopt-thrash mechanisms in the JIT — `=` with a string operand
deopted on every native activation, and a join whose edges carried different representations
(`(or p X)`, `(if c x 7)`) was compiled as an unconditional deopt — meant any arm comparing a
string or merging a boxed value with a scalar ran native for sixteen activations and then
interpreted forever. ADR-352's DFA lexers are exactly that shape. The fixed-baseline A/B read the
row at −30.5% against a 0.8% floor before the refresh, so the published move is the expected
one, not this row's documented ~17% cross-invocation swing (which is still there; see the
measurement traps).

`spawn` reads +5.0% (1.9% spread) and was attributed rather than believed: the delta sits on
the `brood-jit` thread — two arms that used to be refused at lowering now compile
(`%match-splice-fail-in` 3.2 ms, the `receive` matcher 2.9 ms), the per-run compile constant a
short-lived program pays — while direct timings at three `BENCH_N` sizes read parity or
better. The other concurrency rows moved inside their documented drift. Every other row is
within ±2% of the b092e62b column.

## The 0.27.0 refresh: a correctness fix that cost 61% on one row (2026-09-10)

The column had been stale since 0.24.0 (`staleness.py` had been saying so for three
versions). The refresh found the field moving the right way — `startup` −19%, `reduce`
−18%, `http` −17%, `strings` −15%, `wordcount` −11% — and **one row that was not noise:
`errors-deep` +72%**, three interleaved invocations agreeing to 0.6%.

Two `make ab --floor` runs in the brood repo bracketed it to a single commit, `04e0fe36`
(brood's KI-117): the fix that gave JIT'd code a stack trace called a per-native-frame
callback that *built* a trace frame — allocating a copy of the arm's file name — and then
handed it to a `push_trace` which discards everything past a 32-frame cap. 50 frames deep ×
50,000 throws = 2.5M frames built, 1.6M kept, where the 0.24.0 binary built none.

Fixed in brood (KI-123) by consulting `trace_full()` before building, and by making the
frame's file field the `Arc<str>` every producer already holds: **+61% → +19%** against the
pre-fix commit. This column reads **+30% against 0.24.0**, which is the same runtime measured
against an older baseline and with the harness's own pinning rather than `ab-bench`'s.

**The lesson is about which changes get benchmarked.** KI-117 was a correctness fix — days of
work to make a `:trace` appear, guarded by a test asserting the trace's *contents*, reviewed
as a correctness fix. Nothing in that framing suggests running a benchmark, and the row that
would have objected lives in this repo, which is only measured when someone refreshes the
column. When a fix adds work to a path that runs per frame, per element or per message, A/B
the row that exercises it: `./scripts/ab-bench.sh --list` names them and one row is ninety
seconds.

## `sort`'s +8.6% was the 0.24.0 column's own reading, not a runtime regression (CLOSED 2026-09-10)

The 0.27.0 refresh read **`sort` +8.6%** (125.7 vs 115.7 ms wall) and this section filed it as
an open regression somewhere in `8162245c..04e0fe36`, with a three-or-four-point sweep as the
next step. **There is nothing in that range.** The sweep was never needed: the two endpoints
agree with each other, and the gap is in the *baseline reading*.

Re-measured 2026-09-10, both binaries built through `make release-brood`, both `:state :live`
on their own stdlib image and both materialising 9 modules under `BROOD_IMAGE_TRACE=1` (checked
— an image miss is worth ~10 ms, which is the size of the thing being explained):

| method | base `8162245c` | new `7b0327fb` | delta |
|---|---|---|---|
| `make ab --floor sort` — 1-core pin, best-of-7 | 150 ms | 152 ms | +1.3% (floor 0.7%) |
| interleaved min-of-9, cores 8-11 (the harness's own pin) | 125 ms | 128 ms | +2.4% |
| **`bench/harness.py --only sort --langs brood --runs 3`** | **121.8 ms** | **123.8 ms** | **+1.6%** |

Three methods, one box, one session, agreeing on **~+1.5-2.5%** — at or just above this row's
noise floor and under the `max(5%, 2 x floor)` bar. The published columns say +8.6% because
**the unchanged baseline binary measures 121.8-125 ms today against its own published 115.7**.
Nothing about the runtime accounts for that; the 115.7 is simply not reproducible.

Two controls rule out the obvious alternatives. The base is *stable* today — four separate
invocation groups read min 125/126/125/125, a 0.8% spread — so this is not within-session
wander. And the machine was quiet (load 0.02, no stray process older than an hour), so it is
not the orphaned-load-spinner shape that inflated everything measured 2026-09-03 -> 09-08.

**The methodology finding, which is the part worth keeping.** Compute rows are **best of 3**,
and `whklat` is a *laptop* — an i5-11500H on the `powersave` governor, clocking 0.8-3.7 GHz per
core. Best-of-3 is enough to rank languages *within* one session, where every column pays the
same clock state, but it is **not enough to make a row's absolute value comparable across
sessions weeks apart**. A row whose real movement is ~0 can therefore surface as a confident
+8.6% with a "stable, 2.7% spread over three invocations" note attached — the spread was real
and measured *within* the new session, and it says nothing about the old one. Before filing a
single-row regression from a column refresh, **re-measure the OLD commit's binary in the same
session as the new one**; that costs one worktree build and is the only comparison the numbers
support. A/B against a rebuilt baseline is evidence; column-vs-column across sessions is a
hypothesis.

Not investigated, and deliberately not claimed: peak RSS read 238.8 vs 262.0 MB on these two
single runs where the published columns read 245.4 vs 248.5 MB. Single-run RSS on this
allocator is purge-delay dependent (see `MIMALLOC_PURGE_DELAY`), so neither pair is a result.

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
