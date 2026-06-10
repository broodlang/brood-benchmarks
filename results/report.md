# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-10 18:16.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.7ms | 2.7× | 4/6 | 28.7ms | — | 14.1 MB | 2/6 | 0 |
| elixir | 258.6ms | 24.4× | 6/6 | 258.6ms | — | 77.4 MB | 6/6 | 0 |
| python | 10.6ms | 1.0× | 1/6 | 10.6ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.1ms | 1.7× | 2/6 | 18.1ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 43.9ms | 4.1× | 5/6 | 43.9ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 22.9ms | 2.2× | 3/6 | 22.9ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 228.4ms | 73.7× | 6/6 | 257.1ms | 28.7ms | 14.1 MB | 2/6 | 832040 |
| elixir | 40.1ms | 12.9× | 3/6 | 298.7ms | 258.6ms | 81.7 MB | 6/6 | 832040 |
| python | 68.6ms | 22.1× | 5/6 | 79.2ms | 10.6ms | 9.7 MB | 1/6 | 832040 |
| node | 6.9ms | 2.2× | 2/6 | 25.0ms | 18.1ms | 48.5 MB | 5/6 | 832040 |
| ruby | 52.2ms | 16.8× | 4/6 | 96.1ms | 43.9ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 3.1ms | 1.0× | 1/6 | 26.0ms | 22.9ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.1ms | 147.1× | 5/6 | 175.8ms | 28.7ms | 14.0 MB | 2/6 | 3000000 |
| elixir | 48.4ms | 48.4× | 3/6 | 307.0ms | 258.6ms | 83.7 MB | 6/6 | 3000000 |
| python | 192.3ms | 192.3× | 6/6 | 202.9ms | 10.6ms | 9.7 MB | 1/6 | 3000000 |
| node | 2.4ms | 2.4× | 2/6 | 20.5ms | 18.1ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 58.8ms | 58.8× | 4/6 | 102.7ms | 43.9ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 0.0ms | < 1× | 1/6 | 22.7ms | 22.9ms | 26.0 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 21.3ms | 21.3× | 6/6 | 50.0ms | 28.7ms | 14.0 MB | 2/6 | 499999500000 |
| elixir | 4.7ms | 4.7× | 4/6 | 263.3ms | 258.6ms | 77.9 MB | 6/6 | 499999500000 |
| python | 6.1ms | 6.1× | 5/6 | 16.7ms | 10.6ms | 9.8 MB | 1/6 | 499999500000 |
| node | 2.9ms | 2.9× | 3/6 | 21.0ms | 18.1ms | 50.3 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 42.4ms | 43.9ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 0.7ms | < 1× | 2/6 | 23.6ms | 22.9ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.3ms | 20.2× | 5/6 | 53.0ms | 28.7ms | 14.1 MB | 2/6 | 2262 |
| elixir | 42.8ms | 35.7× | 6/6 | 301.4ms | 258.6ms | 84.2 MB | 6/6 | 2262 |
| python | 8.8ms | 7.3× | 4/6 | 19.4ms | 10.6ms | 9.9 MB | 1/6 | 2262 |
| node | 1.4ms | 1.2× | 2/6 | 19.5ms | 18.1ms | 49.0 MB | 5/6 | 2262 |
| ruby | 6.2ms | 5.2× | 3/6 | 50.1ms | 43.9ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.2ms | 1.0× | 1/6 | 24.1ms | 22.9ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 281.0ms | 85.2× | 6/6 | 309.7ms | 28.7ms | 26.6 MB | 4/6 | 307 |
| elixir | 58.4ms | 17.7× | 3/6 | 317.0ms | 258.6ms | 83.6 MB | 6/6 | 307 |
| python | 244.1ms | 74.0× | 5/6 | 254.7ms | 10.6ms | 9.8 MB | 1/6 | 307 |
| node | 7.8ms | 2.4× | 2/6 | 25.9ms | 18.1ms | 48.6 MB | 5/6 | 307 |
| ruby | 82.3ms | 24.9× | 4/6 | 126.2ms | 43.9ms | 23.5 MB | 2/6 | 307 |
| dotnet | 3.3ms | 1.0× | 1/6 | 26.2ms | 22.9ms | 26.0 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.2ms | 67.5× | 6/6 | 102.9ms | 28.7ms | 14.0 MB | 2/6 | 345426 |
| elixir | 65.1ms | 59.2× | 4/6 | 323.7ms | 258.6ms | 83.9 MB | 6/6 | 345426 |
| python | 73.0ms | 66.4× | 5/6 | 83.6ms | 10.6ms | 10.0 MB | 1/6 | 345426 |
| node | 2.8ms | 2.5× | 2/6 | 20.9ms | 18.1ms | 50.3 MB | 5/6 | 345426 |
| ruby | 24.9ms | 22.6× | 3/6 | 68.8ms | 43.9ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.1ms | 1.0× | 1/6 | 24.0ms | 22.9ms | 26.0 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.5ms | 152.5× | 6/6 | 181.2ms | 28.7ms | 28.3 MB | 4/6 | 229499993 |
| elixir | 35.5ms | 35.5× | 4/6 | 294.1ms | 258.6ms | 78.1 MB | 6/6 | 229499993 |
| python | 47.0ms | 47.0× | 5/6 | 57.6ms | 10.6ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.2ms | 3.2× | 2/6 | 21.3ms | 18.1ms | 49.1 MB | 5/6 | 229499993 |
| ruby | 28.8ms | 28.8× | 3/6 | 72.7ms | 43.9ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 0.7ms | < 1× | 1/6 | 23.6ms | 22.9ms | 26.1 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.7ms | 16.1× | 6/6 | 91.4ms | 28.7ms | 29.8 MB | 3/6 | 288889 |
| elixir | 20.6ms | 5.3× | 5/6 | 279.2ms | 258.6ms | 86.2 MB | 6/6 | 288889 |
| python | 3.9ms | 1.0× | 2/6 | 14.5ms | 10.6ms | 12.9 MB | 1/6 | 288889 |
| node | 6.0ms | 1.5× | 4/6 | 24.1ms | 18.1ms | 52.5 MB | 5/6 | 288889 |
| ruby | 3.9ms | 1.0× | 1/6 | 47.8ms | 43.9ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 3.9ms | 1.0× | 3/6 | 26.8ms | 22.9ms | 30.0 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 209.2ms | 32.7× | 6/6 | 237.9ms | 28.7ms | 38.2 MB | 4/6 | 50038280 |
| elixir | 30.2ms | 4.7× | 5/6 | 288.8ms | 258.6ms | 78.3 MB | 6/6 | 50038280 |
| python | 22.5ms | 3.5× | 4/6 | 33.1ms | 10.6ms | 9.9 MB | 1/6 | 50038280 |
| node | 6.4ms | 1.0× | 1/6 | 24.5ms | 18.1ms | 50.4 MB | 5/6 | 50038280 |
| ruby | 8.2ms | 1.3× | 2/6 | 52.1ms | 43.9ms | 23.6 MB | 2/6 | 50038280 |
| dotnet | 9.1ms | 1.4× | 3/6 | 32.0ms | 22.9ms | 27.1 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 335.7ms | 129.1× | 6/6 | 364.4ms | 28.7ms | 22.4 MB | 2/6 | 327640 |
| elixir | 46.1ms | 17.7× | 5/6 | 304.7ms | 258.6ms | 81.1 MB | 6/6 | 327640 |
| python | 19.5ms | 7.5× | 4/6 | 30.1ms | 10.6ms | 10.0 MB | 1/6 | 327640 |
| node | 6.6ms | 2.5× | 2/6 | 24.7ms | 18.1ms | 52.4 MB | 5/6 | 327640 |
| ruby | 18.9ms | 7.3× | 3/6 | 62.8ms | 43.9ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 2.6ms | 1.0× | 1/6 | 25.5ms | 22.9ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.6ms | 6.0× | 6/6 | 64.3ms | 28.7ms | 21.3 MB | 2/6 | 102632633 |
| elixir | 18.9ms | 3.2× | 5/6 | 277.5ms | 258.6ms | 85.8 MB | 6/6 | 102632633 |
| python | 17.2ms | 2.9× | 4/6 | 27.8ms | 10.6ms | 12.2 MB | 1/6 | 102632633 |
| node | 16.5ms | 2.8× | 3/6 | 34.6ms | 18.1ms | 51.4 MB | 5/6 | 102632633 |
| ruby | 5.9ms | 1.0× | 1/6 | 49.8ms | 43.9ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 11.3ms | 1.9× | 2/6 | 34.2ms | 22.9ms | 27.0 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.336s | 49.1× | 5/6 | 1.364s | 28.7ms | 183.9 MB | 5/6 | 12200000 |
| elixir | 85.3ms | 3.1× | 2/6 | 343.9ms | 258.6ms | 90.8 MB | 4/6 | 12200000 |
| python | 1.088s | 40.0× | 4/6 | 1.098s | 10.6ms | 35.9 MB | 2/6 | 12200000 |
| node | 106.5ms | 3.9× | 3/6 | 124.6ms | 18.1ms | 55.7 MB | 3/6 | 12200000 |
| ruby | 4.936s | 181.5× | 6/6 | 4.980s | 43.9ms | 247.0 MB | 6/6 | 12200000 |
| dotnet | 27.2ms | 1.0× | 1/6 | 50.1ms | 22.9ms | 32.1 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.535s | 63.4× | 6/6 | 2.564s | 28.7ms | 14.6 MB | 1/6 | 31781100 |
| elixir | 120.6ms | 3.0× | 2/6 | 379.2ms | 258.6ms | 83.0 MB | 5/6 | 31781100 |
| python | 774.2ms | 19.4× | 5/6 | 784.8ms | 10.6ms | 22.3 MB | 2/6 | 31781100 |
| node | 126.6ms | 3.2× | 3/6 | 144.7ms | 18.1ms | 182.4 MB | 6/6 | 31781100 |
| ruby | 492.8ms | 12.3× | 4/6 | 536.7ms | 43.9ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 40.0ms | 1.0× | 1/6 | 62.9ms | 22.9ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 174.3ms | 1.4× | 3/6 | 203.0ms | 28.7ms | 96.6 MB | 5/6 | 500 |
| elixir | 713.8ms | 5.8× | 6/6 | 972.4ms | 258.6ms | 567.2 MB | 6/6 | 500 |
| python | 185.7ms | 1.5× | 4/6 | 196.3ms | 10.6ms | 49.2 MB | 2/6 | 500 |
| node | 124.1ms | 1.0× | 1/6 | 142.2ms | 18.1ms | 65.4 MB | 4/6 | 500 |
| ruby | 216.9ms | 1.7× | 5/6 | 260.8ms | 43.9ms | 50.1 MB | 3/6 | 500 |
| dotnet | 152.3ms | 1.2× | 2/6 | 175.2ms | 22.9ms | 49.1 MB | 1/6 | 500 |
