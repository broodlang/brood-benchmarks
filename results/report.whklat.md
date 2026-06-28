# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-28 12:50.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.8ms | 2.6× | 4/7 | 27.8ms | — | 21.6 MB | 3/7 | 0 |
| elixir | 199.7ms | 19.0× | 6/7 | 199.7ms | — | 69.8 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.2ms | 1.7× | 2/7 | 18.2ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 40.1ms | 3.8× | 5/7 | 40.1ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.4ms | 2.0× | 3/7 | 21.4ms | — | 26.0 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 249.7ms | 5.8× | 4/7 | 277.5ms | 27.8ms | 26.2 MB | 4/7 | 9227465 |
| elixir | 73.4ms | 1.7× | 2/7 | 273.1ms | 199.7ms | 70.4 MB | 6/7 | 9227465 |
| python | 780.5ms | 18.2× | 7/7 | 791.0ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.3ms | 1.8× | 3/7 | 96.5ms | 18.2ms | 48.5 MB | 5/7 | 9227465 |
| ruby | 658.7ms | 15.3× | 6/7 | 698.8ms | 40.1ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 43.0ms | 1.0× | 1/7 | 64.4ms | 21.4ms | 26.0 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 58.8ms | 4.5× | 3/7 | 86.6ms | 27.8ms | 25.6 MB | 3/7 | 449999985000000 |
| elixir | 64.7ms | 4.9× | 4/7 | 264.4ms | 199.7ms | 69.8 MB | 6/7 | 449999985000000 |
| python | 2.394s | 181.4× | 7/7 | 2.405s | 10.5ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 37.4ms | 2.8× | 2/7 | 55.6ms | 18.2ms | 50.3 MB | 5/7 | 449999985000000 |
| ruby | 628.5ms | 47.6× | 6/7 | 668.6ms | 40.1ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 13.2ms | 1.0× | 1/7 | 34.6ms | 21.4ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.1ms | 1.0× | 1/7 | 30.9ms | 27.8ms | 21.7 MB | 3/7 | 12499997500000 |
| elixir | 27.3ms | 8.8× | 3/7 | 227.0ms | 199.7ms | 70.0 MB | 5/7 | 12499997500000 |
| python | 114.9ms | 37.1× | 4/7 | 125.4ms | 10.5ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 236.1ms | 76.2× | 6/7 | 254.3ms | 18.2ms | 90.4 MB | 6/7 | 12499997500000 |
| ruby | 234.6ms | 75.7× | 5/7 | 274.7ms | 40.1ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 13.9ms | 4.5× | 2/7 | 35.3ms | 21.4ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.1ms | 3.2× | 4/7 | 60.9ms | 27.8ms | 25.6 MB | 3/7 | 13848 |
| elixir | 15.3ms | 1.5× | 3/7 | 215.0ms | 199.7ms | 70.3 MB | 6/7 | 13848 |
| python | 138.0ms | 13.5× | 6/7 | 148.5ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 10.2ms | 1.0× | 1/7 | 28.4ms | 18.2ms | 49.0 MB | 5/7 | 13848 |
| ruby | 122.2ms | 12.0× | 5/7 | 162.3ms | 40.1ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 10.8ms | 1.1× | 2/7 | 32.2ms | 21.4ms | 26.4 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.5ms | 2.0× | 2/7 | 118.3ms | 27.8ms | 25.8 MB | 3/7 | 442 |
| elixir | 104.6ms | 2.3× | 3/7 | 304.3ms | 199.7ms | 69.9 MB | 6/7 | 442 |
| python | 2.479s | 53.4× | 7/7 | 2.490s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 177.8ms | 3.8× | 4/7 | 196.0ms | 18.2ms | 48.8 MB | 5/7 | 442 |
| ruby | 904.5ms | 19.5× | 6/7 | 944.6ms | 40.1ms | 19.3 MB | 2/7 | 442 |
| dotnet | 46.4ms | 1.0× | 1/7 | 67.8ms | 21.4ms | 26.4 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 230.3ms | 10.4× | 3/7 | 258.1ms | 27.8ms | 25.9 MB | 3/7 | 6129302 |
| elixir | 265.0ms | 12.0× | 4/7 | 464.7ms | 199.7ms | 70.2 MB | 6/7 | 6129302 |
| python | 1.455s | 65.8× | 7/7 | 1.465s | 10.5ms | 10.0 MB | 1/7 | 6129302 |
| node | 22.1ms | 1.0× | 1/7 | 40.3ms | 18.2ms | 49.6 MB | 5/7 | 6129302 |
| ruby | 448.1ms | 20.3× | 6/7 | 488.2ms | 40.1ms | 19.6 MB | 2/7 | 6129302 |
| dotnet | 32.9ms | 1.5× | 2/7 | 54.3ms | 21.4ms | 26.4 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.8ms | 14.3× | 4/7 | 130.6ms | 27.8ms | 43.6 MB | 4/7 | 654353666 |
| elixir | 58.4ms | 8.1× | 3/7 | 258.1ms | 199.7ms | 75.5 MB | 6/7 | 654353666 |
| python | 483.8ms | 67.2× | 6/7 | 494.3ms | 10.5ms | 10.3 MB | 1/7 | 654353666 |
| node | 36.4ms | 5.1× | 2/7 | 54.6ms | 18.2ms | 52.7 MB | 5/7 | 654353666 |
| ruby | 303.3ms | 42.1× | 5/7 | 343.4ms | 40.1ms | 19.6 MB | 2/7 | 654353666 |
| dotnet | 7.2ms | 1.0× | 1/7 | 28.6ms | 21.4ms | 26.9 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 19.0ms | 1.0× | 1/7 | 46.8ms | 27.8ms | 30.2 MB | 1/7 | 3388889 |
| elixir | 116.0ms | 6.1× | 6/7 | 315.7ms | 199.7ms | 199.3 MB | 7/7 | 3388889 |
| python | 44.4ms | 2.3× | 3/7 | 54.9ms | 10.5ms | 39.8 MB | 2/7 | 3388889 |
| node | 60.0ms | 3.2× | 4/7 | 78.2ms | 18.2ms | 95.8 MB | 5/7 | 3388889 |
| ruby | 89.3ms | 4.7× | 5/7 | 129.4ms | 40.1ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.8ms | 1.7× | 2/7 | 53.2ms | 21.4ms | 56.9 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 392.0ms | 11.2× | 6/7 | 419.8ms | 27.8ms | 96.0 MB | 6/7 | 374854840 |
| elixir | 181.6ms | 5.2× | 4/7 | 381.3ms | 199.7ms | 70.9 MB | 5/7 | 374854840 |
| python | 183.1ms | 5.2× | 5/7 | 193.6ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 35.1ms | 1.0× | 1/7 | 53.3ms | 18.2ms | 50.4 MB | 4/7 | 374854840 |
| ruby | 77.8ms | 2.2× | 3/7 | 117.9ms | 40.1ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 39.6ms | 1.1× | 2/7 | 61.0ms | 21.4ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.1ms | 6.8× | 6/7 | 134.9ms | 27.8ms | 40.2 MB | 4/7 | 1638200 |
| elixir | 18.3ms | 1.2× | 2/7 | 218.0ms | 199.7ms | 70.4 MB | 6/7 | 1638200 |
| python | 103.0ms | 6.5× | 4/7 | 113.5ms | 10.5ms | 10.0 MB | 1/7 | 1638200 |
| node | 24.8ms | 1.6× | 3/7 | 43.0ms | 18.2ms | 56.4 MB | 5/7 | 1638200 |
| ruby | 106.5ms | 6.7× | 5/7 | 146.6ms | 40.1ms | 19.7 MB | 2/7 | 1638200 |
| dotnet | 15.8ms | 1.0× | 1/7 | 37.2ms | 21.4ms | 32.5 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.1ms | 2.3× | 5/7 | 198.9ms | 27.8ms | 136.5 MB | 5/7 | 46468819 |
| elixir | 108.0ms | 1.5× | 3/7 | 307.7ms | 199.7ms | 156.8 MB | 7/7 | 46468819 |
| python | 195.6ms | 2.6× | 6/7 | 206.1ms | 10.5ms | 26.0 MB | 2/7 | 46468819 |
| node | 113.2ms | 1.5× | 4/7 | 131.4ms | 18.2ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 74.3ms | 1.0× | 1/7 | 114.4ms | 40.1ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 77.3ms | 1.0× | 2/7 | 98.7ms | 21.4ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.8ms | 9.5× | 5/7 | 122.6ms | 27.8ms | 32.9 MB | 4/7 | 724 |
| elixir | 13.8ms | 1.4× | 2/7 | 213.5ms | 199.7ms | 70.3 MB | 6/7 | 724 |
| python | 56.0ms | 5.6× | 4/7 | 66.5ms | 10.5ms | 9.9 MB | 1/7 | 724 |
| node | 10.0ms | 1.0× | 1/7 | 28.2ms | 18.2ms | 51.0 MB | 5/7 | 724 |
| ruby | 129.8ms | 13.0× | 6/7 | 169.9ms | 40.1ms | 19.6 MB | 2/7 | 724 |
| dotnet | 21.4ms | 2.1× | 3/7 | 42.8ms | 21.4ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 57.6ms | 2.9× | 3/7 | 85.4ms | 27.8ms | 22.3 MB | 3/7 | 9900000 |
| elixir | 19.6ms | 1.0× | 1/7 | 219.3ms | 199.7ms | 69.8 MB | 6/7 | 9900000 |
| python | 50.0ms | 2.6× | 2/7 | 60.5ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 609.3ms | 31.1× | 6/7 | 627.5ms | 18.2ms | 50.6 MB | 5/7 | 9900000 |
| ruby | 122.6ms | 6.3× | 4/7 | 162.7ms | 40.1ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 314.2ms | 16.0× | 5/7 | 335.6ms | 21.4ms | 32.5 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.0ms | 4.7× | 2/7 | 78.8ms | 27.8ms | 25.8 MB | 2/7 | 2475000 |
| elixir | 10.8ms | 1.0× | 1/7 | 210.5ms | 199.7ms | 69.9 MB | 6/7 | 2475000 |
| python | 234.8ms | 21.7× | 5/7 | 245.3ms | 10.5ms | 9.9 MB | 1/7 | 2475000 |
| node | 223.0ms | 20.6× | 4/7 | 241.2ms | 18.2ms | 50.4 MB | 5/7 | 2475000 |
| ruby | 123.9ms | 11.5× | 3/7 | 164.0ms | 40.1ms | 26.1 MB | 3/7 | 2475000 |
| dotnet | 750.8ms | 69.5× | 6/7 | 772.2ms | 21.4ms | 32.7 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 5.7× | 6/7 | 57.8ms | 27.8ms | 25.7 MB | 3/7 | 155553889038886 |
| elixir | 7.3ms | 1.4× | 2/7 | 207.0ms | 199.7ms | 72.5 MB | 6/7 | 155553889038886 |
| python | 5.3ms | 1.0× | 1/7 | 15.8ms | 10.5ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 9.1ms | 1.7× | 3/7 | 27.3ms | 18.2ms | 52.3 MB | 5/7 | 155553889038886 |
| ruby | 9.9ms | 1.9× | 4/7 | 50.0ms | 40.1ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 17.3ms | 3.3× | 5/7 | 38.7ms | 21.4ms | 28.2 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 118.4ms | 118.4× | 5/7 | 146.2ms | 27.8ms | 93.1 MB | 5/7 | 6100000 |
| elixir | 12.2ms | 12.2× | 2/7 | 211.9ms | 199.7ms | 76.2 MB | 4/7 | 6100000 |
| python | 555.1ms | 555.1× | 6/7 | 565.6ms | 10.5ms | 28.0 MB | 1/7 | 6100000 |
| node | 61.4ms | 61.4× | 4/7 | 79.6ms | 18.2ms | 51.8 MB | 3/7 | 6100000 |
| ruby | 1.648s | 1647.6× | 7/7 | 1.688s | 40.1ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 18.9ms | 18.9× | 3/7 | 40.3ms | 21.4ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 420.6ms | 420.6× | 5/7 | 448.4ms | 27.8ms | 31.5 MB | 4/7 | 31781100 |
| elixir | 82.0ms | 82.0× | 3/7 | 281.7ms | 199.7ms | 71.1 MB | 5/7 | 31781100 |
| python | 719.1ms | 719.1× | 7/7 | 729.6ms | 10.5ms | 22.1 MB | 2/7 | 31781100 |
| node | 120.3ms | 120.3× | 4/7 | 138.5ms | 18.2ms | 182.9 MB | 7/7 | 31781100 |
| ruby | 482.8ms | 482.8× | 6/7 | 522.9ms | 40.1ms | 19.3 MB | 1/7 | 31781100 |
| dotnet | 36.8ms | 36.8× | 2/7 | 58.2ms | 21.4ms | 28.0 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.9ms | 1.2× | 3/7 | 178.7ms | 27.8ms | 124.2 MB | 5/7 | 500 |
| elixir | 622.8ms | 4.9× | 7/7 | 822.5ms | 199.7ms | 476.0 MB | 7/7 | 500 |
| python | 180.7ms | 1.4× | 4/7 | 191.2ms | 10.5ms | 43.9 MB | 1/7 | 500 |
| node | 126.2ms | 1.0× | 1/7 | 144.4ms | 18.2ms | 65.3 MB | 4/7 | 500 |
| ruby | 221.2ms | 1.8× | 5/7 | 261.3ms | 40.1ms | 46.1 MB | 2/7 | 500 |
| dotnet | 148.3ms | 1.2× | 2/7 | 169.7ms | 21.4ms | 48.0 MB | 3/7 | 500 |
