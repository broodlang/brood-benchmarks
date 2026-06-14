# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-14.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.109.
Method: best of 5 runs per benchmark (startup best of 15); the concurrency benchmarks (spawn, pfib, http) take the best of 7, since they bounce more run-to-run. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

> ⚠️ **These numbers are stale — re-run before trusting them.** The workload
> sizes were raised substantially so the work dominates startup noise (e.g. `fib`
> 30→37, `loop` 3M→60M, `wordcount` 100k→1.5M), `reduce` was changed to a real
> higher-order fold (it had been a closed-form/loop in some languages), and two
> benchmarks were added (`nqueens`, `pipeline`). Regenerate with
> `python3 bench/harness.py --label whklat` on the reference machine, then refresh
> the tables below.

> Brood numbers reflect main at `b9e2173`. The wins from `32bbda7` (transient GC
> fix + map combinators), `67c2ec2` (parallel-allocation intern cache + sharded
> counter), `84d3315` (type-of keyword cache) and `b99756d` (JIT'd 2-element vector
> literals → bintree's `make` native) are now in the rows: a low-load re-run
> refreshed the six benchmarks that moved — **bintree 282→247, strings 64→61,
> sort 32→30, collatz 63→61, spawn 1281→1134, http 183→160 ms**. The remaining
> rows are unchanged (a load-independent `perf stat -e instructions` A/B vs the
> prior build shows them flat); they're carried over rather than re-measured
> because the run machine's load spiked intermittently and inflated the shorter
> float/interpreted benchmarks (mandelbrot/fib/primes) on a full re-run, while
> instruction counts confirm those are unmoved. `read-string` (`b9e2173`) is a
> correctness fix (errors on trailing content instead of silently dropping it),
> not a perf change.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 9ms  |
| Node    | 18ms |
| .NET    | 21ms |
| Brood   | 28ms |
| Ruby    | 40ms |
| Elixir  | 251ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 66ms | 56ms | 66ms | 7ms | 59ms | 5ms |

`fib` is the clearest non-tail-recursion case. **Native-to-native call linking** put it on the native path (a JIT'd arm calling a JIT'd callee jumps directly to the callee's native entry instead of round-tripping through VM dispatch), then a **call-site inline cache + in-place frame setup + call-head elision** cut the per-call dispatch cost that remained: **224 → 136 → 66 ms (3.4× over the arc)**. Brood now matches Elixir and Python on naive recursion.

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 18ms | 53ms | 192ms | 4ms | 64ms | 2ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 20ms | 18ms | 7ms | 3ms | 1ms | 2ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 23ms | 49ms | 10ms | 2ms | 11ms | 2ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 61ms | 65ms | 262ms | 8ms | 86ms | 5ms |

`collatz`'s `steps` is an all-integer self-tail loop. It now runs native: two JIT codegen bails that had kept it interpreted are fixed (an arg-map mismatch on `(* 3 m)`-style fused operands, and a dead `Jump` after a tail call), so **289 → 77 ms (~3.8×)**; native-to-native call linking then lowered the outer `scan`'s per-step calls too (**→ 63 ms**) — now in Elixir's range and ahead of Python and Ruby.

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 75ms | 60ms | 81ms | 3ms | 32ms | 3ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 104ms | 28ms | 45ms | 4ms | 32ms | 3ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 61ms | 28ms | 6ms | 7ms | 10ms | 6ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 163ms | 40ms | 24ms | 7ms | 12ms | 10ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 247ms | 57ms | 23ms | 7ms | 23ms | 6ms |

`bintree` builds and walks many 2-node trees. Call linking + call-head elision lowered the `run`/`check` dispatch (**348 → 295 → 282 ms**); the `type-of` keyword cache cut the per-node `nil?`/`pair?` checks, and the JIT now emits `make`'s `[a b]` node literal natively (the first heap-allocating vector literal it lowers) — together **282 → 247 ms**. The remaining cost is the interpreted `check` walk (linking it measures neutral) and the short-lived node allocation.

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 30ms | 29ms | 19ms | 17ms | 12ms | 13ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1134ms | 83ms | 1101ms | 109ms | 5095ms | 22ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks. (Spawning 20 k processes interns heavily; the thread-local intern cache in `67c2ec2` cut this ~9 % — and lifted the near-serial ceiling on allocation-heavy parallel work generally, ~6× → ~2× on an 8-process map-build microbench.)

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 460ms | 133ms | 754ms | 129ms | 480ms | 42ms |

`pfib` is 100 × `fib(28)` across cores — pure non-tail recursion, parallelised. This is the biggest cumulative win in the suite: native-to-native call linking, then the call-site inline cache + in-place frame setup + call-head elision, took it **2342 → 1259 → 460 ms (~5×)** — Brood now finishes ahead of Ruby and holds the lightest memory in the field (~17 MB). (`spawn`, which fans out 20 000 *short* processes, is dominated by spawn/teardown rather than fib compute; the call-head-elision and then the thread-local intern cache moved it 1433 → 1281 → 1134 ms.)

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 160ms | 736ms | 188ms | 128ms | 225ms | 158ms |

Brood is competitive on I/O-concurrent work: ~1.2× behind Node, 3rd of six (just
behind .NET). Note: earlier runs of this row were invalid — every client was
reaching a stray process on the fixed port, not the benchmark server, so all six
counted zero 200s (checksum 0) and Python errored. The harness now binds a free
port and verifies the server is its own, so every language returns the full 500.
