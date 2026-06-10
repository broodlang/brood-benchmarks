# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-10.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.108.
Method: best of 3 runs per benchmark; the concurrency benchmarks (spawn, pfib, http) take the best of 7, since they bounce more run-to-run. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 10ms |
| Node    | 17ms |
| .NET    | 21ms |
| Brood   | 28ms |
| Ruby    | 42ms |
| Elixir  | 263ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 225ms | 47ms | 70ms | 8ms | 54ms | 4ms |

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 133ms | 40ms | 196ms | 3ms | 60ms | 2ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 98ms | 2ms | 7ms | 3ms | 2ms | 2ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 23ms | 40ms | 10ms | 2ms | 7ms | 2ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 268ms | 51ms | 238ms | 8ms | 83ms | 5ms |

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 72ms | 55ms | 77ms | 4ms | 23ms | 3ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 661ms | 17ms | 45ms | 3ms | 28ms | 2ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 140ms | 11ms | 4ms | 6ms | 7ms | 6ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 211ms | 22ms | 24ms | 7ms | 9ms | 11ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 401ms | 33ms | 20ms | 7ms | 21ms | 5ms |

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 32ms | 15ms | 20ms | 18ms | 8ms | 14ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1322ms | 78ms | 1075ms | 105ms | 4890ms | 21ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 2202ms | 119ms | 749ms | 128ms | 487ms | 40ms |

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 180ms | 682ms | 185ms | 123ms | 210ms | 154ms |

Brood is competitive on I/O-concurrent work: 1.5× behind Node, 3rd of six (behind
Node and .NET). Note: earlier runs of this row were invalid — every client was
reaching a stray process on the fixed port, not the benchmark server, so all six
counted zero 200s (checksum 0) and Python errored. The harness now binds a free
port and verifies the server is its own, so every language returns the full 500.
