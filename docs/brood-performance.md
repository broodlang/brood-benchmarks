# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-11). Numbers are compute time (wall − boot) unless noted.

---

## Recently addressed

**Data-structure fixes** (in `main`; see `perf-investigation.md` for the root-cause analysis) — all preserve checksums and tree-walker parity:

- **Inline `nth` / `vector-ref` as a 2-ary VM primitive** (`PrimOp::VectorRef`, a bounds-checked slab read; `(nth v i)` recognised at the call site via a PRELUDE-region identity guard, deopting to the real `nth` for list / out-of-range / default). matmul/bintree.
- **Primitive-reducer fast path in `range_reduce`** for `+` / `*`. **reduce 98 → 21 ms (4.7×)**.
- **Native single-pass `%string-join`**. **strings 140 → 64 ms (2.2×)**.
- **Fixed-arity arms for `get` / `assoc`** (skip the variadic-rest dispatch + `assoc--pairs` loop). **wordcount 209 → 161 ms (1.3×)**.

**JIT fixes** (branch `perf/jit-call-dispatch`):

- **Back-edge tiering** — a self-tail loop is a single arm entry that loops via inline `SelfCall`, so it never reached the per-entry tier threshold and ran interpreted forever. Now `SelfCall` back-edges count toward the threshold and hand the loop to the driver to compile, then run native. **A pure 200M-iter loop went 8 s → 0.55 s (~14.5×); the `loop` benchmark 142 → 26 ms (5.4×).**
- **`VectorRef` Cranelift codegen** (a slab read via `brood_rt_vector_ref`, deopting to the VM on non-vector/out-of-range). With back-edge tiering, matmul's `dot` k-loop now runs native. **matmul 153 → 108 ms (1.4×).** Also fixed a latent crash: the background compiler thread panicked (and silently disabled the JIT) if a `brood_rt_*` symbol wasn't registered in `Jit::new()`.

---

## Where Brood is already good

**Boot time (27 ms)** — fourth-fastest of six, ahead of Ruby and far ahead of the BEAM.

**I/O concurrency (http, 1.4× Node)** — 500 in-flight GETs complete in ~209 ms (wall), 3rd of six behind Node (145 ms) and .NET (175 ms), well ahead of Python/Ruby/Elixir.

**Tight integer loops (now JIT'd)** — with back-edge tiering, `loop` runs at ~26 ms (native), close to the interpreters; the young VM finally has a native path for the most common hot-loop shape.

**Memory** — 14–38 MB across the compute and I/O benchmarks; only Python is as light.

---

## Priority improvement areas

### 1. JIT subset coverage — collatz 288 ms, mandelbrot 74 ms

Back-edge tiering compiles self-tail loops, but `collatz`/`mandelbrot` still run interpreted because their loop bodies fall outside the JIT subset: `collatz` uses `even?` (a call) + `quot`/`rem`, `mandelbrot` is floating-point (the subset is integer-only). Extending the subset — **float arithmetic**, confirming **division (`rem`/`quot`) lowering**, and inlining `even?` — would let these tier like `loop` did.

### 2. Non-tail call dispatch — fib 225 ms, bintree 391 ms, pfib 2.2 s

The remaining big gap. A non-tail call costs ~237 ns in the VM, and a JIT'd arm's calls still round-trip through `brood_rt_call_slow → jit_dispatch_call →` full VM dispatch, so lowering the body doesn't remove it:

- **`fib`** — ~1 M non-tail calls; trivial body.
- **`bintree`** — walk-bound, not alloc-bound (build-only is 0.06 s of the 0.35 s run); `check` is two non-tail recursive calls per node.
- **`pfib`** — *not* a scheduler problem (runs at **1147 % CPU**, ~11.5 cores); it's 100 × `fib(28)` at the per-call cost.

The two-call-recursion *spill* (so such arms can lower) is done on `perf/jit-twocall-spill` but **neutral** without the next step: **native-to-native call linking** (a JIT'd caller invoking a JIT'd callee directly, no VM round-trip), or reducing the VM per-call frame-push/arg-bind cost.

### 3. GC / allocation — bintree 391 ms

Secondary to the call cost above: building/walking many short-lived nodes. A bump-pointer nursery for small short-lived objects would cut per-node allocation.

### 4. String / map residuals — strings 64 ms, wordcount 161 ms

`join`/`get`/`assoc` are addressed; the residuals are `map number->string` (~48 % of `strings`) and the CHAMP map rebuild per `assoc` (`wordcount`). Both measured as low-value / idiom-changing — deprioritised.

---

## Summary table

Compute time (Brood); absolute ms is the stable measure (the "× vs fastest" multiple swings because the fastest language is often sub-millisecond).

| area | benchmark | Brood compute | status |
|------|-----------|---------------|--------|
| tight integer loop | loop | 26 ms | **addressed** — back-edge tiering; runs native |
| array indexing | matmul | 108 ms | **addressed** — `VectorRef` codegen + tiering (153→108) |
| higher-order fold | reduce | 21 ms | **addressed** — primitive-reducer fast path |
| string build | strings | 64 ms | **addressed** — native `%string-join` |
| immutable map churn | wordcount | 161 ms | **addressed** — fixed-arity `get`/`assoc` |
| JIT subset gaps | collatz, mandelbrot | 288 / 74 ms | open — float + division + `even?` shapes bail the subset |
| non-tail call dispatch | fib, bintree, pfib | 225 ms / 391 ms / 2.2 s | open — needs native-to-native call linking |

What is **not** the bottleneck (measured): the scheduler (`pfib` spreads across cores), the allocator/GC (bintree build is cheap), and the VM call-site IC (already caches the resolved `(arm, env)` per site).
