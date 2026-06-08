# Brood performance — findings and improvement areas

Based on the whklat benchmark run (2026-06-08). Numbers are compute time (wall − boot).

---

## Where Brood is already good

**Boot time (30.9ms)** — fourth-fastest out of six. Faster than Ruby and far faster than the BEAM. Acceptable for a scripting/application runtime.

**I/O concurrency (http, 1.3× Node)** — Brood's green-process model handles concurrent I/O well. 500 in-flight HTTP requests completes in 162ms, essentially matching .NET (160ms) and close to Node (124ms). The actor-style network stack is working.

**Sort (29ms, 28× Node)** — Brood's sort is its best single-threaded result. Suggests the built-in sort algorithm and list representation are reasonably efficient.

**Memory** — Brood uses 12–20 MB for most compute-only benchmarks. The heap is compact; allocation volume is not yet the dominant problem.

---

## Priority improvement areas

### 1. Tight loop / per-instruction overhead — collatz 124×, loop 302×, matmul 615×

The three worst compute results all share the same root cause: the VM pays a fixed overhead per operation that compounds over many iterations. Collatz (484ms vs .NET's 4ms), plain loop (302ms vs .NET's sub-ms), and matmul (615ms vs .NET's sub-ms) are dominated by raw bytecode dispatch cost, not algorithmic complexity.

**Suggestions:**
- Profile the dispatch loop. Even reducing the per-instruction overhead by 30–40% would move all three benchmarks materially.
- Specialised integer arithmetic opcodes. If `+`, `-`, `<`, `>` on fixnums go through a slow generic path today, a tagged-integer fast path would help collatz and loop most.
- Loop / tail-call fusion. The Brood `loop` benchmark is tail recursion over a counter. If the compiler can recognise this pattern and emit a jump instead of a call, the overhead collapses.

### 2. Array indexing — matmul 615×

Matmul is the worst result. 80×80 matrix multiply is ~1 M index lookups and stores; if each index is a map/list lookup rather than a direct memory read, cost is O(n) per access.

**Suggestions:**
- Introduce a native dense-vector or array type with O(1) indexed read/write. Even a simple `(vector ...)` type backed by a Rust `Vec` would reduce matmul from 615× to something close to Python's 48×.
- This would also improve bintree (343×) and any future numeric workload.

### 3. Parallel scheduling — pfib 55×, spawn 48×

`pfib` (100 × fib(28) in parallel) takes 2.24s for Brood vs 40ms for .NET and 111ms for Elixir. The work is fully independent; on 12 cores this should take ~fib(28)/12 ≈ 180ms. The 2.24s result is close to the single-threaded sequential time, indicating Brood's scheduler is not distributing green processes across cores.

`spawn` (20k processes each computing fib(15)) is 1.056s vs Elixir's 60ms — a 17× gap on a workload where Elixir's BEAM is the target. Much of this is likely the same scheduler issue.

**Suggestions:**
- Verify that the work-stealing scheduler is actually migrating processes to idle OS threads. A simple diagnostic: run pfib and check CPU utilisation — if only 1 core is hot, the processes are running on a single thread.
- If processes are pinned to a single OS thread, enabling multi-threaded scheduling is the highest-leverage change available. This would likely bring pfib from 2.24s to ~200ms in one step.

### 4. Function call overhead — fib 92×, reduce 87×

Recursive fib(30) is 92× behind .NET. The call stack for fib(30) is ~1.5 M recursive calls; at 92× the per-call overhead is roughly 180ns vs .NET's ~2ns. This is inline with an unoptimised interpreter call frame.

`reduce` (fold over 1 M elements with a lambda) at 87× shows that higher-order calls compound this further.

**Suggestions:**
- Reduce call frame allocation cost. Reusing frames for non-escaping calls (common case) avoids heap pressure.
- Inline small known functions at the call site (basic inlining). fib's two arms are tiny — inlining the recursive call once would cut the call count in half.
- These improvements also benefit collatz and loop.

### 5. GC / allocation throughput — bintree 343×

Building and walking `2^40` binary tree nodes stresses allocation rate and GC pause. Brood's 343ms vs Elixir's sub-ms (Elixir is mostly below measurement noise here) and Node's 5ms suggests either allocation is slow or GC pauses are large.

**Suggestions:**
- Check whether tree nodes are heap-allocated one-by-one through the generic allocator. A bump-pointer nursery for small, short-lived objects would reduce allocation cost substantially.
- If GC is stop-the-world and pausing for >50ms, switching to incremental collection would smooth the bintree result.

### 6. String operations — strings 128×

128× behind .NET and 37× behind Python on a join + length of 50k strings. Immutable string concatenation in a loop is quadratic unless the runtime detects it; if Brood's `join` is implemented as repeated append this is the dominant cost.

**Suggestions:**
- Ensure `join` on a list of strings uses a single pre-sized buffer, not incremental concatenation.
- If string values are heap-allocated individually on each operation, interning short strings or using a rope representation would reduce allocation.

---

## Summary table

| area | representative benchmark | current vs fastest | likely cause | estimated impact of fix |
|------|--------------------------|--------------------|--------------|------------------------|
| tight loops | collatz, loop, matmul | 124–615× | per-instruction VM overhead | very high |
| array indexing | matmul | 615× | no O(1) array type | high |
| parallel scheduling | pfib, spawn | 48–55× | processes not distributed across cores | high |
| function call | fib, reduce | 87–92× | call frame cost | medium |
| GC / allocation | bintree | 343× | allocation rate or GC pause | medium |
| string ops | strings | 128× | non-linear join | medium |
