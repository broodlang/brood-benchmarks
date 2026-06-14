# Brood Runtime Performance Investigation

> **Rebased 2026-06-14.** Workload sizes were raised, runs are now CPU-pinned +
> settled (`taskset`), `reduce` became a real higher-order fold, and
> `nqueens`/`pipeline` were added. Absolute ms below are at the **old sizes**; the
> root-cause analysis and relative leverage still apply. Current numbers:
> [`../results/report.md`](../results/report.md), [`../BENCHMARKS.md`](../BENCHMARKS.md).

Audited against `/home/whk/src/broodlang/brood` (runtime) and `brood-benchmarks` (`results/report.whklat.md`). All numbers below are measured on the installed JIT-enabled binary (`BROOD_VM=1 brood`), best-of-N wall, ~28-30ms startup subtracted where noted. Code citations verified against current source.

## 1. Executive Summary — highest leverage first

1. **Inline `nth`/`vector-ref` as a 2-ary VM primitive (`PrimOp::VectorRef`).** matmul ~661ms → ~195ms (**3.4x**, 301x → ~90x), the single biggest lever. Effort: medium. *(impact/effort: highest)*
2. **Native single-pass `%string-join` (skip the interleaved-cons list + reverse).** join phase ~77ms → ~6ms; strings whole-benchmark ~140ms → ~73ms (**~1.9x**, 31.9x → ~16-17x). Effort: medium.
3. **Primitive-reducer fast path in `range_reduce` for `+`/`*`/`max`.** reduce ~98ms → ~60-65ms (**~37%**, 61x → ~38-40x). Effort: small. *(best impact/effort ratio of the three real fixes)*
4. **(Strategic, not a one-fix) Make the tier-1 JIT actually fire on tight loops and naive recursion.** This is the recurring ceiling under loop/fib/collatz/pfib/spawn — see §3. Larger, multi-part effort.

The data-structure fixes (1-3) are the concrete, low-risk, near-term wins. The JIT work (4) is where the order-of-magnitude gaps actually live but is a substantially bigger investment.

---

## 2. Per-fix detail (ordered by leverage)

### Fix 1 — Inline `nth`/`vector-ref` as a 2-ary primitive

**Root cause.** Vectors are already dense O(1) arrays (`heap.rs` `vectors: Vec<Vec<Value>>`; `vector_ref` at `crates/lisp/src/builtins.rs:2741-2756` is a direct slab index). The cost is not storage — it is that `(nth rowa k)` routes through the **prelude variadic** `(defn nth (coll i & default) ...)` at `std/prelude.blsp:505-509`. Each call pays a global lookup + full VM call/frame + the variadic-dispatch machinery, plus the inner `vector?`/`vector-length`/`and`/`>=`/`<` guard calls. The compiler already inlines 1-ary `First`/`Rest` (`compile.rs:113-121`) and 2-ary prims including the heap-touching `Cons` (`compile.rs:138`), so the machinery to add `VectorRef` exists. matmul does ~2 `nth` per inner step over ~512K steps at N=80.

**Code locations.** `std/prelude.blsp:505,508`; `crates/lisp/src/builtins.rs:2741`; `crates/lisp/src/eval/compile.rs:127-143` (`from_native_name`), `:1417-1568` (`prim2_inline`), `:3684-3717` (JIT subset gate, verified: only Add/Sub/Mul/Lt/Le/Eq/Rem/Quot/Div/Cons, catch-all `return None`).

**Proposed change.** Add `PrimOp::VectorRef` to the 2-ary inline set: register in `from_native_name` keyed on `vector-ref`; implement the Int-index bounds-checked slab read in `prim2_inline_fast`/`_exec` (deopt on non-vector/non-int); add to `in_subset_op` so the JIT can lower it to a slab load. Then route `(nth v i)` / `(vector-ref v i)` head-position calls to `Inst::Prim2{VectorRef}`, and give `nth` a fixed 2-arity arm so the common case avoids the variadic dispatch.

**Expected impact.** matmul compute ~661ms → ~195ms (**3.4x**, reproduced), even without JIT. bintree gets ~1.3x (~410ms → ~320ms; 85x → ~65x), secondary — bintree is alloc/GC-bound.

**Effort:** medium. **Risk:** medium. Must preserve `nth` semantics: out-of-range returns `default`/`nil`, not the error `vector-ref` raises — keep the bounds check in the inline path and return `nil` rather than raising. JIT lowering must deopt cleanly on non-vector/non-int. Fixed 2-arity arm interacts with arm selection (`compile.rs` prefers fixed over rest) — needs a test.

**Correction to the original candidate:** the "per-call rest-list allocation / cuts GC pressure" rationale does **not** apply to matmul. `list_from_slice(&[])` returns `Value::Nil` with no allocation, so the 2-arg `(nth v i)` allocates nothing. The win is from removing variadic dispatch + the prelude call frame + the guard sub-calls, not from reduced allocation.

---

### Fix 2 — Native single-pass `%string-join`

**Root cause.** `join` (`std/prelude.blsp:2038-2043`, verified) builds output via `join--parts` consing **2 cells per element** (element + separator) into a reversed accumulator (~2N cons cells), then `(reverse ...)` (a full second traversal/allocation), then `(apply str ...)`. At N=50000 that is ~100K cons cells + a reverse pass. Phase timing of the actual benchmark `(join "," (map number->string (range n)))`: range ~0ms, `map number->string` ~67ms, join ~77ms. Splitting join: cons-build ~31ms + reverse ~50ms dominate; the final `apply str`/`str_concat` is only ~5-6ms.

**Code locations.** `std/prelude.blsp:2036,2038`; `crates/lisp/src/builtins.rs:3028` (`str_concat`).

**Proposed change.** Add a native `(%string-join sep coll)` that walks the collection once, appending each element's display form + separator into one pre-sized `String` — no intermediate cons list, no reverse. Point `join` at it for the `(string-sep, seq)` case; keep the prelude path as fallback for exotic inputs.

**Expected impact.** join phase ~77ms → ~6ms (~13x of the join phase alone). Whole-benchmark is bounded by the untouched `map number->string` (~67ms ≈ 48% of compute): **~140ms → ~73ms ≈ 1.9x**, moving strings 31.9x → ~16-17x vs python. Still double digits — the "toward single digits" framing was optimistic.

**Effort:** medium. **Risk:** medium. Must match `join` semantics exactly: display form via `str` for non-string elements, `""` for empty collection, no trailing sep for single element; handle lists, vectors, and ranges (`seq_items`).

**Note:** str_concat is only ~6ms here, so combining with a separate str_concat optimization adds little to join.

---

### Fix 3 — Primitive-reducer fast path in `range_reduce`

**Root cause.** `reduce` → `fold` → `%range-reduce` (`range_reduce`, `crates/lisp/src/builtins.rs:2619`) calls `apply_value(heap, f, &[acc, Value::Int(i)], env)` once per element (`builtins.rs:2642`, verified). For `(reduce + 0 (range n))`, `f` is the multi-arity Brood `+` closure (`std/prelude.blsp:132`) whose 2-arg arm is the passthrough `(%add a b)` (`:135`). There is **no primitive-reducer fast path** (confirmed). The residual per-element cost is the **passthrough-resolution machinery**, not frame push/pop: `dispatch`'s passthrough-redirect (`compile.rs:2194-2229`) detects `+`'s arm is a pure passthrough, resolves the inner `%add` native (`eval/mod.rs:830`), and calls `call_native` directly (ADR-069) — but it re-reads the closure, runs `select_arm`/`passthrough_arm`, and does an `env_get` of the inner `%add` symbol **every iteration**. That `env_get` is what the ~1.1/element count measures (passthrough resolution, not a frame bind), plus the `apply_value`/dispatch entry.

**Code locations.** `crates/lisp/src/builtins.rs:2619,2642`; `crates/lisp/src/eval/compile.rs:919` (`resolve_prim`); `std/prelude.blsp:132,135`.

**Proposed change.** Before the loop in `range_reduce`, test whether `f` is a known primitive (`+`/`*`/`min`/`max`/`%add`/`%mul`) via `resolve_prim` on the closure name, guarded by an epoch check. If so, run the reduction with the inlined i64/float primitive directly — same op the VM's `Prim2` inline uses, with overflow → BigInt promotion to match `%add` semantics — skipping `apply_value` entirely. Fall back to per-element apply otherwise.

**Expected impact.** Measured ceiling: at N=4M, `reduce +` 430ms, `reduce %add` (native head, no passthrough hop) 280ms, hand-loop 270ms — the passthrough hop costs ~150ms/4M (~37ns/elem). So reduce compute **~98ms → ~60-65ms (~37%)**, 61x → ~38-40x vs dotnet. **Not** a 2x "halving" — the original candidate's N=1e6 micro-benchmark (132 vs 80ms) was noisy; real ratio ~1.6x. reduce stays an order of magnitude behind JIT'd languages because ~60% of per-element cost is the `apply_value`/dispatch entry + range iteration + heap boxing, which this fix does not touch.

**Effort:** small. **Risk:** low — additive fast path guarded by exact operator-identity + epoch check (self-heals if `+` is redefined); must promote on overflow exactly as `%add` does to stay bit-identical.

---

### Out-of-area note: wordcount (28.5x)

Not in the worst-gap list and **not** an indexing/string fix. wordcount's hot loop (`bench/brood/wordcount.blsp:10`) is `(gen x2 (assoc m key (+ (get m key 0) 1)) (+ i 1))` — pure immutable CHAMP map churn (fresh map per iteration, N=100000), no `nth`/`vector-ref`/`join`. The real lever belongs to the maps owner: a transient build via `transient`/`assoc!`/`persistent!` (already exist, `builtins.rs:401-425`). Measured: transient rewrite (same checksum 50038280) cut wall ~0.70-0.77s → ~0.18-0.49s (~2x cold, up to ~4x warm). Flagged so no indexing effort is misattributed here.

---

## 3. The JIT — does it fire? (the recurring ceiling)

**Mostly no, and where it does it's the wrong arm.** This is the single recurring reason the compute benchmarks sit 50-300x behind V8/RyuJIT. Verified via `BROOD_JIT_TRACE` and `perf-stats` builds:

- **loop, fib, reduce, spawn, pfib: zero native iterations.** For loop, the arm reads global `n` every iteration via `Inst::GlobalIc` (`global_ic_hit`=1,000,000); the JIT subset **pre-bails on any `Global`/`GlobalIc`** (`compile.rs:3717` catch-all `return None`, verified above), so even a tiered arm runs zero native iterations. Separately, the tiering counter only increments on arm entry (`jit_tier` invoked only from `compile.rs:3340`/`:3453`), while a self-tail loop is one activation that loops via `continue` — so a global-free in-subset self-loop gets **2** `jit_tier` calls over 2M iterations, never reaching `THRESHOLD=8`. Two independent blockers stacked on loop.
- **fib/pfib/spawn:** the body `(+ (fib (- m 1)) (fib (- m 2)))` bails because the first call's result sits on the operand stack as `Op::Handle` below the second non-tail call (`compile.rs:4335-4338`) — the safepoint can't keep a heap ref in a register across the second call. `jit_native_run`=0; 100% interpreted. Bare spawn of 20k green processes = 0.47s, but spawn-with-fib = 13.5s — i.e. ~13s is VM `fib(15)` × 20000, **not** the scheduler. The scheduler cannot beat the per-core VM floor.
- **collatz:** the **hot** `steps` arm (~1.87M self-tail iters, all-subset prims) **does** reach native code today (real installed pointer observed; `prim2_inline`≈9.8M). Only the lightweight outer `scan` (reads global `n`, calls `steps`/`max`) bails. So collatz's dominant work is already native — its residual gap is subset coverage (Call/Global/division), not tiering.

**Is fixing tiering the single biggest win?** It is the biggest *category*, but no single tiering tweak moves the named benchmarks alone — they each need a *different* subset/lowering gap closed:
- **loop** needs `GlobalIc`-in-subset **and** back-edge tiering (both, gated on each other).
- **fib/pfib/spawn** need naive two-call recursion lowered — spilling the first call result to a heap-rooted slot that survives the safepoint across the second call. This is the highest-value but highest-risk (memory-safety) JIT work; `brood_rt_call_slow` (`jit/mod.rs:304`) is currently `unimplemented!()`.
- **collatz** needs Call/Global/division in the subset so `scan` stops re-entering the interpreter per call.

The honest framing for the maintainer: the JIT exists and works for a narrow shape (in-subset self-tail integer loops), but **every** worst-gap compute benchmark falls outside that shape for a benchmark-specific reason. Closing the subset (Global, Call, VectorRef, division) and fixing back-edge tiering is the strategic program; Fix 1's VectorRef-in-subset is the first concrete step of it.

---

## 4. Investigated and rejected

- **"Tiering counter only increments on arm entry, starving self-tail loops."** Root cause is **real and confirmed** (a global-free in-subset self-loop gets 2 `jit_tier` calls over 2M iters), but it moves **no named benchmark alone**: loop is additionally gated on the deferred `GlobalIc`-in-subset fix; collatz **already** tiers (real native pointer for `steps`); fib already reaches the gate and the change doesn't fix it; reduce is a HOF fold out of subset. Real bug, but not a standalone benchmark win.
- **"Add `GlobalIc`/`Global`/`Call` to the JIT subset."** The whitelist gap is real (`compile.rs:3717`), but the candidate's supporting "WIP tree" evidence was **fabricated** (no `brood_rt_global`/`jit_dispatch_call`/`jit_resolve_global` exist; build is clean). And the scope is overstated: reduce gets zero benefit (no tiered arm at all), collatz's hot arm already JITs, fib gain is moderate and rides the unbuilt `brood_rt_call_slow`. Only loop is a clean target, and it's gated on tiering anyway.
- **"Call-site IC caches only the arm, not the callee value, so a free-global callee re-walks `env_get` every call."** Source reading accurate (callee dropped at `compile.rs:3056/3061`), but the central empirical claim **did not reproduce** when the candidate's own "option (a)" change was applied faithfully — and the JIT doesn't fire on these benchmarks anyway, so the "addressed by JIT-call work" premise is moot today.

---

## 5. Suggested sequence

1. **Fix 1 (VectorRef prim).** Biggest single win, exercises the JIT-subset extension path. **Measure:** `BROOD_VM=1 brood bench/brood/matmul.blsp` at N=80, best-of-3 wall minus ~28ms startup; expect ~0.78s → ~0.22s. Confirm bintree gets the secondary ~1.3x. Add a `nth` out-of-range / fixed-vs-rest-arm test.
2. **Fix 3 (primitive reducer).** Small, low-risk, immediately bankable. **Measure:** `(reduce + 0 (range 4e6))` best-of-5; expect to match the `reduce %add` path (~430ms → ~280ms wall). Verify overflow→BigInt parity and `+`-redefinition self-heal.
3. **Fix 2 (`%string-join`).** **Measure:** phase-split the strings benchmark (range/map/join); expect join ~77ms → ~6ms, whole ~140ms → ~73ms. Assert join semantics on empty/single/non-string/range inputs.
4. **JIT program (strategic, after 1-3).** Order: (a) extend the subset with `VectorRef` (done in Fix 1), division, then `Global`/`GlobalIc`; (b) back-edge tiering for self-tail loops; (c) the hard one — heap-rooted-slot spill for two-call recursion so fib/pfib/spawn can lower, building out `brood_rt_call_slow`. **Measure each** with `BROOD_JIT_TRACE` (look for a real native code pointer + `jit_native_run` > 0) and the per-benchmark wall, not just aggregate.

Measurement hygiene throughout: best-of-N (N≥3, ideally 5), subtract ~28-30ms startup, and confirm checksums/outputs are unchanged before trusting any timing.
---

## 6. Follow-up findings (2026-06-13, post-JIT-arc)

Two runtime fixes landed after the JIT call-path arc (brood `32bbda7`, `67c2ec2`),
both root-caused by profiling rather than the initial hypothesis:

- **Parallel allocation was serialized by the *symbol-interner mutex*, not the
  allocator.** A microbench of N allocation-heavy green processes (each building a
  ~200-entry map in a loop) scaled terribly — 8 procs ≈ 6× one. The natural guess
  (and the brood roadmap's) was a global lock on the allocation/collection path.
  Wrong: per-process heaps bump-allocate lock-free. `perf record` on the 8-proc run
  showed ~45 % kernel/futex, **10 % `Mutex::lock_contended`, 9.5 % `value::intern`**
  — every `intern` took the global `IDS` mutex *even on a hit*, and hot code
  re-interns the same names constantly. Fix: a thread-local name→id cache (hot path
  lock-free; the global mutex only mints new ids). Sharding the global alloc
  byte-counter (`fetch_add` + a `fetch_max` CAS loop per alloc) across 64
  cache-padded counters removed the *secondary* point. **8 procs 10.8 s → 3.4 s
  (~1.3× → ~4× parallelism); `spawn` ~9 %.** Lesson: confirm the contended resource
  with `perf` before sharding — the first sharding attempt (allocator only) moved
  nothing because the interner mutex dominated.

- **Transients corrupted across a *tenuring* collection.** `assoc!`-building a
  transient whose values allocate panicked nondeterministically. Cause: once the
  build crosses `min_tenure` the transient cell tenures to the old gen; a later
  `assoc!` points its root at a young node (an OLD→YOUNG edge), and a minor *flip*
  skips the old gen, dangling the root. Fixed with a `remembered_transients` write
  barrier; the prelude's multi-assoc combinators (`merge`/`update-vals`/…) now build
  through a transient (~1.4–1.6×).

Regression check on the merge: an old-vs-new A/B (load-independent
`perf stat -e instructions` + best-of-N wall) found the suite neutral within noise
— `spawn` improved, a +2–4 % instruction bump on the JIT'd integer loops
(`loop`/`collatz`) from the call-path/lazy-slot refactor, nothing else moved.

## 7. Float JIT attempt — `mandelbrot` (2026-06-14, brood branch `perf/jit-float`, NOT merged)

Pursued §3/§4's float gap: `mandelbrot`'s `esc` is a pure-`f64` self-tail loop, so if it
lowered it would run native like `loop`/`collatz` did. The float codegen was implemented and
is **correct** — a top-level pure-`f64` self-tail loop runs native (**~20×**, 4.06s→0.20s,
exact-bit vs `BROOD_VM=0`) — but **`mandelbrot` did not win**, and the reason is instructive.

`esc`'s win is blocked not by floats but by its **nested self-tail control flow**, which trips
a *different* deep tier-1-JIT bug under every structural form of `(if (and (<= …) (< i maxi)) …)`:

- **`and` (as written).** `(and a b)` → `(let (g a) (if g b g))`; the 2nd compare (an `i8`
  bool) crosses a block boundary at the inner-`if` merge. The Cranelift verifier rejects the
  bare-`i8` block-arg; zero-extending to `i64` fixes that, then `esc` runs native and correct
  for ~5000 iterations and **hangs** — `perf` shows a **preempt/back-edge ping-pong**
  (`vm_run_bc` → esc-native + `brood_rt_tick`, not converging once the reduction budget
  exhausts). The same shape *without* `and` handles preempt fine.
- **Nested `if`** (`(if A (if B X Y) Y)`, no bool value-merge). No hang, correct, but **bails**
  a block-param *depth mismatch* (`jump block5(v224): got 1, expected 2`) — the dead `Jump`
  after the tail `SelfCall` inside the nested then-branch breaks the leader/depth analysis.

A pre-existing JIT bug *was* fixed along the way (worth keeping): `and`/`or` in any hot arm
deopted because `JumpIfFalse` tag-checked a boxed `Bool` condition `== Int`; it now branches on
Brood truthiness, so slot-based `and`/`or` lower.

**Net:** float codegen sound; `esc` stays on the VM (crossing-widening reverted → no hang, no
win, ~+2 % tiering overhead). Unlocking it needs real JIT-internals work (fix the preempt
ping-pong for multi-merge-block arms, or the depth analysis for dead-jumps-after-tailcall, or
type-aware block params) — a focused project, not a small change. Full write-up: brood
`docs/jit-float.md` on `perf/jit-float`.
