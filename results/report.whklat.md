# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-28 14:10.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.3ms | 2.6× | 4/7 | 28.3ms | — | 21.8 MB | 3/7 | 0 |
| elixir | 190.5ms | 17.5× | 6/7 | 190.5ms | — | 72.4 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.6ms | 1.7× | 2/7 | 18.6ms | — | 43.2 MB | 5/7 | 0 |
| ruby | 40.8ms | 3.7× | 5/7 | 40.8ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 22.6ms | 2.1× | 3/7 | 22.6ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 242.4ms | 5.7× | 5/7 | 270.7ms | 28.3ms | 26.3 MB | 4/7 | 9227465 |
| elixir | 76.4ms | 1.8× | 2/7 | 266.9ms | 190.5ms | 72.2 MB | 6/7 | 9227465 |
| python | 770.0ms | 18.2× | 7/7 | 780.9ms | 10.9ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.0ms | 1.8× | 3/7 | 96.6ms | 18.6ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 625.6ms | 14.8× | 6/7 | 666.4ms | 40.8ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 42.2ms | 1.0× | 1/7 | 64.8ms | 22.6ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.5ms | 3.0× | 3/7 | 66.8ms | 28.3ms | 25.1 MB | 3/7 | 449999985000000 |
| elixir | 61.5ms | 4.8× | 4/7 | 252.0ms | 190.5ms | 71.6 MB | 6/7 | 449999985000000 |
| python | 2.465s | 191.1× | 7/7 | 2.476s | 10.9ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 31.0ms | 2.4× | 2/7 | 49.6ms | 18.6ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 609.8ms | 47.3× | 6/7 | 650.6ms | 40.8ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.9ms | 1.0× | 1/7 | 35.5ms | 22.6ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.7ms | 1.0× | 1/7 | 31.0ms | 28.3ms | 21.6 MB | 3/7 | 12499997500000 |
| elixir | 31.5ms | 11.7× | 3/7 | 222.0ms | 190.5ms | 72.4 MB | 5/7 | 12499997500000 |
| python | 115.1ms | 42.6× | 4/7 | 126.0ms | 10.9ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 242.4ms | 89.8× | 7/7 | 261.0ms | 18.6ms | 90.5 MB | 6/7 | 12499997500000 |
| ruby | 238.3ms | 88.3× | 6/7 | 279.1ms | 40.8ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 12.5ms | 4.6× | 2/7 | 35.1ms | 22.6ms | 27.4 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.8ms | 3.2× | 4/7 | 62.1ms | 28.3ms | 25.7 MB | 3/7 | 13848 |
| elixir | 18.9ms | 1.8× | 3/7 | 209.4ms | 190.5ms | 73.0 MB | 6/7 | 13848 |
| python | 127.4ms | 12.1× | 6/7 | 138.3ms | 10.9ms | 10.0 MB | 1/7 | 13848 |
| node | 11.6ms | 1.1× | 2/7 | 30.2ms | 18.6ms | 49.1 MB | 5/7 | 13848 |
| ruby | 121.9ms | 11.6× | 5/7 | 162.7ms | 40.8ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 10.5ms | 1.0× | 1/7 | 33.1ms | 22.6ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.0ms | 1.7× | 2/7 | 113.3ms | 28.3ms | 26.0 MB | 3/7 | 442 |
| elixir | 114.9ms | 2.3× | 3/7 | 305.4ms | 190.5ms | 70.1 MB | 6/7 | 442 |
| python | 2.500s | 51.0× | 7/7 | 2.511s | 10.9ms | 9.8 MB | 1/7 | 442 |
| node | 185.2ms | 3.8× | 4/7 | 203.8ms | 18.6ms | 48.7 MB | 5/7 | 442 |
| ruby | 900.4ms | 18.4× | 6/7 | 941.2ms | 40.8ms | 19.3 MB | 2/7 | 442 |
| dotnet | 49.0ms | 1.0× | 1/7 | 71.6ms | 22.6ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 237.5ms | 11.2× | 4/7 | 265.8ms | 28.3ms | 25.3 MB | 3/7 | 6129302 |
| elixir | 261.9ms | 12.4× | 5/7 | 452.4ms | 190.5ms | 72.9 MB | 6/7 | 6129302 |
| python | 1.430s | 67.5× | 7/7 | 1.441s | 10.9ms | 10.1 MB | 1/7 | 6129302 |
| node | 23.4ms | 1.1× | 2/7 | 42.0ms | 18.6ms | 50.4 MB | 5/7 | 6129302 |
| ruby | 443.0ms | 20.9× | 6/7 | 483.8ms | 40.8ms | 19.6 MB | 2/7 | 6129302 |
| dotnet | 21.2ms | 1.0× | 1/7 | 43.8ms | 22.6ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.0ms | 17.2× | 4/7 | 119.3ms | 28.3ms | 44.3 MB | 4/7 | 654353666 |
| elixir | 65.1ms | 12.3× | 3/7 | 255.6ms | 190.5ms | 74.7 MB | 6/7 | 654353666 |
| python | 471.1ms | 88.9× | 7/7 | 482.0ms | 10.9ms | 10.4 MB | 1/7 | 654353666 |
| node | 17.2ms | 3.2× | 2/7 | 35.8ms | 18.6ms | 52.8 MB | 5/7 | 654353666 |
| ruby | 307.3ms | 58.0× | 6/7 | 348.1ms | 40.8ms | 19.6 MB | 2/7 | 654353666 |
| dotnet | 5.3ms | 1.0× | 1/7 | 27.9ms | 22.6ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.2ms | 1.0× | 1/7 | 40.5ms | 28.3ms | 30.1 MB | 1/7 | 3388889 |
| elixir | 129.7ms | 10.6× | 6/7 | 320.2ms | 190.5ms | 202.2 MB | 7/7 | 3388889 |
| python | 46.0ms | 3.8× | 3/7 | 56.9ms | 10.9ms | 39.9 MB | 2/7 | 3388889 |
| node | 67.0ms | 5.5× | 4/7 | 85.6ms | 18.6ms | 95.7 MB | 5/7 | 3388889 |
| ruby | 89.9ms | 7.4× | 5/7 | 130.7ms | 40.8ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 34.1ms | 2.8× | 2/7 | 56.7ms | 22.6ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 410.5ms | 12.7× | 7/7 | 438.8ms | 28.3ms | 96.5 MB | 6/7 | 374854840 |
| elixir | 182.1ms | 5.6× | 4/7 | 372.6ms | 190.5ms | 70.6 MB | 5/7 | 374854840 |
| python | 184.1ms | 5.7× | 5/7 | 195.0ms | 10.9ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.4ms | 1.0× | 1/7 | 51.0ms | 18.6ms | 50.7 MB | 4/7 | 374854840 |
| ruby | 74.0ms | 2.3× | 3/7 | 114.8ms | 40.8ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 42.3ms | 1.3× | 2/7 | 64.9ms | 22.6ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.5ms | 6.2× | 5/7 | 131.8ms | 28.3ms | 40.0 MB | 4/7 | 1638200 |
| elixir | 17.7ms | 1.1× | 2/7 | 208.2ms | 190.5ms | 72.1 MB | 6/7 | 1638200 |
| python | 99.8ms | 6.0× | 4/7 | 110.7ms | 10.9ms | 10.0 MB | 1/7 | 1638200 |
| node | 24.7ms | 1.5× | 3/7 | 43.3ms | 18.6ms | 56.5 MB | 5/7 | 1638200 |
| ruby | 106.3ms | 6.4× | 6/7 | 147.1ms | 40.8ms | 19.7 MB | 2/7 | 1638200 |
| dotnet | 16.7ms | 1.0× | 1/7 | 39.3ms | 22.6ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 177.7ms | 2.6× | 5/7 | 206.0ms | 28.3ms | 135.9 MB | 6/7 | 46468819 |
| elixir | 127.2ms | 1.9× | 4/7 | 317.7ms | 190.5ms | 157.2 MB | 7/7 | 46468819 |
| python | 217.5ms | 3.2× | 6/7 | 228.4ms | 10.9ms | 26.0 MB | 2/7 | 46468819 |
| node | 111.6ms | 1.6× | 3/7 | 130.2ms | 18.6ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 76.8ms | 1.1× | 2/7 | 117.6ms | 40.8ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 68.0ms | 1.0× | 1/7 | 90.6ms | 22.6ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.7ms | 6.7× | 5/7 | 124.0ms | 28.3ms | 35.5 MB | 4/7 | 724 |
| elixir | 14.4ms | 1.0× | 2/7 | 204.9ms | 190.5ms | 73.0 MB | 6/7 | 724 |
| python | 58.6ms | 4.1× | 4/7 | 69.5ms | 10.9ms | 9.9 MB | 1/7 | 724 |
| node | 14.3ms | 1.0× | 1/7 | 32.9ms | 18.6ms | 51.2 MB | 5/7 | 724 |
| ruby | 166.8ms | 11.7× | 6/7 | 207.6ms | 40.8ms | 19.6 MB | 2/7 | 724 |
| dotnet | 28.5ms | 2.0× | 3/7 | 51.1ms | 22.6ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.5ms | 1.9× | 3/7 | 84.8ms | 28.3ms | 22.3 MB | 3/7 | 9900000 |
| elixir | 29.8ms | 1.0× | 1/7 | 220.3ms | 190.5ms | 71.3 MB | 6/7 | 9900000 |
| python | 51.6ms | 1.7× | 2/7 | 62.5ms | 10.9ms | 9.8 MB | 1/7 | 9900000 |
| node | 604.7ms | 20.3× | 6/7 | 623.3ms | 18.6ms | 50.6 MB | 5/7 | 9900000 |
| ruby | 123.4ms | 4.1× | 4/7 | 164.2ms | 40.8ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 296.6ms | 10.0× | 5/7 | 319.2ms | 22.6ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.0ms | 4.2× | 2/7 | 80.3ms | 28.3ms | 25.5 MB | 2/7 | 2475000 |
| elixir | 12.4ms | 1.0× | 1/7 | 202.9ms | 190.5ms | 70.9 MB | 6/7 | 2475000 |
| python | 231.6ms | 18.7× | 5/7 | 242.5ms | 10.9ms | 9.9 MB | 1/7 | 2475000 |
| node | 228.9ms | 18.5× | 4/7 | 247.5ms | 18.6ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 127.4ms | 10.3× | 3/7 | 168.2ms | 40.8ms | 26.1 MB | 3/7 | 2475000 |
| dotnet | 724.2ms | 58.4× | 6/7 | 746.8ms | 22.6ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.2ms | 7.0× | 6/7 | 58.5ms | 28.3ms | 25.6 MB | 3/7 | 155553889038886 |
| elixir | 12.9ms | 3.0× | 5/7 | 203.4ms | 190.5ms | 73.5 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.0× | 1/7 | 15.2ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 8.7ms | 2.0× | 4/7 | 27.3ms | 18.6ms | 52.3 MB | 5/7 | 155553889038886 |
| ruby | 7.3ms | 1.7× | 2/7 | 48.1ms | 40.8ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.6ms | 2.0× | 3/7 | 31.2ms | 22.6ms | 28.0 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 120.2ms | 6.8× | 4/7 | 148.5ms | 28.3ms | 107.5 MB | 5/7 | 6100000 |
| elixir | 21.7ms | 1.2× | 2/7 | 212.2ms | 190.5ms | 76.1 MB | 4/7 | 6100000 |
| python | 575.2ms | 32.5× | 6/7 | 586.1ms | 10.9ms | 28.1 MB | 1/7 | 6100000 |
| node | 56.8ms | 3.2× | 3/7 | 75.4ms | 18.6ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.713s | 96.8× | 7/7 | 1.754s | 40.8ms | 133.2 MB | 6/7 | 6100000 |
| dotnet | 17.7ms | 1.0× | 1/7 | 40.3ms | 22.6ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 414.5ms | 10.5× | 5/7 | 442.8ms | 28.3ms | 31.8 MB | 4/7 | 31781100 |
| elixir | 83.3ms | 2.1× | 2/7 | 273.8ms | 190.5ms | 71.1 MB | 5/7 | 31781100 |
| python | 774.7ms | 19.7× | 7/7 | 785.6ms | 10.9ms | 22.2 MB | 2/7 | 31781100 |
| node | 143.3ms | 3.6× | 3/7 | 161.9ms | 18.6ms | 183.4 MB | 7/7 | 31781100 |
| ruby | 469.7ms | 11.9× | 6/7 | 510.5ms | 40.8ms | 19.3 MB | 1/7 | 31781100 |
| dotnet | 39.4ms | 1.0× | 1/7 | 62.0ms | 22.6ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 156.8ms | 1.2× | 3/7 | 185.1ms | 28.3ms | 121.0 MB | 5/7 | 500 |
| elixir | 642.3ms | 5.1× | 6/7 | 832.8ms | 190.5ms | 485.1 MB | 7/7 | 500 |
| python | 181.4ms | 1.4× | 4/7 | 192.3ms | 10.9ms | 43.9 MB | 1/7 | 500 |
| node | 126.4ms | 1.0× | 1/7 | 145.0ms | 18.6ms | 65.1 MB | 4/7 | 500 |
| ruby | 220.3ms | 1.7× | 5/7 | 261.1ms | 40.8ms | 46.0 MB | 2/7 | 500 |
| dotnet | 152.8ms | 1.2× | 2/7 | 175.4ms | 22.6ms | 48.3 MB | 3/7 | 500 |
