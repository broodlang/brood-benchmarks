# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-01 17:30.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.8ms | 2.8× | 4/7 | 29.8ms | — | 23.5 MB | 3/7 | 0 |
| clojure | 344.2ms | 32.8× | 7/7 | 344.2ms | — | 103.0 MB | 7/7 | 0 |
| elixir | 186.3ms | 17.7× | 6/7 | 186.3ms | — | 71.2 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.8ms | 1.7× | 2/7 | 17.8ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.1ms | 3.7× | 5/7 | 39.1ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 22.4ms | 2.1× | 3/7 | 22.4ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 237.1ms | 6.2× | 5/7 | 266.9ms | 29.8ms | 27.3 MB | 4/7 | 9227465 |
| clojure | 200.0ms | 5.3× | 4/7 | 544.2ms | 344.2ms | 109.0 MB | 7/7 | 9227465 |
| elixir | 72.7ms | 1.9× | 3/7 | 259.0ms | 186.3ms | 70.5 MB | 6/7 | 9227465 |
| python | 734.9ms | 19.3× | 7/7 | 745.4ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 72.5ms | 1.9× | 2/7 | 90.3ms | 17.8ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 602.1ms | 15.8× | 6/7 | 641.2ms | 39.1ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 38.0ms | 1.0× | 1/7 | 60.4ms | 22.4ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.0ms | 3.1× | 3/7 | 64.8ms | 29.8ms | 26.8 MB | 4/7 | 449999985000000 |
| clojure | 142.0ms | 12.6× | 5/7 | 486.2ms | 344.2ms | 107.6 MB | 7/7 | 449999985000000 |
| elixir | 59.9ms | 5.3× | 4/7 | 246.2ms | 186.3ms | 70.9 MB | 6/7 | 449999985000000 |
| python | 2.407s | 213.0× | 7/7 | 2.417s | 10.5ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.2ms | 2.6× | 2/7 | 47.0ms | 17.8ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 638.9ms | 56.5× | 6/7 | 678.0ms | 39.1ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.3ms | 1.0× | 1/7 | 33.7ms | 22.4ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.2ms | 1.0× | 1/7 | 32.0ms | 29.8ms | 23.7 MB | 3/7 | 12499997500000 |
| clojure | 170.0ms | 77.3× | 5/7 | 514.2ms | 344.2ms | 221.4 MB | 7/7 | 12499997500000 |
| elixir | 26.8ms | 12.2× | 3/7 | 213.1ms | 186.3ms | 71.3 MB | 5/7 | 12499997500000 |
| python | 105.2ms | 47.8× | 4/7 | 115.7ms | 10.5ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 216.9ms | 98.6× | 6/7 | 234.7ms | 17.8ms | 89.6 MB | 6/7 | 12499997500000 |
| ruby | 232.6ms | 105.7× | 7/7 | 271.7ms | 39.1ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 11.5ms | 5.2× | 2/7 | 33.9ms | 22.4ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.4ms | 4.8× | 4/7 | 63.2ms | 29.8ms | 27.4 MB | 4/7 | 13848 |
| clojure | 137.2ms | 19.6× | 7/7 | 481.4ms | 344.2ms | 108.7 MB | 7/7 | 13848 |
| elixir | 11.9ms | 1.7× | 3/7 | 198.2ms | 186.3ms | 71.0 MB | 6/7 | 13848 |
| python | 120.9ms | 17.3× | 6/7 | 131.4ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 8.0ms | 1.1× | 2/7 | 25.8ms | 17.8ms | 48.1 MB | 5/7 | 13848 |
| ruby | 117.0ms | 16.7× | 5/7 | 156.1ms | 39.1ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 7.0ms | 1.0× | 1/7 | 29.4ms | 22.4ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.6ms | 1.7× | 2/7 | 103.4ms | 29.8ms | 26.8 MB | 4/7 | 442 |
| clojure | 418.0ms | 9.4× | 5/7 | 762.2ms | 344.2ms | 371.0 MB | 7/7 | 442 |
| elixir | 95.9ms | 2.2× | 3/7 | 282.2ms | 186.3ms | 72.3 MB | 6/7 | 442 |
| python | 2.443s | 54.9× | 7/7 | 2.453s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 177.8ms | 4.0× | 4/7 | 195.6ms | 17.8ms | 48.0 MB | 5/7 | 442 |
| ruby | 870.5ms | 19.6× | 6/7 | 909.6ms | 39.1ms | 19.3 MB | 2/7 | 442 |
| dotnet | 44.5ms | 1.0× | 1/7 | 66.9ms | 22.4ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 213.6ms | 12.1× | 4/7 | 243.4ms | 29.8ms | 27.5 MB | 4/7 | 6129302 |
| clojure | 153.6ms | 8.7× | 3/7 | 497.8ms | 344.2ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 246.0ms | 14.0× | 5/7 | 432.3ms | 186.3ms | 73.0 MB | 6/7 | 6129302 |
| python | 1.299s | 73.8× | 7/7 | 1.309s | 10.5ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.2ms | 1.1× | 2/7 | 38.0ms | 17.8ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 426.8ms | 24.2× | 6/7 | 465.9ms | 39.1ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 17.6ms | 1.0× | 1/7 | 40.0ms | 22.4ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.9ms | 23.3× | 4/7 | 120.7ms | 29.8ms | 40.0 MB | 4/7 | 654353666 |
| clojure | 188.4ms | 48.3× | 5/7 | 532.6ms | 344.2ms | 119.3 MB | 7/7 | 654353666 |
| elixir | 53.6ms | 13.7× | 3/7 | 239.9ms | 186.3ms | 74.9 MB | 6/7 | 654353666 |
| python | 438.3ms | 112.4× | 7/7 | 448.8ms | 10.5ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.1ms | 4.1× | 2/7 | 33.9ms | 17.8ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 299.3ms | 76.7× | 6/7 | 338.4ms | 39.1ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 3.9ms | 1.0× | 1/7 | 26.3ms | 22.4ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.5ms | 1.0× | 1/7 | 40.3ms | 29.8ms | 30.0 MB | 1/7 | 3388889 |
| clojure | 151.7ms | 14.4× | 7/7 | 495.9ms | 344.2ms | 167.4 MB | 6/7 | 3388889 |
| elixir | 121.1ms | 11.5× | 6/7 | 307.4ms | 186.3ms | 203.3 MB | 7/7 | 3388889 |
| python | 42.4ms | 4.0× | 3/7 | 52.9ms | 10.5ms | 39.8 MB | 2/7 | 3388889 |
| node | 63.8ms | 6.1× | 4/7 | 81.6ms | 17.8ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 82.9ms | 7.9× | 5/7 | 122.0ms | 39.1ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 29.9ms | 2.8× | 2/7 | 52.3ms | 22.4ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.8ms | 3.6× | 4/7 | 136.6ms | 29.8ms | 28.0 MB | 4/7 | 374854840 |
| clojure | 273.5ms | 9.2× | 7/7 | 617.7ms | 344.2ms | 302.5 MB | 7/7 | 374854840 |
| elixir | 159.5ms | 5.4× | 5/7 | 345.8ms | 186.3ms | 69.9 MB | 6/7 | 374854840 |
| python | 170.0ms | 5.7× | 6/7 | 180.5ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.6ms | 1.0× | 1/7 | 47.4ms | 17.8ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 69.8ms | 2.4× | 3/7 | 108.9ms | 39.1ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.2ms | 1.2× | 2/7 | 58.6ms | 22.4ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.3ms | 14.5× | 4/7 | 115.1ms | 29.8ms | 43.1 MB | 4/7 | 1638200 |
| clojure | 164.7ms | 27.9× | 7/7 | 508.9ms | 344.2ms | 150.6 MB | 7/7 | 1638200 |
| elixir | 5.9ms | 1.0× | 1/7 | 192.2ms | 186.3ms | 72.2 MB | 6/7 | 1638200 |
| python | 93.1ms | 15.8× | 5/7 | 103.6ms | 10.5ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.1ms | 3.4× | 3/7 | 37.9ms | 17.8ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 96.6ms | 16.4× | 6/7 | 135.7ms | 39.1ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 13.6ms | 2.3× | 2/7 | 36.0ms | 22.4ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.6ms | 2.4× | 5/7 | 180.4ms | 29.8ms | 153.7 MB | 6/7 | 46468819 |
| clojure | 240.5ms | 3.8× | 7/7 | 584.7ms | 344.2ms | 124.1 MB | 5/7 | 46468819 |
| elixir | 106.7ms | 1.7× | 4/7 | 293.0ms | 186.3ms | 157.2 MB | 7/7 | 46468819 |
| python | 178.7ms | 2.8× | 6/7 | 189.2ms | 10.5ms | 25.8 MB | 2/7 | 46468819 |
| node | 105.9ms | 1.7× | 3/7 | 123.7ms | 17.8ms | 64.5 MB | 4/7 | 46468819 |
| ruby | 75.3ms | 1.2× | 2/7 | 114.4ms | 39.1ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 63.8ms | 1.0× | 1/7 | 86.2ms | 22.4ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.1ms | 16.2× | 5/7 | 131.9ms | 29.8ms | 41.9 MB | 4/7 | 724 |
| clojure | 186.6ms | 29.6× | 7/7 | 530.8ms | 344.2ms | 129.2 MB | 7/7 | 724 |
| elixir | 6.3ms | 1.0× | 1/7 | 192.6ms | 186.3ms | 70.1 MB | 6/7 | 724 |
| python | 54.4ms | 8.6× | 4/7 | 64.9ms | 10.5ms | 9.8 MB | 1/7 | 724 |
| node | 7.2ms | 1.1× | 2/7 | 25.0ms | 17.8ms | 50.1 MB | 5/7 | 724 |
| ruby | 119.8ms | 19.0× | 6/7 | 158.9ms | 39.1ms | 19.6 MB | 2/7 | 724 |
| dotnet | 18.4ms | 2.9× | 3/7 | 40.8ms | 22.4ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.7ms | 2.1× | 2/7 | 67.5ms | 29.8ms | 24.5 MB | 3/7 | 9900000 |
| clojure | 1.067s | 58.3× | 7/7 | 1.411s | 344.2ms | 371.0 MB | 7/7 | 9900000 |
| elixir | 18.3ms | 1.0× | 1/7 | 204.6ms | 186.3ms | 73.5 MB | 6/7 | 9900000 |
| python | 46.7ms | 2.6× | 3/7 | 57.2ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 556.6ms | 30.4× | 6/7 | 574.4ms | 17.8ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 106.3ms | 5.8× | 4/7 | 145.4ms | 39.1ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 283.6ms | 15.5× | 5/7 | 306.0ms | 22.4ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.0ms | 10.4× | 2/7 | 81.8ms | 29.8ms | 27.6 MB | 3/7 | 2475000 |
| clojure | 1.329s | 265.8× | 7/7 | 1.673s | 344.2ms | 374.9 MB | 7/7 | 2475000 |
| elixir | 5.0ms | 1.0× | 1/7 | 191.3ms | 186.3ms | 72.6 MB | 6/7 | 2475000 |
| python | 216.4ms | 43.3× | 4/7 | 226.9ms | 10.5ms | 9.8 MB | 1/7 | 2475000 |
| node | 225.4ms | 45.1× | 5/7 | 243.2ms | 17.8ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 123.5ms | 24.7× | 3/7 | 162.6ms | 39.1ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 679.1ms | 135.8× | 6/7 | 701.5ms | 22.4ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 32.0× | 6/7 | 61.8ms | 29.8ms | 27.1 MB | 3/7 | 155553889038886 |
| clojure | 125.8ms | 125.8× | 7/7 | 470.0ms | 344.2ms | 109.4 MB | 7/7 | 155553889038886 |
| elixir | 0.8ms | < 1× | 1/7 | 187.1ms | 186.3ms | 70.9 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 3.9× | 2/7 | 14.4ms | 10.5ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 7.7× | 4/7 | 25.5ms | 17.8ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.8ms | 7.8× | 5/7 | 46.9ms | 39.1ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 6.6ms | 6.6× | 3/7 | 29.0ms | 22.4ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 126.3ms | 7.3× | 4/7 | 156.1ms | 29.8ms | 87.9 MB | 5/7 | 6100000 |
| clojure | 185.2ms | 10.7× | 5/7 | 529.4ms | 344.2ms | 133.6 MB | 7/7 | 6100000 |
| elixir | 19.0ms | 1.1× | 2/7 | 205.3ms | 186.3ms | 77.5 MB | 4/7 | 6100000 |
| python | 543.3ms | 31.4× | 6/7 | 553.8ms | 10.5ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.0ms | 3.0× | 3/7 | 69.8ms | 17.8ms | 51.2 MB | 3/7 | 6100000 |
| ruby | 1.583s | 91.5× | 7/7 | 1.623s | 39.1ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 17.3ms | 1.0× | 1/7 | 39.7ms | 22.4ms | 31.2 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 385.7ms | 11.7× | 5/7 | 415.5ms | 29.8ms | 34.0 MB | 4/7 | 31781100 |
| clojure | 218.4ms | 6.6× | 4/7 | 562.6ms | 344.2ms | 133.7 MB | 6/7 | 31781100 |
| elixir | 76.8ms | 2.3× | 2/7 | 263.1ms | 186.3ms | 70.9 MB | 5/7 | 31781100 |
| python | 674.8ms | 20.5× | 7/7 | 685.3ms | 10.5ms | 22.2 MB | 2/7 | 31781100 |
| node | 108.9ms | 3.3× | 3/7 | 126.7ms | 17.8ms | 181.2 MB | 7/7 | 31781100 |
| ruby | 429.5ms | 13.1× | 6/7 | 468.6ms | 39.1ms | 19.4 MB | 1/7 | 31781100 |
| dotnet | 32.9ms | 1.0× | 1/7 | 55.3ms | 22.4ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.1ms | 1.2× | 3/7 | 180.9ms | 29.8ms | 124.7 MB | 5/7 | 500 |
| clojure | 813.6ms | 6.7× | 7/7 | 1.158s | 344.2ms | 314.6 MB | 6/7 | 500 |
| elixir | 588.4ms | 4.9× | 6/7 | 774.7ms | 186.3ms | 510.2 MB | 7/7 | 500 |
| python | 174.0ms | 1.4× | 4/7 | 184.5ms | 10.5ms | 46.8 MB | 2/7 | 500 |
| node | 120.9ms | 1.0× | 1/7 | 138.7ms | 17.8ms | 64.7 MB | 4/7 | 500 |
| ruby | 214.6ms | 1.8× | 5/7 | 253.7ms | 39.1ms | 45.8 MB | 1/7 | 500 |
| dotnet | 144.1ms | 1.2× | 2/7 | 166.5ms | 22.4ms | 48.1 MB | 3/7 | 500 |
