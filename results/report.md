# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 18:58.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.8ms | 2.4× | 4/7 | 25.8ms | — | 20.4 MB | 2/7 | 0 |
| elixir | 202.2ms | 18.6× | 6/7 | 202.2ms | — | 70.2 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.7ms | 1.7× | 2/7 | 18.7ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 42.7ms | 3.9× | 5/7 | 42.7ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.0ms | 2.0× | 3/7 | 22.0ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 281.3ms | 5.4× | 4/7 | 307.1ms | 25.8ms | 24.0 MB | 3/7 | 9227465 |
| elixir | 80.3ms | 1.6× | 2/7 | 282.5ms | 202.2ms | 69.8 MB | 6/7 | 9227465 |
| python | 782.4ms | 15.1× | 7/7 | 793.3ms | 10.9ms | 9.8 MB | 1/7 | 9227465 |
| node | 94.9ms | 1.8× | 3/7 | 113.6ms | 18.7ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 751.4ms | 14.5× | 6/7 | 794.1ms | 42.7ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 51.8ms | 1.0× | 1/7 | 73.8ms | 22.0ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.7ms | 4.2× | 3/7 | 99.5ms | 25.8ms | 23.9 MB | 3/7 | 449999985000000 |
| elixir | 109.4ms | 6.2× | 4/7 | 311.6ms | 202.2ms | 69.7 MB | 6/7 | 449999985000000 |
| python | 2.793s | 158.7× | 7/7 | 2.804s | 10.9ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 39.6ms | 2.2× | 2/7 | 58.3ms | 18.7ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 703.7ms | 40.0× | 6/7 | 746.4ms | 42.7ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 17.6ms | 1.0× | 1/7 | 39.6ms | 22.0ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 126.4ms | 7.9× | 3/7 | 152.2ms | 25.8ms | 20.5 MB | 2/7 | 12499997500000 |
| elixir | 60.7ms | 3.8× | 2/7 | 262.9ms | 202.2ms | 69.7 MB | 5/7 | 12499997500000 |
| python | 129.0ms | 8.0× | 4/7 | 139.9ms | 10.9ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 268.2ms | 16.7× | 5/7 | 286.9ms | 18.7ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 273.0ms | 17.0× | 6/7 | 315.7ms | 42.7ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 16.1ms | 1.0× | 1/7 | 38.1ms | 22.0ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 49.0ms | 3.8× | 4/7 | 74.8ms | 25.8ms | 24.1 MB | 3/7 | 13848 |
| elixir | 46.7ms | 3.6× | 3/7 | 248.9ms | 202.2ms | 69.8 MB | 6/7 | 13848 |
| python | 142.4ms | 11.0× | 6/7 | 153.3ms | 10.9ms | 9.9 MB | 1/7 | 13848 |
| node | 13.9ms | 1.1× | 2/7 | 32.6ms | 18.7ms | 49.1 MB | 5/7 | 13848 |
| ruby | 140.7ms | 10.9× | 5/7 | 183.4ms | 42.7ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 12.9ms | 1.0× | 1/7 | 34.9ms | 22.0ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 419.7ms | 8.1× | 4/7 | 445.5ms | 25.8ms | 37.8 MB | 4/7 | 442 |
| elixir | 128.4ms | 2.5× | 2/7 | 330.6ms | 202.2ms | 69.8 MB | 6/7 | 442 |
| python | 2.658s | 51.6× | 7/7 | 2.669s | 10.9ms | 9.8 MB | 1/7 | 442 |
| node | 197.9ms | 3.8× | 3/7 | 216.6ms | 18.7ms | 48.9 MB | 5/7 | 442 |
| ruby | 951.3ms | 18.5× | 6/7 | 994.0ms | 42.7ms | 23.5 MB | 2/7 | 442 |
| dotnet | 51.5ms | 1.0× | 1/7 | 73.5ms | 22.0ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 239.0ms | 10.1× | 3/7 | 264.8ms | 25.8ms | 24.1 MB | 3/7 | 6129302 |
| elixir | 292.7ms | 12.4× | 4/7 | 494.9ms | 202.2ms | 70.0 MB | 6/7 | 6129302 |
| python | 1.502s | 63.4× | 7/7 | 1.513s | 10.9ms | 10.1 MB | 1/7 | 6129302 |
| node | 25.9ms | 1.1× | 2/7 | 44.6ms | 18.7ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 491.9ms | 20.8× | 5/7 | 534.6ms | 42.7ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 23.7ms | 1.0× | 1/7 | 45.7ms | 22.0ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 121.0ms | 24.7× | 4/7 | 146.8ms | 25.8ms | 36.7 MB | 4/7 | 654353666 |
| elixir | 93.1ms | 19.0× | 3/7 | 295.3ms | 202.2ms | 79.2 MB | 6/7 | 654353666 |
| python | 458.1ms | 93.5× | 6/7 | 469.0ms | 10.9ms | 10.4 MB | 1/7 | 654353666 |
| node | 26.0ms | 5.3× | 2/7 | 44.7ms | 18.7ms | 52.7 MB | 5/7 | 654353666 |
| ruby | 297.9ms | 60.8× | 5/7 | 340.6ms | 42.7ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.9ms | 1.0× | 1/7 | 26.9ms | 22.0ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.2ms | 1.0× | 1/7 | 39.0ms | 25.8ms | 30.5 MB | 1/7 | 3388889 |
| elixir | 121.6ms | 9.2× | 6/7 | 323.8ms | 202.2ms | 199.4 MB | 7/7 | 3388889 |
| python | 45.2ms | 3.4× | 3/7 | 56.1ms | 10.9ms | 39.9 MB | 2/7 | 3388889 |
| node | 59.8ms | 4.5× | 4/7 | 78.5ms | 18.7ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 89.4ms | 6.8× | 5/7 | 132.1ms | 42.7ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 33.1ms | 2.5× | 2/7 | 55.1ms | 22.0ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 433.9ms | 12.8× | 6/7 | 459.7ms | 25.8ms | 93.4 MB | 6/7 | 374854840 |
| elixir | 173.0ms | 5.1× | 4/7 | 375.2ms | 202.2ms | 70.6 MB | 5/7 | 374854840 |
| python | 177.7ms | 5.2× | 5/7 | 188.6ms | 10.9ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.9ms | 1.0× | 1/7 | 52.6ms | 18.7ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 72.9ms | 2.2× | 3/7 | 115.6ms | 42.7ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 38.6ms | 1.1× | 2/7 | 60.6ms | 22.0ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 116.1ms | 6.8× | 5/7 | 141.9ms | 25.8ms | 39.4 MB | 4/7 | 1638200 |
| elixir | 33.4ms | 2.0× | 3/7 | 235.6ms | 202.2ms | 70.1 MB | 6/7 | 1638200 |
| python | 112.5ms | 6.6× | 4/7 | 123.4ms | 10.9ms | 10.0 MB | 1/7 | 1638200 |
| node | 25.5ms | 1.5× | 2/7 | 44.2ms | 18.7ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 123.0ms | 7.2× | 6/7 | 165.7ms | 42.7ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 17.1ms | 1.0× | 1/7 | 39.1ms | 22.0ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 210.9ms | 2.8× | 5/7 | 236.7ms | 25.8ms | 132.7 MB | 5/7 | 46468819 |
| elixir | 136.1ms | 1.8× | 4/7 | 338.3ms | 202.2ms | 156.7 MB | 7/7 | 46468819 |
| python | 214.4ms | 2.8× | 6/7 | 225.3ms | 10.9ms | 26.0 MB | 1/7 | 46468819 |
| node | 123.7ms | 1.6× | 3/7 | 142.4ms | 18.7ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 87.0ms | 1.1× | 2/7 | 129.7ms | 42.7ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 76.1ms | 1.0× | 1/7 | 98.1ms | 22.0ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 321.1ms | 21.6× | 6/7 | 346.9ms | 25.8ms | 33.6 MB | 4/7 | 724 |
| elixir | 41.3ms | 2.8× | 3/7 | 243.5ms | 202.2ms | 70.2 MB | 6/7 | 724 |
| python | 64.6ms | 4.3× | 4/7 | 75.5ms | 10.9ms | 9.8 MB | 1/7 | 724 |
| node | 14.9ms | 1.0× | 1/7 | 33.6ms | 18.7ms | 51.2 MB | 5/7 | 724 |
| ruby | 148.6ms | 10.0× | 5/7 | 191.3ms | 42.7ms | 23.8 MB | 2/7 | 724 |
| dotnet | 25.6ms | 1.7× | 2/7 | 47.6ms | 22.0ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 202.1ms | 10.1× | 4/7 | 227.9ms | 25.8ms | 36.2 MB | 4/7 | 9900000 |
| elixir | 20.0ms | 1.0× | 1/7 | 222.2ms | 202.2ms | 69.8 MB | 6/7 | 9900000 |
| python | 50.7ms | 2.5× | 2/7 | 61.6ms | 10.9ms | 9.8 MB | 1/7 | 9900000 |
| node | 590.6ms | 29.5× | 6/7 | 609.3ms | 18.7ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 113.8ms | 5.7× | 3/7 | 156.5ms | 42.7ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 301.6ms | 15.1× | 5/7 | 323.6ms | 22.0ms | 32.5 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 270.1ms | 10.7× | 5/7 | 295.9ms | 25.8ms | 36.6 MB | 4/7 | 2475000 |
| elixir | 25.3ms | 1.0× | 1/7 | 227.5ms | 202.2ms | 70.5 MB | 6/7 | 2475000 |
| python | 256.6ms | 10.1× | 4/7 | 267.5ms | 10.9ms | 9.9 MB | 1/7 | 2475000 |
| node | 248.9ms | 9.8× | 3/7 | 267.6ms | 18.7ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 135.2ms | 5.3× | 2/7 | 177.9ms | 42.7ms | 30.1 MB | 2/7 | 2475000 |
| dotnet | 801.1ms | 31.7× | 6/7 | 823.1ms | 22.0ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.7ms | 8.2× | 6/7 | 68.5ms | 25.8ms | 24.1 MB | 3/7 | 155553889038886 |
| elixir | 19.7ms | 3.8× | 5/7 | 221.9ms | 202.2ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 5.2ms | 1.0× | 1/7 | 16.1ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 11.9ms | 2.3× | 4/7 | 30.6ms | 18.7ms | 52.6 MB | 5/7 | 155553889038886 |
| ruby | 10.8ms | 2.1× | 3/7 | 53.5ms | 42.7ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 10.6ms | 2.0× | 2/7 | 32.6ms | 22.0ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.3ms | 128.3× | 5/7 | 154.1ms | 25.8ms | 73.8 MB | 4/7 | 6100000 |
| elixir | 6.4ms | 6.4× | 2/7 | 208.6ms | 202.2ms | 76.0 MB | 5/7 | 6100000 |
| python | 575.1ms | 575.1× | 6/7 | 586.0ms | 10.9ms | 28.2 MB | 1/7 | 6100000 |
| node | 57.6ms | 57.6× | 4/7 | 76.3ms | 18.7ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.635s | 1635.5× | 7/7 | 1.678s | 42.7ms | 137.0 MB | 7/7 | 6100000 |
| dotnet | 18.8ms | 18.8× | 3/7 | 40.8ms | 22.0ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 404.2ms | 404.2× | 5/7 | 430.0ms | 25.8ms | 29.1 MB | 4/7 | 31781100 |
| elixir | 71.8ms | 71.8× | 3/7 | 274.0ms | 202.2ms | 72.9 MB | 5/7 | 31781100 |
| python | 731.9ms | 731.9× | 7/7 | 742.8ms | 10.9ms | 22.3 MB | 1/7 | 31781100 |
| node | 142.5ms | 142.5× | 4/7 | 161.2ms | 18.7ms | 182.7 MB | 7/7 | 31781100 |
| ruby | 545.0ms | 545.0× | 6/7 | 587.7ms | 42.7ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 38.1ms | 38.1× | 2/7 | 60.1ms | 22.0ms | 28.0 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.1ms | 1.2× | 2/7 | 176.9ms | 25.8ms | 119.3 MB | 5/7 | 500 |
| elixir | 594.2ms | 4.6× | 7/7 | 796.4ms | 202.2ms | 463.4 MB | 7/7 | 500 |
| python | 182.3ms | 1.4× | 4/7 | 193.2ms | 10.9ms | 43.2 MB | 1/7 | 500 |
| node | 128.2ms | 1.0× | 1/7 | 146.9ms | 18.7ms | 65.0 MB | 4/7 | 500 |
| ruby | 215.3ms | 1.7× | 5/7 | 258.0ms | 42.7ms | 50.1 MB | 2/7 | 500 |
| dotnet | 159.4ms | 1.2× | 3/7 | 181.4ms | 22.0ms | 50.9 MB | 3/7 | 500 |
