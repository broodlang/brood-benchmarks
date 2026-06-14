# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-13). Numbers are compute time (wall − boot) unless noted.

The absolute tables below were measured on commit `939aba3` (the JIT call-path
arc). Several wins have since landed on `main` (`32bbda7`, `67c2ec2`, `84d3315`,
`b99756d`). A load-independent A/B (`perf stat -e instructions`, current main vs
`939aba3`) gives the **cumulative compute delta** — the run machine has stayed
loaded, so this instruction-count A/B, not a fresh wall-clock run, is the reliable
"where we are":

| benchmark | Δ instr vs `939aba3` | driver |
|-----------|----------------------|--------|
| **bintree**   | **−13.6 %** | type-of keyword cache + JIT'd `make` (2-elem vector literal) |
| **strings**   | **−4.6 %**  | type-of keyword cache |
| **sort**      | **−4.2 %**  | type-of keyword cache |
| **wordcount** | **−2.9 %**  | type-of keyword cache |
| collatz / matmul / primes / mandelbrot / reduce / fib | ±0.8 % | neutral |
| **loop**      | **+3.1 %**  | lazy-slot tag-check regression (call-path refactor; tracked) |

Not in this compute survey: **`spawn` ~−9 %** (the interner/parallel-alloc fix, a
wall-clock/concurrency effect) and the **transient map combinators ~1.4–1.6×**
(`merge`/`update-vals`/… — paths the micro-suite doesn't isolate). The `loop`
+3.1 % is a real but small regression from the lazy-slot rework (a redundant
per-iteration tag-check on slot args), more than offset by the wins above and
tracked for recovery. The absolute tables predate these and so slightly *overstate*
the current times (bintree most); a fresh clean-load full run is pending.

---

## Recently addressed

**`type-of` keyword cache** (`main`, commit `84d3315`) — `type-of` returned
`value::kw(tag.name())`, re-interning the tag-name string on every call. The seq
predicates (`nil?`/`pair?`/`empty?`/… are all `(%eq (type-of x) :kw)`) hit it once
per element, so on list-heavy code it was *the* interning cost — a backtrace +
counter showed `"pair"` was ~98 % of all interns (one per cons, via iteration's
`nil?`/`pair?`). Caching the interned keyword per `Tag` (a fixed set of 19) made
`type-of` intern-free. **bintree −6.9 %, strings −4.9 %, sort −4.4 %, wordcount
−3.2 %, collatz −3.1 %, matmul −1.9 %** (instructions); reduce/primes/fib neutral.

**JIT'd 2-element vector literals → bintree's `make` runs native** (`main`, commit
`b99756d`) — the JIT already allocated (`cons`) and read vectors (`VectorRef`), but
a `[a b]` literal (`MakeVector(2)`) bailed, so `make`
(`(if (= d 0) nil [(make …) (make …)])`) stayed interpreted despite being a clean
two-call recursion the spill path handles. No CFG-model change was needed: the
nil/vector branches merge through `roots[base]` (handle-capable), so only two small
additions — a `brood_rt_make_vector2` bump-allocate helper (mirroring `cons`) and
admitting `Const(Nil)` to the JIT subset. **bintree −6.6 %** more (−13.6 %
cumulative with the type-of cache); every other benchmark dead-neutral; VM-vs-JIT
differential corpus agrees, GC_VERIFY clean. First time the JIT emits a
heap-allocating vector literal. (`make`'s sibling `check`, the walk, is still
interpreted — 3 calls + VectorRef, and the link benefit gate measured it neutral.)

**Parallel allocation: thread-local intern cache + sharded alloc counter**
(`main`, commit `67c2ec2`) — allocation-heavy green processes barely scaled (8 ran
~6× one, near-serial). Profiling the fan-out showed the bottleneck was **not** the
heap allocator (per-process heaps bump-allocate lock-free) but the **global
symbol-interner mutex**, taken on every `intern` including hits (call heads,
keywords, fields re-interned constantly): ~10 % `lock_contended` plus the futex
waits behind it. A **thread-local intern cache** makes the hot path lock-free
(ids are append-only + globally consistent, so a cached id is valid forever);
sharding the global alloc byte-counter (a `fetch_add` + a `fetch_max` CAS loop per
alloc) across 64 cache-padded counters removes the secondary point.
**8 alloc-heavy processes 10.8 s → 3.4 s (effective parallelism ~1.3× → ~4×);
`spawn` ~9 % faster.** This is the runtime ceiling `brood-life` flagged (its
SIM/RENDERER split was a frame-time no-op because both are allocation-bound).

**Transient GC fix + transient-built map combinators** (`main`, commit `32bbda7`)
— a live `transient` tenured to the old gen, then mutated, created an OLD→YOUNG
edge a minor flip skipped, dangling its root (silent corruption in release). Fixed
with a `remembered_transients` write barrier. With the surface now GC-safe across
safepoints, the prelude's multi-assoc combinators (`merge`, `merge-with`,
`select-keys`, `update-vals`, `update-keys`) build through a transient instead of
folding immutable `assoc` — **merge ~1.6×, update-vals ~1.4×** on large inputs.
Not isolated by the micro-suite (`wordcount` uses `reduce`+`assoc`, not these),
but it roughly halves `brood-life`'s `recolor` map-build cost.

**Data-structure fixes** (in `main`; see `perf-investigation.md` for the root-cause analysis) — all preserve checksums and tree-walker parity:

- **Inline `nth` / `vector-ref` as a 2-ary VM primitive** (`PrimOp::VectorRef`, a bounds-checked slab read; `(nth v i)` recognised at the call site via a PRELUDE-region identity guard, deopting to the real `nth` for list / out-of-range / default). matmul/bintree.
- **Primitive-reducer fast path in `range_reduce`** for `+` / `*`. **reduce 98 → 21 ms (4.7×)**.
- **Native single-pass `%string-join`**. **strings 140 → 64 ms (2.2×)**.
- **Fixed-arity arms for `get` / `assoc`** (skip the variadic-rest dispatch + `assoc--pairs` loop). **wordcount 209 → 161 ms (1.3×)**.

**JIT fixes** (branch `perf/jit-call-dispatch`):

- **Back-edge tiering** — a self-tail loop is a single arm entry that loops via inline `SelfCall`, so it never reached the per-entry tier threshold and ran interpreted forever. Now `SelfCall` back-edges count toward the threshold and hand the loop to the driver to compile, then run native. **A pure 200M-iter loop went 8 s → 0.55 s (~14.5×); the `loop` benchmark 142 → 26 ms (5.4×).**
- **`VectorRef` Cranelift codegen** (a slab read via `brood_rt_vector_ref`, deopting to the VM on non-vector/out-of-range). With back-edge tiering, matmul's `dot` k-loop now runs native. **matmul 153 → 114 ms (1.3×).** Also fixed a latent crash: the background compiler thread panicked (and silently disabled the JIT) if a `brood_rt_*` symbol wasn't registered in `Jit::new()`.
- **Two codegen bails that kept `collatz` interpreted** (found by profiling — both general, not collatz-specific). (a) `chunk_ops_all_native` compared a `Prim2SlotInt`'s *stored* arg-map against `resolve_prim`'s *natural* map; a `(Const, Local)` fusion like `(* 3 m)` inverts the map (`swapped`), so a valid arm was spuriously marked BAILED and never compiled — now the swapped map is un-inverted before comparison. (b) `jit_lower_arm` failed an arm on a `Jump`-to-`Done` whose operand stack wasn't exactly 1, but that's dead code after a tail `SelfCall` (which never falls through) — now routed to `deopt`. With both fixed, `collatz`'s `steps` self-tail loop compiles and runs native. **collatz 289 → 77 ms (~3.8×).**

**Native-to-native call linking** (in `main`) — closes the non-tail-call gap that had been the largest remaining frontier. A JIT'd arm's non-tail Brood→Brood call used to round-trip through the full VM dispatch chain (`dispatch → vm_apply → vm_run_bc → jit_tier`) even when the callee already had native code. Now `jit_dispatch_call` links directly to a native callee — sets up its frame and calls its entry, skipping the chain. Pieces: a **handle spill** so two-call recursion (`fib`'s `(+ (fib …) (fib …))`) can lower at all; the **direct link** with a native-recursion depth cap that drains overflow onto the VM (so deep non-tail recursion stays at VM parity instead of aborting); and a **tiering back-off** when the compile queue saturates (without it, 20 000 short-lived `spawn` processes each tiering their own arm copy thrashed the queue with ~36 M redundant re-validations — found with `perf`). Result (vs the prior run): **fib 218 → 136 ms (1.6×), pfib 2246 → 1259 ms (1.8×), bintree 345 → 295 ms (1.2×), loop 26 → 19 ms (1.4×), collatz 77 → 63 ms (1.2×)**; `spawn`/`http` neutral (verified same-machine: no regression); everything else within noise. All checksums + tree-walker parity preserved.

**Per-call cost: cache + eliminate the call target** (in `main`) — profiling the linked path showed the native fib arithmetic was <1 %; the rest was per-call dispatch, dominated by re-resolving the callee every call. Three cuts:

- **Call-site inline cache.** `jit_dispatch_call` resolves the callee's compiled arm through the VM's existing per-site `vm_call_ic` (epoch-stamped) instead of a `compiled_arm_for` / `vm_cache_arm` lookup every call (~23 % of pfib). **fib/pfib −20 %.**
- **In-place frame setup + JIT state on the heap.** The staged args become the callee frame in place (no temp copy, no re-push); the per-call JIT state (env / native-depth / force-VM / pending-error) moved from thread-locals to `Heap` fields (plain loads, ~4×/call) — also fixing a `force_vm`-loss bug under worker migration. **fib −12 %, pfib −15 %.**
- **Call-head elision** (the deep simplification). A free-global call no longer emits a head `Global` to stage the callee — the `Inst::Call` carries `head`+`site` and owns resolution via the call IC, so the per-call call-head `env_get` is gone for **both** the VM and the JIT, and the bytecode is one inst shorter per call. **fib −30 %, pfib −38 %, spawn −11 %, bintree −10 %, wordcount −6 %**; loop/matmul neutral.

Cumulative over the call-path arc: **fib 218 → 66 ms (3.3×), pfib 2342 → 460 ms (~5×, now ahead of Ruby), spawn 1447 → 1281 ms.** `fib` now matches Elixir/Python; `pfib` beats Ruby.

---

## Where Brood is already good

**Boot time (27 ms)** — fourth-fastest of six, ahead of Ruby and far ahead of the BEAM.

**I/O concurrency (http, 1.4× Node)** — 500 in-flight GETs complete in ~221 ms (wall), 3rd of six behind Node (158 ms) and .NET (184 ms), well ahead of Python/Ruby/Elixir.

**Tight integer loops (now JIT'd)** — with back-edge tiering, `loop` runs at ~18 ms (native), faster than every interpreter in the field; the young VM finally has a native path for the most common hot-loop shape.

**Memory** — 14–38 MB across the compute and I/O benchmarks; only Python is as light.

---

## Priority improvement areas

### 1. JIT subset coverage (float) — mandelbrot 75 ms

`mandelbrot`'s `esc` is a self-tail loop, but it bails immediately: it's floating-point and the JIT subset is integer-only (it bails on the first float constant). Float support needs **type-specialized tiering** — design in `docs/jit-float.md` (brood repo). This is now the only integer-vs-float gap: `collatz`, the other self-tail loop that wasn't tiering, was an all-integer arm blocked by two codegen bugs (now fixed — see "Recently addressed").

### 2. GC / allocation — bintree 247 ms

Still the largest single integer benchmark, down from 282 ms (type-of cache +
JIT'd `make`; **−13.6 %** by instruction count, confirmed by a low-load re-run). `bintree` is build + walk: `make` now runs native (the JIT
emits its `[a b]` node literal — commit `b99756d`); the **walk (`check`) is the
remaining interpreted half** — it's a two-call recursion + `VectorRef` + a `nil?`
call (3 calls), and the link benefit gate measured it neutral, so it stays on the
VM. Beyond that, a bump-pointer nursery for the many short-lived nodes would cut
per-node allocation. The residual after `make` went native is the `check` walk and
the node allocation.

### 3. String / map residuals — strings 64 ms, wordcount 163 ms

`join`/`get`/`assoc` are addressed; the residuals are `map number->string` (~48 % of `strings`) and the CHAMP map rebuild per `assoc` (`wordcount`). Both measured as low-value / idiom-changing — deprioritised.

---

## Summary table

Compute time (Brood); absolute ms is the stable measure (the "× vs fastest" multiple swings because the fastest language is often sub-millisecond).

| area | benchmark | Brood compute | status |
|------|-----------|---------------|--------|
| tight integer loop | loop | 18 ms | **addressed** — back-edge tiering; runs native |
| integer self-tail loop | collatz | 63 ms | **addressed** — fixed two codegen bails (289→77, ~3.8×); linking → 63 |
| array indexing | matmul | 104 ms | **addressed** — `VectorRef` codegen + tiering (153→104) |
| higher-order fold | reduce | 20 ms | **addressed** — primitive-reducer fast path |
| string build | strings | 64 ms | **addressed** — native `%string-join` |
| immutable map churn | wordcount | 163 ms | **addressed** — fixed-arity `get`/`assoc` |
| non-tail call dispatch | fib, pfib | 66 ms / 460 ms | **addressed** — linking + call-site IC + call-head elision (fib 3.3×, pfib ~5×; pfib now ahead of Ruby) |
| allocation / walk | bintree | 247 ms | **partly addressed** — linking/elision + type-of cache + JIT'd `make` (348→247); residual is the interpreted `check` walk (links neutral) + node alloc |
| JIT subset gap (float) | mandelbrot | 75 ms | open — integer-only subset; needs float specialization (docs/jit-float.md) |

What is **not** the bottleneck (measured): the scheduler (`pfib` spreads across cores) and the VM call-site IC (already caches the resolved `(arm, env)` per site). With non-tail dispatch addressed, the main open frontier is **float JIT** (mandelbrot) and **allocation** (bintree).
