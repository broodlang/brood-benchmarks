# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-06 09:44.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.1ms | 3.0× | 4/7 | 31.1ms | — | 25.6 MB | 3/7 | 0 |
| clojure | 339.6ms | 33.3× | 7/7 | 339.6ms | — | 103.4 MB | 7/7 | 0 |
| elixir | 195.4ms | 19.2× | 6/7 | 195.4ms | — | 72.0 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.0ms | 1.8× | 2/7 | 18.0ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 40.9ms | 4.0× | 5/7 | 40.9ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.4ms | 2.1× | 3/7 | 21.4ms | — | 25.6 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.3ms | 1.2× | 2/7 | 85.4ms | 31.1ms | 29.1 MB | 4/7 | 9227465 |
| clojure | 218.8ms | 5.0× | 5/7 | 558.4ms | 339.6ms | 107.4 MB | 7/7 | 9227465 |
| elixir | 71.3ms | 1.6× | 3/7 | 266.7ms | 195.4ms | 71.1 MB | 6/7 | 9227465 |
| python | 748.5ms | 16.9× | 7/7 | 758.7ms | 10.2ms | 9.7 MB | 1/7 | 9227465 |
| node | 74.4ms | 1.7× | 4/7 | 92.4ms | 18.0ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 616.4ms | 13.9× | 6/7 | 657.3ms | 40.9ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 44.2ms | 1.0× | 1/7 | 65.6ms | 21.4ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.4ms | 2.7× | 3/7 | 69.5ms | 31.1ms | 29.0 MB | 4/7 | 449999985000000 |
| clojure | 158.3ms | 11.0× | 5/7 | 497.9ms | 339.6ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 55.2ms | 3.8× | 4/7 | 250.6ms | 195.4ms | 70.0 MB | 6/7 | 449999985000000 |
| python | 2.450s | 170.2× | 7/7 | 2.461s | 10.2ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 31.3ms | 2.2× | 2/7 | 49.3ms | 18.0ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 578.8ms | 40.2× | 6/7 | 619.7ms | 40.9ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 14.4ms | 1.0× | 1/7 | 35.8ms | 21.4ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.7ms | 1.0× | 1/7 | 33.8ms | 31.1ms | 25.2 MB | 3/7 | 12499997500000 |
| clojure | 199.9ms | 74.0× | 5/7 | 539.5ms | 339.6ms | 220.4 MB | 7/7 | 12499997500000 |
| elixir | 25.4ms | 9.4× | 3/7 | 220.8ms | 195.4ms | 71.9 MB | 5/7 | 12499997500000 |
| python | 116.3ms | 43.1× | 4/7 | 126.5ms | 10.2ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 226.7ms | 84.0× | 7/7 | 244.7ms | 18.0ms | 90.2 MB | 6/7 | 12499997500000 |
| ruby | 222.4ms | 82.4× | 6/7 | 263.3ms | 40.9ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 12.6ms | 4.7× | 2/7 | 34.0ms | 21.4ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.6ms | 5.0× | 4/7 | 67.7ms | 31.1ms | 29.4 MB | 4/7 | 13848 |
| clojure | 166.0ms | 22.7× | 7/7 | 505.6ms | 339.6ms | 108.9 MB | 7/7 | 13848 |
| elixir | 7.3ms | 1.0× | 1/7 | 202.7ms | 195.4ms | 70.8 MB | 6/7 | 13848 |
| python | 124.0ms | 17.0× | 6/7 | 134.2ms | 10.2ms | 9.9 MB | 1/7 | 13848 |
| node | 11.1ms | 1.5× | 3/7 | 29.1ms | 18.0ms | 48.6 MB | 5/7 | 13848 |
| ruby | 117.1ms | 16.0× | 5/7 | 158.0ms | 40.9ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.9ms | 1.2× | 2/7 | 30.3ms | 21.4ms | 26.2 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.2ms | 1.7× | 2/7 | 112.3ms | 31.1ms | 29.0 MB | 4/7 | 442 |
| clojure | 451.9ms | 9.6× | 5/7 | 791.5ms | 339.6ms | 371.1 MB | 7/7 | 442 |
| elixir | 94.1ms | 2.0× | 3/7 | 289.5ms | 195.4ms | 70.8 MB | 6/7 | 442 |
| python | 2.446s | 51.9× | 7/7 | 2.457s | 10.2ms | 9.7 MB | 1/7 | 442 |
| node | 174.7ms | 3.7× | 4/7 | 192.7ms | 18.0ms | 48.4 MB | 5/7 | 442 |
| ruby | 871.8ms | 18.5× | 6/7 | 912.7ms | 40.9ms | 19.3 MB | 2/7 | 442 |
| dotnet | 47.1ms | 1.0× | 1/7 | 68.5ms | 21.4ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 216.8ms | 10.5× | 4/7 | 247.9ms | 31.1ms | 29.4 MB | 4/7 | 6129302 |
| clojure | 165.2ms | 8.0× | 3/7 | 504.8ms | 339.6ms | 115.2 MB | 7/7 | 6129302 |
| elixir | 273.4ms | 13.3× | 5/7 | 468.8ms | 195.4ms | 72.9 MB | 6/7 | 6129302 |
| python | 1.396s | 67.8× | 7/7 | 1.407s | 10.2ms | 9.9 MB | 1/7 | 6129302 |
| node | 22.8ms | 1.1× | 2/7 | 40.8ms | 18.0ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 412.5ms | 20.0× | 6/7 | 453.4ms | 40.9ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 20.6ms | 1.0× | 1/7 | 42.0ms | 21.4ms | 26.2 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.4ms | 18.9× | 4/7 | 125.5ms | 31.1ms | 43.2 MB | 4/7 | 654353666 |
| clojure | 197.1ms | 39.4× | 5/7 | 536.7ms | 339.6ms | 117.7 MB | 7/7 | 654353666 |
| elixir | 49.3ms | 9.9× | 3/7 | 244.7ms | 195.4ms | 78.0 MB | 6/7 | 654353666 |
| python | 457.9ms | 91.6× | 7/7 | 468.1ms | 10.2ms | 10.4 MB | 1/7 | 654353666 |
| node | 17.1ms | 3.4× | 2/7 | 35.1ms | 18.0ms | 52.1 MB | 5/7 | 654353666 |
| ruby | 317.6ms | 63.5× | 6/7 | 358.5ms | 40.9ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.0ms | 1.0× | 1/7 | 26.4ms | 21.4ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.8ms | 1.0× | 1/7 | 42.9ms | 31.1ms | 33.1 MB | 1/7 | 3388889 |
| clojure | 168.7ms | 14.3× | 7/7 | 508.3ms | 339.6ms | 168.2 MB | 6/7 | 3388889 |
| elixir | 105.5ms | 8.9× | 6/7 | 300.9ms | 195.4ms | 199.7 MB | 7/7 | 3388889 |
| python | 42.7ms | 3.6× | 3/7 | 52.9ms | 10.2ms | 39.8 MB | 2/7 | 3388889 |
| node | 65.4ms | 5.5× | 4/7 | 83.4ms | 18.0ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 82.8ms | 7.0× | 5/7 | 123.7ms | 40.9ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 32.5ms | 2.8× | 2/7 | 53.9ms | 21.4ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.9ms | 3.8× | 4/7 | 145.0ms | 31.1ms | 29.9 MB | 4/7 | 374854840 |
| clojure | 279.2ms | 9.2× | 7/7 | 618.8ms | 339.6ms | 302.6 MB | 7/7 | 374854840 |
| elixir | 150.5ms | 5.0× | 5/7 | 345.9ms | 195.4ms | 70.2 MB | 6/7 | 374854840 |
| python | 174.8ms | 5.8× | 6/7 | 185.0ms | 10.2ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.3ms | 1.0× | 1/7 | 48.3ms | 18.0ms | 50.1 MB | 5/7 | 374854840 |
| ruby | 75.1ms | 2.5× | 3/7 | 116.0ms | 40.9ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 37.6ms | 1.2× | 2/7 | 59.0ms | 21.4ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 89.6ms | 89.6× | 4/7 | 120.7ms | 31.1ms | 50.9 MB | 4/7 | 1638200 |
| clojure | 175.6ms | 175.6× | 7/7 | 515.2ms | 339.6ms | 149.9 MB | 7/7 | 1638200 |
| elixir | 0.0ms | < 1× | 1/7 | 194.7ms | 195.4ms | 70.9 MB | 6/7 | 1638200 |
| python | 93.6ms | 93.6× | 5/7 | 103.8ms | 10.2ms | 10.0 MB | 1/7 | 1638200 |
| node | 21.8ms | 21.8× | 3/7 | 39.8ms | 18.0ms | 56.0 MB | 5/7 | 1638200 |
| ruby | 97.4ms | 97.4× | 6/7 | 138.3ms | 40.9ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 15.7ms | 15.7× | 2/7 | 37.1ms | 21.4ms | 32.1 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.5ms | 2.2× | 5/7 | 179.6ms | 31.1ms | 165.7 MB | 7/7 | 46468819 |
| clojure | 266.2ms | 4.0× | 7/7 | 605.8ms | 339.6ms | 124.4 MB | 5/7 | 46468819 |
| elixir | 102.5ms | 1.5× | 4/7 | 297.9ms | 195.4ms | 157.5 MB | 6/7 | 46468819 |
| python | 185.5ms | 2.8× | 6/7 | 195.7ms | 10.2ms | 25.9 MB | 2/7 | 46468819 |
| node | 101.9ms | 1.5× | 3/7 | 119.9ms | 18.0ms | 64.8 MB | 4/7 | 46468819 |
| ruby | 74.0ms | 1.1× | 2/7 | 114.9ms | 40.9ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 66.2ms | 1.0× | 1/7 | 87.6ms | 21.4ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.9ms | 80.9× | 5/7 | 112.0ms | 31.1ms | 41.4 MB | 4/7 | 724 |
| clojure | 237.3ms | 237.3× | 7/7 | 576.9ms | 339.6ms | 132.5 MB | 7/7 | 724 |
| elixir | 0.0ms | < 1× | 1/7 | 192.1ms | 195.4ms | 69.7 MB | 6/7 | 724 |
| python | 53.7ms | 53.7× | 4/7 | 63.9ms | 10.2ms | 9.7 MB | 1/7 | 724 |
| node | 7.5ms | 7.5× | 2/7 | 25.5ms | 18.0ms | 50.5 MB | 5/7 | 724 |
| ruby | 126.8ms | 126.8× | 6/7 | 167.7ms | 40.9ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.1ms | 20.1× | 3/7 | 41.5ms | 21.4ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 4.2× | 2/7 | 74.2ms | 31.1ms | 29.3 MB | 3/7 | 9900000 |
| clojure | 1.113s | 109.1× | 7/7 | 1.452s | 339.6ms | 371.5 MB | 7/7 | 9900000 |
| elixir | 10.2ms | 1.0× | 1/7 | 205.6ms | 195.4ms | 70.4 MB | 6/7 | 9900000 |
| python | 50.0ms | 4.9× | 3/7 | 60.2ms | 10.2ms | 9.7 MB | 1/7 | 9900000 |
| node | 574.2ms | 56.3× | 6/7 | 592.2ms | 18.0ms | 50.3 MB | 5/7 | 9900000 |
| ruby | 106.5ms | 10.4× | 4/7 | 147.4ms | 40.9ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 285.2ms | 28.0× | 5/7 | 306.6ms | 21.4ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.6ms | 51.6× | 2/7 | 82.7ms | 31.1ms | 28.9 MB | 3/7 | 2475000 |
| clojure | 1.385s | 1384.9× | 7/7 | 1.724s | 339.6ms | 375.3 MB | 7/7 | 2475000 |
| elixir | 0.0ms | < 1× | 1/7 | 188.6ms | 195.4ms | 70.7 MB | 6/7 | 2475000 |
| python | 225.4ms | 225.4× | 5/7 | 235.6ms | 10.2ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.8ms | 210.8× | 4/7 | 228.8ms | 18.0ms | 50.2 MB | 5/7 | 2475000 |
| ruby | 115.3ms | 115.3× | 3/7 | 156.2ms | 40.9ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 709.9ms | 709.9× | 6/7 | 731.3ms | 21.4ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.9ms | 26.9× | 6/7 | 58.0ms | 31.1ms | 29.2 MB | 4/7 | 155553889038886 |
| clojure | 152.4ms | 152.4× | 7/7 | 492.0ms | 339.6ms | 109.0 MB | 7/7 | 155553889038886 |
| elixir | 0.0ms | < 1× | 1/7 | 192.9ms | 195.4ms | 72.7 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 4.5× | 2/7 | 14.7ms | 10.2ms | 9.7 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 7.7× | 4/7 | 25.7ms | 18.0ms | 52.0 MB | 5/7 | 155553889038886 |
| ruby | 6.3ms | 6.3× | 3/7 | 47.2ms | 40.9ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.5ms | 8.5× | 5/7 | 29.9ms | 21.4ms | 27.9 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.6ms | 7.3× | 4/7 | 140.7ms | 31.1ms | 85.7 MB | 5/7 | 6100000 |
| clojure | 206.3ms | 13.7× | 5/7 | 545.9ms | 339.6ms | 135.0 MB | 7/7 | 6100000 |
| elixir | 15.1ms | 1.0× | 1/7 | 210.5ms | 195.4ms | 76.8 MB | 4/7 | 6100000 |
| python | 552.5ms | 36.6× | 6/7 | 562.7ms | 10.2ms | 28.0 MB | 1/7 | 6100000 |
| node | 53.6ms | 3.5× | 3/7 | 71.6ms | 18.0ms | 51.6 MB | 3/7 | 6100000 |
| ruby | 1.647s | 109.0× | 7/7 | 1.687s | 40.9ms | 133.0 MB | 6/7 | 6100000 |
| dotnet | 18.8ms | 1.2× | 2/7 | 40.2ms | 21.4ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 167.8ms | 1.5× | 2/7 | 198.9ms | 31.1ms | 32.0 MB | 4/7 | 134626900 |
| clojure | 403.1ms | 3.5× | 5/7 | 742.7ms | 339.6ms | 136.0 MB | 6/7 | 134626900 |
| elixir | 297.2ms | 2.6× | 3/7 | 492.6ms | 195.4ms | 71.7 MB | 5/7 | 134626900 |
| python | 2.644s | 23.3× | 7/7 | 2.654s | 10.2ms | 22.0 MB | 2/7 | 134626900 |
| node | 300.6ms | 2.6× | 4/7 | 318.6ms | 18.0ms | 181.8 MB | 7/7 | 134626900 |
| ruby | 1.905s | 16.8× | 6/7 | 1.946s | 40.9ms | 19.3 MB | 1/7 | 134626900 |
| dotnet | 113.7ms | 1.0× | 1/7 | 135.1ms | 21.4ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.5ms | 1.2× | 2/7 | 178.6ms | 31.1ms | 124.6 MB | 5/7 | 500 |
| clojure | 806.8ms | 6.5× | 7/7 | 1.146s | 339.6ms | 281.5 MB | 6/7 | 500 |
| elixir | 588.3ms | 4.7× | 6/7 | 783.7ms | 195.4ms | 472.0 MB | 7/7 | 500 |
| python | 172.8ms | 1.4× | 4/7 | 183.0ms | 10.2ms | 45.0 MB | 1/7 | 500 |
| node | 124.1ms | 1.0× | 1/7 | 142.1ms | 18.0ms | 65.0 MB | 4/7 | 500 |
| ruby | 202.6ms | 1.6× | 5/7 | 243.5ms | 40.9ms | 46.0 MB | 2/7 | 500 |
| dotnet | 154.0ms | 1.2× | 3/7 | 175.4ms | 21.4ms | 48.3 MB | 3/7 | 500 |
