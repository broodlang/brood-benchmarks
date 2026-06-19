# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 16:42.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.2ms | 1.9× | 4/7 | 29.2ms | — | 20.6 MB | 2/7 | 0 |
| elixir | 229.7ms | 14.9× | 6/7 | 229.7ms | — | 70.0 MB | 6/7 | 0 |
| python | 15.4ms | 1.0× | 1/7 | 15.4ms | — | 9.8 MB | 1/7 | 0 |
| node | 19.3ms | 1.3× | 2/7 | 19.3ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 45.0ms | 2.9× | 5/7 | 45.0ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 23.8ms | 1.5× | 3/7 | 23.8ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 355.6ms | 8.4× | 4/7 | 384.8ms | 29.2ms | 24.1 MB | 3/7 | 9227465 |
| elixir | 70.6ms | 1.7× | 2/7 | 300.3ms | 229.7ms | 70.0 MB | 6/7 | 9227465 |
| python | 857.7ms | 20.2× | 7/7 | 873.1ms | 15.4ms | 9.8 MB | 1/7 | 9227465 |
| node | 80.0ms | 1.9× | 3/7 | 99.3ms | 19.3ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 659.7ms | 15.5× | 5/7 | 704.7ms | 45.0ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 42.5ms | 1.0× | 1/7 | 66.3ms | 23.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 58.6ms | 5.0× | 4/7 | 87.8ms | 29.2ms | 24.0 MB | 3/7 | 449999985000000 |
| elixir | 41.5ms | 3.5× | 3/7 | 271.2ms | 229.7ms | 69.6 MB | 6/7 | 449999985000000 |
| python | 2.555s | 218.4× | 7/7 | 2.570s | 15.4ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 36.3ms | 3.1× | 2/7 | 55.6ms | 19.3ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 622.6ms | 53.2× | 6/7 | 667.6ms | 45.0ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 11.7ms | 1.0× | 1/7 | 35.5ms | 23.8ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.4ms | 24.4× | 4/7 | 136.6ms | 29.2ms | 20.5 MB | 2/7 | 12499997500000 |
| elixir | 4.4ms | 1.0× | 1/7 | 234.1ms | 229.7ms | 69.9 MB | 5/7 | 12499997500000 |
| python | 107.0ms | 24.3× | 3/7 | 122.4ms | 15.4ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 239.5ms | 54.4× | 5/7 | 258.8ms | 19.3ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 244.4ms | 55.5× | 6/7 | 289.4ms | 45.0ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 11.8ms | 2.7× | 2/7 | 35.6ms | 23.8ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.2ms | 38.2× | 4/7 | 67.4ms | 29.2ms | 24.1 MB | 3/7 | 13848 |
| elixir | 0.0ms | < 1× | 1/7 | 225.2ms | 229.7ms | 69.8 MB | 6/7 | 13848 |
| python | 124.0ms | 124.0× | 6/7 | 139.4ms | 15.4ms | 9.9 MB | 1/7 | 13848 |
| node | 12.0ms | 12.0× | 3/7 | 31.3ms | 19.3ms | 49.1 MB | 5/7 | 13848 |
| ruby | 120.5ms | 120.5× | 5/7 | 165.5ms | 45.0ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 8.5ms | 8.5× | 2/7 | 32.3ms | 23.8ms | 26.2 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 391.1ms | 8.5× | 4/7 | 420.3ms | 29.2ms | 38.0 MB | 4/7 | 442 |
| elixir | 81.6ms | 1.8× | 2/7 | 311.3ms | 229.7ms | 69.7 MB | 6/7 | 442 |
| python | 2.498s | 54.4× | 7/7 | 2.514s | 15.4ms | 9.8 MB | 1/7 | 442 |
| node | 184.7ms | 4.0× | 3/7 | 204.0ms | 19.3ms | 48.9 MB | 5/7 | 442 |
| ruby | 896.7ms | 19.5× | 6/7 | 941.7ms | 45.0ms | 23.5 MB | 2/7 | 442 |
| dotnet | 45.9ms | 1.0× | 1/7 | 69.7ms | 23.8ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 226.8ms | 11.6× | 3/7 | 256.0ms | 29.2ms | 24.1 MB | 3/7 | 6129302 |
| elixir | 245.5ms | 12.6× | 4/7 | 475.2ms | 229.7ms | 70.0 MB | 6/7 | 6129302 |
| python | 1.467s | 75.3× | 7/7 | 1.483s | 15.4ms | 10.1 MB | 1/7 | 6129302 |
| node | 22.3ms | 1.1× | 2/7 | 41.6ms | 19.3ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 441.0ms | 22.6× | 5/7 | 486.0ms | 45.0ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 19.5ms | 1.0× | 1/7 | 43.3ms | 23.8ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.0ms | 22.2× | 4/7 | 131.2ms | 29.2ms | 36.9 MB | 4/7 | 654353666 |
| elixir | 36.2ms | 7.9× | 3/7 | 265.9ms | 229.7ms | 75.3 MB | 6/7 | 654353666 |
| python | 454.3ms | 98.8× | 6/7 | 469.7ms | 15.4ms | 10.4 MB | 1/7 | 654353666 |
| node | 23.6ms | 5.1× | 2/7 | 42.9ms | 19.3ms | 52.7 MB | 5/7 | 654353666 |
| ruby | 304.0ms | 66.1× | 5/7 | 349.0ms | 45.0ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.6ms | 1.0× | 1/7 | 28.4ms | 23.8ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.7ms | 1.0× | 1/7 | 39.9ms | 29.2ms | 30.4 MB | 1/7 | 3388889 |
| elixir | 99.7ms | 9.3× | 6/7 | 329.4ms | 229.7ms | 199.2 MB | 7/7 | 3388889 |
| python | 40.4ms | 3.8× | 3/7 | 55.8ms | 15.4ms | 39.9 MB | 2/7 | 3388889 |
| node | 60.8ms | 5.7× | 4/7 | 80.1ms | 19.3ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 88.0ms | 8.2× | 5/7 | 133.0ms | 45.0ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 32.5ms | 3.0× | 2/7 | 56.3ms | 23.8ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 431.1ms | 13.0× | 6/7 | 460.3ms | 29.2ms | 93.7 MB | 6/7 | 374854840 |
| elixir | 154.1ms | 4.6× | 4/7 | 383.8ms | 229.7ms | 70.5 MB | 5/7 | 374854840 |
| python | 176.4ms | 5.3× | 5/7 | 191.8ms | 15.4ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.2ms | 1.0× | 1/7 | 52.5ms | 19.3ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 73.9ms | 2.2× | 3/7 | 118.9ms | 45.0ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 39.3ms | 1.2× | 2/7 | 63.1ms | 23.8ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 230.4ms | 20.0× | 6/7 | 259.6ms | 29.2ms | 38.7 MB | 4/7 | 1638200 |
| elixir | 11.5ms | 1.0× | 1/7 | 241.2ms | 229.7ms | 70.8 MB | 6/7 | 1638200 |
| python | 114.4ms | 9.9× | 4/7 | 129.8ms | 15.4ms | 10.0 MB | 1/7 | 1638200 |
| node | 28.4ms | 2.5× | 3/7 | 47.7ms | 19.3ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 119.2ms | 10.4× | 5/7 | 164.2ms | 45.0ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 17.5ms | 1.5× | 2/7 | 41.3ms | 23.8ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 209.2ms | 2.7× | 5/7 | 238.4ms | 29.2ms | 132.9 MB | 5/7 | 46468819 |
| elixir | 128.4ms | 1.7× | 4/7 | 358.1ms | 229.7ms | 157.2 MB | 7/7 | 46468819 |
| python | 224.9ms | 2.9× | 6/7 | 240.3ms | 15.4ms | 26.0 MB | 1/7 | 46468819 |
| node | 126.4ms | 1.6× | 3/7 | 145.7ms | 19.3ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 87.3ms | 1.1× | 2/7 | 132.3ms | 45.0ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 76.8ms | 1.0× | 1/7 | 100.6ms | 23.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 320.4ms | 86.6× | 6/7 | 349.6ms | 29.2ms | 33.7 MB | 4/7 | 724 |
| elixir | 3.7ms | 1.0× | 1/7 | 233.4ms | 229.7ms | 69.7 MB | 6/7 | 724 |
| python | 57.6ms | 15.6× | 4/7 | 73.0ms | 15.4ms | 9.8 MB | 1/7 | 724 |
| node | 11.0ms | 3.0× | 2/7 | 30.3ms | 19.3ms | 51.1 MB | 5/7 | 724 |
| ruby | 143.5ms | 38.8× | 5/7 | 188.5ms | 45.0ms | 23.8 MB | 2/7 | 724 |
| dotnet | 22.2ms | 6.0× | 3/7 | 46.0ms | 23.8ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.3ms | 15.1× | 4/7 | 247.5ms | 29.2ms | 36.2 MB | 4/7 | 9900000 |
| elixir | 14.5ms | 1.0× | 1/7 | 244.2ms | 229.7ms | 69.8 MB | 6/7 | 9900000 |
| python | 51.5ms | 3.6× | 2/7 | 66.9ms | 15.4ms | 9.8 MB | 1/7 | 9900000 |
| node | 678.5ms | 46.8× | 6/7 | 697.8ms | 19.3ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 130.2ms | 9.0× | 3/7 | 175.2ms | 45.0ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 328.0ms | 22.6× | 5/7 | 351.8ms | 23.8ms | 32.5 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 298.0ms | 298.0× | 5/7 | 327.2ms | 29.2ms | 36.6 MB | 4/7 | 2475000 |
| elixir | 0.0ms | < 1× | 1/7 | 216.5ms | 229.7ms | 72.9 MB | 6/7 | 2475000 |
| python | 228.1ms | 228.1× | 4/7 | 243.5ms | 15.4ms | 9.9 MB | 1/7 | 2475000 |
| node | 219.0ms | 219.0× | 3/7 | 238.3ms | 19.3ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 117.7ms | 117.7× | 2/7 | 162.7ms | 45.0ms | 30.2 MB | 2/7 | 2475000 |
| dotnet | 726.6ms | 726.6× | 6/7 | 750.4ms | 23.8ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.5ms | 44.5× | 6/7 | 73.7ms | 29.2ms | 24.2 MB | 3/7 | 155553889038886 |
| elixir | 0.0ms | < 1× | 1/7 | 207.9ms | 229.7ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 0.2ms | < 1× | 2/7 | 15.6ms | 15.4ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 9.0ms | 9.0× | 5/7 | 28.3ms | 19.3ms | 52.5 MB | 5/7 | 155553889038886 |
| ruby | 5.9ms | 5.9× | 3/7 | 50.9ms | 45.0ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 7.3ms | 7.3× | 4/7 | 31.1ms | 23.8ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.9ms | 109.9× | 5/7 | 139.1ms | 29.2ms | 72.0 MB | 4/7 | 6100000 |
| elixir | 8.8ms | 8.8× | 2/7 | 238.5ms | 229.7ms | 75.7 MB | 5/7 | 6100000 |
| python | 636.6ms | 636.6× | 6/7 | 652.0ms | 15.4ms | 28.1 MB | 1/7 | 6100000 |
| node | 64.5ms | 64.5× | 4/7 | 83.8ms | 19.3ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.854s | 1854.2× | 7/7 | 1.899s | 45.0ms | 137.2 MB | 7/7 | 6100000 |
| dotnet | 22.6ms | 22.6× | 3/7 | 46.4ms | 23.8ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 382.2ms | 382.2× | 5/7 | 411.4ms | 29.2ms | 29.1 MB | 4/7 | 31781100 |
| elixir | 39.8ms | 39.8× | 3/7 | 269.5ms | 229.7ms | 72.3 MB | 5/7 | 31781100 |
| python | 722.1ms | 722.1× | 7/7 | 737.5ms | 15.4ms | 22.3 MB | 1/7 | 31781100 |
| node | 124.6ms | 124.6× | 4/7 | 143.9ms | 19.3ms | 182.9 MB | 7/7 | 31781100 |
| ruby | 495.1ms | 495.1× | 6/7 | 540.1ms | 45.0ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 35.8ms | 35.8× | 2/7 | 59.6ms | 23.8ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.9ms | 1.1× | 2/7 | 175.1ms | 29.2ms | 117.5 MB | 5/7 | 500 |
| elixir | 577.6ms | 4.5× | 7/7 | 807.3ms | 229.7ms | 498.6 MB | 7/7 | 500 |
| python | 178.3ms | 1.4× | 4/7 | 193.7ms | 15.4ms | 42.8 MB | 1/7 | 500 |
| node | 128.2ms | 1.0× | 1/7 | 147.5ms | 19.3ms | 65.2 MB | 4/7 | 500 |
| ruby | 218.0ms | 1.7× | 5/7 | 263.0ms | 45.0ms | 50.1 MB | 3/7 | 500 |
| dotnet | 150.1ms | 1.2× | 3/7 | 173.9ms | 23.8ms | 48.9 MB | 2/7 | 500 |
