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
| Node    | 17ms |
| .NET    | 22ms |
| Brood   | 28ms |
| Ruby    | 42ms |
| Elixir  | 259ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 222ms | 42ms | 65ms | 7ms | 53ms | 4ms |

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 229ms | 36ms | 188ms | 3ms | 58ms | 1ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 94ms | 4ms | 7ms | 3ms | < 1ms | < 1ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 24ms | 32ms | 8ms | 2ms | 6ms | 1ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 273ms | 45ms | 240ms | 8ms | 88ms | 5ms |

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 74ms | 50ms | 76ms | 4ms | 26ms | 2ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 628ms | 13ms | 44ms | 3ms | 28ms | 2ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 137ms | 19ms | 6ms | 8ms | 8ms | 6ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 204ms | 39ms | 22ms | 7ms | 8ms | 9ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 383ms | 43ms | 20ms | 7ms | 19ms | 5ms |

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 32ms | 22ms | 19ms | 15ms | 7ms | 14ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 923ms | 83ms | 1111ms | 104ms | 4912ms | 23ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 2029ms | 133ms | 680ms | 118ms | 441ms | 37ms |

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 120ms | 602ms | n/a | 107ms | 200ms | 127ms |

Brood is competitive on I/O-concurrent work: 1.1× behind Node. (Python's
http run errored this round, so it has no figure.)
