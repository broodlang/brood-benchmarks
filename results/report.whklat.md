# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-11 14:25.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.7ms | 2.8× | 4/6 | 26.7ms | — | 14.5 MB | 2/6 | 0 |
| elixir | 254.0ms | 26.7× | 6/6 | 254.0ms | — | 79.0 MB | 6/6 | 0 |
| python | 9.5ms | 1.0× | 1/6 | 9.5ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.2ms | 1.9× | 2/6 | 18.2ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 41.1ms | 4.3× | 5/6 | 41.1ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.4ms | 2.3× | 3/6 | 21.4ms | — | 25.8 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 225.2ms | 46.9× | 6/6 | 251.9ms | 26.7ms | 14.4 MB | 2/6 | 832040 |
| elixir | 53.6ms | 11.2× | 3/6 | 307.6ms | 254.0ms | 82.8 MB | 6/6 | 832040 |
| python | 69.6ms | 14.5× | 5/6 | 79.1ms | 9.5ms | 9.8 MB | 1/6 | 832040 |
| node | 7.7ms | 1.6× | 2/6 | 25.9ms | 18.2ms | 48.5 MB | 5/6 | 832040 |
| ruby | 55.5ms | 11.6× | 4/6 | 96.6ms | 41.1ms | 23.6 MB | 3/6 | 832040 |
| dotnet | 4.8ms | 1.0× | 1/6 | 26.2ms | 21.4ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.4ms | 17.6× | 3/6 | 53.1ms | 26.7ms | 15.2 MB | 2/6 | 3000000 |
| elixir | 42.6ms | 28.4× | 4/6 | 296.6ms | 254.0ms | 81.3 MB | 6/6 | 3000000 |
| python | 193.4ms | 128.9× | 6/6 | 202.9ms | 9.5ms | 9.8 MB | 1/6 | 3000000 |
| node | 2.7ms | 1.8× | 2/6 | 20.9ms | 18.2ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 61.8ms | 41.2× | 5/6 | 102.9ms | 41.1ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.5ms | 1.0× | 1/6 | 22.9ms | 21.4ms | 26.2 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.7ms | 23.7× | 6/6 | 50.4ms | 26.7ms | 14.5 MB | 2/6 | 499999500000 |
| elixir | 15.3ms | 15.3× | 5/6 | 269.3ms | 254.0ms | 77.4 MB | 6/6 | 499999500000 |
| python | 7.0ms | 7.0× | 4/6 | 16.5ms | 9.5ms | 9.8 MB | 1/6 | 499999500000 |
| node | 2.3ms | 2.3× | 3/6 | 20.5ms | 18.2ms | 50.3 MB | 5/6 | 499999500000 |
| ruby | 0.3ms | < 1× | 1/6 | 41.4ms | 41.1ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.0ms | 1.0× | 2/6 | 22.4ms | 21.4ms | 26.2 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.8ms | 19.1× | 5/6 | 51.5ms | 26.7ms | 14.5 MB | 2/6 | 2262 |
| elixir | 53.3ms | 41.0× | 6/6 | 307.3ms | 254.0ms | 80.9 MB | 6/6 | 2262 |
| python | 10.0ms | 7.7× | 4/6 | 19.5ms | 9.5ms | 9.9 MB | 1/6 | 2262 |
| node | 1.3ms | 1.0× | 1/6 | 19.5ms | 18.2ms | 49.0 MB | 5/6 | 2262 |
| ruby | 9.0ms | 6.9× | 3/6 | 50.1ms | 41.1ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.7ms | 1.3× | 2/6 | 23.1ms | 21.4ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 287.9ms | 53.3× | 6/6 | 314.6ms | 26.7ms | 26.9 MB | 4/6 | 307 |
| elixir | 56.9ms | 10.5× | 3/6 | 310.9ms | 254.0ms | 83.0 MB | 6/6 | 307 |
| python | 246.4ms | 45.6× | 5/6 | 255.9ms | 9.5ms | 9.8 MB | 1/6 | 307 |
| node | 7.4ms | 1.4× | 2/6 | 25.6ms | 18.2ms | 48.6 MB | 5/6 | 307 |
| ruby | 84.2ms | 15.6× | 4/6 | 125.3ms | 41.1ms | 23.5 MB | 2/6 | 307 |
| dotnet | 5.4ms | 1.0× | 1/6 | 26.8ms | 21.4ms | 26.2 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.8ms | 29.5× | 5/6 | 100.5ms | 26.7ms | 14.5 MB | 2/6 | 345426 |
| elixir | 67.4ms | 27.0× | 4/6 | 321.4ms | 254.0ms | 82.8 MB | 6/6 | 345426 |
| python | 77.6ms | 31.0× | 6/6 | 87.1ms | 9.5ms | 10.1 MB | 1/6 | 345426 |
| node | 3.0ms | 1.2× | 2/6 | 21.2ms | 18.2ms | 50.7 MB | 5/6 | 345426 |
| ruby | 26.5ms | 10.6× | 3/6 | 67.6ms | 41.1ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 2.5ms | 1.0× | 1/6 | 23.9ms | 21.4ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.6ms | 53.8× | 6/6 | 134.3ms | 26.7ms | 28.5 MB | 4/6 | 229499993 |
| elixir | 21.6ms | 10.8× | 3/6 | 275.6ms | 254.0ms | 78.6 MB | 6/6 | 229499993 |
| python | 43.2ms | 21.6× | 5/6 | 52.7ms | 9.5ms | 9.9 MB | 1/6 | 229499993 |
| node | 2.7ms | 1.3× | 2/6 | 20.9ms | 18.2ms | 49.1 MB | 5/6 | 229499993 |
| ruby | 26.7ms | 13.3× | 4/6 | 67.8ms | 41.1ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 2.0ms | 1.0× | 1/6 | 23.4ms | 21.4ms | 26.3 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 63.8ms | 12.8× | 6/6 | 90.5ms | 26.7ms | 30.0 MB | 3/6 | 288889 |
| elixir | 22.5ms | 4.5× | 5/6 | 276.5ms | 254.0ms | 87.3 MB | 6/6 | 288889 |
| python | 5.7ms | 1.1× | 3/6 | 15.2ms | 9.5ms | 12.8 MB | 1/6 | 288889 |
| node | 5.6ms | 1.1× | 2/6 | 23.8ms | 18.2ms | 52.5 MB | 5/6 | 288889 |
| ruby | 8.6ms | 1.7× | 4/6 | 49.7ms | 41.1ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.0ms | 1.0× | 1/6 | 26.4ms | 21.4ms | 30.1 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 161.3ms | 24.1× | 6/6 | 188.0ms | 26.7ms | 53.8 MB | 5/6 | 50038280 |
| elixir | 44.1ms | 6.6× | 5/6 | 298.1ms | 254.0ms | 77.9 MB | 6/6 | 50038280 |
| python | 22.5ms | 3.4× | 4/6 | 32.0ms | 9.5ms | 9.9 MB | 1/6 | 50038280 |
| node | 6.7ms | 1.0× | 1/6 | 24.9ms | 18.2ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 9.6ms | 1.4× | 3/6 | 50.7ms | 41.1ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 9.3ms | 1.4× | 2/6 | 30.7ms | 21.4ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 391.1ms | 85.0× | 6/6 | 417.8ms | 26.7ms | 22.5 MB | 2/6 | 327640 |
| elixir | 54.7ms | 11.9× | 5/6 | 308.7ms | 254.0ms | 80.8 MB | 6/6 | 327640 |
| python | 21.1ms | 4.6× | 4/6 | 30.6ms | 9.5ms | 10.0 MB | 1/6 | 327640 |
| node | 6.8ms | 1.5× | 2/6 | 25.0ms | 18.2ms | 52.4 MB | 5/6 | 327640 |
| ruby | 20.0ms | 4.3× | 3/6 | 61.1ms | 41.1ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.6ms | 1.0× | 1/6 | 26.0ms | 21.4ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.7ms | 3.7× | 5/6 | 58.4ms | 26.7ms | 25.1 MB | 3/6 | 102632633 |
| elixir | 33.9ms | 4.0× | 6/6 | 287.9ms | 254.0ms | 87.2 MB | 6/6 | 102632633 |
| python | 19.8ms | 2.3× | 4/6 | 29.3ms | 9.5ms | 12.2 MB | 1/6 | 102632633 |
| node | 15.1ms | 1.8× | 2/6 | 33.3ms | 18.2ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 8.5ms | 1.0× | 1/6 | 49.6ms | 41.1ms | 24.1 MB | 2/6 | 102632633 |
| dotnet | 15.2ms | 1.8× | 3/6 | 36.6ms | 21.4ms | 27.0 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.394s | 66.4× | 5/6 | 1.421s | 26.7ms | 183.1 MB | 5/6 | 12200000 |
| elixir | 90.6ms | 4.3× | 2/6 | 344.6ms | 254.0ms | 88.8 MB | 4/6 | 12200000 |
| python | 1.100s | 52.4× | 4/6 | 1.109s | 9.5ms | 35.9 MB | 2/6 | 12200000 |
| node | 105.2ms | 5.0× | 3/6 | 123.4ms | 18.2ms | 55.6 MB | 3/6 | 12200000 |
| ruby | 4.907s | 233.7× | 6/6 | 4.948s | 41.1ms | 246.5 MB | 6/6 | 12200000 |
| dotnet | 21.0ms | 1.0× | 1/6 | 42.4ms | 21.4ms | 32.2 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.182s | 55.1× | 6/6 | 2.209s | 26.7ms | 14.5 MB | 1/6 | 31781100 |
| elixir | 138.3ms | 3.5× | 3/6 | 392.3ms | 254.0ms | 81.6 MB | 5/6 | 31781100 |
| python | 763.7ms | 19.3× | 5/6 | 773.2ms | 9.5ms | 22.2 MB | 2/6 | 31781100 |
| node | 133.7ms | 3.4× | 2/6 | 151.9ms | 18.2ms | 181.6 MB | 6/6 | 31781100 |
| ruby | 490.3ms | 12.4× | 4/6 | 531.4ms | 41.1ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 39.6ms | 1.0× | 1/6 | 61.0ms | 21.4ms | 27.8 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 181.7ms | 1.4× | 4/6 | 208.4ms | 26.7ms | 102.6 MB | 5/6 | 500 |
| elixir | 734.1ms | 5.8× | 6/6 | 988.1ms | 254.0ms | 576.5 MB | 6/6 | 500 |
| python | 178.3ms | 1.4× | 3/6 | 187.8ms | 9.5ms | 48.2 MB | 1/6 | 500 |
| node | 126.6ms | 1.0× | 1/6 | 144.8ms | 18.2ms | 65.4 MB | 4/6 | 500 |
| ruby | 223.1ms | 1.8× | 5/6 | 264.2ms | 41.1ms | 50.1 MB | 3/6 | 500 |
| dotnet | 153.9ms | 1.2× | 2/6 | 175.3ms | 21.4ms | 48.4 MB | 2/6 | 500 |
