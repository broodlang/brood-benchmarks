# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-09.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.108.
Method: best of 3 runs per benchmark. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 10ms |
| Node    | 18ms |
| .NET    | 22ms |
| Brood   | 28ms |
| Ruby    | 44ms |
| Elixir  | 259ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 226ms | 54ms | 66ms | 7ms | 68ms | 3ms |

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 155ms | 43ms | 195ms | 2ms | 61ms | 1ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 95ms | 8ms | 6ms | 2ms | < 1ms | < 1ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 24ms | 49ms | 8ms | < 1ms | 7ms | 2ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 270ms | 65ms | 261ms | 7ms | 83ms | 4ms |

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 73ms | 63ms | 75ms | 3ms | 21ms | 1ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 670ms | 15ms | 50ms | 2ms | 29ms | 2ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 141ms | 17ms | 4ms | 6ms | 4ms | 5ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 212ms | 35ms | 25ms | 7ms | 6ms | 10ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 402ms | 49ms | 19ms | 6ms | 20ms | 4ms |

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 32ms | 22ms | 20ms | 16ms | 7ms | 12ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1359ms | 97ms | 1365ms | 106ms | 4846ms | 20ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 2254ms | 127ms | 758ms | 130ms | 488ms | 39ms |

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 148ms | 628ms | n/a | 112ms | 197ms | 101ms |

Brood is competitive on I/O-concurrent work: 1.3× behind Node. (Python's
http run errored this round, so it has no figure.)
