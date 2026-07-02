# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 14:58.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 3.0× | 4/7 | 30.0ms | — | 23.8 MB | 3/7 | 0 |
| clojure | 350.8ms | 35.1× | 7/7 | 350.8ms | — | 101.8 MB | 7/7 | 0 |
| elixir | 184.8ms | 18.5× | 6/7 | 184.8ms | — | 70.7 MB | 6/7 | 0 |
| python | 10.0ms | 1.0× | 1/7 | 10.0ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.5ms | 1.8× | 2/7 | 17.5ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.9× | 5/7 | 38.8ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 23.0ms | 2.3× | 3/7 | 23.0ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.0ms | 1.3× | 2/7 | 81.0ms | 30.0ms | 27.4 MB | 4/7 | 9227465 |
| clojure | 213.7ms | 5.5× | 5/7 | 564.5ms | 350.8ms | 107.8 MB | 7/7 | 9227465 |
| elixir | 78.3ms | 2.0× | 4/7 | 263.1ms | 184.8ms | 72.4 MB | 6/7 | 9227465 |
| python | 739.4ms | 19.1× | 7/7 | 749.4ms | 10.0ms | 9.8 MB | 1/7 | 9227465 |
| node | 74.6ms | 1.9× | 3/7 | 92.1ms | 17.5ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 607.6ms | 15.7× | 6/7 | 646.4ms | 38.8ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 38.8ms | 1.0× | 1/7 | 61.8ms | 23.0ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.2ms | 3.0× | 3/7 | 65.2ms | 30.0ms | 27.3 MB | 4/7 | 449999985000000 |
| clojure | 143.9ms | 12.4× | 5/7 | 494.7ms | 350.8ms | 108.3 MB | 7/7 | 449999985000000 |
| elixir | 60.2ms | 5.2× | 4/7 | 245.0ms | 184.8ms | 72.5 MB | 6/7 | 449999985000000 |
| python | 2.401s | 207.0× | 7/7 | 2.411s | 10.0ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.3ms | 2.5× | 2/7 | 46.8ms | 17.5ms | 49.4 MB | 5/7 | 449999985000000 |
| ruby | 603.3ms | 52.0× | 6/7 | 642.1ms | 38.8ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.6ms | 1.0× | 1/7 | 34.6ms | 23.0ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.8ms | 1.0× | 1/7 | 31.8ms | 30.0ms | 23.8 MB | 3/7 | 12499997500000 |
| clojure | 170.4ms | 94.7× | 5/7 | 521.2ms | 350.8ms | 219.8 MB | 7/7 | 12499997500000 |
| elixir | 29.3ms | 16.3× | 3/7 | 214.1ms | 184.8ms | 70.7 MB | 5/7 | 12499997500000 |
| python | 106.6ms | 59.2× | 4/7 | 116.6ms | 10.0ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 229.2ms | 127.3× | 7/7 | 246.7ms | 17.5ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 226.0ms | 125.6× | 6/7 | 264.8ms | 38.8ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 10.4ms | 5.8× | 2/7 | 33.4ms | 23.0ms | 27.7 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.4ms | 4.1× | 4/7 | 62.4ms | 30.0ms | 27.5 MB | 4/7 | 13848 |
| clojure | 135.4ms | 17.1× | 7/7 | 486.2ms | 350.8ms | 108.9 MB | 7/7 | 13848 |
| elixir | 15.1ms | 1.9× | 3/7 | 199.9ms | 184.8ms | 70.9 MB | 6/7 | 13848 |
| python | 121.8ms | 15.4× | 6/7 | 131.8ms | 10.0ms | 9.9 MB | 1/7 | 13848 |
| node | 11.0ms | 1.4× | 2/7 | 28.5ms | 17.5ms | 48.1 MB | 5/7 | 13848 |
| ruby | 117.0ms | 14.8× | 5/7 | 155.8ms | 38.8ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 7.9ms | 1.0× | 1/7 | 30.9ms | 23.0ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.9ms | 1.7× | 2/7 | 104.9ms | 30.0ms | 27.1 MB | 4/7 | 442 |
| clojure | 435.4ms | 9.7× | 5/7 | 786.2ms | 350.8ms | 371.0 MB | 7/7 | 442 |
| elixir | 108.7ms | 2.4× | 3/7 | 293.5ms | 184.8ms | 70.6 MB | 6/7 | 442 |
| python | 2.348s | 52.3× | 7/7 | 2.358s | 10.0ms | 9.8 MB | 1/7 | 442 |
| node | 173.0ms | 3.9× | 4/7 | 190.5ms | 17.5ms | 47.8 MB | 5/7 | 442 |
| ruby | 853.5ms | 19.0× | 6/7 | 892.3ms | 38.8ms | 19.3 MB | 2/7 | 442 |
| dotnet | 44.9ms | 1.0× | 1/7 | 67.9ms | 23.0ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 212.0ms | 12.0× | 4/7 | 242.0ms | 30.0ms | 27.4 MB | 4/7 | 6129302 |
| clojure | 152.1ms | 8.6× | 3/7 | 502.9ms | 350.8ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 260.0ms | 14.7× | 5/7 | 444.8ms | 184.8ms | 70.8 MB | 6/7 | 6129302 |
| python | 1.359s | 76.8× | 7/7 | 1.369s | 10.0ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.5ms | 1.2× | 2/7 | 38.0ms | 17.5ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 419.7ms | 23.7× | 6/7 | 458.5ms | 38.8ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 17.7ms | 1.0× | 1/7 | 40.7ms | 23.0ms | 26.2 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.2ms | 31.4× | 4/7 | 121.2ms | 30.0ms | 41.1 MB | 4/7 | 654353666 |
| clojure | 193.7ms | 66.8× | 5/7 | 544.5ms | 350.8ms | 118.0 MB | 7/7 | 654353666 |
| elixir | 65.1ms | 22.4× | 3/7 | 249.9ms | 184.8ms | 75.2 MB | 6/7 | 654353666 |
| python | 455.9ms | 157.2× | 7/7 | 465.9ms | 10.0ms | 10.4 MB | 1/7 | 654353666 |
| node | 15.4ms | 5.3× | 2/7 | 32.9ms | 17.5ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 289.9ms | 100.0× | 6/7 | 328.7ms | 38.8ms | 19.6 MB | 2/7 | 654353666 |
| dotnet | 2.9ms | 1.0× | 1/7 | 25.9ms | 23.0ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.1ms | 1.0× | 1/7 | 41.1ms | 30.0ms | 30.2 MB | 1/7 | 3388889 |
| clojure | 149.0ms | 13.4× | 7/7 | 499.8ms | 350.8ms | 168.6 MB | 6/7 | 3388889 |
| elixir | 118.6ms | 10.7× | 6/7 | 303.4ms | 184.8ms | 200.1 MB | 7/7 | 3388889 |
| python | 43.5ms | 3.9× | 3/7 | 53.5ms | 10.0ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.9ms | 5.8× | 4/7 | 82.4ms | 17.5ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 82.4ms | 7.4× | 5/7 | 121.2ms | 38.8ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.7ms | 2.8× | 2/7 | 53.7ms | 23.0ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.0ms | 3.6× | 4/7 | 139.0ms | 30.0ms | 28.6 MB | 4/7 | 374854840 |
| clojure | 271.5ms | 9.0× | 7/7 | 622.3ms | 350.8ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 171.8ms | 5.7× | 6/7 | 356.6ms | 184.8ms | 72.4 MB | 6/7 | 374854840 |
| python | 170.5ms | 5.7× | 5/7 | 180.5ms | 10.0ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.0ms | 1.0× | 1/7 | 47.5ms | 17.5ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 72.1ms | 2.4× | 3/7 | 110.9ms | 38.8ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 35.1ms | 1.2× | 2/7 | 58.1ms | 23.0ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.5ms | 9.5× | 4/7 | 115.5ms | 30.0ms | 43.7 MB | 4/7 | 1638200 |
| clojure | 159.0ms | 17.7× | 7/7 | 509.8ms | 350.8ms | 150.4 MB | 7/7 | 1638200 |
| elixir | 9.0ms | 1.0× | 1/7 | 193.8ms | 184.8ms | 71.2 MB | 6/7 | 1638200 |
| python | 96.8ms | 10.8× | 5/7 | 106.8ms | 10.0ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.1ms | 2.2× | 3/7 | 37.6ms | 17.5ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 97.0ms | 10.8× | 6/7 | 135.8ms | 38.8ms | 19.7 MB | 2/7 | 1638200 |
| dotnet | 11.4ms | 1.3× | 2/7 | 34.4ms | 23.0ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 153.9ms | 2.4× | 5/7 | 183.9ms | 30.0ms | 154.9 MB | 6/7 | 46468819 |
| clojure | 243.9ms | 3.8× | 7/7 | 594.7ms | 350.8ms | 123.5 MB | 5/7 | 46468819 |
| elixir | 112.9ms | 1.8× | 4/7 | 297.7ms | 184.8ms | 157.3 MB | 7/7 | 46468819 |
| python | 194.6ms | 3.0× | 6/7 | 204.6ms | 10.0ms | 25.8 MB | 2/7 | 46468819 |
| node | 103.8ms | 1.6× | 3/7 | 121.3ms | 17.5ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 71.7ms | 1.1× | 2/7 | 110.5ms | 38.8ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 64.0ms | 1.0× | 1/7 | 87.0ms | 23.0ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 99.1ms | 14.2× | 5/7 | 129.1ms | 30.0ms | 41.9 MB | 4/7 | 724 |
| clojure | 257.1ms | 36.7× | 7/7 | 607.9ms | 350.8ms | 132.8 MB | 7/7 | 724 |
| elixir | 7.8ms | 1.1× | 2/7 | 192.6ms | 184.8ms | 70.4 MB | 6/7 | 724 |
| python | 53.7ms | 7.7× | 4/7 | 63.7ms | 10.0ms | 9.8 MB | 1/7 | 724 |
| node | 7.0ms | 1.0× | 1/7 | 24.5ms | 17.5ms | 50.1 MB | 5/7 | 724 |
| ruby | 123.7ms | 17.7× | 6/7 | 162.5ms | 38.8ms | 19.6 MB | 2/7 | 724 |
| dotnet | 19.4ms | 2.8× | 3/7 | 42.4ms | 23.0ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.4ms | 1.8× | 2/7 | 69.4ms | 30.0ms | 24.7 MB | 3/7 | 9900000 |
| clojure | 1.091s | 48.7× | 7/7 | 1.442s | 350.8ms | 371.4 MB | 7/7 | 9900000 |
| elixir | 22.4ms | 1.0× | 1/7 | 207.2ms | 184.8ms | 70.0 MB | 6/7 | 9900000 |
| python | 48.5ms | 2.2× | 3/7 | 58.5ms | 10.0ms | 9.8 MB | 1/7 | 9900000 |
| node | 567.3ms | 25.3× | 6/7 | 584.8ms | 17.5ms | 49.7 MB | 5/7 | 9900000 |
| ruby | 113.1ms | 5.0× | 4/7 | 151.9ms | 38.8ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 287.2ms | 12.8× | 5/7 | 310.2ms | 23.0ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.3ms | 7.4× | 2/7 | 80.3ms | 30.0ms | 27.9 MB | 3/7 | 2475000 |
| clojure | 1.337s | 196.7× | 7/7 | 1.688s | 350.8ms | 375.1 MB | 7/7 | 2475000 |
| elixir | 6.8ms | 1.0× | 1/7 | 191.6ms | 184.8ms | 70.4 MB | 6/7 | 2475000 |
| python | 219.1ms | 32.2× | 5/7 | 229.1ms | 10.0ms | 9.9 MB | 1/7 | 2475000 |
| node | 210.5ms | 31.0× | 4/7 | 228.0ms | 17.5ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 115.8ms | 17.0× | 3/7 | 154.6ms | 38.8ms | 26.1 MB | 2/7 | 2475000 |
| dotnet | 690.7ms | 101.6× | 6/7 | 713.7ms | 23.0ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.3ms | 7.3× | 6/7 | 61.3ms | 30.0ms | 27.5 MB | 3/7 | 155553889038886 |
| clojure | 133.9ms | 31.1× | 7/7 | 484.7ms | 350.8ms | 107.6 MB | 7/7 | 155553889038886 |
| elixir | 8.5ms | 2.0× | 3/7 | 193.3ms | 184.8ms | 72.1 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.0× | 1/7 | 14.3ms | 10.0ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.7ms | 2.0× | 4/7 | 26.2ms | 17.5ms | 51.5 MB | 5/7 | 155553889038886 |
| ruby | 10.3ms | 2.4× | 5/7 | 49.1ms | 38.8ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.0ms | 1.6× | 2/7 | 30.0ms | 23.0ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.1ms | 5.2× | 4/7 | 120.1ms | 30.0ms | 67.6 MB | 4/7 | 6100000 |
| clojure | 178.3ms | 10.2× | 5/7 | 529.1ms | 350.8ms | 133.6 MB | 7/7 | 6100000 |
| elixir | 22.4ms | 1.3× | 2/7 | 207.2ms | 184.8ms | 76.2 MB | 5/7 | 6100000 |
| python | 546.9ms | 31.4× | 6/7 | 556.9ms | 10.0ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.2ms | 3.0× | 3/7 | 69.7ms | 17.5ms | 51.2 MB | 3/7 | 6100000 |
| ruby | 1.611s | 92.6× | 7/7 | 1.650s | 38.8ms | 133.0 MB | 6/7 | 6100000 |
| dotnet | 17.4ms | 1.0× | 1/7 | 40.4ms | 23.0ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.8ms | 1.3× | 2/7 | 178.8ms | 30.0ms | 30.6 MB | 4/7 | 134626900 |
| clojure | 381.8ms | 3.4× | 5/7 | 732.6ms | 350.8ms | 135.8 MB | 6/7 | 134626900 |
| elixir | 307.6ms | 2.7× | 4/7 | 492.4ms | 184.8ms | 72.7 MB | 5/7 | 134626900 |
| python | 2.545s | 22.4× | 7/7 | 2.555s | 10.0ms | 22.2 MB | 2/7 | 134626900 |
| node | 298.3ms | 2.6× | 3/7 | 315.8ms | 17.5ms | 181.0 MB | 7/7 | 134626900 |
| ruby | 1.868s | 16.5× | 6/7 | 1.907s | 38.8ms | 19.3 MB | 1/7 | 134626900 |
| dotnet | 113.4ms | 1.0× | 1/7 | 136.4ms | 23.0ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.0ms | 1.2× | 2/7 | 178.0ms | 30.0ms | 125.7 MB | 5/7 | 500 |
| clojure | 819.8ms | 6.9× | 7/7 | 1.171s | 350.8ms | 283.5 MB | 6/7 | 500 |
| elixir | 584.6ms | 4.9× | 6/7 | 769.4ms | 184.8ms | 519.4 MB | 7/7 | 500 |
| python | 176.0ms | 1.5× | 4/7 | 186.0ms | 10.0ms | 43.7 MB | 1/7 | 500 |
| node | 118.8ms | 1.0× | 1/7 | 136.3ms | 17.5ms | 64.5 MB | 4/7 | 500 |
| ruby | 212.4ms | 1.8× | 5/7 | 251.2ms | 38.8ms | 45.9 MB | 2/7 | 500 |
| dotnet | 152.8ms | 1.3× | 3/7 | 175.8ms | 23.0ms | 48.1 MB | 3/7 | 500 |
