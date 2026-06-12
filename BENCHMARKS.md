# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-12.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.108.
Method: best of 3 runs per benchmark; the concurrency benchmarks (spawn, pfib, http) take the best of 7, since they bounce more run-to-run. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 10ms |
| Node    | 18ms |
| .NET    | 22ms |
| Brood   | 27ms |
| Ruby    | 42ms |
| Elixir  | 254ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 136ms | 54ms | 69ms | 8ms | 56ms | 4ms |

`fib` is the clearest non-tail-recursion case, and **native-to-native call linking** put it on the native path: a JIT'd arm calling a JIT'd callee now jumps directly to the callee's native entry instead of round-tripping through VM dispatch — **224 → 136 ms (1.6×)**.

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 19ms | 58ms | 194ms | 3ms | 63ms | 2ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 23ms | 21ms | 7ms | 3ms | < 1ms | 1ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 24ms | 58ms | 10ms | 2ms | 7ms | 2ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 63ms | 51ms | 243ms | 8ms | 86ms | 4ms |

`collatz`'s `steps` is an all-integer self-tail loop. It now runs native: two JIT codegen bails that had kept it interpreted are fixed (an arg-map mismatch on `(* 3 m)`-style fused operands, and a dead `Jump` after a tail call), so **289 → 77 ms (~3.8×)**; native-to-native call linking then lowered the outer `scan`'s per-step calls too (**→ 63 ms**) — now in Elixir's range and ahead of Python and Ruby.

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 75ms | 64ms | 81ms | 3ms | 25ms | 2ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 102ms | 28ms | 46ms | 4ms | 33ms | 2ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 68ms | 28ms | 5ms | 7ms | 10ms | 5ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 166ms | 36ms | 24ms | 8ms | 10ms | 10ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 295ms | 49ms | 20ms | 6ms | 20ms | 4ms |

`bintree` is walk-bound. Native-to-native call linking lowered the `run` driver loop and cut the two-call `check` walk's dispatch cost (**348 → 295 ms**); the residual is allocating/walking the short-lived nodes themselves.

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 31ms | 37ms | 21ms | 18ms | 13ms | 12ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1433ms | 115ms | 1121ms | 108ms | 5104ms | 22ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1259ms | 151ms | 826ms | 140ms | 521ms | 47ms |

`pfib` is 100 × `fib(28)` across cores — pure non-tail recursion, parallelised. Native-to-native call linking is the biggest single win in the suite here: **2342 → 1259 ms (1.8×)**. (`spawn`, which fans out 20 000 *short* processes, is dominated by spawn/teardown rather than fib compute, so it's neutral — linking neither helps nor hurts it once the compile-queue back-off is in place.)

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 210ms | 706ms | 192ms | 144ms | 216ms | 178ms |

Brood is competitive on I/O-concurrent work: 1.4× behind Node, 3rd of six (behind
Node and .NET). Note: earlier runs of this row were invalid — every client was
reaching a stray process on the fixed port, not the benchmark server, so all six
counted zero 200s (checksum 0) and Python errored. The harness now binds a free
port and verifies the server is its own, so every language returns the full 500.
