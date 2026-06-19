# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 10:14.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.7ms | 3.4× | 4/7 | 35.7ms | — | 24.1 MB | 3/7 | 0 |
| elixir | 196.4ms | 18.7× | 6/7 | 196.4ms | — | 72.0 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.8 MB | 1/7 | 0 |
| node | 17.7ms | 1.7× | 2/7 | 17.7ms | — | 46.4 MB | 5/7 | 0 |
| ruby | 41.0ms | 3.9× | 5/7 | 41.0ms | — | 23.5 MB | 2/7 | 0 |
| dotnet | 21.5ms | 2.0× | 3/7 | 21.5ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 271.4ms | 7.0× | 4/7 | 307.1ms | 35.7ms | 27.9 MB | 4/7 | 9227465 |
| elixir | 79.4ms | 2.0× | 3/7 | 275.8ms | 196.4ms | 69.8 MB | 6/7 | 9227465 |
| python | 760.2ms | 19.5× | 7/7 | 770.7ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 76.1ms | 2.0× | 2/7 | 93.8ms | 17.7ms | 52.3 MB | 5/7 | 9227465 |
| ruby | 624.7ms | 16.1× | 6/7 | 665.7ms | 41.0ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 38.9ms | 1.0× | 1/7 | 60.4ms | 21.5ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 58.9ms | 4.7× | 3/7 | 94.6ms | 35.7ms | 27.6 MB | 4/7 | 449999985000000 |
| elixir | 65.3ms | 5.2× | 4/7 | 261.7ms | 196.4ms | 70.4 MB | 6/7 | 449999985000000 |
| python | 2.392s | 189.8× | 7/7 | 2.402s | 10.5ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 30.9ms | 2.5× | 2/7 | 48.6ms | 17.7ms | 54.4 MB | 5/7 | 449999985000000 |
| ruby | 588.2ms | 46.7× | 6/7 | 629.2ms | 41.0ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 12.6ms | 1.0× | 1/7 | 34.1ms | 21.5ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.7ms | 9.8× | 3/7 | 145.4ms | 35.7ms | 24.1 MB | 3/7 | 12499997500000 |
| elixir | 32.0ms | 2.9× | 2/7 | 228.4ms | 196.4ms | 69.9 MB | 5/7 | 12499997500000 |
| python | 111.4ms | 9.9× | 4/7 | 121.9ms | 10.5ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 229.6ms | 20.5× | 5/7 | 247.3ms | 17.7ms | 94.5 MB | 6/7 | 12499997500000 |
| ruby | 236.8ms | 21.1× | 6/7 | 277.8ms | 41.0ms | 23.5 MB | 2/7 | 12499997500000 |
| dotnet | 11.2ms | 1.0× | 1/7 | 32.7ms | 21.5ms | 27.7 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.9ms | 4.7× | 4/7 | 73.6ms | 35.7ms | 27.7 MB | 4/7 | 13848 |
| elixir | 14.6ms | 1.8× | 2/7 | 211.0ms | 196.4ms | 70.0 MB | 6/7 | 13848 |
| python | 128.7ms | 15.9× | 5/7 | 139.2ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 23.8ms | 2.9× | 3/7 | 41.5ms | 17.7ms | 52.8 MB | 5/7 | 13848 |
| ruby | 132.0ms | 16.3× | 6/7 | 173.0ms | 41.0ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 8.1ms | 1.0× | 1/7 | 29.6ms | 21.5ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 461.9ms | 7.9× | 4/7 | 497.6ms | 35.7ms | 41.9 MB | 4/7 | 442 |
| elixir | 98.6ms | 1.7× | 2/7 | 295.0ms | 196.4ms | 69.8 MB | 6/7 | 442 |
| python | 2.478s | 42.5× | 7/7 | 2.489s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 176.5ms | 3.0× | 3/7 | 194.2ms | 17.7ms | 52.7 MB | 5/7 | 442 |
| ruby | 871.7ms | 15.0× | 6/7 | 912.7ms | 41.0ms | 23.5 MB | 2/7 | 442 |
| dotnet | 58.3ms | 1.0× | 1/7 | 79.8ms | 21.5ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 234.8ms | 12.2× | 3/7 | 270.5ms | 35.7ms | 27.9 MB | 4/7 | 6129302 |
| elixir | 252.1ms | 13.1× | 4/7 | 448.5ms | 196.4ms | 70.1 MB | 6/7 | 6129302 |
| python | 1.342s | 69.5× | 7/7 | 1.352s | 10.5ms | 10.1 MB | 1/7 | 6129302 |
| node | 20.1ms | 1.0× | 2/7 | 37.8ms | 17.7ms | 54.1 MB | 5/7 | 6129302 |
| ruby | 428.2ms | 22.2× | 6/7 | 469.2ms | 41.0ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 19.3ms | 1.0× | 1/7 | 40.8ms | 21.5ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 142.2ms | 23.7× | 4/7 | 177.9ms | 35.7ms | 38.1 MB | 4/7 | 654353666 |
| elixir | 55.6ms | 9.3× | 3/7 | 252.0ms | 196.4ms | 75.5 MB | 6/7 | 654353666 |
| python | 446.5ms | 74.4× | 6/7 | 457.0ms | 10.5ms | 10.4 MB | 1/7 | 654353666 |
| node | 23.0ms | 3.8× | 2/7 | 40.7ms | 17.7ms | 56.6 MB | 5/7 | 654353666 |
| ruby | 292.3ms | 48.7× | 5/7 | 333.3ms | 41.0ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 6.0ms | 1.0× | 1/7 | 27.5ms | 21.5ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.8ms | 1.0× | 1/7 | 61.5ms | 35.7ms | 34.3 MB | 1/7 | 3388889 |
| elixir | 111.2ms | 4.3× | 6/7 | 307.6ms | 196.4ms | 199.2 MB | 7/7 | 3388889 |
| python | 57.0ms | 2.2× | 3/7 | 67.5ms | 10.5ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.0ms | 2.5× | 4/7 | 81.7ms | 17.7ms | 99.8 MB | 5/7 | 3388889 |
| ruby | 99.0ms | 3.8× | 5/7 | 140.0ms | 41.0ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 30.9ms | 1.2× | 2/7 | 52.4ms | 21.5ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 810.4ms | 17.6× | 7/7 | 846.1ms | 35.7ms | 93.7 MB | 6/7 | 374854840 |
| elixir | 174.5ms | 3.8× | 5/7 | 370.9ms | 196.4ms | 72.3 MB | 5/7 | 374854840 |
| python | 172.6ms | 3.8× | 4/7 | 183.1ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 46.0ms | 1.0× | 1/7 | 63.7ms | 17.7ms | 54.7 MB | 4/7 | 374854840 |
| ruby | 80.8ms | 1.8× | 3/7 | 121.8ms | 41.0ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 50.8ms | 1.1× | 2/7 | 72.3ms | 21.5ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 385.4ms | 20.5× | 6/7 | 421.1ms | 35.7ms | 40.4 MB | 4/7 | 1638200 |
| elixir | 18.8ms | 1.0× | 1/7 | 215.2ms | 196.4ms | 70.1 MB | 6/7 | 1638200 |
| python | 108.5ms | 5.8× | 4/7 | 119.0ms | 10.5ms | 10.1 MB | 1/7 | 1638200 |
| node | 35.8ms | 1.9× | 3/7 | 53.5ms | 17.7ms | 60.5 MB | 5/7 | 1638200 |
| ruby | 112.3ms | 6.0× | 5/7 | 153.3ms | 41.0ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 24.0ms | 1.3× | 2/7 | 45.5ms | 21.5ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 276.9ms | 3.7× | 6/7 | 312.6ms | 35.7ms | 123.6 MB | 5/7 | 46468819 |
| elixir | 107.4ms | 1.5× | 3/7 | 303.8ms | 196.4ms | 157.8 MB | 7/7 | 46468819 |
| python | 184.0ms | 2.5× | 5/7 | 194.5ms | 10.5ms | 26.0 MB | 1/7 | 46468819 |
| node | 108.2ms | 1.5× | 4/7 | 125.9ms | 17.7ms | 69.4 MB | 4/7 | 46468819 |
| ruby | 74.0ms | 1.0× | 1/7 | 115.0ms | 41.0ms | 29.2 MB | 2/7 | 46468819 |
| dotnet | 79.1ms | 1.1× | 2/7 | 100.6ms | 21.5ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 491.2ms | 29.6× | 7/7 | 526.9ms | 35.7ms | 37.5 MB | 4/7 | 724 |
| elixir | 16.6ms | 1.0× | 1/7 | 213.0ms | 196.4ms | 69.7 MB | 6/7 | 724 |
| python | 68.4ms | 4.1× | 4/7 | 78.9ms | 10.5ms | 9.8 MB | 1/7 | 724 |
| node | 25.6ms | 1.5× | 2/7 | 43.3ms | 17.7ms | 55.2 MB | 5/7 | 724 |
| ruby | 125.3ms | 7.5× | 5/7 | 166.3ms | 41.0ms | 23.8 MB | 2/7 | 724 |
| dotnet | 33.6ms | 2.0× | 3/7 | 55.1ms | 21.5ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 187.8ms | 10.2× | 4/7 | 223.5ms | 35.7ms | 41.5 MB | 4/7 | 9900000 |
| elixir | 18.4ms | 1.0× | 1/7 | 214.8ms | 196.4ms | 69.9 MB | 6/7 | 9900000 |
| python | 48.0ms | 2.6× | 2/7 | 58.5ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 582.8ms | 31.7× | 6/7 | 600.5ms | 17.7ms | 54.8 MB | 5/7 | 9900000 |
| ruby | 110.3ms | 6.0× | 3/7 | 151.3ms | 41.0ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 293.5ms | 16.0× | 5/7 | 315.0ms | 21.5ms | 32.4 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 272.9ms | 15.6× | 5/7 | 308.6ms | 35.7ms | 42.5 MB | 4/7 | 2475000 |
| elixir | 17.5ms | 1.0× | 1/7 | 213.9ms | 196.4ms | 69.8 MB | 6/7 | 2475000 |
| python | 237.6ms | 13.6× | 4/7 | 248.1ms | 10.5ms | 9.9 MB | 1/7 | 2475000 |
| node | 225.0ms | 12.9× | 3/7 | 242.7ms | 17.7ms | 54.5 MB | 5/7 | 2475000 |
| ruby | 127.5ms | 7.3× | 2/7 | 168.5ms | 41.0ms | 30.2 MB | 2/7 | 2475000 |
| dotnet | 700.0ms | 40.0× | 6/7 | 721.5ms | 21.5ms | 32.6 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.7ms | 9.4× | 6/7 | 72.4ms | 35.7ms | 27.6 MB | 3/7 | 155553889038886 |
| elixir | 3.9ms | 1.0× | 1/7 | 200.3ms | 196.4ms | 71.0 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 1.2× | 2/7 | 15.0ms | 10.5ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 21.1ms | 5.4× | 5/7 | 38.8ms | 17.7ms | 56.4 MB | 5/7 | 155553889038886 |
| ruby | 10.9ms | 2.8× | 4/7 | 51.9ms | 41.0ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 8.6ms | 2.2× | 3/7 | 30.1ms | 21.5ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.5ms | 101.5× | 5/7 | 137.2ms | 35.7ms | 74.6 MB | 4/7 | 6100000 |
| elixir | 11.4ms | 11.4× | 2/7 | 207.8ms | 196.4ms | 78.6 MB | 5/7 | 6100000 |
| python | 551.2ms | 551.2× | 6/7 | 561.7ms | 10.5ms | 28.2 MB | 1/7 | 6100000 |
| node | 62.8ms | 62.8× | 4/7 | 80.5ms | 17.7ms | 55.6 MB | 3/7 | 6100000 |
| ruby | 1.602s | 1601.8× | 7/7 | 1.643s | 41.0ms | 136.7 MB | 7/7 | 6100000 |
| dotnet | 19.0ms | 19.0× | 3/7 | 40.5ms | 21.5ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 402.9ms | 402.9× | 5/7 | 438.6ms | 35.7ms | 31.4 MB | 4/7 | 31781100 |
| elixir | 65.7ms | 65.7× | 3/7 | 262.1ms | 196.4ms | 71.3 MB | 5/7 | 31781100 |
| python | 681.1ms | 681.1× | 7/7 | 691.6ms | 10.5ms | 22.3 MB | 1/7 | 31781100 |
| node | 109.8ms | 109.8× | 4/7 | 127.5ms | 17.7ms | 187.1 MB | 7/7 | 31781100 |
| ruby | 440.6ms | 440.6× | 6/7 | 481.6ms | 41.0ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 36.2ms | 36.2× | 2/7 | 57.7ms | 21.5ms | 28.0 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 146.8ms | 1.2× | 2/7 | 182.5ms | 35.7ms | 129.3 MB | 5/7 | 500 |
| elixir | 562.5ms | 4.4× | 7/7 | 758.9ms | 196.4ms | 466.0 MB | 7/7 | 500 |
| python | 174.1ms | 1.4× | 4/7 | 184.6ms | 10.5ms | 43.5 MB | 1/7 | 500 |
| node | 127.1ms | 1.0× | 1/7 | 144.8ms | 17.7ms | 69.5 MB | 4/7 | 500 |
| ruby | 216.4ms | 1.7× | 5/7 | 257.4ms | 41.0ms | 50.1 MB | 3/7 | 500 |
| dotnet | 158.2ms | 1.2× | 3/7 | 179.7ms | 21.5ms | 47.8 MB | 2/7 | 500 |
