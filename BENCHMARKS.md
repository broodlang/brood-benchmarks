# Brood Benchmarks

Machine: `whklat`, 12-core x86-64, Linux 7.0.0, 2026-06-10.
Runtimes: Brood 0.1.0 · Elixir 1.20.0 / OTP 28 · Python 3.14.4 · Node 22.21.0 · Ruby 3.3.8 · .NET 10.0.108.
Method: best of 3 runs per benchmark; the concurrency benchmarks (spawn, pfib, http) take the best of 7, since they bounce more run-to-run. Compute = wall − startup, so boot cost is not charged against compute-heavy benchmarks.

---

## Boot time

Cold start to first instruction. Lower is better.

| runtime | boot |
|---------|------|
| Python  | 11ms |
| Node    | 18ms |
| .NET    | 23ms |
| Brood   | 29ms |
| Ruby    | 44ms |
| Elixir  | 259ms |

Brood is the fourth-fastest boot, ahead of Ruby and well ahead of the BEAM.

---

## Compute times

Wall time minus boot cost. `< 1ms` means the benchmark finished in less time than the startup measurement — the work is sub-millisecond. All times in ms unless noted. Lower is better.

### fib(30) — naive recursion

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 228ms | 40ms | 69ms | 7ms | 52ms | 3ms |

### loop 3 M — raw iteration

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 147ms | 48ms | 192ms | 2ms | 59ms | < 1ms |

### reduce 1 M — higher-order fold

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 21ms | 5ms | 6ms | 3ms | < 1ms | < 1ms |

### primes 20 k — trial division

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 24ms | 43ms | 9ms | 1ms | 6ms | 1ms |

### collatz 30 k — tight integer loop

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 281ms | 58ms | 244ms | 8ms | 82ms | 3ms |

### mandelbrot 128×128 — floating point

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 74ms | 65ms | 73ms | 3ms | 25ms | 1ms |

### matmul 80×80 — nested loops + array indexing

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 152ms | 36ms | 47ms | 3ms | 29ms | < 1ms |

### strings 50 k — join + length

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 63ms | 21ms | 4ms | 6ms | 4ms | 4ms |

### wordcount 100 k — hash-map build

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 209ms | 30ms | 22ms | 6ms | 8ms | 9ms |

### bintree depth 40 — allocation + GC

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 336ms | 46ms | 20ms | 7ms | 19ms | 3ms |

### sort 50 k — sort + walk

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 36ms | 19ms | 17ms | 16ms | 6ms | 11ms |

### spawn 20 k — concurrent fan-out, each fib(15)

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 1336ms | 85ms | 1088ms | 106ms | 4936ms | 27ms |

Brood uses green processes + message passing. Python uses asyncio coroutines. Node uses Promises. Ruby uses OS threads. .NET uses thread-pool tasks.

### pfib 100 × fib(28) in parallel — CPU parallelism

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 2535ms | 121ms | 774ms | 127ms | 493ms | 40ms |

### http 500 concurrent GETs — I/O concurrency

| Brood | Elixir | Python | Node | Ruby | .NET |
|-------|--------|--------|------|------|------|
| 174ms | 714ms | 186ms | 124ms | 217ms | 152ms |

Brood is competitive on I/O-concurrent work: 1.4× behind Node, 3rd of six (behind
Node and .NET). Note: earlier runs of this row were invalid — every client was
reaching a stray process on the fixed port, not the benchmark server, so all six
counted zero 200s (checksum 0) and Python errored. The harness now binds a free
port and verifies the server is its own, so every language returns the full 500.
