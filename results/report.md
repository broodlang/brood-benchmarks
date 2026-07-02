# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 19:08.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.1ms | 2.8× | 4/7 | 29.1ms | — | 23.8 MB | 3/7 | 0 |
| clojure | 338.4ms | 32.5× | 7/7 | 338.4ms | — | 103.2 MB | 7/7 | 0 |
| elixir | 184.8ms | 17.8× | 6/7 | 184.8ms | — | 70.6 MB | 6/7 | 0 |
| python | 10.4ms | 1.0× | 1/7 | 10.4ms | — | 9.5 MB | 1/7 | 0 |
| node | 17.8ms | 1.7× | 2/7 | 17.8ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 38.9ms | 3.7× | 5/7 | 38.9ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.9ms | 2.1× | 3/7 | 21.9ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.1ms | 1.3× | 2/7 | 81.2ms | 29.1ms | 26.8 MB | 4/7 | 9227465 |
| clojure | 199.5ms | 5.0× | 5/7 | 537.9ms | 338.4ms | 108.8 MB | 7/7 | 9227465 |
| elixir | 73.8ms | 1.8× | 4/7 | 258.6ms | 184.8ms | 70.0 MB | 6/7 | 9227465 |
| python | 730.4ms | 18.2× | 7/7 | 740.8ms | 10.4ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.7ms | 1.8× | 3/7 | 91.5ms | 17.8ms | 47.9 MB | 5/7 | 9227465 |
| ruby | 603.3ms | 15.0× | 6/7 | 642.2ms | 38.9ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 40.2ms | 1.0× | 1/7 | 62.1ms | 21.9ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 3.3× | 3/7 | 65.2ms | 29.1ms | 27.3 MB | 4/7 | 449999985000000 |
| clojure | 142.5ms | 13.0× | 5/7 | 480.9ms | 338.4ms | 108.3 MB | 7/7 | 449999985000000 |
| elixir | 54.1ms | 4.9× | 4/7 | 238.9ms | 184.8ms | 70.6 MB | 6/7 | 449999985000000 |
| python | 2.407s | 218.8× | 7/7 | 2.417s | 10.4ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.7ms | 2.7× | 2/7 | 47.5ms | 17.8ms | 49.9 MB | 5/7 | 449999985000000 |
| ruby | 593.0ms | 53.9× | 6/7 | 631.9ms | 38.9ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.0ms | 1.0× | 1/7 | 32.9ms | 21.9ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.6ms | 1.0× | 1/7 | 32.7ms | 29.1ms | 23.7 MB | 3/7 | 12499997500000 |
| clojure | 182.7ms | 50.7× | 5/7 | 521.1ms | 338.4ms | 221.0 MB | 7/7 | 12499997500000 |
| elixir | 35.2ms | 9.8× | 3/7 | 220.0ms | 184.8ms | 71.9 MB | 5/7 | 12499997500000 |
| python | 106.2ms | 29.5× | 4/7 | 116.6ms | 10.4ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 218.1ms | 60.6× | 6/7 | 235.9ms | 17.8ms | 90.0 MB | 6/7 | 12499997500000 |
| ruby | 227.3ms | 63.1× | 7/7 | 266.2ms | 38.9ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 12.7ms | 3.5× | 2/7 | 34.6ms | 21.9ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.3ms | 4.0× | 4/7 | 62.4ms | 29.1ms | 27.4 MB | 4/7 | 13848 |
| clojure | 144.5ms | 17.4× | 7/7 | 482.9ms | 338.4ms | 108.8 MB | 7/7 | 13848 |
| elixir | 15.9ms | 1.9× | 3/7 | 200.7ms | 184.8ms | 72.5 MB | 6/7 | 13848 |
| python | 121.3ms | 14.6× | 6/7 | 131.7ms | 10.4ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.0× | 2/7 | 26.3ms | 17.8ms | 48.5 MB | 5/7 | 13848 |
| ruby | 117.2ms | 14.1× | 5/7 | 156.1ms | 38.9ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.3ms | 1.0× | 1/7 | 30.2ms | 21.9ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.3ms | 1.7× | 2/7 | 104.4ms | 29.1ms | 27.3 MB | 4/7 | 442 |
| clojure | 430.0ms | 9.5× | 5/7 | 768.4ms | 338.4ms | 370.8 MB | 7/7 | 442 |
| elixir | 102.3ms | 2.3× | 3/7 | 287.1ms | 184.8ms | 73.0 MB | 6/7 | 442 |
| python | 2.479s | 54.8× | 7/7 | 2.489s | 10.4ms | 9.8 MB | 1/7 | 442 |
| node | 172.3ms | 3.8× | 4/7 | 190.1ms | 17.8ms | 48.2 MB | 5/7 | 442 |
| ruby | 836.2ms | 18.5× | 6/7 | 875.1ms | 38.9ms | 19.3 MB | 2/7 | 442 |
| dotnet | 45.2ms | 1.0× | 1/7 | 67.1ms | 21.9ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 217.4ms | 11.8× | 4/7 | 246.5ms | 29.1ms | 27.2 MB | 4/7 | 6129302 |
| clojure | 174.3ms | 9.5× | 3/7 | 512.7ms | 338.4ms | 115.9 MB | 7/7 | 6129302 |
| elixir | 252.5ms | 13.7× | 5/7 | 437.3ms | 184.8ms | 72.1 MB | 6/7 | 6129302 |
| python | 1.335s | 72.6× | 7/7 | 1.345s | 10.4ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.7ms | 1.1× | 2/7 | 38.5ms | 17.8ms | 49.7 MB | 5/7 | 6129302 |
| ruby | 419.1ms | 22.8× | 6/7 | 458.0ms | 38.9ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 18.4ms | 1.0× | 1/7 | 40.3ms | 21.9ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.4ms | 16.6× | 4/7 | 120.5ms | 29.1ms | 40.8 MB | 4/7 | 654353666 |
| clojure | 197.5ms | 35.9× | 5/7 | 535.9ms | 338.4ms | 118.9 MB | 7/7 | 654353666 |
| elixir | 59.1ms | 10.7× | 3/7 | 243.9ms | 184.8ms | 77.4 MB | 6/7 | 654353666 |
| python | 467.0ms | 84.9× | 7/7 | 477.4ms | 10.4ms | 10.5 MB | 1/7 | 654353666 |
| node | 15.1ms | 2.7× | 2/7 | 32.9ms | 17.8ms | 52.2 MB | 5/7 | 654353666 |
| ruby | 286.4ms | 52.1× | 6/7 | 325.3ms | 38.9ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.5ms | 1.0× | 1/7 | 27.4ms | 21.9ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.0ms | 1.0× | 1/7 | 40.1ms | 29.1ms | 30.1 MB | 1/7 | 3388889 |
| clojure | 169.2ms | 15.4× | 7/7 | 507.6ms | 338.4ms | 168.5 MB | 6/7 | 3388889 |
| elixir | 118.1ms | 10.7× | 6/7 | 302.9ms | 184.8ms | 203.0 MB | 7/7 | 3388889 |
| python | 43.2ms | 3.9× | 3/7 | 53.6ms | 10.4ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.4ms | 5.9× | 4/7 | 82.2ms | 17.8ms | 95.0 MB | 5/7 | 3388889 |
| ruby | 83.1ms | 7.6× | 5/7 | 122.0ms | 38.9ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.3ms | 2.8× | 2/7 | 52.2ms | 21.9ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.0ms | 3.7× | 4/7 | 138.1ms | 29.1ms | 28.2 MB | 4/7 | 374854840 |
| clojure | 292.1ms | 9.8× | 7/7 | 630.5ms | 338.4ms | 302.8 MB | 7/7 | 374854840 |
| elixir | 170.6ms | 5.7× | 5/7 | 355.4ms | 184.8ms | 71.5 MB | 6/7 | 374854840 |
| python | 179.4ms | 6.0× | 6/7 | 189.8ms | 10.4ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.7ms | 1.0× | 1/7 | 47.5ms | 17.8ms | 49.9 MB | 5/7 | 374854840 |
| ruby | 74.7ms | 2.5× | 3/7 | 113.6ms | 38.9ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 37.1ms | 1.2× | 2/7 | 59.0ms | 21.9ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.6ms | 6.0× | 4/7 | 116.7ms | 29.1ms | 44.2 MB | 4/7 | 1638200 |
| clojure | 189.0ms | 13.0× | 7/7 | 527.4ms | 338.4ms | 150.6 MB | 7/7 | 1638200 |
| elixir | 15.3ms | 1.1× | 2/7 | 200.1ms | 184.8ms | 70.2 MB | 6/7 | 1638200 |
| python | 95.7ms | 6.6× | 5/7 | 106.1ms | 10.4ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.5ms | 1.5× | 3/7 | 39.3ms | 17.8ms | 55.8 MB | 5/7 | 1638200 |
| ruby | 102.0ms | 7.0× | 6/7 | 140.9ms | 38.9ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.5ms | 1.0× | 1/7 | 36.4ms | 21.9ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.1ms | 2.3× | 5/7 | 177.2ms | 29.1ms | 154.5 MB | 6/7 | 46468819 |
| clojure | 260.5ms | 4.0× | 7/7 | 598.9ms | 338.4ms | 123.2 MB | 5/7 | 46468819 |
| elixir | 114.7ms | 1.8× | 4/7 | 299.5ms | 184.8ms | 158.5 MB | 7/7 | 46468819 |
| python | 189.3ms | 2.9× | 6/7 | 199.7ms | 10.4ms | 25.8 MB | 2/7 | 46468819 |
| node | 103.5ms | 1.6× | 3/7 | 121.3ms | 17.8ms | 64.9 MB | 4/7 | 46468819 |
| ruby | 71.6ms | 1.1× | 2/7 | 110.5ms | 38.9ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 65.3ms | 1.0× | 1/7 | 87.2ms | 21.9ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.4ms | 14.5× | 5/7 | 124.5ms | 29.1ms | 42.2 MB | 4/7 | 724 |
| clojure | 274.1ms | 41.5× | 7/7 | 612.5ms | 338.4ms | 136.0 MB | 7/7 | 724 |
| elixir | 6.8ms | 1.0× | 2/7 | 191.6ms | 184.8ms | 71.0 MB | 6/7 | 724 |
| python | 54.3ms | 8.2× | 4/7 | 64.7ms | 10.4ms | 9.8 MB | 1/7 | 724 |
| node | 6.6ms | 1.0× | 1/7 | 24.4ms | 17.8ms | 50.4 MB | 5/7 | 724 |
| ruby | 124.4ms | 18.8× | 6/7 | 163.3ms | 38.9ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.6ms | 3.0× | 3/7 | 41.5ms | 21.9ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.4ms | 2.0× | 2/7 | 69.5ms | 29.1ms | 24.6 MB | 3/7 | 9900000 |
| clojure | 1.099s | 53.1× | 7/7 | 1.438s | 338.4ms | 371.1 MB | 7/7 | 9900000 |
| elixir | 20.7ms | 1.0× | 1/7 | 205.5ms | 184.8ms | 70.5 MB | 6/7 | 9900000 |
| python | 48.5ms | 2.3× | 3/7 | 58.9ms | 10.4ms | 9.8 MB | 1/7 | 9900000 |
| node | 566.8ms | 27.4× | 6/7 | 584.6ms | 17.8ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 111.0ms | 5.4× | 4/7 | 149.9ms | 38.9ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 290.6ms | 14.0× | 5/7 | 312.5ms | 21.9ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.7ms | 5.8× | 2/7 | 82.8ms | 29.1ms | 27.6 MB | 3/7 | 2475000 |
| clojure | 1.382s | 150.3× | 7/7 | 1.721s | 338.4ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 9.2ms | 1.0× | 1/7 | 194.0ms | 184.8ms | 70.2 MB | 6/7 | 2475000 |
| python | 222.4ms | 24.2× | 5/7 | 232.8ms | 10.4ms | 9.8 MB | 1/7 | 2475000 |
| node | 212.4ms | 23.1× | 4/7 | 230.2ms | 17.8ms | 49.8 MB | 5/7 | 2475000 |
| ruby | 115.2ms | 12.5× | 3/7 | 154.1ms | 38.9ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 694.0ms | 75.4× | 6/7 | 715.9ms | 21.9ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.8ms | 6.8× | 6/7 | 56.9ms | 29.1ms | 27.3 MB | 3/7 | 155553889038886 |
| clojure | 143.3ms | 35.0× | 7/7 | 481.7ms | 338.4ms | 109.0 MB | 7/7 | 155553889038886 |
| elixir | 9.3ms | 2.3× | 5/7 | 194.1ms | 184.8ms | 73.0 MB | 6/7 | 155553889038886 |
| python | 4.1ms | 1.0× | 1/7 | 14.5ms | 10.4ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.8ms | 2.1× | 4/7 | 26.6ms | 17.8ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 8.2ms | 2.0× | 3/7 | 47.1ms | 38.9ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.1ms | 1.7× | 2/7 | 29.0ms | 21.9ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 93.3ms | 5.6× | 4/7 | 122.4ms | 29.1ms | 68.9 MB | 4/7 | 6100000 |
| clojure | 215.7ms | 12.9× | 5/7 | 554.1ms | 338.4ms | 134.5 MB | 7/7 | 6100000 |
| elixir | 23.8ms | 1.4× | 2/7 | 208.6ms | 184.8ms | 77.7 MB | 5/7 | 6100000 |
| python | 552.5ms | 33.1× | 6/7 | 562.9ms | 10.4ms | 28.1 MB | 1/7 | 6100000 |
| node | 53.5ms | 3.2× | 3/7 | 71.3ms | 17.8ms | 51.4 MB | 3/7 | 6100000 |
| ruby | 1.621s | 97.1× | 7/7 | 1.660s | 38.9ms | 133.1 MB | 6/7 | 6100000 |
| dotnet | 16.7ms | 1.0× | 1/7 | 38.6ms | 21.9ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 153.6ms | 1.3× | 2/7 | 182.7ms | 29.1ms | 30.8 MB | 4/7 | 134626900 |
| clojure | 422.2ms | 3.6× | 5/7 | 760.6ms | 338.4ms | 135.6 MB | 6/7 | 134626900 |
| elixir | 313.5ms | 2.7× | 4/7 | 498.3ms | 184.8ms | 73.0 MB | 5/7 | 134626900 |
| python | 2.578s | 22.2× | 7/7 | 2.588s | 10.4ms | 22.2 MB | 2/7 | 134626900 |
| node | 303.0ms | 2.6× | 3/7 | 320.8ms | 17.8ms | 181.8 MB | 7/7 | 134626900 |
| ruby | 1.903s | 16.4× | 6/7 | 1.942s | 38.9ms | 19.4 MB | 1/7 | 134626900 |
| dotnet | 116.1ms | 1.0× | 1/7 | 138.0ms | 21.9ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.8ms | 1.3× | 3/7 | 180.9ms | 29.1ms | 125.4 MB | 5/7 | 500 |
| clojure | 850.6ms | 7.1× | 7/7 | 1.189s | 338.4ms | 301.9 MB | 6/7 | 500 |
| elixir | 579.2ms | 4.8× | 6/7 | 764.0ms | 184.8ms | 475.6 MB | 7/7 | 500 |
| python | 171.9ms | 1.4× | 4/7 | 182.3ms | 10.4ms | 45.4 MB | 1/7 | 500 |
| node | 119.6ms | 1.0× | 1/7 | 137.4ms | 17.8ms | 64.8 MB | 4/7 | 500 |
| ruby | 208.7ms | 1.7× | 5/7 | 247.6ms | 38.9ms | 46.3 MB | 2/7 | 500 |
| dotnet | 149.5ms | 1.2× | 2/7 | 171.4ms | 21.9ms | 48.7 MB | 3/7 | 500 |
