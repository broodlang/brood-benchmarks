# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-28 19:51.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.7ms | 2.9× | 4/7 | 32.7ms | — | 23.7 MB | 3/7 | 0 |
| elixir | 195.9ms | 17.2× | 6/7 | 195.9ms | — | 70.1 MB | 6/7 | 0 |
| python | 11.4ms | 1.0× | 1/7 | 11.4ms | — | 9.8 MB | 1/7 | 0 |
| node | 19.1ms | 1.7× | 2/7 | 19.1ms | — | 42.8 MB | 5/7 | 0 |
| ruby | 44.3ms | 3.9× | 5/7 | 44.3ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 23.6ms | 2.1× | 3/7 | 23.6ms | — | 25.6 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 244.0ms | 5.8× | 5/7 | 276.7ms | 32.7ms | 27.8 MB | 4/7 | 9227465 |
| elixir | 91.9ms | 2.2× | 2/7 | 287.8ms | 195.9ms | 71.5 MB | 6/7 | 9227465 |
| python | 795.1ms | 18.8× | 7/7 | 806.5ms | 11.4ms | 9.8 MB | 1/7 | 9227465 |
| node | 93.3ms | 2.2× | 3/7 | 112.4ms | 19.1ms | 48.2 MB | 5/7 | 9227465 |
| ruby | 655.1ms | 15.5× | 6/7 | 699.4ms | 44.3ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 42.3ms | 1.0× | 1/7 | 65.9ms | 23.6ms | 25.7 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.7ms | 3.1× | 3/7 | 71.4ms | 32.7ms | 27.0 MB | 4/7 | 449999985000000 |
| elixir | 57.9ms | 4.6× | 4/7 | 253.8ms | 195.9ms | 72.1 MB | 6/7 | 449999985000000 |
| python | 2.417s | 191.8× | 7/7 | 2.428s | 11.4ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 32.5ms | 2.6× | 2/7 | 51.6ms | 19.1ms | 50.2 MB | 5/7 | 449999985000000 |
| ruby | 611.7ms | 48.5× | 6/7 | 656.0ms | 44.3ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.6ms | 1.0× | 1/7 | 36.2ms | 23.6ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 36.0ms | 32.7ms | 23.7 MB | 3/7 | 12499997500000 |
| elixir | 24.6ms | 7.5× | 3/7 | 220.5ms | 195.9ms | 69.9 MB | 5/7 | 12499997500000 |
| python | 131.0ms | 39.7× | 4/7 | 142.4ms | 11.4ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 244.5ms | 74.1× | 6/7 | 263.6ms | 19.1ms | 90.4 MB | 6/7 | 12499997500000 |
| ruby | 254.3ms | 77.1× | 7/7 | 298.6ms | 44.3ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 13.5ms | 4.1× | 2/7 | 37.1ms | 23.6ms | 27.4 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.0ms | 4.1× | 4/7 | 68.7ms | 32.7ms | 27.1 MB | 4/7 | 13848 |
| elixir | 22.8ms | 2.6× | 3/7 | 218.7ms | 195.9ms | 70.6 MB | 6/7 | 13848 |
| python | 131.5ms | 15.1× | 6/7 | 142.9ms | 11.4ms | 10.0 MB | 1/7 | 13848 |
| node | 10.0ms | 1.1× | 2/7 | 29.1ms | 19.1ms | 48.7 MB | 5/7 | 13848 |
| ruby | 122.9ms | 14.1× | 5/7 | 167.2ms | 44.3ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.7ms | 1.0× | 1/7 | 32.3ms | 23.6ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.0ms | 1.6× | 2/7 | 112.7ms | 32.7ms | 27.2 MB | 4/7 | 442 |
| elixir | 109.8ms | 2.3× | 3/7 | 305.7ms | 195.9ms | 71.9 MB | 6/7 | 442 |
| python | 2.703s | 55.5× | 7/7 | 2.715s | 11.4ms | 9.8 MB | 1/7 | 442 |
| node | 189.0ms | 3.9× | 4/7 | 208.1ms | 19.1ms | 48.4 MB | 5/7 | 442 |
| ruby | 938.2ms | 19.3× | 6/7 | 982.5ms | 44.3ms | 19.3 MB | 2/7 | 442 |
| dotnet | 48.7ms | 1.0× | 1/7 | 72.3ms | 23.6ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 234.6ms | 12.0× | 4/7 | 267.3ms | 32.7ms | 27.4 MB | 4/7 | 6129302 |
| elixir | 291.6ms | 15.0× | 5/7 | 487.5ms | 195.9ms | 73.1 MB | 6/7 | 6129302 |
| python | 1.627s | 83.4× | 7/7 | 1.639s | 11.4ms | 10.0 MB | 1/7 | 6129302 |
| node | 22.5ms | 1.2× | 2/7 | 41.6ms | 19.1ms | 50.0 MB | 5/7 | 6129302 |
| ruby | 474.7ms | 24.3× | 6/7 | 519.0ms | 44.3ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 19.5ms | 1.0× | 1/7 | 43.1ms | 23.6ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 100.0ms | 22.2× | 4/7 | 132.7ms | 32.7ms | 44.3 MB | 4/7 | 654353666 |
| elixir | 57.0ms | 12.7× | 3/7 | 252.9ms | 195.9ms | 77.3 MB | 6/7 | 654353666 |
| python | 533.4ms | 118.5× | 7/7 | 544.8ms | 11.4ms | 10.4 MB | 1/7 | 654353666 |
| node | 18.1ms | 4.0× | 2/7 | 37.2ms | 19.1ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 327.4ms | 72.8× | 6/7 | 371.7ms | 44.3ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 28.1ms | 23.6ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.9ms | 1.0× | 1/7 | 43.6ms | 32.7ms | 29.8 MB | 1/7 | 3388889 |
| elixir | 124.1ms | 11.4× | 6/7 | 320.0ms | 195.9ms | 202.1 MB | 7/7 | 3388889 |
| python | 44.8ms | 4.1× | 3/7 | 56.2ms | 11.4ms | 39.9 MB | 2/7 | 3388889 |
| node | 68.8ms | 6.3× | 4/7 | 87.9ms | 19.1ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 88.3ms | 8.1× | 5/7 | 132.6ms | 44.3ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 32.6ms | 3.0× | 2/7 | 56.2ms | 23.6ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 117.5ms | 3.7× | 4/7 | 150.2ms | 32.7ms | 28.3 MB | 4/7 | 374854840 |
| elixir | 167.0ms | 5.2× | 5/7 | 362.9ms | 195.9ms | 70.5 MB | 6/7 | 374854840 |
| python | 211.4ms | 6.6× | 6/7 | 222.8ms | 11.4ms | 9.9 MB | 1/7 | 374854840 |
| node | 31.9ms | 1.0× | 1/7 | 51.0ms | 19.1ms | 50.2 MB | 5/7 | 374854840 |
| ruby | 72.8ms | 2.3× | 3/7 | 117.1ms | 44.3ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 38.8ms | 1.2× | 2/7 | 62.4ms | 23.6ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.4ms | 16.8× | 5/7 | 142.1ms | 32.7ms | 42.0 MB | 4/7 | 1638200 |
| elixir | 6.5ms | 1.0× | 1/7 | 202.4ms | 195.9ms | 71.2 MB | 6/7 | 1638200 |
| python | 101.3ms | 15.6× | 4/7 | 112.7ms | 11.4ms | 10.0 MB | 1/7 | 1638200 |
| node | 22.5ms | 3.5× | 3/7 | 41.6ms | 19.1ms | 56.1 MB | 5/7 | 1638200 |
| ruby | 119.1ms | 18.3× | 6/7 | 163.4ms | 44.3ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 14.5ms | 2.2× | 2/7 | 38.1ms | 23.6ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 187.1ms | 2.7× | 5/7 | 219.8ms | 32.7ms | 145.1 MB | 6/7 | 46468819 |
| elixir | 126.4ms | 1.8× | 4/7 | 322.3ms | 195.9ms | 157.1 MB | 7/7 | 46468819 |
| python | 210.5ms | 3.0× | 6/7 | 221.9ms | 11.4ms | 26.0 MB | 2/7 | 46468819 |
| node | 112.3ms | 1.6× | 3/7 | 131.4ms | 19.1ms | 65.0 MB | 4/7 | 46468819 |
| ruby | 74.5ms | 1.1× | 2/7 | 118.8ms | 44.3ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 70.3ms | 1.0× | 1/7 | 93.9ms | 23.6ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.2ms | 14.2× | 5/7 | 137.9ms | 32.7ms | 40.7 MB | 4/7 | 724 |
| elixir | 7.4ms | 1.0× | 1/7 | 203.3ms | 195.9ms | 72.5 MB | 6/7 | 724 |
| python | 57.1ms | 7.7× | 4/7 | 68.5ms | 11.4ms | 9.8 MB | 1/7 | 724 |
| node | 7.9ms | 1.1× | 2/7 | 27.0ms | 19.1ms | 50.6 MB | 5/7 | 724 |
| ruby | 133.0ms | 18.0× | 6/7 | 177.3ms | 44.3ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.1ms | 2.7× | 3/7 | 43.7ms | 23.6ms | 29.1 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.9ms | 2.3× | 2/7 | 73.6ms | 32.7ms | 24.2 MB | 3/7 | 9900000 |
| elixir | 17.7ms | 1.0× | 1/7 | 213.6ms | 195.9ms | 71.4 MB | 6/7 | 9900000 |
| python | 50.6ms | 2.9× | 3/7 | 62.0ms | 11.4ms | 9.8 MB | 1/7 | 9900000 |
| node | 606.5ms | 34.3× | 6/7 | 625.6ms | 19.1ms | 50.4 MB | 5/7 | 9900000 |
| ruby | 113.5ms | 6.4× | 4/7 | 157.8ms | 44.3ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 305.3ms | 17.2× | 5/7 | 328.9ms | 23.6ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.9ms | 53.9× | 2/7 | 86.6ms | 32.7ms | 27.2 MB | 3/7 | 2475000 |
| elixir | 0.2ms | < 1× | 1/7 | 196.1ms | 195.9ms | 72.8 MB | 6/7 | 2475000 |
| python | 238.9ms | 238.9× | 5/7 | 250.3ms | 11.4ms | 9.8 MB | 1/7 | 2475000 |
| node | 228.0ms | 228.0× | 4/7 | 247.1ms | 19.1ms | 50.2 MB | 5/7 | 2475000 |
| ruby | 122.7ms | 122.7× | 3/7 | 167.0ms | 44.3ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 782.4ms | 782.4× | 6/7 | 806.0ms | 23.6ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.7ms | 8.5× | 6/7 | 67.4ms | 32.7ms | 27.2 MB | 3/7 | 155553889038886 |
| elixir | 8.0ms | 2.0× | 3/7 | 203.9ms | 195.9ms | 70.8 MB | 6/7 | 155553889038886 |
| python | 4.1ms | 1.0× | 1/7 | 15.5ms | 11.4ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 9.0ms | 2.2× | 5/7 | 28.1ms | 19.1ms | 52.1 MB | 5/7 | 155553889038886 |
| ruby | 8.1ms | 2.0× | 4/7 | 52.4ms | 44.3ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.8ms | 1.9× | 2/7 | 31.4ms | 23.6ms | 27.9 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 143.5ms | 9.4× | 4/7 | 176.2ms | 32.7ms | 102.8 MB | 5/7 | 6100000 |
| elixir | 15.3ms | 1.0× | 1/7 | 211.2ms | 195.9ms | 76.9 MB | 4/7 | 6100000 |
| python | 591.0ms | 38.6× | 6/7 | 602.4ms | 11.4ms | 28.0 MB | 1/7 | 6100000 |
| node | 57.2ms | 3.7× | 3/7 | 76.3ms | 19.1ms | 51.6 MB | 3/7 | 6100000 |
| ruby | 1.680s | 109.8× | 7/7 | 1.724s | 44.3ms | 132.9 MB | 6/7 | 6100000 |
| dotnet | 18.4ms | 1.2× | 2/7 | 42.0ms | 23.6ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 452.4ms | 13.0× | 5/7 | 485.1ms | 32.7ms | 32.2 MB | 4/7 | 31781100 |
| elixir | 77.5ms | 2.2× | 2/7 | 273.4ms | 195.9ms | 71.0 MB | 5/7 | 31781100 |
| python | 774.5ms | 22.3× | 7/7 | 785.9ms | 11.4ms | 22.3 MB | 2/7 | 31781100 |
| node | 122.5ms | 3.5× | 3/7 | 141.6ms | 19.1ms | 181.9 MB | 7/7 | 31781100 |
| ruby | 502.3ms | 14.4× | 6/7 | 546.6ms | 44.3ms | 19.3 MB | 1/7 | 31781100 |
| dotnet | 34.8ms | 1.0× | 1/7 | 58.4ms | 23.6ms | 27.9 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.0ms | 1.2× | 2/7 | 183.7ms | 32.7ms | 127.2 MB | 5/7 | 500 |
| elixir | 612.6ms | 4.7× | 6/7 | 808.5ms | 195.9ms | 487.5 MB | 7/7 | 500 |
| python | 181.9ms | 1.4× | 4/7 | 193.3ms | 11.4ms | 44.2 MB | 1/7 | 500 |
| node | 129.1ms | 1.0× | 1/7 | 148.2ms | 19.1ms | 64.9 MB | 4/7 | 500 |
| ruby | 215.6ms | 1.7× | 5/7 | 259.9ms | 44.3ms | 45.8 MB | 2/7 | 500 |
| dotnet | 157.1ms | 1.2× | 3/7 | 180.7ms | 23.6ms | 50.0 MB | 3/7 | 500 |
