# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 19:39.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.7ms | 2.4× | 4/7 | 26.7ms | — | 20.6 MB | 2/7 | 0 |
| elixir | 202.0ms | 18.4× | 6/7 | 202.0ms | — | 69.7 MB | 6/7 | 0 |
| python | 11.0ms | 1.0× | 1/7 | 11.0ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.6ms | 1.7× | 2/7 | 18.6ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 43.6ms | 4.0× | 5/7 | 43.6ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.7ms | 2.1× | 3/7 | 22.7ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 278.7ms | 6.7× | 4/7 | 305.4ms | 26.7ms | 24.0 MB | 3/7 | 9227465 |
| elixir | 76.3ms | 1.8× | 2/7 | 278.3ms | 202.0ms | 69.7 MB | 6/7 | 9227465 |
| python | 772.7ms | 18.5× | 7/7 | 783.7ms | 11.0ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.9ms | 1.9× | 3/7 | 97.5ms | 18.6ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 642.2ms | 15.4× | 6/7 | 685.8ms | 43.6ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 41.8ms | 1.0× | 1/7 | 64.5ms | 22.7ms | 26.0 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 60.1ms | 4.6× | 3/7 | 86.8ms | 26.7ms | 23.9 MB | 3/7 | 449999985000000 |
| elixir | 66.1ms | 5.1× | 4/7 | 268.1ms | 202.0ms | 69.7 MB | 6/7 | 449999985000000 |
| python | 2.463s | 189.5× | 7/7 | 2.474s | 11.0ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 33.6ms | 2.6× | 2/7 | 52.2ms | 18.6ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 619.2ms | 47.6× | 6/7 | 662.8ms | 43.6ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 13.0ms | 1.0× | 1/7 | 35.7ms | 22.7ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.5ms | 8.8× | 3/7 | 136.2ms | 26.7ms | 20.6 MB | 2/7 | 12499997500000 |
| elixir | 32.2ms | 2.6× | 2/7 | 234.2ms | 202.0ms | 69.7 MB | 5/7 | 12499997500000 |
| python | 112.7ms | 9.0× | 4/7 | 123.7ms | 11.0ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 237.3ms | 19.0× | 5/7 | 255.9ms | 18.6ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 244.0ms | 19.5× | 6/7 | 287.6ms | 43.6ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 12.5ms | 1.0× | 1/7 | 35.2ms | 22.7ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.5ms | 4.7× | 4/7 | 68.2ms | 26.7ms | 24.1 MB | 3/7 | 13848 |
| elixir | 20.1ms | 2.3× | 3/7 | 222.1ms | 202.0ms | 69.8 MB | 6/7 | 13848 |
| python | 130.8ms | 14.9× | 6/7 | 141.8ms | 11.0ms | 9.9 MB | 1/7 | 13848 |
| node | 11.2ms | 1.3× | 2/7 | 29.8ms | 18.6ms | 49.1 MB | 5/7 | 13848 |
| ruby | 122.6ms | 13.9× | 5/7 | 166.2ms | 43.6ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 8.8ms | 1.0× | 1/7 | 31.5ms | 22.7ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 359.2ms | 7.6× | 4/7 | 385.9ms | 26.7ms | 38.3 MB | 4/7 | 442 |
| elixir | 111.1ms | 2.4× | 2/7 | 313.1ms | 202.0ms | 69.8 MB | 6/7 | 442 |
| python | 2.530s | 53.6× | 7/7 | 2.542s | 11.0ms | 9.8 MB | 1/7 | 442 |
| node | 186.4ms | 3.9× | 3/7 | 205.0ms | 18.6ms | 48.9 MB | 5/7 | 442 |
| ruby | 907.0ms | 19.2× | 6/7 | 950.6ms | 43.6ms | 23.5 MB | 2/7 | 442 |
| dotnet | 47.2ms | 1.0× | 1/7 | 69.9ms | 22.7ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.1ms | 11.4× | 3/7 | 250.8ms | 26.7ms | 24.0 MB | 3/7 | 6129302 |
| elixir | 264.9ms | 13.4× | 4/7 | 466.9ms | 202.0ms | 70.0 MB | 6/7 | 6129302 |
| python | 1.413s | 71.7× | 7/7 | 1.423s | 11.0ms | 10.1 MB | 1/7 | 6129302 |
| node | 22.4ms | 1.1× | 2/7 | 41.0ms | 18.6ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 441.9ms | 22.4× | 5/7 | 485.5ms | 43.6ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 19.7ms | 1.0× | 1/7 | 42.4ms | 22.7ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.5ms | 21.4× | 4/7 | 123.2ms | 26.7ms | 36.8 MB | 4/7 | 654353666 |
| elixir | 65.6ms | 14.6× | 3/7 | 267.6ms | 202.0ms | 75.3 MB | 6/7 | 654353666 |
| python | 471.0ms | 104.7× | 6/7 | 482.0ms | 11.0ms | 10.3 MB | 1/7 | 654353666 |
| node | 25.9ms | 5.8× | 2/7 | 44.5ms | 18.6ms | 52.8 MB | 5/7 | 654353666 |
| ruby | 302.0ms | 67.1× | 5/7 | 345.6ms | 43.6ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 27.2ms | 22.7ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.1ms | 1.0× | 1/7 | 38.8ms | 26.7ms | 30.4 MB | 1/7 | 3388889 |
| elixir | 116.9ms | 9.7× | 6/7 | 318.9ms | 202.0ms | 199.2 MB | 7/7 | 3388889 |
| python | 45.1ms | 3.7× | 3/7 | 56.1ms | 11.0ms | 39.9 MB | 2/7 | 3388889 |
| node | 60.7ms | 5.0× | 4/7 | 79.3ms | 18.6ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 88.1ms | 7.3× | 5/7 | 131.7ms | 43.6ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 31.9ms | 2.6× | 2/7 | 54.6ms | 22.7ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 433.4ms | 12.3× | 6/7 | 460.1ms | 26.7ms | 93.7 MB | 6/7 | 374854840 |
| elixir | 186.5ms | 5.3× | 4/7 | 388.5ms | 202.0ms | 70.5 MB | 5/7 | 374854840 |
| python | 188.9ms | 5.4× | 5/7 | 199.9ms | 11.0ms | 9.9 MB | 1/7 | 374854840 |
| node | 35.2ms | 1.0× | 1/7 | 53.8ms | 18.6ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 74.1ms | 2.1× | 3/7 | 117.7ms | 43.6ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 37.7ms | 1.1× | 2/7 | 60.4ms | 22.7ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.5ms | 10.7× | 5/7 | 130.2ms | 26.7ms | 38.4 MB | 4/7 | 1638200 |
| elixir | 9.7ms | 1.0× | 1/7 | 211.7ms | 202.0ms | 70.2 MB | 6/7 | 1638200 |
| python | 99.5ms | 10.3× | 4/7 | 110.5ms | 11.0ms | 10.0 MB | 1/7 | 1638200 |
| node | 24.9ms | 2.6× | 3/7 | 43.5ms | 18.6ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 105.1ms | 10.8× | 6/7 | 148.7ms | 43.6ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 14.6ms | 1.5× | 2/7 | 37.3ms | 22.7ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 178.6ms | 2.2× | 5/7 | 205.3ms | 26.7ms | 132.8 MB | 5/7 | 46468819 |
| elixir | 173.5ms | 2.1× | 4/7 | 375.5ms | 202.0ms | 156.7 MB | 7/7 | 46468819 |
| python | 236.0ms | 2.9× | 6/7 | 247.0ms | 11.0ms | 26.0 MB | 1/7 | 46468819 |
| node | 135.0ms | 1.6× | 3/7 | 153.6ms | 18.6ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 96.5ms | 1.2× | 2/7 | 140.1ms | 43.6ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 82.2ms | 1.0× | 1/7 | 104.9ms | 22.7ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 166.4ms | 12.9× | 6/7 | 193.1ms | 26.7ms | 34.3 MB | 4/7 | 724 |
| elixir | 34.2ms | 2.7× | 3/7 | 236.2ms | 202.0ms | 69.7 MB | 6/7 | 724 |
| python | 62.2ms | 4.8× | 4/7 | 73.2ms | 11.0ms | 9.8 MB | 1/7 | 724 |
| node | 12.9ms | 1.0× | 1/7 | 31.5ms | 18.6ms | 51.2 MB | 5/7 | 724 |
| ruby | 146.4ms | 11.3× | 5/7 | 190.0ms | 43.6ms | 23.8 MB | 2/7 | 724 |
| dotnet | 22.4ms | 1.7× | 2/7 | 45.1ms | 22.7ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.7ms | 5.7× | 4/7 | 251.4ms | 26.7ms | 36.1 MB | 4/7 | 9900000 |
| elixir | 39.6ms | 1.0× | 1/7 | 241.6ms | 202.0ms | 70.2 MB | 6/7 | 9900000 |
| python | 55.8ms | 1.4× | 2/7 | 66.8ms | 11.0ms | 9.8 MB | 1/7 | 9900000 |
| node | 689.3ms | 17.4× | 6/7 | 707.9ms | 18.6ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 129.5ms | 3.3× | 3/7 | 173.1ms | 43.6ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 328.9ms | 8.3× | 5/7 | 351.6ms | 22.7ms | 32.5 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 302.5ms | 14.3× | 5/7 | 329.2ms | 26.7ms | 36.6 MB | 4/7 | 2475000 |
| elixir | 21.1ms | 1.0× | 1/7 | 223.1ms | 202.0ms | 69.8 MB | 6/7 | 2475000 |
| python | 247.8ms | 11.7× | 4/7 | 258.8ms | 11.0ms | 9.9 MB | 1/7 | 2475000 |
| node | 240.7ms | 11.4× | 3/7 | 259.3ms | 18.6ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 129.4ms | 6.1× | 2/7 | 173.0ms | 43.6ms | 30.1 MB | 2/7 | 2475000 |
| dotnet | 784.2ms | 37.2× | 6/7 | 806.9ms | 22.7ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.7ms | 8.3× | 6/7 | 68.4ms | 26.7ms | 24.2 MB | 3/7 | 155553889038886 |
| elixir | 19.9ms | 4.0× | 5/7 | 221.9ms | 202.0ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 5.0ms | 1.0× | 1/7 | 16.0ms | 11.0ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 11.1ms | 2.2× | 4/7 | 29.7ms | 18.6ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 9.9ms | 2.0× | 3/7 | 53.5ms | 43.6ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 8.7ms | 1.7× | 2/7 | 31.4ms | 22.7ms | 28.0 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 122.2ms | 122.2× | 5/7 | 148.9ms | 26.7ms | 90.2 MB | 5/7 | 6100000 |
| elixir | 12.5ms | 12.5× | 2/7 | 214.5ms | 202.0ms | 76.9 MB | 4/7 | 6100000 |
| python | 600.3ms | 600.3× | 6/7 | 611.3ms | 11.0ms | 28.1 MB | 1/7 | 6100000 |
| node | 60.0ms | 60.0× | 4/7 | 78.6ms | 18.6ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.661s | 1660.5× | 7/7 | 1.704s | 43.6ms | 137.5 MB | 7/7 | 6100000 |
| dotnet | 19.2ms | 19.2× | 3/7 | 41.9ms | 22.7ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 378.4ms | 378.4× | 5/7 | 405.1ms | 26.7ms | 29.7 MB | 4/7 | 31781100 |
| elixir | 99.3ms | 99.3× | 3/7 | 301.3ms | 202.0ms | 73.0 MB | 5/7 | 31781100 |
| python | 715.6ms | 715.6× | 7/7 | 726.6ms | 11.0ms | 22.2 MB | 1/7 | 31781100 |
| node | 128.6ms | 128.6× | 4/7 | 147.2ms | 18.6ms | 182.9 MB | 7/7 | 31781100 |
| ruby | 503.3ms | 503.3× | 6/7 | 546.9ms | 43.6ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 35.4ms | 35.4× | 2/7 | 58.1ms | 22.7ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.6ms | 1.1× | 2/7 | 172.3ms | 26.7ms | 117.2 MB | 5/7 | 500 |
| elixir | 560.9ms | 4.4× | 7/7 | 762.9ms | 202.0ms | 469.0 MB | 7/7 | 500 |
| python | 178.0ms | 1.4× | 4/7 | 189.0ms | 11.0ms | 44.0 MB | 1/7 | 500 |
| node | 128.7ms | 1.0× | 1/7 | 147.3ms | 18.6ms | 65.5 MB | 4/7 | 500 |
| ruby | 215.3ms | 1.7× | 5/7 | 258.9ms | 43.6ms | 49.9 MB | 2/7 | 500 |
| dotnet | 157.1ms | 1.2× | 3/7 | 179.8ms | 22.7ms | 50.7 MB | 3/7 | 500 |
