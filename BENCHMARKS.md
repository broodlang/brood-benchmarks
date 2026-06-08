# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-08.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.108.
Method: best of 3 runs per benchmark. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 11ms |
| Node    | 18ms |
| .NET    | 22ms |
| Brood   | 28ms |
| Ruby    | 48ms |
| Elixir  | 273ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 245ms | 84ms | 80ms | 13ms | 66ms | 5ms |

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 164ms | 120ms | 264ms | 6ms | 62ms | 2ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 112ms | 7ms | 7ms | 6ms | < 1ms | 1ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 28ms | 58ms | 12ms | 7ms | 17ms | 7ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 300ms | 61ms | 341ms | 16ms | 123ms | 14ms |

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 107ms | 154ms | 92ms | 5ms | 23ms | 2ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 718ms | 19ms | 53ms | 3ms | 29ms | 2ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 156ms | 21ms | 4ms | 7ms | 6ms | 7ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 228ms | 48ms | 24ms | 8ms | 7ms | 11ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 422ms | 118ms | 29ms | 17ms | 44ms | 16ms |

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 58ms | 129ms | 29ms | 28ms | 19ms | 22ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1285ms | 200ms | 1182ms | 118ms | 5552ms | 30ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 2451ms | 187ms | 973ms | 171ms | 652ms | 67ms |

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 228ms | 799ms | 201ms | 141ms | 232ms | 187ms |

Brood is competitive on I/O-concurrent work: 1.6× behind Node.
