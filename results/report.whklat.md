# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 21:23.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 5 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.0ms | 2.7× | 4/6 | 27.0ms | — | 12.0 MB | 2/6 | 0 |
| elixir | 265.2ms | 26.8× | 6/6 | 265.2ms | — | 76.9 MB | 6/6 | 0 |
| python | 9.9ms | 1.0× | 1/6 | 9.9ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.8ms | 1.8× | 2/6 | 17.8ms | — | 42.8 MB | 5/6 | 0 |
| ruby | 42.3ms | 4.3× | 5/6 | 42.3ms | — | 23.6 MB | 3/6 | 0 |
| dotnet | 22.4ms | 2.3× | 3/6 | 22.4ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.2ms | 65.9× | 6/6 | 251.2ms | 27.0ms | 11.9 MB | 2/6 | 832040 |
| elixir | 45.3ms | 13.3× | 3/6 | 310.5ms | 265.2ms | 83.1 MB | 6/6 | 832040 |
| python | 67.5ms | 19.9× | 5/6 | 77.4ms | 9.9ms | 9.8 MB | 1/6 | 832040 |
| node | 7.3ms | 2.1× | 2/6 | 25.1ms | 17.8ms | 48.0 MB | 5/6 | 832040 |
| ruby | 57.1ms | 16.8× | 4/6 | 99.4ms | 42.3ms | 23.6 MB | 3/6 | 832040 |
| dotnet | 3.4ms | 1.0× | 1/6 | 25.8ms | 22.4ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 175.7ms | 103.4× | 5/6 | 202.7ms | 27.0ms | 12.0 MB | 2/6 | 3000000 |
| elixir | 35.6ms | 20.9× | 3/6 | 300.8ms | 265.2ms | 83.7 MB | 6/6 | 3000000 |
| python | 197.9ms | 116.4× | 6/6 | 207.8ms | 9.9ms | 9.7 MB | 1/6 | 3000000 |
| node | 4.1ms | 2.4× | 2/6 | 21.9ms | 17.8ms | 47.8 MB | 5/6 | 3000000 |
| ruby | 64.4ms | 37.9× | 4/6 | 106.7ms | 42.3ms | 23.6 MB | 3/6 | 3000000 |
| dotnet | 1.7ms | 1.0× | 1/6 | 24.1ms | 22.4ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.5ms | 102.5× | 6/6 | 129.5ms | 27.0ms | 11.9 MB | 2/6 | 499999500000 |
| elixir | 2.3ms | 2.3× | 3/6 | 267.5ms | 265.2ms | 77.1 MB | 6/6 | 499999500000 |
| python | 7.1ms | 7.1× | 5/6 | 17.0ms | 9.9ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.4ms | 3.4× | 4/6 | 21.2ms | 17.8ms | 49.9 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 42.2ms | 42.3ms | 23.6 MB | 3/6 | 499999500000 |
| dotnet | 0.9ms | < 1× | 2/6 | 23.3ms | 22.4ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.4ms | 21.0× | 5/6 | 56.4ms | 27.0ms | 12.0 MB | 2/6 | 2262 |
| elixir | 46.3ms | 33.1× | 6/6 | 311.5ms | 265.2ms | 81.0 MB | 6/6 | 2262 |
| python | 9.0ms | 6.4× | 4/6 | 18.9ms | 9.9ms | 10.0 MB | 1/6 | 2262 |
| node | 1.4ms | 1.0× | 1/6 | 19.2ms | 17.8ms | 48.5 MB | 5/6 | 2262 |
| ruby | 7.9ms | 5.6× | 3/6 | 50.2ms | 42.3ms | 23.6 MB | 3/6 | 2262 |
| dotnet | 1.5ms | 1.1× | 2/6 | 23.9ms | 22.4ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 299.0ms | 71.2× | 6/6 | 326.0ms | 27.0ms | 21.0 MB | 2/6 | 307 |
| elixir | 51.5ms | 12.3× | 3/6 | 316.7ms | 265.2ms | 82.3 MB | 6/6 | 307 |
| python | 232.2ms | 55.3× | 5/6 | 242.1ms | 9.9ms | 9.8 MB | 1/6 | 307 |
| node | 6.9ms | 1.6× | 2/6 | 24.7ms | 17.8ms | 48.0 MB | 5/6 | 307 |
| ruby | 86.9ms | 20.7× | 4/6 | 129.2ms | 42.3ms | 23.6 MB | 3/6 | 307 |
| dotnet | 4.2ms | 1.0× | 1/6 | 26.6ms | 22.4ms | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.3ms | 50.2× | 6/6 | 107.3ms | 27.0ms | 12.0 MB | 2/6 | 345426 |
| elixir | 48.3ms | 30.2× | 4/6 | 313.5ms | 265.2ms | 81.4 MB | 6/6 | 345426 |
| python | 77.0ms | 48.1× | 5/6 | 86.9ms | 9.9ms | 10.0 MB | 1/6 | 345426 |
| node | 4.1ms | 2.6× | 2/6 | 21.9ms | 17.8ms | 50.1 MB | 5/6 | 345426 |
| ruby | 23.5ms | 14.7× | 3/6 | 65.8ms | 42.3ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.6ms | 1.0× | 1/6 | 24.0ms | 22.4ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 664.9ms | 554.1× | 6/6 | 691.9ms | 27.0ms | 23.3 MB | 2/6 | 229499993 |
| elixir | 12.2ms | 10.2× | 3/6 | 277.4ms | 265.2ms | 78.3 MB | 6/6 | 229499993 |
| python | 45.2ms | 37.7× | 5/6 | 55.1ms | 9.9ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.5ms | 2.9× | 2/6 | 21.3ms | 17.8ms | 48.6 MB | 5/6 | 229499993 |
| ruby | 26.6ms | 22.2× | 4/6 | 68.9ms | 42.3ms | 23.7 MB | 3/6 | 229499993 |
| dotnet | 1.2ms | 1.0× | 1/6 | 23.6ms | 22.4ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 146.1ms | 33.2× | 6/6 | 173.1ms | 27.0ms | 41.8 MB | 4/6 | 288889 |
| elixir | 10.7ms | 2.4× | 5/6 | 275.9ms | 265.2ms | 90.3 MB | 6/6 | 288889 |
| python | 4.8ms | 1.1× | 2/6 | 14.7ms | 9.9ms | 12.8 MB | 1/6 | 288889 |
| node | 6.3ms | 1.4× | 3/6 | 24.1ms | 17.8ms | 52.1 MB | 5/6 | 288889 |
| ruby | 7.6ms | 1.7× | 4/6 | 49.9ms | 42.3ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 4.4ms | 1.0× | 1/6 | 26.8ms | 22.4ms | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 197.4ms | 29.5× | 6/6 | 224.4ms | 27.0ms | 27.4 MB | 4/6 | 50038280 |
| elixir | 30.9ms | 4.6× | 5/6 | 296.1ms | 265.2ms | 79.5 MB | 6/6 | 50038280 |
| python | 23.4ms | 3.5× | 4/6 | 33.3ms | 9.9ms | 9.9 MB | 1/6 | 50038280 |
| node | 6.7ms | 1.0× | 1/6 | 24.5ms | 17.8ms | 49.9 MB | 5/6 | 50038280 |
| ruby | 10.4ms | 1.6× | 3/6 | 52.7ms | 42.3ms | 23.6 MB | 2/6 | 50038280 |
| dotnet | 9.9ms | 1.5× | 2/6 | 32.3ms | 22.4ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 385.7ms | 75.6× | 6/6 | 412.7ms | 27.0ms | 16.2 MB | 2/6 | 327640 |
| elixir | 43.4ms | 8.5× | 5/6 | 308.6ms | 265.2ms | 83.7 MB | 6/6 | 327640 |
| python | 21.3ms | 4.2× | 3/6 | 31.2ms | 9.9ms | 10.1 MB | 1/6 | 327640 |
| node | 7.2ms | 1.4× | 2/6 | 25.0ms | 17.8ms | 51.9 MB | 5/6 | 327640 |
| ruby | 24.7ms | 4.8× | 4/6 | 67.0ms | 42.3ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 5.1ms | 1.0× | 1/6 | 27.5ms | 22.4ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.2ms | 3.8× | 6/6 | 63.2ms | 27.0ms | 19.0 MB | 2/6 | 102632633 |
| elixir | 20.0ms | 2.1× | 5/6 | 285.2ms | 265.2ms | 85.8 MB | 6/6 | 102632633 |
| python | 17.8ms | 1.9× | 4/6 | 27.7ms | 9.9ms | 12.1 MB | 1/6 | 102632633 |
| node | 17.4ms | 1.8× | 3/6 | 35.2ms | 17.8ms | 50.9 MB | 5/6 | 102632633 |
| ruby | 9.5ms | 1.0× | 1/6 | 51.8ms | 42.3ms | 24.1 MB | 3/6 | 102632633 |
| dotnet | 13.6ms | 1.4× | 2/6 | 36.0ms | 22.4ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.003s | 45.8× | 4/6 | 1.030s | 27.0ms | 164.1 MB | 5/6 | 12200000 |
| elixir | 98.5ms | 4.5× | 2/6 | 363.7ms | 265.2ms | 90.1 MB | 4/6 | 12200000 |
| python | 1.085s | 49.5× | 5/6 | 1.095s | 9.9ms | 35.9 MB | 2/6 | 12200000 |
| node | 108.3ms | 4.9× | 3/6 | 126.1ms | 17.8ms | 55.2 MB | 3/6 | 12200000 |
| ruby | 5.064s | 231.3× | 6/6 | 5.107s | 42.3ms | 246.7 MB | 6/6 | 12200000 |
| dotnet | 21.9ms | 1.0× | 1/6 | 44.3ms | 22.4ms | 31.9 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.992s | 47.9× | 6/6 | 2.019s | 27.0ms | 12.0 MB | 1/6 | 31781100 |
| elixir | 145.7ms | 3.5× | 3/6 | 410.9ms | 265.2ms | 84.9 MB | 5/6 | 31781100 |
| python | 761.7ms | 18.3× | 5/6 | 771.6ms | 9.9ms | 22.1 MB | 2/6 | 31781100 |
| node | 130.0ms | 3.1× | 2/6 | 147.8ms | 17.8ms | 181.1 MB | 6/6 | 31781100 |
| ruby | 522.0ms | 12.5× | 4/6 | 564.3ms | 42.3ms | 23.6 MB | 3/6 | 31781100 |
| dotnet | 41.6ms | 1.0× | 1/6 | 64.0ms | 22.4ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.2ms | 1.2× | 3/5 | 179.2ms | 27.0ms | 68.2 MB | 4/5 | 0 |
| elixir | 686.1ms | 5.6× | 5/5 | 951.3ms | 265.2ms | 487.2 MB | 5/5 | 0 |
| python | — | — | — | — | — | — | — | ERROR |
| node | 123.3ms | 1.0× | 1/5 | 141.1ms | 17.8ms | 63.9 MB | 3/5 | 0 |
| ruby | 214.6ms | 1.7× | 4/5 | 256.9ms | 42.3ms | 50.5 MB | 2/5 | 0 |
| dotnet | 132.2ms | 1.1× | 2/5 | 154.6ms | 22.4ms | 48.3 MB | 1/5 | 0 |
