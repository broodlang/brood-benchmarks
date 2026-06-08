# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-08). Numbers are compute time (wall − boot).

---

## Where Brood is already good

**Boot time (28ms)** — fourth-fastest out of six. Faster than Ruby and well ahead of the BEAM. Acceptable for a scripting/application runtime.

**I/O concurrency (http, 1.3× Node)** — Brood's green-process model handles concurrent I/O well. 500 in-flight HTTP requests completes in 172ms (wall), close to .NET (129ms) and Node (128ms). The actor-style network stack is working.

**Sort (60ms wall, ~2× Node)** — Brood's sort stays within ~2× of most runtimes. Suggests the built-in sort algorithm and list representation are reasonably efficient.

**Memory** — Brood uses 12–20 MB for most compute-only benchmarks. The heap is compact; allocation volume is not yet the dominant problem.

---

## Priority improvement areas

### 1. Tight loop / per-instruction overhead — collatz 30×, loop 126×, matmul 280×

The three worst compute results all share the same root cause: the VM pays a fixed overhead per operation that compounds over many iterations.

Integer arithmetic was improved in an earlier session (ADR: `Prim2SlotSlot`/`Prim2SlotInt` fusion + `prim2_int_fast` inline fast path), bringing loop from ~199ms to ~176ms and collatz from ~327ms to ~299ms.

`defn` tail self-calls now emit `Inst::SelfCall` (the same inline frame-reset path previously only used for `letrec` closures). This eliminates the IC probe, RefCell borrow, and Arc clone paid on every tail-recursive iteration when calling a named function. Measured improvement: loop 176ms → 164ms, collatz ~8% faster.

**Remaining suggestions:**
- Further reduce root-stack overhead. The dominant remaining cost is that every intermediate value must be heap-rooted via `Vec` array ops; BEAM uses register-based addressing.
- Loop / tail-call fusion. If the compiler can recognise a counter loop pattern and emit a native integer loop, the overhead collapses.

### 2. Array indexing — matmul 280×

Matmul is the worst result. 80×80 matrix multiply is ~1 M index lookups and stores; if each index is a map/list lookup rather than a direct memory read, cost is O(n) per access.

**Suggestions:**
- Introduce a native dense-vector or array type with O(1) indexed read/write. Even a simple `(vector ...)` type backed by a Rust `Vec` would reduce matmul dramatically.
- This would also improve bintree (139×) and any future numeric workload.

### 3. Parallel scheduling — pfib 55×, spawn 55×

`pfib` (100 × fib(28) in parallel) takes 2.27s for Brood vs 42ms for .NET. The work is fully independent; on 12 cores this should take ~fib(28)/12 ≈ 180ms. The result suggests Brood's scheduler is not distributing green processes across cores.

`spawn` (20k processes each computing fib(15)) is 1.11s vs Elixir's 80ms.

**Suggestions:**
- Verify that the work-stealing scheduler is actually migrating processes to idle OS threads. A simple diagnostic: run pfib and check CPU utilisation — if only 1 core is hot, the processes are running on a single thread.
- If processes are pinned to a single OS thread, enabling multi-threaded scheduling is the highest-leverage change available.

### 4. Function call overhead — fib 76×, reduce 102×

Recursive fib(30) is 76× behind .NET. The call stack for fib(30) is ~1.5 M recursive calls; the per-call overhead is roughly 150ns vs .NET's ~2ns.

`reduce` (fold over 1 M elements with a lambda) at 102× shows that higher-order calls compound this further.

**Suggestions:**
- Reduce call frame allocation cost. Reusing frames for non-escaping calls (common case) avoids heap pressure.
- The `defn` self-call optimisation (SelfCall) handles the tail-recursive case; the remaining fib overhead is in non-tail calls that still go through the full dispatch path.

### 5. GC / allocation throughput — bintree 139×

Building and walking `2^40` binary tree nodes stresses allocation rate and GC pause. Brood's 417ms vs Node's 7ms suggests either allocation is slow or GC pauses are large.

**Suggestions:**
- Check whether tree nodes are heap-allocated one-by-one through the generic allocator. A bump-pointer nursery for small, short-lived objects would reduce allocation cost substantially.

### 6. String operations — strings 31×

31× behind .NET on a join + length of 50k strings.

**Suggestions:**
- Ensure `join` on a list of strings uses a single pre-sized buffer, not incremental concatenation.

---

## Summary table

| area | representative benchmark | current vs fastest | likely cause | estimated impact of fix |
|------|--------------------------|--------------------|--------------|------------------------|
| tight loops | collatz, loop, matmul | 30–280× | per-instruction VM overhead | very high |
| array indexing | matmul | 280× | no O(1) array type | high |
| parallel scheduling | pfib, spawn | 55× | processes not distributed across cores | high |
| function call | fib, reduce | 76–102× | call frame cost | medium |
| GC / allocation | bintree | 139× | allocation rate or GC pause | medium |
| string ops | strings | 31× | non-linear join | medium |
