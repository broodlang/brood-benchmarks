# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-12 19:57.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.7ms | 3.0× | 4/6 | 27.7ms | — | 13.7 MB | 2/6 | 0 |
| elixir | 255.6ms | 28.1× | 6/6 | 255.6ms | — | 79.9 MB | 6/6 | 0 |
| python | 9.1ms | 1.0× | 1/6 | 9.1ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.0ms | 2.0× | 2/6 | 18.0ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 41.4ms | 4.5× | 5/6 | 41.4ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.9ms | 2.4× | 3/6 | 21.9ms | — | 25.8 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 136.0ms | 34.0× | 6/6 | 163.7ms | 27.7ms | 14.5 MB | 2/6 | 832040 |
| elixir | 53.5ms | 13.4× | 3/6 | 309.1ms | 255.6ms | 80.7 MB | 6/6 | 832040 |
| python | 69.3ms | 17.3× | 5/6 | 78.4ms | 9.1ms | 9.8 MB | 1/6 | 832040 |
| node | 7.8ms | 2.0× | 2/6 | 25.8ms | 18.0ms | 48.5 MB | 5/6 | 832040 |
| ruby | 55.9ms | 14.0× | 4/6 | 97.3ms | 41.4ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.0ms | 1.0× | 1/6 | 25.9ms | 21.9ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 19.1ms | 11.9× | 3/6 | 46.8ms | 27.7ms | 14.4 MB | 2/6 | 3000000 |
| elixir | 57.9ms | 36.2× | 4/6 | 313.5ms | 255.6ms | 82.6 MB | 6/6 | 3000000 |
| python | 194.0ms | 121.2× | 6/6 | 203.1ms | 9.1ms | 9.8 MB | 1/6 | 3000000 |
| node | 3.3ms | 2.1× | 2/6 | 21.3ms | 18.0ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 62.5ms | 39.1× | 5/6 | 103.9ms | 41.4ms | 23.6 MB | 3/6 | 3000000 |
| dotnet | 1.6ms | 1.0× | 1/6 | 23.5ms | 21.9ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 21.8ms | 21.8× | 6/6 | 49.5ms | 27.7ms | 13.8 MB | 2/6 | 499999500000 |
| elixir | 12.2ms | 12.2× | 5/6 | 267.8ms | 255.6ms | 78.7 MB | 6/6 | 499999500000 |
| python | 6.9ms | 6.9× | 4/6 | 16.0ms | 9.1ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.0ms | 3.0× | 3/6 | 21.0ms | 18.0ms | 50.3 MB | 5/6 | 499999500000 |
| ruby | 0.5ms | < 1× | 1/6 | 41.9ms | 41.4ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.0ms | 1.0× | 2/6 | 22.9ms | 21.9ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.9ms | 17.8× | 5/6 | 52.6ms | 27.7ms | 13.8 MB | 2/6 | 2262 |
| elixir | 44.6ms | 31.9× | 6/6 | 300.2ms | 255.6ms | 80.9 MB | 6/6 | 2262 |
| python | 10.0ms | 7.1× | 4/6 | 19.1ms | 9.1ms | 9.9 MB | 1/6 | 2262 |
| node | 1.4ms | 1.0× | 1/6 | 19.4ms | 18.0ms | 48.9 MB | 5/6 | 2262 |
| ruby | 9.6ms | 6.9× | 3/6 | 51.0ms | 41.4ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.7ms | 1.2× | 2/6 | 23.6ms | 21.9ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.7ms | 14.2× | 4/6 | 90.4ms | 27.7ms | 26.0 MB | 3/6 | 307 |
| elixir | 51.2ms | 11.6× | 3/6 | 306.8ms | 255.6ms | 82.4 MB | 6/6 | 307 |
| python | 242.6ms | 55.1× | 6/6 | 251.7ms | 9.1ms | 9.8 MB | 1/6 | 307 |
| node | 7.5ms | 1.7× | 2/6 | 25.5ms | 18.0ms | 48.5 MB | 5/6 | 307 |
| ruby | 86.3ms | 19.6× | 5/6 | 127.7ms | 41.4ms | 23.5 MB | 2/6 | 307 |
| dotnet | 4.4ms | 1.0× | 1/6 | 26.3ms | 21.9ms | 26.2 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.4ms | 37.7× | 5/6 | 103.1ms | 27.7ms | 13.8 MB | 2/6 | 345426 |
| elixir | 69.8ms | 34.9× | 4/6 | 325.4ms | 255.6ms | 83.3 MB | 6/6 | 345426 |
| python | 77.7ms | 38.9× | 6/6 | 86.8ms | 9.1ms | 10.0 MB | 1/6 | 345426 |
| node | 3.4ms | 1.7× | 2/6 | 21.4ms | 18.0ms | 50.4 MB | 5/6 | 345426 |
| ruby | 32.1ms | 16.1× | 3/6 | 73.5ms | 41.4ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 2.0ms | 1.0× | 1/6 | 23.9ms | 21.9ms | 26.2 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.6ms | 59.8× | 6/6 | 129.3ms | 27.7ms | 27.7 MB | 4/6 | 229499993 |
| elixir | 28.0ms | 16.5× | 3/6 | 283.6ms | 255.6ms | 77.9 MB | 6/6 | 229499993 |
| python | 46.4ms | 27.3× | 5/6 | 55.5ms | 9.1ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.5ms | 2.1× | 2/6 | 21.5ms | 18.0ms | 48.8 MB | 5/6 | 229499993 |
| ruby | 32.9ms | 19.4× | 4/6 | 74.3ms | 41.4ms | 23.6 MB | 2/6 | 229499993 |
| dotnet | 1.7ms | 1.0× | 1/6 | 23.6ms | 21.9ms | 26.3 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.0ms | 13.2× | 6/6 | 89.7ms | 27.7ms | 29.1 MB | 3/6 | 288889 |
| elixir | 16.1ms | 3.4× | 5/6 | 271.7ms | 255.6ms | 86.3 MB | 6/6 | 288889 |
| python | 5.8ms | 1.2× | 2/6 | 14.9ms | 9.1ms | 12.8 MB | 1/6 | 288889 |
| node | 6.3ms | 1.3× | 3/6 | 24.3ms | 18.0ms | 52.5 MB | 5/6 | 288889 |
| ruby | 7.5ms | 1.6× | 4/6 | 48.9ms | 41.4ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 4.7ms | 1.0× | 1/6 | 26.6ms | 21.9ms | 30.1 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 157.0ms | 22.1× | 6/6 | 184.7ms | 27.7ms | 52.9 MB | 5/6 | 50038280 |
| elixir | 47.7ms | 6.7× | 5/6 | 303.3ms | 255.6ms | 78.1 MB | 6/6 | 50038280 |
| python | 24.0ms | 3.4× | 4/6 | 33.1ms | 9.1ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.1ms | 1.0× | 1/6 | 25.1ms | 18.0ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 9.4ms | 1.3× | 2/6 | 50.8ms | 41.4ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.0ms | 1.4× | 3/6 | 31.9ms | 21.9ms | 27.3 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 294.9ms | 67.0× | 6/6 | 322.6ms | 27.7ms | 19.3 MB | 2/6 | 327640 |
| elixir | 48.9ms | 11.1× | 5/6 | 304.5ms | 255.6ms | 80.8 MB | 6/6 | 327640 |
| python | 20.4ms | 4.6× | 4/6 | 29.5ms | 9.1ms | 10.0 MB | 1/6 | 327640 |
| node | 6.3ms | 1.4× | 2/6 | 24.3ms | 18.0ms | 52.3 MB | 5/6 | 327640 |
| ruby | 19.7ms | 4.5× | 3/6 | 61.1ms | 41.4ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.4ms | 1.0× | 1/6 | 26.3ms | 21.9ms | 30.9 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.3ms | 2.8× | 6/6 | 58.0ms | 27.7ms | 24.2 MB | 3/6 | 102632633 |
| elixir | 26.7ms | 2.4× | 5/6 | 282.3ms | 255.6ms | 88.5 MB | 6/6 | 102632633 |
| python | 21.0ms | 1.9× | 4/6 | 30.1ms | 9.1ms | 12.2 MB | 1/6 | 102632633 |
| node | 15.6ms | 1.4× | 3/6 | 33.6ms | 18.0ms | 51.5 MB | 5/6 | 102632633 |
| ruby | 10.9ms | 1.0× | 1/6 | 52.3ms | 41.4ms | 24.0 MB | 2/6 | 102632633 |
| dotnet | 14.9ms | 1.4× | 2/6 | 36.8ms | 21.9ms | 27.2 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.433s | 66.1× | 5/6 | 1.461s | 27.7ms | 196.5 MB | 5/6 | 12200000 |
| elixir | 115.3ms | 5.3× | 3/6 | 370.9ms | 255.6ms | 91.6 MB | 4/6 | 12200000 |
| python | 1.121s | 51.7× | 4/6 | 1.131s | 9.1ms | 35.9 MB | 2/6 | 12200000 |
| node | 107.5ms | 5.0× | 2/6 | 125.5ms | 18.0ms | 55.9 MB | 3/6 | 12200000 |
| ruby | 5.104s | 235.2× | 6/6 | 5.145s | 41.4ms | 246.8 MB | 6/6 | 12200000 |
| dotnet | 21.7ms | 1.0× | 1/6 | 43.6ms | 21.9ms | 31.9 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.259s | 27.0× | 6/6 | 1.286s | 27.7ms | 16.4 MB | 1/6 | 31781100 |
| elixir | 151.1ms | 3.2× | 3/6 | 406.7ms | 255.6ms | 82.5 MB | 5/6 | 31781100 |
| python | 826.3ms | 17.7× | 5/6 | 835.4ms | 9.1ms | 22.2 MB | 2/6 | 31781100 |
| node | 139.7ms | 3.0× | 2/6 | 157.7ms | 18.0ms | 182.2 MB | 6/6 | 31781100 |
| ruby | 520.6ms | 11.1× | 4/6 | 562.0ms | 41.4ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 46.7ms | 1.0× | 1/6 | 68.6ms | 21.9ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 209.9ms | 1.7× | 4/6 | 237.6ms | 27.7ms | 101.9 MB | 5/6 | 500 |
| elixir | 769.7ms | 6.2× | 6/6 | 1.025s | 255.6ms | 549.3 MB | 6/6 | 500 |
| python | 193.9ms | 1.6× | 3/6 | 203.0ms | 9.1ms | 46.8 MB | 1/6 | 500 |
| node | 124.6ms | 1.0× | 1/6 | 142.6ms | 18.0ms | 65.6 MB | 4/6 | 500 |
| ruby | 215.5ms | 1.7× | 5/6 | 256.9ms | 41.4ms | 50.3 MB | 3/6 | 500 |
| dotnet | 156.1ms | 1.3× | 2/6 | 178.0ms | 21.9ms | 48.5 MB | 2/6 | 500 |
