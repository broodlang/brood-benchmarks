# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-11 16:17.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.1ms | 2.8× | 4/6 | 27.1ms | — | 14.5 MB | 2/6 | 0 |
| elixir | 254.4ms | 26.2× | 6/6 | 254.4ms | — | 78.5 MB | 6/6 | 0 |
| python | 9.7ms | 1.0× | 1/6 | 9.7ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.7ms | 1.8× | 2/6 | 17.7ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 41.9ms | 4.3× | 5/6 | 41.9ms | — | 23.6 MB | 3/6 | 0 |
| dotnet | 22.0ms | 2.3× | 3/6 | 22.0ms | — | 25.8 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 223.7ms | 54.6× | 6/6 | 250.8ms | 27.1ms | 14.4 MB | 2/6 | 832040 |
| elixir | 56.7ms | 13.8× | 4/6 | 311.1ms | 254.4ms | 80.8 MB | 6/6 | 832040 |
| python | 67.9ms | 16.6× | 5/6 | 77.6ms | 9.7ms | 9.8 MB | 1/6 | 832040 |
| node | 8.6ms | 2.1× | 2/6 | 26.3ms | 17.7ms | 48.5 MB | 5/6 | 832040 |
| ruby | 54.7ms | 13.3× | 3/6 | 96.6ms | 41.9ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.1ms | 1.0× | 1/6 | 26.1ms | 22.0ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.2ms | 13.4× | 3/6 | 51.3ms | 27.1ms | 15.4 MB | 2/6 | 3000000 |
| elixir | 56.7ms | 31.5× | 4/6 | 311.1ms | 254.4ms | 82.4 MB | 6/6 | 3000000 |
| python | 197.0ms | 109.4× | 6/6 | 206.7ms | 9.7ms | 9.8 MB | 1/6 | 3000000 |
| node | 3.3ms | 1.8× | 2/6 | 21.0ms | 17.7ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 60.9ms | 33.8× | 5/6 | 102.8ms | 41.9ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.8ms | 1.0× | 1/6 | 23.8ms | 22.0ms | 26.2 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.3ms | 23.3× | 6/6 | 50.4ms | 27.1ms | 14.4 MB | 2/6 | 499999500000 |
| elixir | 21.2ms | 21.2× | 5/6 | 275.6ms | 254.4ms | 79.1 MB | 6/6 | 499999500000 |
| python | 6.8ms | 6.8× | 4/6 | 16.5ms | 9.7ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.0ms | 3.0× | 3/6 | 20.7ms | 17.7ms | 50.3 MB | 5/6 | 499999500000 |
| ruby | 0.4ms | < 1× | 1/6 | 42.3ms | 41.9ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.4ms | 1.4× | 2/6 | 23.4ms | 22.0ms | 26.2 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.9ms | 12.6× | 5/6 | 51.0ms | 27.1ms | 14.4 MB | 2/6 | 2262 |
| elixir | 57.8ms | 30.4× | 6/6 | 312.2ms | 254.4ms | 80.9 MB | 6/6 | 2262 |
| python | 9.7ms | 5.1× | 4/6 | 19.4ms | 9.7ms | 9.9 MB | 1/6 | 2262 |
| node | 1.9ms | 1.0× | 1/6 | 19.6ms | 17.7ms | 49.0 MB | 5/6 | 2262 |
| ruby | 7.4ms | 3.9× | 3/6 | 49.3ms | 41.9ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 2.1ms | 1.1× | 2/6 | 24.1ms | 22.0ms | 26.2 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 288.7ms | 50.6× | 6/6 | 315.8ms | 27.1ms | 26.8 MB | 4/6 | 307 |
| elixir | 67.5ms | 11.8× | 3/6 | 321.9ms | 254.4ms | 81.2 MB | 6/6 | 307 |
| python | 254.5ms | 44.6× | 5/6 | 264.2ms | 9.7ms | 9.8 MB | 1/6 | 307 |
| node | 8.5ms | 1.5× | 2/6 | 26.2ms | 17.7ms | 48.5 MB | 5/6 | 307 |
| ruby | 92.1ms | 16.2× | 4/6 | 134.0ms | 41.9ms | 23.5 MB | 2/6 | 307 |
| dotnet | 5.7ms | 1.0× | 1/6 | 27.7ms | 22.0ms | 26.2 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.0ms | 35.7× | 5/6 | 102.1ms | 27.1ms | 14.4 MB | 2/6 | 345426 |
| elixir | 64.1ms | 30.5× | 4/6 | 318.5ms | 254.4ms | 82.0 MB | 6/6 | 345426 |
| python | 81.0ms | 38.6× | 6/6 | 90.7ms | 9.7ms | 10.1 MB | 1/6 | 345426 |
| node | 3.4ms | 1.6× | 2/6 | 21.1ms | 17.7ms | 50.6 MB | 5/6 | 345426 |
| ruby | 24.7ms | 11.8× | 3/6 | 66.6ms | 41.9ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 2.1ms | 1.0× | 1/6 | 24.1ms | 22.0ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 114.3ms | 87.9× | 6/6 | 141.4ms | 27.1ms | 28.5 MB | 4/6 | 229499993 |
| elixir | 32.5ms | 25.0× | 4/6 | 286.9ms | 254.4ms | 78.1 MB | 6/6 | 229499993 |
| python | 43.4ms | 33.4× | 5/6 | 53.1ms | 9.7ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.6ms | 2.8× | 2/6 | 21.3ms | 17.7ms | 48.8 MB | 5/6 | 229499993 |
| ruby | 30.7ms | 23.6× | 3/6 | 72.6ms | 41.9ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 1.3ms | 1.0× | 1/6 | 23.3ms | 22.0ms | 26.3 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 68.5ms | 14.0× | 6/6 | 95.6ms | 27.1ms | 30.0 MB | 3/6 | 288889 |
| elixir | 28.2ms | 5.8× | 5/6 | 282.6ms | 254.4ms | 86.3 MB | 6/6 | 288889 |
| python | 5.1ms | 1.0× | 2/6 | 14.8ms | 9.7ms | 12.8 MB | 1/6 | 288889 |
| node | 6.6ms | 1.3× | 3/6 | 24.3ms | 17.7ms | 52.5 MB | 5/6 | 288889 |
| ruby | 10.2ms | 2.1× | 4/6 | 52.1ms | 41.9ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 4.9ms | 1.0× | 1/6 | 26.9ms | 22.0ms | 30.1 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 165.8ms | 20.0× | 6/6 | 192.9ms | 27.1ms | 53.8 MB | 5/6 | 50038280 |
| elixir | 36.5ms | 4.4× | 5/6 | 290.9ms | 254.4ms | 78.0 MB | 6/6 | 50038280 |
| python | 24.0ms | 2.9× | 4/6 | 33.7ms | 9.7ms | 9.9 MB | 1/6 | 50038280 |
| node | 8.3ms | 1.0× | 1/6 | 26.0ms | 17.7ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 10.0ms | 1.2× | 2/6 | 51.9ms | 41.9ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.2ms | 1.2× | 3/6 | 32.2ms | 22.0ms | 27.3 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 348.1ms | 79.1× | 6/6 | 375.2ms | 27.1ms | 22.3 MB | 2/6 | 327640 |
| elixir | 60.2ms | 13.7× | 5/6 | 314.6ms | 254.4ms | 81.4 MB | 6/6 | 327640 |
| python | 21.4ms | 4.9× | 4/6 | 31.1ms | 9.7ms | 10.0 MB | 1/6 | 327640 |
| node | 7.2ms | 1.6× | 2/6 | 24.9ms | 17.7ms | 52.3 MB | 5/6 | 327640 |
| ruby | 20.8ms | 4.7× | 3/6 | 62.7ms | 41.9ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.4ms | 1.0× | 1/6 | 26.4ms | 22.0ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.8ms | 2.5× | 5/6 | 57.9ms | 27.1ms | 25.1 MB | 3/6 | 102632633 |
| elixir | 37.0ms | 3.0× | 6/6 | 291.4ms | 254.4ms | 88.8 MB | 6/6 | 102632633 |
| python | 20.6ms | 1.7× | 4/6 | 30.3ms | 9.7ms | 12.2 MB | 1/6 | 102632633 |
| node | 18.1ms | 1.5× | 3/6 | 35.8ms | 17.7ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 13.3ms | 1.1× | 2/6 | 55.2ms | 41.9ms | 24.1 MB | 2/6 | 102632633 |
| dotnet | 12.4ms | 1.0× | 1/6 | 34.4ms | 22.0ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.447s | 61.1× | 5/6 | 1.474s | 27.1ms | 184.4 MB | 5/6 | 12200000 |
| elixir | 112.1ms | 4.7× | 3/6 | 366.5ms | 254.4ms | 89.6 MB | 4/6 | 12200000 |
| python | 1.129s | 47.6× | 4/6 | 1.138s | 9.7ms | 36.0 MB | 2/6 | 12200000 |
| node | 110.7ms | 4.7× | 2/6 | 128.4ms | 17.7ms | 55.9 MB | 3/6 | 12200000 |
| ruby | 5.052s | 213.2× | 6/6 | 5.094s | 41.9ms | 246.2 MB | 6/6 | 12200000 |
| dotnet | 23.7ms | 1.0× | 1/6 | 45.7ms | 22.0ms | 31.9 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.342s | 55.1× | 6/6 | 2.369s | 27.1ms | 14.7 MB | 1/6 | 31781100 |
| elixir | 143.0ms | 3.4× | 3/6 | 397.4ms | 254.4ms | 83.4 MB | 5/6 | 31781100 |
| python | 783.9ms | 18.4× | 5/6 | 793.6ms | 9.7ms | 22.3 MB | 2/6 | 31781100 |
| node | 141.3ms | 3.3× | 2/6 | 159.0ms | 17.7ms | 182.4 MB | 6/6 | 31781100 |
| ruby | 517.5ms | 12.2× | 4/6 | 559.4ms | 41.9ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 42.5ms | 1.0× | 1/6 | 64.5ms | 22.0ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.8ms | 1.4× | 4/6 | 220.9ms | 27.1ms | 102.2 MB | 5/6 | 500 |
| elixir | 702.6ms | 5.0× | 6/6 | 957.0ms | 254.4ms | 537.9 MB | 6/6 | 500 |
| python | 187.6ms | 1.3× | 3/6 | 197.3ms | 9.7ms | 46.5 MB | 1/6 | 500 |
| node | 140.4ms | 1.0× | 1/6 | 158.1ms | 17.7ms | 65.6 MB | 4/6 | 500 |
| ruby | 222.7ms | 1.6× | 5/6 | 264.6ms | 41.9ms | 50.2 MB | 3/6 | 500 |
| dotnet | 162.5ms | 1.2× | 2/6 | 184.5ms | 22.0ms | 48.6 MB | 2/6 | 500 |
