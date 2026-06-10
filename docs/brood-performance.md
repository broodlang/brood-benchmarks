# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-10). Numbers are compute time (wall − boot) unless noted. Ratios are "× vs the fastest language" (a denominator floored at 1 ms, so a sub-millisecond winner shows as a large multiple).

---

## Recently addressed (this session)

Three data-structure fixes landed in the runtime (see `perf-investigation.md` for the full root-cause analysis); all preserve checksums and tree-walker parity:

- **Inline `nth` / `vector-ref` as a 2-ary VM primitive** (`PrimOp::VectorRef`, a bounds-checked slab read; `(nth v i)` recognised at the call site via a PRELUDE-region identity guard, deopting to the real `nth` for the list / out-of-range / default cases). **matmul 661 → 152 ms (4.3×)**; **bintree 401 → 336 ms (1.2×)**. Redefinition-safe.
- **Primitive-reducer fast path in `range_reduce`** for `+` / `*` (fold with the inlined scalar op, skipping per-element `apply_value`; overflow defers to BigInt). **reduce 98 → 21 ms (4.7×)**.
- **Native single-pass `%string-join`** for a string separator (one pre-sized buffer, no interleaved cons list + reverse). **strings 140 → 63 ms (2.2×)**.
- **Fixed-arity arms for `get` / `assoc`** (the single-pair `(assoc m k v)` and `(get m k d)` map cases compile to bytecode and hit `map-assoc`/`map-get` directly, skipping the variadic-rest dispatch + `assoc--pairs` loop). **wordcount 209 → 162 ms (1.3×)**.

Separately, the tier-1 JIT was extended to **Brood→Brood calls** (non-tail + tail-call TCO), so it now fires on call-shaped bodies, not just self-tail integer loops.

---

## Where Brood is already good

**Boot time (28 ms)** — fourth-fastest of six, ahead of Ruby and far ahead of the BEAM. Fine for a scripting/application runtime.

**I/O concurrency (http, 1.5× Node)** — the green-process model handles concurrent I/O well: 500 in-flight GETs complete in 214 ms (wall), 3rd of six behind Node (145 ms) and .NET (174 ms), well ahead of Python/Ruby/Elixir. The actor-style network stack is working.

**Sort (64 ms wall, ~2× Node)** — stays within ~2× of most runtimes; the built-in sort and list representation are reasonably efficient.

**Memory** — 14–38 MB across the compute and I/O benchmarks; only Python is as light. The heap is compact and allocation volume is not the dominant problem outside `bintree`.

---

## Priority improvement areas

### 1. Tight loop / per-instruction overhead — loop 142 ms, collatz 301 ms, matmul 153 ms (≈60–70× the JITs)

The remaining worst compute results share one root cause: a fixed per-operation overhead that compounds over millions of iterations. With the indexing cost removed (below), `matmul`'s residual gap is now this same per-op overhead, not data-structure access.

**Suggestions:**
- Land the JIT subset extensions that these need: `Global`/`GlobalIc` in-subset (so `loop`'s global read stops bailing the arm) and back-edge tiering for self-tail loops. See `perf-investigation.md` §3.
- Reduce root-stack overhead — every intermediate is heap-rooted via `Vec` ops where the BEAM uses register addressing.

### 2. Array indexing — addressed (matmul 661 → 153 ms, 4.3×)

`(nth v i)` / `(vector-ref v i)` now inline to a direct slab read instead of routing through the variadic prelude `nth` + a native call (the previous ~5× per-access overhead, isolated by micro-benchmark: 50 s → 9 s for 10 M reads). matmul improved 4.3×. The remaining gap is per-op overhead (area 1), not indexing.

### 3. Parallel scheduling — pfib 2.3 s, spawn 1.3 s

`pfib` (100 × fib(28) in parallel) takes ~2.5 s vs .NET's 40 ms; on 12 cores it should be ~fib(28)/12 ≈ 180 ms, so green processes do not appear to be spreading across cores. `spawn` (20k processes each computing fib(15)) is ~1.3 s vs Elixir's 85 ms — but most of that is the per-core VM `fib(15)` cost, not the scheduler (a bare 20k-process spawn is ~0.5 s).

**Suggestions:**
- Confirm the work-stealing scheduler migrates processes to idle OS threads (check core utilisation during `pfib`); if processes are pinned to one thread, multi-threaded scheduling is the highest-leverage change.
- Lowering the per-core compute floor (areas 1 & 4 / JIT) lifts `pfib`/`spawn` indirectly, since each process runs the same VM.

### 4. Function call overhead — fib 230 ms (≈55× the JITs)

Recursive `fib(30)` is ~74× behind .NET: ~1.5 M non-tail calls, roughly 150 ns/call vs .NET's ~3 ns. The `SelfCall` optimisation handles tail recursion; the residual is non-tail calls through the full dispatch path. The new JIT tier-2 call lowering targets exactly this shape — measure whether it now fires on `fib` (the audit found two-call recursion previously bailed at the safepoint).

### 5. GC / allocation throughput — bintree 339 ms

Building and walking many short-lived tree nodes stresses allocation rate and GC pause (339 ms vs Node's 7 ms). A bump-pointer nursery for small, short-lived objects would cut per-node allocation cost; the inline `vector-ref` already shaved ~1.2× off the walk.

### 6. String operations — improved (strings 140 → 64 ms)

`join` now uses the native single-pass `%string-join`. The residual `strings` time is dominated by `map number->string` (~48% of compute), so a faster integer→string path is the next lever there.

### 7. Immutable map churn — improved (wordcount 209 → 162 ms)

`get`/`assoc` got fixed-arity arms (above), cutting the per-op wrapper cost. The residual ~160 ms is the CHAMP map rebuild itself — a fresh persistent map per `assoc` over 100k tallies. A transient build (`transient`/`assoc!`/`persistent!`, already in the kernel) would cut it further but changes the immutable idiom the benchmark deliberately uses.

---

## Summary table

Compute time (Brood); the "× vs fastest" multiple swings run-to-run because the fastest language's time is often sub-millisecond, so absolute ms is the stable measure.

| area | representative benchmark | Brood compute | status / likely cause |
|------|--------------------------|---------------|------------------------|
| tight loops | loop, collatz, matmul | 142 / 301 / 153 ms | open — per-op VM overhead; JIT subset gaps (Global, back-edge tiering) |
| array indexing | matmul | 153 ms | **addressed** — `nth`/`vector-ref` inlined; residual is per-op overhead |
| parallel scheduling | pfib, spawn | 2.3 s / 1.3 s | open — processes likely not spread across cores |
| function call | fib | 230 ms | open — non-tail dispatch cost; JIT tier-2 call lowering may help |
| GC / allocation | bintree | 339 ms | open — per-node allocation / GC pauses |
| string ops | strings | 64 ms | **addressed** — native `%string-join`; residual is `number->string` |
| higher-order fold | reduce | 21 ms | **addressed** — primitive-reducer fast path |
| immutable map churn | wordcount | 162 ms | **addressed** — fixed-arity `get`/`assoc`; residual is CHAMP rebuild |
