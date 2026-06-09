# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-09 08:23.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.5ms | 2.9× | 4/6 | 27.5ms | — | 14.2 MB | 2/6 | 0 |
| elixir | 259.2ms | 27.3× | 6/6 | 259.2ms | — | 79.7 MB | 6/6 | 0 |
| python | 9.5ms | 1.0× | 1/6 | 9.5ms | — | 9.7 MB | 1/6 | 0 |
| node | 17.1ms | 1.8× | 2/6 | 17.1ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 41.6ms | 4.4× | 5/6 | 41.6ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.5ms | 2.3× | 3/6 | 21.5ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 221.5ms | 54.0× | 6/6 | 249.0ms | 27.5ms | 14.4 MB | 2/6 | 832040 |
| elixir | 41.9ms | 10.2× | 3/6 | 301.1ms | 259.2ms | 80.9 MB | 6/6 | 832040 |
| python | 64.9ms | 15.8× | 5/6 | 74.4ms | 9.5ms | 9.7 MB | 1/6 | 832040 |
| node | 7.4ms | 1.8× | 2/6 | 24.5ms | 17.1ms | 48.5 MB | 5/6 | 832040 |
| ruby | 53.5ms | 13.0× | 4/6 | 95.1ms | 41.6ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.1ms | 1.0× | 1/6 | 25.6ms | 21.5ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 229.1ms | 163.6× | 6/6 | 256.6ms | 27.5ms | 14.3 MB | 2/6 | 3000000 |
| elixir | 35.9ms | 25.6× | 3/6 | 295.1ms | 259.2ms | 80.4 MB | 6/6 | 3000000 |
| python | 187.9ms | 134.2× | 5/6 | 197.4ms | 9.5ms | 9.8 MB | 1/6 | 3000000 |
| node | 2.7ms | 1.9× | 2/6 | 19.8ms | 17.1ms | 48.3 MB | 5/6 | 3000000 |
| ruby | 58.4ms | 41.7× | 4/6 | 100.0ms | 41.6ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.4ms | 1.0× | 1/6 | 22.9ms | 21.5ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.5ms | 94.5× | 6/6 | 122.0ms | 27.5ms | 14.3 MB | 2/6 | 499999500000 |
| elixir | 4.1ms | 4.1× | 4/6 | 263.3ms | 259.2ms | 77.3 MB | 6/6 | 499999500000 |
| python | 6.6ms | 6.6× | 5/6 | 16.1ms | 9.5ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.2ms | 3.2× | 3/6 | 20.3ms | 17.1ms | 50.2 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 39.8ms | 41.6ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 0.9ms | < 1× | 2/6 | 22.4ms | 21.5ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.0ms | 18.5× | 5/6 | 51.5ms | 27.5ms | 14.3 MB | 2/6 | 2262 |
| elixir | 31.5ms | 24.2× | 6/6 | 290.7ms | 259.2ms | 80.9 MB | 6/6 | 2262 |
| python | 8.5ms | 6.5× | 4/6 | 18.0ms | 9.5ms | 9.9 MB | 1/6 | 2262 |
| node | 1.6ms | 1.2× | 2/6 | 18.7ms | 17.1ms | 48.8 MB | 5/6 | 2262 |
| ruby | 6.4ms | 4.9× | 3/6 | 48.0ms | 41.6ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.3ms | 1.0× | 1/6 | 22.8ms | 21.5ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 272.9ms | 55.7× | 6/6 | 300.4ms | 27.5ms | 26.6 MB | 4/6 | 307 |
| elixir | 45.2ms | 9.2× | 3/6 | 304.4ms | 259.2ms | 82.4 MB | 6/6 | 307 |
| python | 239.8ms | 48.9× | 5/6 | 249.3ms | 9.5ms | 9.8 MB | 1/6 | 307 |
| node | 7.5ms | 1.5× | 2/6 | 24.6ms | 17.1ms | 48.5 MB | 5/6 | 307 |
| ruby | 88.1ms | 18.0× | 4/6 | 129.7ms | 41.6ms | 23.4 MB | 2/6 | 307 |
| dotnet | 4.9ms | 1.0× | 1/6 | 26.4ms | 21.5ms | 26.1 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.5ms | 38.7× | 5/6 | 101.0ms | 27.5ms | 14.2 MB | 2/6 | 345426 |
| elixir | 50.2ms | 26.4× | 4/6 | 309.4ms | 259.2ms | 81.3 MB | 6/6 | 345426 |
| python | 76.4ms | 40.2× | 6/6 | 85.9ms | 9.5ms | 10.1 MB | 1/6 | 345426 |
| node | 4.3ms | 2.3× | 2/6 | 21.4ms | 17.1ms | 50.2 MB | 5/6 | 345426 |
| ruby | 26.0ms | 13.7× | 3/6 | 67.6ms | 41.6ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.9ms | 1.0× | 1/6 | 23.4ms | 21.5ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 628.0ms | 314.0× | 6/6 | 655.5ms | 27.5ms | 25.3 MB | 3/6 | 229499993 |
| elixir | 13.1ms | 6.6× | 3/6 | 272.3ms | 259.2ms | 78.3 MB | 6/6 | 229499993 |
| python | 43.7ms | 21.9× | 5/6 | 53.2ms | 9.5ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.1ms | 1.5× | 2/6 | 20.2ms | 17.1ms | 48.7 MB | 5/6 | 229499993 |
| ruby | 27.8ms | 13.9× | 4/6 | 69.4ms | 41.6ms | 23.5 MB | 2/6 | 229499993 |
| dotnet | 2.0ms | 1.0× | 1/6 | 23.5ms | 21.5ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.4ms | 23.7× | 6/6 | 164.9ms | 27.5ms | 45.2 MB | 4/6 | 288889 |
| elixir | 19.3ms | 3.3× | 5/6 | 278.5ms | 259.2ms | 86.1 MB | 6/6 | 288889 |
| python | 5.8ms | 1.0× | 1/6 | 15.3ms | 9.5ms | 12.8 MB | 1/6 | 288889 |
| node | 7.7ms | 1.3× | 4/6 | 24.8ms | 17.1ms | 52.5 MB | 5/6 | 288889 |
| ruby | 7.6ms | 1.3× | 3/6 | 49.2ms | 41.6ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.8ms | 1.0× | 2/6 | 27.3ms | 21.5ms | 30.1 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 204.0ms | 27.6× | 6/6 | 231.5ms | 27.5ms | 35.9 MB | 4/6 | 50038280 |
| elixir | 38.8ms | 5.2× | 5/6 | 298.0ms | 259.2ms | 78.1 MB | 6/6 | 50038280 |
| python | 22.3ms | 3.0× | 4/6 | 31.8ms | 9.5ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.4ms | 1.0× | 1/6 | 24.5ms | 17.1ms | 50.4 MB | 5/6 | 50038280 |
| ruby | 8.0ms | 1.1× | 2/6 | 49.6ms | 41.6ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 9.3ms | 1.3× | 3/6 | 30.8ms | 21.5ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 382.7ms | 81.4× | 6/6 | 410.2ms | 27.5ms | 20.2 MB | 2/6 | 327640 |
| elixir | 42.6ms | 9.1× | 5/6 | 301.8ms | 259.2ms | 83.1 MB | 6/6 | 327640 |
| python | 19.8ms | 4.2× | 4/6 | 29.3ms | 9.5ms | 10.0 MB | 1/6 | 327640 |
| node | 7.0ms | 1.5× | 2/6 | 24.1ms | 17.1ms | 52.2 MB | 5/6 | 327640 |
| ruby | 19.4ms | 4.1× | 3/6 | 61.0ms | 41.6ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.7ms | 1.0× | 1/6 | 26.2ms | 21.5ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.4ms | 4.4× | 6/6 | 59.9ms | 27.5ms | 21.4 MB | 2/6 | 102632633 |
| elixir | 21.6ms | 2.9× | 5/6 | 280.8ms | 259.2ms | 85.9 MB | 6/6 | 102632633 |
| python | 19.1ms | 2.6× | 4/6 | 28.6ms | 9.5ms | 12.1 MB | 1/6 | 102632633 |
| node | 15.1ms | 2.0× | 3/6 | 32.2ms | 17.1ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 7.4ms | 1.0× | 1/6 | 49.0ms | 41.6ms | 24.1 MB | 3/6 | 102632633 |
| dotnet | 14.5ms | 2.0× | 2/6 | 36.0ms | 21.5ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 923.1ms | 39.8× | 4/6 | 950.6ms | 27.5ms | 170.6 MB | 5/6 | 12200000 |
| elixir | 82.9ms | 3.6× | 2/6 | 342.1ms | 259.2ms | 89.9 MB | 4/6 | 12200000 |
| python | 1.111s | 47.9× | 5/6 | 1.121s | 9.5ms | 35.9 MB | 2/6 | 12200000 |
| node | 103.8ms | 4.5× | 3/6 | 120.9ms | 17.1ms | 55.7 MB | 3/6 | 12200000 |
| ruby | 4.912s | 211.7× | 6/6 | 4.953s | 41.6ms | 246.8 MB | 6/6 | 12200000 |
| dotnet | 23.2ms | 1.0× | 1/6 | 44.7ms | 21.5ms | 31.9 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.029s | 55.3× | 6/6 | 2.057s | 27.5ms | 14.2 MB | 1/6 | 31781100 |
| elixir | 133.4ms | 3.6× | 3/6 | 392.6ms | 259.2ms | 81.4 MB | 5/6 | 31781100 |
| python | 680.4ms | 18.5× | 5/6 | 689.9ms | 9.5ms | 22.1 MB | 2/6 | 31781100 |
| node | 117.8ms | 3.2× | 2/6 | 134.9ms | 17.1ms | 181.6 MB | 6/6 | 31781100 |
| ruby | 440.6ms | 12.0× | 4/6 | 482.2ms | 41.6ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 36.7ms | 1.0× | 1/6 | 58.2ms | 21.5ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 120.3ms | 1.1× | 2/5 | 147.8ms | 27.5ms | 75.2 MB | 4/5 | 0 |
| elixir | 601.8ms | 5.6× | 5/5 | 861.0ms | 259.2ms | 527.6 MB | 5/5 | 0 |
| python | — | — | — | — | — | — | — | ERROR |
| node | 107.3ms | 1.0× | 1/5 | 124.4ms | 17.1ms | 64.3 MB | 3/5 | 0 |
| ruby | 200.2ms | 1.9× | 4/5 | 241.8ms | 41.6ms | 50.9 MB | 2/5 | 0 |
| dotnet | 127.3ms | 1.2× | 3/5 | 148.8ms | 21.5ms | 48.0 MB | 1/5 | 0 |
