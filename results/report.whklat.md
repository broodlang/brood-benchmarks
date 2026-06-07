# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-07 18:56.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). `compute` ≈ wall − that language's own `startup` (so a slow-booting runtime's real compute speed is visible — e.g. the BEAM). RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 36.6ms | — | 2.5× | 3/6 | 12.0 MB | 2/6 | 0 |
| elixir | 387.7ms | — | 26.6× | 6/6 | 78.1 MB | 6/6 | 0 |
| python | 14.6ms | — | 1.0× | 1/6 | 9.8 MB | 1/6 | 0 |
| node | 24.5ms | — | 1.7× | 2/6 | 44.7 MB | 5/6 | 0 |
| ruby | 70.1ms | — | 4.8× | 5/6 | 23.5 MB | 3/6 | 0 |
| dotnet | 36.6ms | — | 2.5× | 4/6 | 25.6 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 444.6ms | 408.0ms | 13.3× | 5/6 | 11.9 MB | 2/6 | 832040 |
| elixir | 464.7ms | 77.0ms | 13.9× | 6/6 | 84.1 MB | 6/6 | 832040 |
| python | 120.0ms | 105.4ms | 3.6× | 3/6 | 9.8 MB | 1/6 | 832040 |
| node | 33.4ms | 8.9ms | 1.0× | 1/6 | 50.4 MB | 5/6 | 832040 |
| ruby | 132.7ms | 62.6ms | 4.0× | 4/6 | 23.5 MB | 3/6 | 832040 |
| dotnet | 34.8ms | 0.0ms | 1.0× | 2/6 | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 564.4ms | 527.8ms | 25.5× | 6/6 | 11.8 MB | 2/6 | 3000000 |
| elixir | 411.8ms | 24.1ms | 18.6× | 5/6 | 80.4 MB | 6/6 | 3000000 |
| python | 226.9ms | 212.3ms | 10.3× | 4/6 | 9.7 MB | 1/6 | 3000000 |
| node | 22.1ms | 0.0ms | 1.0× | 1/6 | 50.1 MB | 5/6 | 3000000 |
| ruby | 134.8ms | 64.7ms | 6.1× | 3/6 | 23.6 MB | 3/6 | 3000000 |
| dotnet | 25.6ms | 0.0ms | 1.2× | 2/6 | 26.2 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 137.6ms | 101.0ms | 5.8× | 5/6 | 11.8 MB | 2/6 | 499999500000 |
| elixir | 319.7ms | 0.0ms | 13.5× | 6/6 | 77.4 MB | 6/6 | 499999500000 |
| python | 23.7ms | 9.1ms | 1.0× | 1/6 | 9.8 MB | 1/6 | 499999500000 |
| node | 28.1ms | 3.6ms | 1.2× | 3/6 | 52.2 MB | 5/6 | 499999500000 |
| ruby | 50.2ms | 0.0ms | 2.1× | 4/6 | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 27.6ms | 0.0ms | 1.2× | 2/6 | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 83.3ms | 46.7ms | 4.0× | 5/6 | 11.9 MB | 2/6 | 2262 |
| elixir | 336.6ms | 0.0ms | 16.1× | 6/6 | 82.2 MB | 6/6 | 2262 |
| python | 20.9ms | 6.3ms | 1.0× | 1/6 | 9.9 MB | 1/6 | 2262 |
| node | 24.6ms | 0.1ms | 1.2× | 2/6 | 50.8 MB | 5/6 | 2262 |
| ruby | 65.0ms | 0.0ms | 3.1× | 4/6 | 23.5 MB | 3/6 | 2262 |
| dotnet | 27.6ms | 0.0ms | 1.3× | 3/6 | 26.0 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 691.8ms | 655.2ms | 24.4× | 6/6 | 19.7 MB | 2/6 | 307 |
| elixir | 336.8ms | 0.0ms | 11.9× | 5/6 | 81.6 MB | 6/6 | 307 |
| python | 298.0ms | 283.4ms | 10.5× | 4/6 | 9.8 MB | 1/6 | 307 |
| node | 36.5ms | 12.0ms | 1.3× | 2/6 | 50.3 MB | 5/6 | 307 |
| ruby | 139.1ms | 69.0ms | 4.9× | 3/6 | 23.5 MB | 3/6 | 307 |
| dotnet | 28.3ms | 0.0ms | 1.0× | 1/6 | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 158.5ms | 121.9ms | 5.3× | 5/6 | 12.0 MB | 2/6 | 345426 |
| elixir | 324.9ms | 0.0ms | 10.9× | 6/6 | 85.3 MB | 6/6 | 345426 |
| python | 109.7ms | 95.1ms | 3.7× | 4/6 | 10.1 MB | 1/6 | 345426 |
| node | 30.1ms | 5.6ms | 1.0× | 2/6 | 52.2 MB | 5/6 | 345426 |
| ruby | 95.5ms | 25.4ms | 3.2× | 3/6 | 23.7 MB | 3/6 | 345426 |
| dotnet | 29.7ms | 0.0ms | 1.0× | 1/6 | 26.0 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 899.2ms | 862.6ms | 42.0× | 6/6 | 20.2 MB | 2/6 | 229499993 |
| elixir | 286.7ms | 0.0ms | 13.4× | 5/6 | 78.0 MB | 6/6 | 229499993 |
| python | 58.8ms | 44.2ms | 2.7× | 3/6 | 9.9 MB | 1/6 | 229499993 |
| node | 21.4ms | 0.0ms | 1.0× | 1/6 | 50.5 MB | 5/6 | 229499993 |
| ruby | 80.8ms | 10.7ms | 3.8× | 4/6 | 23.7 MB | 3/6 | 229499993 |
| dotnet | 27.8ms | 0.0ms | 1.3× | 2/6 | 26.1 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 236.7ms | 200.1ms | 15.5× | 5/6 | 36.1 MB | 4/6 | 288889 |
| elixir | 346.1ms | 0.0ms | 22.6× | 6/6 | 87.0 MB | 6/6 | 288889 |
| python | 15.3ms | 0.7ms | 1.0× | 1/6 | 12.9 MB | 1/6 | 288889 |
| node | 25.3ms | 0.8ms | 1.7× | 2/6 | 54.4 MB | 5/6 | 288889 |
| ruby | 62.7ms | 0.0ms | 4.1× | 4/6 | 25.8 MB | 2/6 | 288889 |
| dotnet | 29.8ms | 0.0ms | 1.9× | 3/6 | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 274.2ms | 237.6ms | 10.8× | 5/6 | 28.1 MB | 4/6 | 50038280 |
| elixir | 328.7ms | 0.0ms | 12.9× | 6/6 | 80.3 MB | 6/6 | 50038280 |
| python | 35.4ms | 20.8ms | 1.4× | 3/6 | 9.8 MB | 1/6 | 50038280 |
| node | 25.5ms | 1.0ms | 1.0× | 1/6 | 52.3 MB | 5/6 | 50038280 |
| ruby | 63.7ms | 0.0ms | 2.5× | 4/6 | 23.5 MB | 2/6 | 50038280 |
| dotnet | 35.2ms | 0.0ms | 1.4× | 2/6 | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 545.7ms | 509.1ms | 18.6× | 6/6 | 15.8 MB | 2/6 | 327640 |
| elixir | 397.6ms | 9.9ms | 13.5× | 5/6 | 82.0 MB | 6/6 | 327640 |
| python | 37.1ms | 22.5ms | 1.3× | 3/6 | 10.0 MB | 1/6 | 327640 |
| node | 29.4ms | 4.9ms | 1.0× | 1/6 | 54.2 MB | 5/6 | 327640 |
| ruby | 80.1ms | 10.0ms | 2.7× | 4/6 | 23.8 MB | 3/6 | 327640 |
| dotnet | 33.4ms | 0.0ms | 1.1× | 2/6 | 30.6 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 79.3ms | 42.7ms | 2.0× | 5/6 | 16.5 MB | 2/6 | 102632633 |
| elixir | 344.2ms | 0.0ms | 8.5× | 6/6 | 87.2 MB | 6/6 | 102632633 |
| python | 41.6ms | 27.0ms | 1.0× | 2/6 | 12.2 MB | 1/6 | 102632633 |
| node | 49.7ms | 25.2ms | 1.2× | 3/6 | 53.3 MB | 5/6 | 102632633 |
| ruby | 65.3ms | 0.0ms | 1.6× | 4/6 | 24.1 MB | 3/6 | 102632633 |
| dotnet | 40.6ms | 4.0ms | 1.0× | 1/6 | 27.0 MB | 4/6 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 338.8ms | 302.2ms | 1.1× | 2/2 | 35.9 MB | 1/2 | 199990000 |
| elixir | 309.0ms | 0.0ms | 1.0× | 1/2 | 86.4 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 3.066s | 3.030s | 39.1× | 6/6 | 22.0 MB | 1/6 | 31781100 |
| elixir | 428.1ms | 40.4ms | 5.5× | 3/6 | 82.6 MB | 5/6 | 31781100 |
| python | 895.0ms | 880.4ms | 11.4× | 5/6 | 22.3 MB | 2/6 | 31781100 |
| node | 178.9ms | 154.4ms | 2.3× | 2/6 | 184.7 MB | 6/6 | 31781100 |
| ruby | 658.5ms | 588.4ms | 8.4× | 4/6 | 23.7 MB | 3/6 | 31781100 |
| dotnet | 78.5ms | 41.9ms | 1.0× | 1/6 | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 208.9ms | 172.3ms | 1.4× | 2/6 | 78.3 MB | 5/6 | 500 |
| elixir | 1.121s | 732.8ms | 7.5× | 6/6 | 560.4 MB | 6/6 | 500 |
| python | 217.2ms | 202.6ms | 1.5× | 3/6 | 44.3 MB | 1/6 | 500 |
| node | 148.7ms | 124.2ms | 1.0× | 1/6 | 67.5 MB | 4/6 | 500 |
| ruby | 304.3ms | 234.2ms | 2.0× | 5/6 | 49.8 MB | 3/6 | 500 |
| dotnet | 235.4ms | 198.8ms | 1.6× | 4/6 | 48.1 MB | 2/6 | 500 |
