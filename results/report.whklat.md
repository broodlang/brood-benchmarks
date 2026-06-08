# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 22:38.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.6ms | 2.6× | 4/6 | 27.6ms | — | 12.4 MB | 2/6 | 0 |
| elixir | 273.1ms | 25.3× | 6/6 | 273.1ms | — | 76.2 MB | 6/6 | 0 |
| python | 10.8ms | 1.0× | 1/6 | 10.8ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.9ms | 1.7× | 2/6 | 17.9ms | — | 42.8 MB | 5/6 | 0 |
| ruby | 48.2ms | 4.5× | 5/6 | 48.2ms | — | 23.6 MB | 3/6 | 0 |
| dotnet | 22.4ms | 2.1× | 3/6 | 22.4ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 245.3ms | 47.2× | 6/6 | 272.9ms | 27.6ms | 12.4 MB | 2/6 | 832040 |
| elixir | 83.8ms | 16.1× | 5/6 | 356.9ms | 273.1ms | 80.9 MB | 6/6 | 832040 |
| python | 79.5ms | 15.3× | 4/6 | 90.3ms | 10.8ms | 9.7 MB | 1/6 | 832040 |
| node | 12.8ms | 2.5× | 2/6 | 30.7ms | 17.9ms | 48.0 MB | 5/6 | 832040 |
| ruby | 65.7ms | 12.6× | 3/6 | 113.9ms | 48.2ms | 23.6 MB | 3/6 | 832040 |
| dotnet | 5.2ms | 1.0× | 1/6 | 27.6ms | 22.4ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.4ms | 78.3× | 5/6 | 192.0ms | 27.6ms | 12.4 MB | 2/6 | 3000000 |
| elixir | 120.3ms | 57.3× | 4/6 | 393.4ms | 273.1ms | 81.0 MB | 6/6 | 3000000 |
| python | 263.5ms | 125.5× | 6/6 | 274.3ms | 10.8ms | 9.8 MB | 1/6 | 3000000 |
| node | 5.9ms | 2.8× | 2/6 | 23.8ms | 17.9ms | 47.8 MB | 5/6 | 3000000 |
| ruby | 61.6ms | 29.3× | 3/6 | 109.8ms | 48.2ms | 23.6 MB | 3/6 | 3000000 |
| dotnet | 2.1ms | 1.0× | 1/6 | 24.5ms | 22.4ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.2ms | 112.2× | 6/6 | 139.8ms | 27.6ms | 12.5 MB | 2/6 | 499999500000 |
| elixir | 7.3ms | 7.3× | 5/6 | 280.4ms | 273.1ms | 77.2 MB | 6/6 | 499999500000 |
| python | 7.0ms | 7.0× | 4/6 | 17.8ms | 10.8ms | 9.8 MB | 1/6 | 499999500000 |
| node | 5.5ms | 5.5× | 3/6 | 23.4ms | 17.9ms | 49.7 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 47.8ms | 48.2ms | 23.6 MB | 3/6 | 499999500000 |
| dotnet | 1.0ms | 1.0× | 2/6 | 23.4ms | 22.4ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.4ms | 4.2× | 5/6 | 56.0ms | 27.6ms | 12.6 MB | 2/6 | 2262 |
| elixir | 58.2ms | 8.7× | 6/6 | 331.3ms | 273.1ms | 80.9 MB | 6/6 | 2262 |
| python | 12.3ms | 1.8× | 3/6 | 23.1ms | 10.8ms | 9.9 MB | 1/6 | 2262 |
| node | 7.1ms | 1.1× | 2/6 | 25.0ms | 17.9ms | 48.4 MB | 5/6 | 2262 |
| ruby | 17.3ms | 2.6× | 4/6 | 65.5ms | 48.2ms | 23.6 MB | 3/6 | 2262 |
| dotnet | 6.7ms | 1.0× | 1/6 | 29.1ms | 22.4ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 300.2ms | 21.4× | 5/6 | 327.8ms | 27.6ms | 21.4 MB | 2/6 | 307 |
| elixir | 60.8ms | 4.3× | 3/6 | 333.9ms | 273.1ms | 82.2 MB | 6/6 | 307 |
| python | 340.8ms | 24.3× | 6/6 | 351.6ms | 10.8ms | 9.8 MB | 1/6 | 307 |
| node | 16.1ms | 1.2× | 2/6 | 34.0ms | 17.9ms | 48.0 MB | 5/6 | 307 |
| ruby | 123.0ms | 8.8× | 4/6 | 171.2ms | 48.2ms | 23.6 MB | 3/6 | 307 |
| dotnet | 14.0ms | 1.0× | 1/6 | 36.4ms | 22.4ms | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.7ms | 56.2× | 5/6 | 134.3ms | 27.6ms | 12.5 MB | 2/6 | 345426 |
| elixir | 153.8ms | 80.9× | 6/6 | 426.9ms | 273.1ms | 81.9 MB | 6/6 | 345426 |
| python | 91.8ms | 48.3× | 4/6 | 102.6ms | 10.8ms | 10.1 MB | 1/6 | 345426 |
| node | 4.9ms | 2.6× | 2/6 | 22.8ms | 17.9ms | 50.1 MB | 5/6 | 345426 |
| ruby | 23.3ms | 12.3× | 3/6 | 71.5ms | 48.2ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.9ms | 1.0× | 1/6 | 24.3ms | 22.4ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 718.2ms | 422.5× | 6/6 | 745.8ms | 27.6ms | 23.9 MB | 3/6 | 229499993 |
| elixir | 19.3ms | 11.4× | 3/6 | 292.4ms | 273.1ms | 80.1 MB | 6/6 | 229499993 |
| python | 53.1ms | 31.2× | 5/6 | 63.9ms | 10.8ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.4ms | 2.0× | 2/6 | 21.3ms | 17.9ms | 48.6 MB | 5/6 | 229499993 |
| ruby | 28.6ms | 16.8× | 4/6 | 76.8ms | 48.2ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 1.7ms | 1.0× | 1/6 | 24.1ms | 22.4ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 156.0ms | 37.1× | 6/6 | 183.6ms | 27.6ms | 42.3 MB | 4/6 | 288889 |
| elixir | 20.5ms | 4.9× | 5/6 | 293.6ms | 273.1ms | 88.0 MB | 6/6 | 288889 |
| python | 4.2ms | 1.0× | 1/6 | 15.0ms | 10.8ms | 12.8 MB | 1/6 | 288889 |
| node | 6.8ms | 1.6× | 3/6 | 24.7ms | 17.9ms | 52.0 MB | 5/6 | 288889 |
| ruby | 5.7ms | 1.4× | 2/6 | 53.9ms | 48.2ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 6.8ms | 1.6× | 4/6 | 29.2ms | 22.4ms | 30.1 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 227.8ms | 34.0× | 6/6 | 255.4ms | 27.6ms | 27.8 MB | 4/6 | 50038280 |
| elixir | 48.3ms | 7.2× | 5/6 | 321.4ms | 273.1ms | 79.4 MB | 6/6 | 50038280 |
| python | 24.2ms | 3.6× | 4/6 | 35.0ms | 10.8ms | 9.9 MB | 1/6 | 50038280 |
| node | 8.4ms | 1.3× | 2/6 | 26.3ms | 17.9ms | 49.9 MB | 5/6 | 50038280 |
| ruby | 6.7ms | 1.0× | 1/6 | 54.9ms | 48.2ms | 23.6 MB | 2/6 | 50038280 |
| dotnet | 10.6ms | 1.6× | 3/6 | 33.0ms | 22.4ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 422.4ms | 26.2× | 6/6 | 450.0ms | 27.6ms | 16.7 MB | 2/6 | 327640 |
| elixir | 117.9ms | 7.3× | 5/6 | 391.0ms | 273.1ms | 81.2 MB | 6/6 | 327640 |
| python | 28.6ms | 1.8× | 3/6 | 39.4ms | 10.8ms | 10.0 MB | 1/6 | 327640 |
| node | 16.6ms | 1.0× | 2/6 | 34.5ms | 17.9ms | 51.9 MB | 5/6 | 327640 |
| ruby | 44.4ms | 2.8× | 4/6 | 92.6ms | 48.2ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 16.1ms | 1.0× | 1/6 | 38.5ms | 22.4ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 58.1ms | 3.1× | 5/6 | 85.7ms | 27.6ms | 19.5 MB | 2/6 | 102632633 |
| elixir | 128.5ms | 6.8× | 6/6 | 401.6ms | 273.1ms | 86.1 MB | 6/6 | 102632633 |
| python | 28.8ms | 1.5× | 4/6 | 39.6ms | 10.8ms | 12.2 MB | 1/6 | 102632633 |
| node | 28.3ms | 1.5× | 3/6 | 46.2ms | 17.9ms | 51.1 MB | 5/6 | 102632633 |
| ruby | 18.9ms | 1.0× | 1/6 | 67.1ms | 48.2ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 22.4ms | 1.2× | 2/6 | 44.8ms | 22.4ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.285s | 42.3× | 5/6 | 1.312s | 27.6ms | 168.5 MB | 5/6 | 12200000 |
| elixir | 199.6ms | 6.6× | 3/6 | 472.7ms | 273.1ms | 90.3 MB | 4/6 | 12200000 |
| python | 1.182s | 38.9× | 4/6 | 1.193s | 10.8ms | 35.8 MB | 2/6 | 12200000 |
| node | 117.6ms | 3.9× | 2/6 | 135.5ms | 17.9ms | 55.2 MB | 3/6 | 12200000 |
| ruby | 5.552s | 182.6× | 6/6 | 5.600s | 48.2ms | 246.6 MB | 6/6 | 12200000 |
| dotnet | 30.4ms | 1.0× | 1/6 | 52.8ms | 22.4ms | 32.3 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.451s | 36.9× | 6/6 | 2.478s | 27.6ms | 12.6 MB | 1/6 | 31781100 |
| elixir | 186.7ms | 2.8× | 3/6 | 459.8ms | 273.1ms | 85.1 MB | 5/6 | 31781100 |
| python | 972.9ms | 14.6× | 5/6 | 983.7ms | 10.8ms | 22.2 MB | 2/6 | 31781100 |
| node | 171.3ms | 2.6× | 2/6 | 189.2ms | 17.9ms | 181.1 MB | 6/6 | 31781100 |
| ruby | 651.6ms | 9.8× | 4/6 | 699.8ms | 48.2ms | 23.6 MB | 3/6 | 31781100 |
| dotnet | 66.5ms | 1.0× | 1/6 | 88.9ms | 22.4ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 227.9ms | 1.6× | 4/6 | 255.5ms | 27.6ms | 91.2 MB | 5/6 | 500 |
| elixir | 798.9ms | 5.7× | 6/6 | 1.072s | 273.1ms | 501.8 MB | 6/6 | 500 |
| python | 201.3ms | 1.4× | 3/6 | 212.1ms | 10.8ms | 44.9 MB | 1/6 | 500 |
| node | 141.0ms | 1.0× | 1/6 | 158.9ms | 17.9ms | 64.5 MB | 4/6 | 500 |
| ruby | 231.9ms | 1.6× | 5/6 | 280.1ms | 48.2ms | 49.9 MB | 3/6 | 500 |
| dotnet | 187.1ms | 1.3× | 2/6 | 209.5ms | 22.4ms | 48.4 MB | 2/6 | 500 |
