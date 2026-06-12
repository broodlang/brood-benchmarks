# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-12). Numbers are compute time (wall − boot) unless noted.

---

## Recently addressed

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

---

## Where Brood is already good

**Boot time (27 ms)** — fourth-fastest of six, ahead of Ruby and far ahead of the BEAM.

**I/O concurrency (http, 1.4× Node)** — 500 in-flight GETs complete in ~221 ms (wall), 3rd of six behind Node (158 ms) and .NET (184 ms), well ahead of Python/Ruby/Elixir.

**Tight integer loops (now JIT'd)** — with back-edge tiering, `loop` runs at ~24 ms (native), close to the interpreters; the young VM finally has a native path for the most common hot-loop shape.

**Memory** — 14–38 MB across the compute and I/O benchmarks; only Python is as light.

---

## Priority improvement areas

### 1. JIT subset coverage (float) — mandelbrot 75 ms

`mandelbrot`'s `esc` is a self-tail loop, but it bails immediately: it's floating-point and the JIT subset is integer-only (it bails on the first float constant). Float support needs **type-specialized tiering** — design in `docs/jit-float.md` (brood repo). This is now the only integer-vs-float gap: `collatz`, the other self-tail loop that wasn't tiering, was an all-integer arm blocked by two codegen bugs (now fixed — see "Recently addressed").

### 2. GC / allocation — bintree 295 ms

Now the largest single integer benchmark. `bintree` is walk-bound, and native-to-native linking already lowered the `run` driver loop and cut the walk (`check`) cost (345 → 295 ms); the residual is building/walking many short-lived nodes. A bump-pointer nursery for small short-lived objects would cut per-node allocation. (`check` itself stays on the VM — a `VectorRef`-walking two-call arm regresses if linked, so the benefit gate excludes it.)

### 3. String / map residuals — strings 62 ms, wordcount 157 ms

`join`/`get`/`assoc` are addressed; the residuals are `map number->string` (~48 % of `strings`) and the CHAMP map rebuild per `assoc` (`wordcount`). Both measured as low-value / idiom-changing — deprioritised.

---

## Summary table

Compute time (Brood); absolute ms is the stable measure (the "× vs fastest" multiple swings because the fastest language is often sub-millisecond).

| area | benchmark | Brood compute | status |
|------|-----------|---------------|--------|
| tight integer loop | loop | 26 ms | **addressed** — back-edge tiering; runs native |
| integer self-tail loop | collatz | 77 ms | **addressed** — fixed two codegen bails (289→77, ~3.8×) |
| array indexing | matmul | 107 ms | **addressed** — `VectorRef` codegen + tiering (153→107) |
| higher-order fold | reduce | 22 ms | **addressed** — primitive-reducer fast path |
| string build | strings | 63 ms | **addressed** — native `%string-join` |
| immutable map churn | wordcount | 157 ms | **addressed** — fixed-arity `get`/`assoc` |
| non-tail call dispatch | fib, pfib | 136 ms / 1.26 s | **addressed** — native-to-native call linking (fib 1.6×, pfib 1.8×) |
| allocation / walk | bintree | 295 ms | **partly addressed** — linking lowered the driver loop (345→295); residual is node alloc |
| JIT subset gap (float) | mandelbrot | 75 ms | open — integer-only subset; needs float specialization (docs/jit-float.md) |

What is **not** the bottleneck (measured): the scheduler (`pfib` spreads across cores) and the VM call-site IC (already caches the resolved `(arm, env)` per site). With non-tail dispatch addressed, the main open frontier is **float JIT** (mandelbrot) and **allocation** (bintree).
