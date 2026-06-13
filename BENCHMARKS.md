# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-13.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.109.
Method: best of 5 runs per benchmark (startup best of 15); the concurrency benchmarks (spawn, pfib, http) take the best of 7, since they bounce more run-to-run. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

> These tables were measured on the brood build at commit `939aba3`. Two fixes have
> since landed (`32bbda7` transient GC-correctness + map combinators; `67c2ec2`
> parallel-allocation: thread-local intern cache + sharded alloc counter). An
> old-vs-new A/B (same machine; load-independent `perf stat -e instructions` + best-of-N
> wall) confirms these numbers hold within noise on the new build — `spawn` improved
> ~9 %, and a +2–4 % instruction-count bump on `loop`/`collatz` from the call-path
> refactor is below the rounding here. A fresh clean-load full run is pending.

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
| 63ms | 65ms | 262ms | 8ms | 86ms | 5ms |

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
| 64ms | 28ms | 6ms | 7ms | 10ms | 6ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 163ms | 40ms | 24ms | 7ms | 12ms | 10ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 282ms | 57ms | 23ms | 7ms | 23ms | 6ms |

`bintree` is walk-bound. Native-to-native call linking lowered the `run` driver loop and cut the two-call `check` walk's dispatch cost, and call-head elision trimmed it again (**348 → 295 → 282 ms**); the residual is allocating/walking the short-lived nodes themselves.

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 32ms | 29ms | 19ms | 17ms | 12ms | 13ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1281ms | 83ms | 1101ms | 109ms | 5095ms | 22ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks. (Spawning 20 k processes interns heavily; the thread-local intern cache in `67c2ec2` cut this ~9 % — and lifted the near-serial ceiling on allocation-heavy parallel work generally, ~6× → ~2× on an 8-process map-build microbench.)

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 460ms | 133ms | 754ms | 129ms | 480ms | 42ms |

`pfib` is 100 × `fib(28)` across cores — pure non-tail recursion, parallelised. This is the biggest cumulative win in the suite: native-to-native call linking, then the call-site inline cache + in-place frame setup + call-head elision, took it **2342 → 1259 → 460 ms (~5×)** — Brood now finishes ahead of Ruby and holds the lightest memory in the field (~17 MB). (`spawn`, which fans out 20 000 *short* processes, is dominated by spawn/teardown rather than fib compute, so it sees only the call-head-elision slice — 1433 → 1281 ms.)

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 183ms | 736ms | 188ms | 128ms | 225ms | 158ms |

Brood is competitive on I/O-concurrent work: 1.4× behind Node, 3rd of six (behind
Node and .NET). Note: earlier runs of this row were invalid — every client was
reaching a stray process on the fixed port, not the benchmark server, so all six
counted zero 200s (checksum 0) and Python errored. The harness now binds a free
port and verifies the server is its own, so every language returns the full 500.
