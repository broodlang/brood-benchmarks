# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-01 11:22.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.7ms | 2.8× | 4/7 | 29.7ms | — | 24.5 MB | 3/7 | 0 |
| clojure | 335.2ms | 31.9× | 7/7 | 335.2ms | — | 102.6 MB | 7/7 | 0 |
| elixir | 180.4ms | 17.2× | 6/7 | 180.4ms | — | 72.6 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.5ms | 1.7× | 2/7 | 17.5ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.1ms | 3.7× | 5/7 | 39.1ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.8ms | 2.1× | 3/7 | 21.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 220.6ms | 5.7× | 5/7 | 250.3ms | 29.7ms | 28.1 MB | 4/7 | 9227465 |
| clojure | 199.9ms | 5.1× | 4/7 | 535.1ms | 335.2ms | 109.2 MB | 7/7 | 9227465 |
| elixir | 74.0ms | 1.9× | 3/7 | 254.4ms | 180.4ms | 71.2 MB | 6/7 | 9227465 |
| python | 727.7ms | 18.7× | 7/7 | 738.2ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.0ms | 1.9× | 2/7 | 90.5ms | 17.5ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 616.3ms | 15.8× | 6/7 | 655.4ms | 39.1ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.0ms | 1.0× | 1/7 | 60.8ms | 21.8ms | 25.7 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.1ms | 3.3× | 3/7 | 66.8ms | 29.7ms | 27.6 MB | 4/7 | 449999985000000 |
| clojure | 144.8ms | 13.0× | 5/7 | 480.0ms | 335.2ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 58.0ms | 5.2× | 4/7 | 238.4ms | 180.4ms | 70.2 MB | 6/7 | 449999985000000 |
| python | 2.346s | 211.4× | 7/7 | 2.357s | 10.5ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.4ms | 2.6× | 2/7 | 46.9ms | 17.5ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 589.7ms | 53.1× | 6/7 | 628.8ms | 39.1ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.1ms | 1.0× | 1/7 | 32.9ms | 21.8ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.9ms | 1.0× | 1/7 | 32.6ms | 29.7ms | 24.5 MB | 3/7 | 12499997500000 |
| clojure | 181.1ms | 62.4× | 5/7 | 516.3ms | 335.2ms | 220.0 MB | 7/7 | 12499997500000 |
| elixir | 32.9ms | 11.3× | 3/7 | 213.3ms | 180.4ms | 72.4 MB | 5/7 | 12499997500000 |
| python | 107.9ms | 37.2× | 4/7 | 118.4ms | 10.5ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 222.9ms | 76.9× | 7/7 | 240.4ms | 17.5ms | 89.6 MB | 6/7 | 12499997500000 |
| ruby | 222.8ms | 76.8× | 6/7 | 261.9ms | 39.1ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 11.6ms | 4.0× | 2/7 | 33.4ms | 21.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.9ms | 4.1× | 4/7 | 63.6ms | 29.7ms | 28.2 MB | 4/7 | 13848 |
| clojure | 149.9ms | 18.1× | 7/7 | 485.1ms | 335.2ms | 108.8 MB | 7/7 | 13848 |
| elixir | 20.3ms | 2.4× | 3/7 | 200.7ms | 180.4ms | 73.3 MB | 6/7 | 13848 |
| python | 119.8ms | 14.4× | 6/7 | 130.3ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.0× | 2/7 | 26.0ms | 17.5ms | 48.2 MB | 5/7 | 13848 |
| ruby | 116.4ms | 14.0× | 5/7 | 155.5ms | 39.1ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.3ms | 1.0× | 1/7 | 30.1ms | 21.8ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.3ms | 1.7× | 2/7 | 104.0ms | 29.7ms | 28.3 MB | 4/7 | 442 |
| clojure | 435.6ms | 9.7× | 5/7 | 770.8ms | 335.2ms | 371.1 MB | 7/7 | 442 |
| elixir | 106.4ms | 2.4× | 3/7 | 286.8ms | 180.4ms | 70.4 MB | 6/7 | 442 |
| python | 2.471s | 54.9× | 7/7 | 2.482s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 173.5ms | 3.9× | 4/7 | 191.0ms | 17.5ms | 48.0 MB | 5/7 | 442 |
| ruby | 837.4ms | 18.6× | 6/7 | 876.5ms | 39.1ms | 19.3 MB | 2/7 | 442 |
| dotnet | 45.0ms | 1.0× | 1/7 | 66.8ms | 21.8ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 216.1ms | 12.0× | 4/7 | 245.8ms | 29.7ms | 28.1 MB | 4/7 | 6129302 |
| clojure | 168.3ms | 9.4× | 3/7 | 503.5ms | 335.2ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 249.3ms | 13.9× | 5/7 | 429.7ms | 180.4ms | 70.5 MB | 6/7 | 6129302 |
| python | 1.304s | 72.4× | 7/7 | 1.314s | 10.5ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.8ms | 1.2× | 2/7 | 38.3ms | 17.5ms | 49.3 MB | 5/7 | 6129302 |
| ruby | 409.4ms | 22.7× | 6/7 | 448.5ms | 39.1ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 18.0ms | 1.0× | 1/7 | 39.8ms | 21.8ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.7ms | 21.3× | 4/7 | 121.4ms | 29.7ms | 46.8 MB | 4/7 | 654353666 |
| clojure | 197.6ms | 46.0× | 5/7 | 532.8ms | 335.2ms | 118.1 MB | 7/7 | 654353666 |
| elixir | 63.3ms | 14.7× | 3/7 | 243.7ms | 180.4ms | 74.1 MB | 6/7 | 654353666 |
| python | 443.0ms | 103.0× | 7/7 | 453.5ms | 10.5ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.3ms | 3.8× | 2/7 | 33.8ms | 17.5ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 279.7ms | 65.0× | 6/7 | 318.8ms | 39.1ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.3ms | 1.0× | 1/7 | 26.1ms | 21.8ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.6ms | 1.0× | 1/7 | 41.3ms | 29.7ms | 33.0 MB | 1/7 | 3388889 |
| clojure | 165.9ms | 14.3× | 7/7 | 501.1ms | 335.2ms | 169.2 MB | 6/7 | 3388889 |
| elixir | 122.0ms | 10.5× | 6/7 | 302.4ms | 180.4ms | 202.5 MB | 7/7 | 3388889 |
| python | 41.9ms | 3.6× | 3/7 | 52.4ms | 10.5ms | 39.9 MB | 2/7 | 3388889 |
| node | 63.8ms | 5.5× | 4/7 | 81.3ms | 17.5ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 82.4ms | 7.1× | 5/7 | 121.5ms | 39.1ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.0ms | 2.6× | 2/7 | 51.8ms | 21.8ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.2ms | 3.6× | 4/7 | 134.9ms | 29.7ms | 28.9 MB | 4/7 | 374854840 |
| clojure | 277.6ms | 9.5× | 7/7 | 612.8ms | 335.2ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 171.1ms | 5.8× | 6/7 | 351.5ms | 180.4ms | 70.8 MB | 6/7 | 374854840 |
| python | 167.5ms | 5.7× | 5/7 | 178.0ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.3ms | 1.0× | 1/7 | 46.8ms | 17.5ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 68.7ms | 2.3× | 3/7 | 107.8ms | 39.1ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.8ms | 1.3× | 2/7 | 58.6ms | 21.8ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 97.8ms | 6.7× | 6/7 | 127.5ms | 29.7ms | 41.0 MB | 4/7 | 1638200 |
| clojure | 170.1ms | 11.7× | 7/7 | 505.3ms | 335.2ms | 149.8 MB | 7/7 | 1638200 |
| elixir | 15.3ms | 1.1× | 2/7 | 195.7ms | 180.4ms | 70.8 MB | 6/7 | 1638200 |
| python | 93.3ms | 6.4× | 4/7 | 103.8ms | 10.5ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.1ms | 1.4× | 3/7 | 37.6ms | 17.5ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 95.2ms | 6.6× | 5/7 | 134.3ms | 39.1ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.5ms | 1.0× | 1/7 | 36.3ms | 21.8ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.9ms | 2.7× | 5/7 | 203.6ms | 29.7ms | 137.3 MB | 6/7 | 46468819 |
| clojure | 241.6ms | 3.7× | 7/7 | 576.8ms | 335.2ms | 123.5 MB | 5/7 | 46468819 |
| elixir | 119.5ms | 1.8× | 4/7 | 299.9ms | 180.4ms | 157.7 MB | 7/7 | 46468819 |
| python | 185.5ms | 2.9× | 6/7 | 196.0ms | 10.5ms | 25.8 MB | 2/7 | 46468819 |
| node | 102.3ms | 1.6× | 3/7 | 119.8ms | 17.5ms | 64.5 MB | 4/7 | 46468819 |
| ruby | 70.9ms | 1.1× | 2/7 | 110.0ms | 39.1ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 64.8ms | 1.0× | 1/7 | 86.6ms | 21.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.8ms | 13.8× | 5/7 | 126.5ms | 29.7ms | 32.1 MB | 4/7 | 724 |
| clojure | 203.9ms | 29.1× | 7/7 | 539.1ms | 335.2ms | 132.7 MB | 7/7 | 724 |
| elixir | 13.0ms | 1.9× | 2/7 | 193.4ms | 180.4ms | 70.0 MB | 6/7 | 724 |
| python | 53.0ms | 7.6× | 4/7 | 63.5ms | 10.5ms | 9.8 MB | 1/7 | 724 |
| node | 7.0ms | 1.0× | 1/7 | 24.5ms | 17.5ms | 50.5 MB | 5/7 | 724 |
| ruby | 133.5ms | 19.1× | 6/7 | 172.6ms | 39.1ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.1ms | 2.9× | 3/7 | 41.9ms | 21.8ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.8ms | 1.7× | 2/7 | 68.5ms | 29.7ms | 25.5 MB | 3/7 | 9900000 |
| clojure | 1.090s | 47.2× | 7/7 | 1.426s | 335.2ms | 371.5 MB | 7/7 | 9900000 |
| elixir | 23.1ms | 1.0× | 1/7 | 203.5ms | 180.4ms | 71.4 MB | 6/7 | 9900000 |
| python | 48.3ms | 2.1× | 3/7 | 58.8ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 559.5ms | 24.2× | 6/7 | 577.0ms | 17.5ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 109.2ms | 4.7× | 4/7 | 148.3ms | 39.1ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 284.3ms | 12.3× | 5/7 | 306.1ms | 21.8ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 49.2ms | 6.6× | 2/7 | 78.9ms | 29.7ms | 28.4 MB | 3/7 | 2475000 |
| clojure | 1.332s | 177.6× | 7/7 | 1.667s | 335.2ms | 374.3 MB | 7/7 | 2475000 |
| elixir | 7.5ms | 1.0× | 1/7 | 187.9ms | 180.4ms | 72.6 MB | 6/7 | 2475000 |
| python | 216.2ms | 28.8× | 5/7 | 226.7ms | 10.5ms | 9.8 MB | 1/7 | 2475000 |
| node | 207.0ms | 27.6× | 4/7 | 224.5ms | 17.5ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 114.0ms | 15.2× | 3/7 | 153.1ms | 39.1ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 688.8ms | 91.8× | 6/7 | 710.6ms | 21.8ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 7.0× | 6/7 | 61.7ms | 29.7ms | 27.8 MB | 3/7 | 155553889038886 |
| clojure | 136.0ms | 29.6× | 7/7 | 471.2ms | 335.2ms | 109.2 MB | 7/7 | 155553889038886 |
| elixir | 10.2ms | 2.2× | 5/7 | 190.6ms | 180.4ms | 71.7 MB | 6/7 | 155553889038886 |
| python | 4.6ms | 1.0× | 1/7 | 15.1ms | 10.5ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.8ms | 1.7× | 4/7 | 25.3ms | 17.5ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.7ms | 1.7× | 3/7 | 46.8ms | 39.1ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.2ms | 1.6× | 2/7 | 29.0ms | 21.8ms | 28.2 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.0ms | 6.3× | 4/7 | 141.7ms | 29.7ms | 74.7 MB | 4/7 | 6100000 |
| clojure | 205.4ms | 11.5× | 5/7 | 540.6ms | 335.2ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 26.7ms | 1.5× | 2/7 | 207.1ms | 180.4ms | 75.3 MB | 5/7 | 6100000 |
| python | 548.3ms | 30.8× | 6/7 | 558.8ms | 10.5ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.3ms | 2.9× | 3/7 | 69.8ms | 17.5ms | 50.9 MB | 3/7 | 6100000 |
| ruby | 1.590s | 89.3× | 7/7 | 1.629s | 39.1ms | 133.4 MB | 6/7 | 6100000 |
| dotnet | 17.8ms | 1.0× | 1/7 | 39.6ms | 21.8ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 398.4ms | 11.8× | 5/7 | 428.1ms | 29.7ms | 34.7 MB | 4/7 | 31781100 |
| clojure | 217.9ms | 6.4× | 4/7 | 553.1ms | 335.2ms | 133.8 MB | 6/7 | 31781100 |
| elixir | 78.3ms | 2.3× | 2/7 | 258.7ms | 180.4ms | 71.7 MB | 5/7 | 31781100 |
| python | 685.3ms | 20.3× | 7/7 | 695.8ms | 10.5ms | 22.2 MB | 2/7 | 31781100 |
| node | 109.6ms | 3.2× | 3/7 | 127.1ms | 17.5ms | 181.1 MB | 7/7 | 31781100 |
| ruby | 423.3ms | 12.5× | 6/7 | 462.4ms | 39.1ms | 19.4 MB | 1/7 | 31781100 |
| dotnet | 33.8ms | 1.0× | 1/7 | 55.6ms | 21.8ms | 28.0 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.1ms | 1.2× | 2/7 | 174.8ms | 29.7ms | 123.4 MB | 5/7 | 500 |
| clojure | 824.6ms | 7.1× | 7/7 | 1.160s | 335.2ms | 288.3 MB | 6/7 | 500 |
| elixir | 554.2ms | 4.7× | 6/7 | 734.6ms | 180.4ms | 505.6 MB | 7/7 | 500 |
| python | 171.6ms | 1.5× | 4/7 | 182.1ms | 10.5ms | 44.3 MB | 1/7 | 500 |
| node | 116.7ms | 1.0× | 1/7 | 134.2ms | 17.5ms | 65.0 MB | 4/7 | 500 |
| ruby | 211.7ms | 1.8× | 5/7 | 250.8ms | 39.1ms | 45.9 MB | 2/7 | 500 |
| dotnet | 150.6ms | 1.3× | 3/7 | 172.4ms | 21.8ms | 48.1 MB | 3/7 | 500 |
