# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-01 13:55.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.9ms | 2.8× | 4/7 | 28.9ms | — | 23.6 MB | 3/7 | 0 |
| clojure | 339.7ms | 33.3× | 7/7 | 339.7ms | — | 102.5 MB | 7/7 | 0 |
| elixir | 180.0ms | 17.6× | 6/7 | 180.0ms | — | 72.1 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.3ms | 1.7× | 2/7 | 17.3ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.2ms | 3.8× | 5/7 | 39.2ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.9ms | 2.1× | 3/7 | 21.9ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.6ms | 5.7× | 5/7 | 253.5ms | 28.9ms | 27.7 MB | 4/7 | 9227465 |
| clojure | 189.9ms | 4.8× | 4/7 | 529.6ms | 339.7ms | 108.1 MB | 7/7 | 9227465 |
| elixir | 77.1ms | 2.0× | 3/7 | 257.1ms | 180.0ms | 70.2 MB | 6/7 | 9227465 |
| python | 722.0ms | 18.3× | 7/7 | 732.2ms | 10.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 72.1ms | 1.8× | 2/7 | 89.4ms | 17.3ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 606.1ms | 15.4× | 6/7 | 645.3ms | 39.2ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.4ms | 1.0× | 1/7 | 61.3ms | 21.9ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.9ms | 3.1× | 3/7 | 65.8ms | 28.9ms | 27.2 MB | 4/7 | 449999985000000 |
| clojure | 142.4ms | 12.0× | 5/7 | 482.1ms | 339.7ms | 108.3 MB | 7/7 | 449999985000000 |
| elixir | 67.5ms | 5.7× | 4/7 | 247.5ms | 180.0ms | 71.2 MB | 6/7 | 449999985000000 |
| python | 2.187s | 183.8× | 7/7 | 2.197s | 10.2ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.3ms | 2.5× | 2/7 | 46.6ms | 17.3ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 591.9ms | 49.7× | 6/7 | 631.1ms | 39.2ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.9ms | 1.0× | 1/7 | 33.8ms | 21.9ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.7ms | 1.0× | 1/7 | 32.6ms | 28.9ms | 23.6 MB | 3/7 | 12499997500000 |
| clojure | 170.5ms | 46.1× | 5/7 | 510.2ms | 339.7ms | 220.3 MB | 7/7 | 12499997500000 |
| elixir | 35.1ms | 9.5× | 3/7 | 215.1ms | 180.0ms | 71.0 MB | 5/7 | 12499997500000 |
| python | 108.9ms | 29.4× | 4/7 | 119.1ms | 10.2ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 220.3ms | 59.5× | 6/7 | 237.6ms | 17.3ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 243.0ms | 65.7× | 7/7 | 282.2ms | 39.2ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 11.7ms | 3.2× | 2/7 | 33.6ms | 21.9ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.3ms | 4.3× | 4/7 | 63.2ms | 28.9ms | 27.0 MB | 4/7 | 13848 |
| clojure | 145.5ms | 18.4× | 7/7 | 485.2ms | 339.7ms | 109.1 MB | 7/7 | 13848 |
| elixir | 17.1ms | 2.2× | 3/7 | 197.1ms | 180.0ms | 72.5 MB | 6/7 | 13848 |
| python | 120.2ms | 15.2× | 6/7 | 130.4ms | 10.2ms | 9.9 MB | 1/7 | 13848 |
| node | 8.7ms | 1.1× | 2/7 | 26.0ms | 17.3ms | 48.1 MB | 5/7 | 13848 |
| ruby | 115.2ms | 14.6× | 5/7 | 154.4ms | 39.2ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 7.9ms | 1.0× | 1/7 | 29.8ms | 21.9ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.6ms | 1.7× | 2/7 | 103.5ms | 28.9ms | 26.9 MB | 4/7 | 442 |
| clojure | 419.2ms | 9.4× | 5/7 | 758.9ms | 339.7ms | 371.1 MB | 7/7 | 442 |
| elixir | 102.8ms | 2.3× | 3/7 | 282.8ms | 180.0ms | 69.9 MB | 6/7 | 442 |
| python | 2.494s | 55.7× | 7/7 | 2.505s | 10.2ms | 9.8 MB | 1/7 | 442 |
| node | 172.6ms | 3.9× | 4/7 | 189.9ms | 17.3ms | 48.0 MB | 5/7 | 442 |
| ruby | 875.1ms | 19.5× | 6/7 | 914.3ms | 39.2ms | 19.3 MB | 2/7 | 442 |
| dotnet | 44.8ms | 1.0× | 1/7 | 66.7ms | 21.9ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.8ms | 11.2× | 4/7 | 240.7ms | 28.9ms | 27.0 MB | 4/7 | 6129302 |
| clojure | 155.8ms | 8.2× | 3/7 | 495.5ms | 339.7ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 254.5ms | 13.5× | 5/7 | 434.5ms | 180.0ms | 70.3 MB | 6/7 | 6129302 |
| python | 1.318s | 69.7× | 7/7 | 1.328s | 10.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.3ms | 1.1× | 2/7 | 37.6ms | 17.3ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 409.7ms | 21.7× | 6/7 | 448.9ms | 39.2ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 18.9ms | 1.0× | 1/7 | 40.8ms | 21.9ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.4ms | 22.7× | 4/7 | 124.3ms | 28.9ms | 40.1 MB | 4/7 | 654353666 |
| clojure | 203.2ms | 48.4× | 5/7 | 542.9ms | 339.7ms | 119.1 MB | 7/7 | 654353666 |
| elixir | 61.3ms | 14.6× | 3/7 | 241.3ms | 180.0ms | 76.2 MB | 6/7 | 654353666 |
| python | 463.1ms | 110.3× | 7/7 | 473.3ms | 10.2ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.4ms | 3.9× | 2/7 | 33.7ms | 17.3ms | 52.0 MB | 5/7 | 654353666 |
| ruby | 293.1ms | 69.8× | 6/7 | 332.3ms | 39.2ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.2ms | 1.0× | 1/7 | 26.1ms | 21.9ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.5ms | 1.0× | 1/7 | 39.4ms | 28.9ms | 30.0 MB | 1/7 | 3388889 |
| clojure | 160.6ms | 15.3× | 7/7 | 500.3ms | 339.7ms | 169.8 MB | 6/7 | 3388889 |
| elixir | 119.1ms | 11.3× | 6/7 | 299.1ms | 180.0ms | 200.8 MB | 7/7 | 3388889 |
| python | 42.7ms | 4.1× | 3/7 | 52.9ms | 10.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.4ms | 6.1× | 4/7 | 81.7ms | 17.3ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 83.0ms | 7.9× | 5/7 | 122.2ms | 39.2ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.7ms | 2.9× | 2/7 | 52.6ms | 21.9ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.2ms | 3.5× | 4/7 | 138.1ms | 28.9ms | 27.8 MB | 4/7 | 374854840 |
| clojure | 287.5ms | 9.3× | 7/7 | 627.2ms | 339.7ms | 302.4 MB | 7/7 | 374854840 |
| elixir | 177.1ms | 5.7× | 6/7 | 357.1ms | 180.0ms | 70.5 MB | 6/7 | 374854840 |
| python | 169.2ms | 5.5× | 5/7 | 179.4ms | 10.2ms | 10.0 MB | 1/7 | 374854840 |
| node | 30.9ms | 1.0× | 1/7 | 48.2ms | 17.3ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 75.7ms | 2.4× | 3/7 | 114.9ms | 39.2ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 39.5ms | 1.3× | 2/7 | 61.4ms | 21.9ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.0ms | 6.1× | 4/7 | 113.9ms | 28.9ms | 42.3 MB | 4/7 | 1638200 |
| clojure | 175.9ms | 12.6× | 7/7 | 515.6ms | 339.7ms | 150.0 MB | 7/7 | 1638200 |
| elixir | 14.0ms | 1.0× | 1/7 | 194.0ms | 180.0ms | 72.2 MB | 6/7 | 1638200 |
| python | 96.4ms | 6.9× | 5/7 | 106.6ms | 10.2ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.9ms | 1.5× | 3/7 | 38.2ms | 17.3ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 97.9ms | 7.0× | 6/7 | 137.1ms | 39.2ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.0ms | 1.0× | 2/7 | 35.9ms | 21.9ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.3ms | 2.7× | 5/7 | 202.2ms | 28.9ms | 146.1 MB | 6/7 | 46468819 |
| clojure | 260.0ms | 4.0× | 7/7 | 599.7ms | 339.7ms | 123.5 MB | 5/7 | 46468819 |
| elixir | 112.1ms | 1.7× | 4/7 | 292.1ms | 180.0ms | 159.7 MB | 7/7 | 46468819 |
| python | 188.1ms | 2.9× | 6/7 | 198.3ms | 10.2ms | 25.9 MB | 2/7 | 46468819 |
| node | 102.4ms | 1.6× | 3/7 | 119.7ms | 17.3ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 72.3ms | 1.1× | 2/7 | 111.5ms | 39.2ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 65.0ms | 1.0× | 1/7 | 86.9ms | 21.9ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 99.7ms | 13.8× | 5/7 | 128.6ms | 28.9ms | 42.2 MB | 4/7 | 724 |
| clojure | 190.4ms | 26.4× | 7/7 | 530.1ms | 339.7ms | 132.2 MB | 7/7 | 724 |
| elixir | 11.8ms | 1.6× | 2/7 | 191.8ms | 180.0ms | 70.3 MB | 6/7 | 724 |
| python | 52.6ms | 7.3× | 4/7 | 62.8ms | 10.2ms | 9.8 MB | 1/7 | 724 |
| node | 7.2ms | 1.0× | 1/7 | 24.5ms | 17.3ms | 50.1 MB | 5/7 | 724 |
| ruby | 124.2ms | 17.3× | 6/7 | 163.4ms | 39.2ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.4ms | 2.8× | 3/7 | 42.3ms | 21.9ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.8ms | 1.9× | 2/7 | 68.7ms | 28.9ms | 24.2 MB | 3/7 | 9900000 |
| clojure | 1.083s | 50.9× | 7/7 | 1.423s | 339.7ms | 370.6 MB | 7/7 | 9900000 |
| elixir | 21.3ms | 1.0× | 1/7 | 201.3ms | 180.0ms | 70.3 MB | 6/7 | 9900000 |
| python | 47.3ms | 2.2× | 3/7 | 57.5ms | 10.2ms | 9.8 MB | 1/7 | 9900000 |
| node | 555.8ms | 26.1× | 6/7 | 573.1ms | 17.3ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 107.2ms | 5.0× | 4/7 | 146.4ms | 39.2ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 283.4ms | 13.3× | 5/7 | 305.3ms | 21.9ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.8ms | 5.1× | 2/7 | 79.7ms | 28.9ms | 27.6 MB | 3/7 | 2475000 |
| clojure | 1.310s | 131.0× | 7/7 | 1.649s | 339.7ms | 374.4 MB | 7/7 | 2475000 |
| elixir | 10.0ms | 1.0× | 1/7 | 190.0ms | 180.0ms | 70.6 MB | 6/7 | 2475000 |
| python | 214.7ms | 21.5× | 5/7 | 224.9ms | 10.2ms | 9.8 MB | 1/7 | 2475000 |
| node | 203.6ms | 20.4× | 4/7 | 220.9ms | 17.3ms | 49.5 MB | 5/7 | 2475000 |
| ruby | 111.6ms | 11.2× | 3/7 | 150.8ms | 39.2ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 672.3ms | 67.2× | 6/7 | 694.2ms | 21.9ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.5ms | 7.6× | 6/7 | 61.4ms | 28.9ms | 27.3 MB | 3/7 | 155553889038886 |
| clojure | 131.0ms | 30.5× | 7/7 | 470.7ms | 339.7ms | 108.9 MB | 7/7 | 155553889038886 |
| elixir | 14.9ms | 3.5× | 5/7 | 194.9ms | 180.0ms | 73.6 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.0× | 1/7 | 14.5ms | 10.2ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.5ms | 2.0× | 4/7 | 25.8ms | 17.3ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.5ms | 1.7× | 2/7 | 46.7ms | 39.2ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.3ms | 1.9× | 3/7 | 30.2ms | 21.9ms | 28.0 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 120.1ms | 6.7× | 4/7 | 149.0ms | 28.9ms | 86.2 MB | 5/7 | 6100000 |
| clojure | 184.7ms | 10.3× | 5/7 | 524.4ms | 339.7ms | 133.2 MB | 7/7 | 6100000 |
| elixir | 25.4ms | 1.4× | 2/7 | 205.4ms | 180.0ms | 76.6 MB | 4/7 | 6100000 |
| python | 550.8ms | 30.8× | 6/7 | 561.0ms | 10.2ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.8ms | 2.9× | 3/7 | 70.1ms | 17.3ms | 51.1 MB | 3/7 | 6100000 |
| ruby | 1.599s | 89.4× | 7/7 | 1.639s | 39.2ms | 132.7 MB | 6/7 | 6100000 |
| dotnet | 17.9ms | 1.0× | 1/7 | 39.8ms | 21.9ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 396.3ms | 12.2× | 5/7 | 425.2ms | 28.9ms | 34.0 MB | 4/7 | 31781100 |
| clojure | 225.4ms | 7.0× | 4/7 | 565.1ms | 339.7ms | 136.5 MB | 6/7 | 31781100 |
| elixir | 89.2ms | 2.8× | 2/7 | 269.2ms | 180.0ms | 73.1 MB | 5/7 | 31781100 |
| python | 686.7ms | 21.2× | 7/7 | 696.9ms | 10.2ms | 22.2 MB | 2/7 | 31781100 |
| node | 113.0ms | 3.5× | 3/7 | 130.3ms | 17.3ms | 181.1 MB | 7/7 | 31781100 |
| ruby | 431.9ms | 13.3× | 6/7 | 471.1ms | 39.2ms | 19.4 MB | 1/7 | 31781100 |
| dotnet | 32.4ms | 1.0× | 1/7 | 54.3ms | 21.9ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 154.8ms | 1.3× | 3/7 | 183.7ms | 28.9ms | 128.1 MB | 5/7 | 500 |
| clojure | 806.8ms | 6.7× | 7/7 | 1.147s | 339.7ms | 277.7 MB | 6/7 | 500 |
| elixir | 542.2ms | 4.5× | 6/7 | 722.2ms | 180.0ms | 482.1 MB | 7/7 | 500 |
| python | 176.1ms | 1.5× | 4/7 | 186.3ms | 10.2ms | 44.9 MB | 1/7 | 500 |
| node | 120.0ms | 1.0× | 1/7 | 137.3ms | 17.3ms | 64.7 MB | 4/7 | 500 |
| ruby | 208.5ms | 1.7× | 5/7 | 247.7ms | 39.2ms | 45.8 MB | 2/7 | 500 |
| dotnet | 152.6ms | 1.3× | 2/7 | 174.5ms | 21.9ms | 48.1 MB | 3/7 | 500 |
