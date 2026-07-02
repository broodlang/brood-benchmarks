# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 17:30.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.0ms | 2.8× | 4/7 | 29.0ms | — | 23.8 MB | 3/7 | 0 |
| clojure | 335.7ms | 32.0× | 7/7 | 335.7ms | — | 103.0 MB | 7/7 | 0 |
| elixir | 180.0ms | 17.1× | 6/7 | 180.0ms | — | 71.7 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.6ms | 1.7× | 2/7 | 17.6ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 38.9ms | 3.7× | 5/7 | 38.9ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.5ms | 2.0× | 3/7 | 21.5ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.9ms | 1.3× | 2/7 | 80.9ms | 29.0ms | 27.2 MB | 4/7 | 9227465 |
| clojure | 199.7ms | 5.1× | 5/7 | 535.4ms | 335.7ms | 109.0 MB | 7/7 | 9227465 |
| elixir | 78.2ms | 2.0× | 4/7 | 258.2ms | 180.0ms | 72.4 MB | 6/7 | 9227465 |
| python | 770.3ms | 19.6× | 7/7 | 780.8ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 74.3ms | 1.9× | 3/7 | 91.9ms | 17.6ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 602.0ms | 15.3× | 6/7 | 640.9ms | 38.9ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.4ms | 1.0× | 1/7 | 60.9ms | 21.5ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 2.9× | 3/7 | 65.1ms | 29.0ms | 27.3 MB | 4/7 | 449999985000000 |
| clojure | 145.4ms | 11.8× | 5/7 | 481.1ms | 335.7ms | 108.0 MB | 7/7 | 449999985000000 |
| elixir | 61.8ms | 5.0× | 4/7 | 241.8ms | 180.0ms | 71.4 MB | 6/7 | 449999985000000 |
| python | 2.267s | 184.3× | 7/7 | 2.278s | 10.5ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.7ms | 2.4× | 2/7 | 47.3ms | 17.6ms | 49.4 MB | 5/7 | 449999985000000 |
| ruby | 562.6ms | 45.7× | 6/7 | 601.5ms | 38.9ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.3ms | 1.0× | 1/7 | 33.8ms | 21.5ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.6ms | 1.0× | 1/7 | 32.6ms | 29.0ms | 23.9 MB | 3/7 | 12499997500000 |
| clojure | 184.9ms | 51.4× | 5/7 | 520.6ms | 335.7ms | 220.9 MB | 7/7 | 12499997500000 |
| elixir | 35.3ms | 9.8× | 3/7 | 215.3ms | 180.0ms | 69.8 MB | 5/7 | 12499997500000 |
| python | 105.4ms | 29.3× | 4/7 | 115.9ms | 10.5ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 230.4ms | 64.0× | 7/7 | 248.0ms | 17.6ms | 89.6 MB | 6/7 | 12499997500000 |
| ruby | 228.7ms | 63.5× | 6/7 | 267.6ms | 38.9ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 12.4ms | 3.4× | 2/7 | 33.9ms | 21.5ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.8ms | 3.8× | 4/7 | 62.8ms | 29.0ms | 27.5 MB | 4/7 | 13848 |
| clojure | 148.1ms | 16.8× | 7/7 | 483.8ms | 335.7ms | 108.9 MB | 7/7 | 13848 |
| elixir | 25.1ms | 2.9× | 3/7 | 205.1ms | 180.0ms | 70.0 MB | 6/7 | 13848 |
| python | 120.1ms | 13.6× | 6/7 | 130.6ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 8.8ms | 1.0× | 1/7 | 26.4ms | 17.6ms | 48.1 MB | 5/7 | 13848 |
| ruby | 116.0ms | 13.2× | 5/7 | 154.9ms | 38.9ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 9.1ms | 1.0× | 2/7 | 30.6ms | 21.5ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.5ms | 1.6× | 2/7 | 103.5ms | 29.0ms | 27.2 MB | 4/7 | 442 |
| clojure | 437.1ms | 9.5× | 5/7 | 772.8ms | 335.7ms | 371.5 MB | 7/7 | 442 |
| elixir | 111.8ms | 2.4× | 3/7 | 291.8ms | 180.0ms | 72.0 MB | 6/7 | 442 |
| python | 2.324s | 50.4× | 7/7 | 2.334s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 173.7ms | 3.8× | 4/7 | 191.3ms | 17.6ms | 48.0 MB | 5/7 | 442 |
| ruby | 848.1ms | 18.4× | 6/7 | 887.0ms | 38.9ms | 19.3 MB | 2/7 | 442 |
| dotnet | 46.1ms | 1.0× | 1/7 | 67.6ms | 21.5ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 214.9ms | 11.7× | 4/7 | 243.9ms | 29.0ms | 27.4 MB | 4/7 | 6129302 |
| clojure | 168.7ms | 9.2× | 3/7 | 504.4ms | 335.7ms | 114.8 MB | 7/7 | 6129302 |
| elixir | 254.9ms | 13.9× | 5/7 | 434.9ms | 180.0ms | 71.8 MB | 6/7 | 6129302 |
| python | 1.338s | 72.7× | 7/7 | 1.348s | 10.5ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.7ms | 1.1× | 2/7 | 38.3ms | 17.6ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 453.8ms | 24.7× | 6/7 | 492.7ms | 38.9ms | 19.6 MB | 2/7 | 6129302 |
| dotnet | 18.4ms | 1.0× | 1/7 | 39.9ms | 21.5ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.9ms | 20.9× | 4/7 | 120.9ms | 29.0ms | 40.5 MB | 4/7 | 654353666 |
| clojure | 198.6ms | 45.1× | 5/7 | 534.3ms | 335.7ms | 119.0 MB | 7/7 | 654353666 |
| elixir | 68.3ms | 15.5× | 3/7 | 248.3ms | 180.0ms | 78.2 MB | 6/7 | 654353666 |
| python | 432.3ms | 98.3× | 7/7 | 442.8ms | 10.5ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.1ms | 3.7× | 2/7 | 33.7ms | 17.6ms | 51.7 MB | 5/7 | 654353666 |
| ruby | 286.9ms | 65.2× | 6/7 | 325.8ms | 38.9ms | 19.6 MB | 2/7 | 654353666 |
| dotnet | 4.4ms | 1.0× | 1/7 | 25.9ms | 21.5ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.2ms | 1.0× | 1/7 | 40.2ms | 29.0ms | 30.5 MB | 1/7 | 3388889 |
| clojure | 166.7ms | 14.9× | 7/7 | 502.4ms | 335.7ms | 168.2 MB | 6/7 | 3388889 |
| elixir | 126.4ms | 11.3× | 6/7 | 306.4ms | 180.0ms | 203.9 MB | 7/7 | 3388889 |
| python | 42.7ms | 3.8× | 3/7 | 53.2ms | 10.5ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.8ms | 5.8× | 4/7 | 82.4ms | 17.6ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 84.9ms | 7.6× | 5/7 | 123.8ms | 38.9ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.6ms | 2.8× | 2/7 | 53.1ms | 21.5ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.6ms | 3.7× | 4/7 | 139.6ms | 29.0ms | 28.3 MB | 4/7 | 374854840 |
| clojure | 285.7ms | 9.5× | 7/7 | 621.4ms | 335.7ms | 302.2 MB | 7/7 | 374854840 |
| elixir | 170.1ms | 5.6× | 5/7 | 350.1ms | 180.0ms | 72.7 MB | 6/7 | 374854840 |
| python | 171.1ms | 5.7× | 6/7 | 181.6ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.2ms | 1.0× | 1/7 | 47.8ms | 17.6ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 70.3ms | 2.3× | 3/7 | 109.2ms | 38.9ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.8ms | 1.2× | 2/7 | 58.3ms | 21.5ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.2ms | 6.2× | 4/7 | 117.2ms | 29.0ms | 43.7 MB | 4/7 | 1638200 |
| clojure | 175.9ms | 12.4× | 7/7 | 511.6ms | 335.7ms | 151.1 MB | 7/7 | 1638200 |
| elixir | 20.3ms | 1.4× | 2/7 | 200.3ms | 180.0ms | 72.0 MB | 6/7 | 1638200 |
| python | 92.8ms | 6.5× | 5/7 | 103.3ms | 10.5ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.5ms | 1.5× | 3/7 | 39.1ms | 17.6ms | 55.7 MB | 5/7 | 1638200 |
| ruby | 97.1ms | 6.8× | 6/7 | 136.0ms | 38.9ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.2ms | 1.0× | 1/7 | 35.7ms | 21.5ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.8ms | 2.2× | 5/7 | 176.8ms | 29.0ms | 154.8 MB | 6/7 | 46468819 |
| clojure | 258.7ms | 3.9× | 7/7 | 594.4ms | 335.7ms | 124.3 MB | 5/7 | 46468819 |
| elixir | 115.3ms | 1.7× | 4/7 | 295.3ms | 180.0ms | 158.8 MB | 7/7 | 46468819 |
| python | 185.3ms | 2.8× | 6/7 | 195.8ms | 10.5ms | 25.8 MB | 2/7 | 46468819 |
| node | 103.8ms | 1.6× | 3/7 | 121.4ms | 17.6ms | 64.5 MB | 4/7 | 46468819 |
| ruby | 71.1ms | 1.1× | 2/7 | 110.0ms | 38.9ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 66.8ms | 1.0× | 1/7 | 88.3ms | 21.5ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 100.0ms | 14.1× | 5/7 | 129.0ms | 29.0ms | 42.1 MB | 4/7 | 724 |
| clojure | 266.4ms | 37.5× | 7/7 | 602.1ms | 335.7ms | 132.8 MB | 7/7 | 724 |
| elixir | 12.1ms | 1.7× | 2/7 | 192.1ms | 180.0ms | 72.1 MB | 6/7 | 724 |
| python | 55.6ms | 7.8× | 4/7 | 66.1ms | 10.5ms | 9.9 MB | 1/7 | 724 |
| node | 7.1ms | 1.0× | 1/7 | 24.7ms | 17.6ms | 50.1 MB | 5/7 | 724 |
| ruby | 133.6ms | 18.8× | 6/7 | 172.5ms | 38.9ms | 19.6 MB | 2/7 | 724 |
| dotnet | 20.1ms | 2.8× | 3/7 | 41.6ms | 21.5ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 1.5× | 2/7 | 67.9ms | 29.0ms | 24.6 MB | 3/7 | 9900000 |
| clojure | 1.128s | 44.1× | 7/7 | 1.464s | 335.7ms | 370.8 MB | 7/7 | 9900000 |
| elixir | 25.6ms | 1.0× | 1/7 | 205.6ms | 180.0ms | 70.6 MB | 6/7 | 9900000 |
| python | 47.5ms | 1.9× | 3/7 | 58.0ms | 10.5ms | 9.9 MB | 1/7 | 9900000 |
| node | 564.6ms | 22.1× | 6/7 | 582.2ms | 17.6ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 114.0ms | 4.5× | 4/7 | 152.9ms | 38.9ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 289.0ms | 11.3× | 5/7 | 310.5ms | 21.5ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.6ms | 4.1× | 2/7 | 81.6ms | 29.0ms | 27.7 MB | 3/7 | 2475000 |
| clojure | 1.344s | 105.9× | 7/7 | 1.680s | 335.7ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 12.7ms | 1.0× | 1/7 | 192.7ms | 180.0ms | 70.1 MB | 6/7 | 2475000 |
| python | 224.3ms | 17.7× | 5/7 | 234.8ms | 10.5ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.4ms | 16.6× | 4/7 | 228.0ms | 17.6ms | 49.6 MB | 5/7 | 2475000 |
| ruby | 115.7ms | 9.1× | 3/7 | 154.6ms | 38.9ms | 26.1 MB | 2/7 | 2475000 |
| dotnet | 704.2ms | 55.4× | 6/7 | 725.7ms | 21.5ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.2ms | 7.9× | 6/7 | 61.2ms | 29.0ms | 27.3 MB | 3/7 | 155553889038886 |
| clojure | 142.7ms | 34.8× | 7/7 | 478.4ms | 335.7ms | 108.9 MB | 7/7 | 155553889038886 |
| elixir | 13.0ms | 3.2× | 5/7 | 193.0ms | 180.0ms | 71.1 MB | 6/7 | 155553889038886 |
| python | 4.1ms | 1.0× | 1/7 | 14.6ms | 10.5ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 1.9× | 2/7 | 25.3ms | 17.6ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 9.1ms | 2.2× | 4/7 | 48.0ms | 38.9ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.8ms | 1.9× | 3/7 | 29.3ms | 21.5ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.3ms | 5.1× | 4/7 | 120.3ms | 29.0ms | 83.0 MB | 5/7 | 6100000 |
| clojure | 195.6ms | 10.9× | 5/7 | 531.3ms | 335.7ms | 133.4 MB | 7/7 | 6100000 |
| elixir | 28.2ms | 1.6× | 2/7 | 208.2ms | 180.0ms | 77.5 MB | 4/7 | 6100000 |
| python | 550.1ms | 30.6× | 6/7 | 560.6ms | 10.5ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.1ms | 2.9× | 3/7 | 69.7ms | 17.6ms | 50.9 MB | 3/7 | 6100000 |
| ruby | 1.613s | 89.6× | 7/7 | 1.651s | 38.9ms | 132.7 MB | 6/7 | 6100000 |
| dotnet | 18.0ms | 1.0× | 1/7 | 39.5ms | 21.5ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.6ms | 1.3× | 2/7 | 181.6ms | 29.0ms | 30.7 MB | 4/7 | 134626900 |
| clojure | 421.6ms | 3.6× | 5/7 | 757.3ms | 335.7ms | 136.0 MB | 6/7 | 134626900 |
| elixir | 315.7ms | 2.7× | 4/7 | 495.7ms | 180.0ms | 71.4 MB | 5/7 | 134626900 |
| python | 2.547s | 22.0× | 7/7 | 2.558s | 10.5ms | 22.1 MB | 2/7 | 134626900 |
| node | 298.4ms | 2.6× | 3/7 | 316.0ms | 17.6ms | 181.2 MB | 7/7 | 134626900 |
| ruby | 1.852s | 16.0× | 6/7 | 1.891s | 38.9ms | 19.3 MB | 1/7 | 134626900 |
| dotnet | 115.6ms | 1.0× | 1/7 | 137.1ms | 21.5ms | 28.1 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.7ms | 1.2× | 2/7 | 176.7ms | 29.0ms | 126.1 MB | 5/7 | 500 |
| clojure | 809.6ms | 6.8× | 7/7 | 1.145s | 335.7ms | 287.2 MB | 6/7 | 500 |
| elixir | 576.0ms | 4.9× | 6/7 | 756.0ms | 180.0ms | 487.5 MB | 7/7 | 500 |
| python | 174.6ms | 1.5× | 4/7 | 185.1ms | 10.5ms | 44.4 MB | 1/7 | 500 |
| node | 118.2ms | 1.0× | 1/7 | 135.8ms | 17.6ms | 64.6 MB | 4/7 | 500 |
| ruby | 210.2ms | 1.8× | 5/7 | 249.1ms | 38.9ms | 46.0 MB | 2/7 | 500 |
| dotnet | 148.5ms | 1.3× | 3/7 | 170.0ms | 21.5ms | 48.1 MB | 3/7 | 500 |
