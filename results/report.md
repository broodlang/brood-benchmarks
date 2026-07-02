# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 09:05.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.6ms | 2.8× | 4/7 | 29.6ms | — | 23.6 MB | 3/7 | 0 |
| clojure | 340.7ms | 32.8× | 7/7 | 340.7ms | — | 101.8 MB | 7/7 | 0 |
| elixir | 185.6ms | 17.8× | 6/7 | 185.6ms | — | 72.6 MB | 6/7 | 0 |
| python | 10.4ms | 1.0× | 1/7 | 10.4ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.6ms | 1.7× | 2/7 | 17.6ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.7× | 5/7 | 38.8ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.4ms | 2.1× | 3/7 | 21.4ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 227.3ms | 5.7× | 5/7 | 256.9ms | 29.6ms | 27.5 MB | 4/7 | 9227465 |
| clojure | 200.3ms | 5.0× | 4/7 | 541.0ms | 340.7ms | 108.7 MB | 7/7 | 9227465 |
| elixir | 75.4ms | 1.9× | 2/7 | 261.0ms | 185.6ms | 70.8 MB | 6/7 | 9227465 |
| python | 737.1ms | 18.6× | 7/7 | 747.5ms | 10.4ms | 9.8 MB | 1/7 | 9227465 |
| node | 76.2ms | 1.9× | 3/7 | 93.8ms | 17.6ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 602.1ms | 15.2× | 6/7 | 640.9ms | 38.8ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.7ms | 1.0× | 1/7 | 61.1ms | 21.4ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.6ms | 2.8× | 3/7 | 65.2ms | 29.6ms | 27.2 MB | 4/7 | 449999985000000 |
| clojure | 144.8ms | 11.2× | 5/7 | 485.5ms | 340.7ms | 107.9 MB | 7/7 | 449999985000000 |
| elixir | 53.3ms | 4.1× | 4/7 | 238.9ms | 185.6ms | 71.6 MB | 6/7 | 449999985000000 |
| python | 2.196s | 170.2× | 7/7 | 2.207s | 10.4ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.4ms | 2.4× | 2/7 | 48.0ms | 17.6ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 587.9ms | 45.6× | 6/7 | 626.7ms | 38.8ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.9ms | 1.0× | 1/7 | 34.3ms | 21.4ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.0ms | 1.0× | 1/7 | 32.6ms | 29.6ms | 23.5 MB | 3/7 | 12499997500000 |
| clojure | 174.1ms | 58.0× | 5/7 | 514.8ms | 340.7ms | 219.4 MB | 7/7 | 12499997500000 |
| elixir | 32.7ms | 10.9× | 3/7 | 218.3ms | 185.6ms | 72.0 MB | 5/7 | 12499997500000 |
| python | 112.4ms | 37.5× | 4/7 | 122.8ms | 10.4ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 221.5ms | 73.8× | 6/7 | 239.1ms | 17.6ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 229.1ms | 76.4× | 7/7 | 267.9ms | 38.8ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 11.8ms | 3.9× | 2/7 | 33.2ms | 21.4ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.5ms | 3.5× | 4/7 | 63.1ms | 29.6ms | 26.9 MB | 4/7 | 13848 |
| clojure | 143.1ms | 14.8× | 7/7 | 483.8ms | 340.7ms | 108.5 MB | 7/7 | 13848 |
| elixir | 13.4ms | 1.4× | 3/7 | 199.0ms | 185.6ms | 73.6 MB | 6/7 | 13848 |
| python | 122.3ms | 12.6× | 6/7 | 132.7ms | 10.4ms | 9.9 MB | 1/7 | 13848 |
| node | 9.7ms | 1.0× | 1/7 | 27.3ms | 17.6ms | 48.2 MB | 5/7 | 13848 |
| ruby | 119.2ms | 12.3× | 5/7 | 158.0ms | 38.8ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 10.2ms | 1.1× | 2/7 | 31.6ms | 21.4ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.9ms | 1.6× | 2/7 | 103.5ms | 29.6ms | 27.0 MB | 4/7 | 442 |
| clojure | 426.3ms | 9.1× | 5/7 | 767.0ms | 340.7ms | 370.9 MB | 7/7 | 442 |
| elixir | 103.3ms | 2.2× | 3/7 | 288.9ms | 185.6ms | 71.2 MB | 6/7 | 442 |
| python | 2.509s | 53.3× | 7/7 | 2.519s | 10.4ms | 9.8 MB | 1/7 | 442 |
| node | 172.4ms | 3.7× | 4/7 | 190.0ms | 17.6ms | 48.1 MB | 5/7 | 442 |
| ruby | 845.1ms | 17.9× | 6/7 | 883.9ms | 38.8ms | 19.3 MB | 2/7 | 442 |
| dotnet | 47.1ms | 1.0× | 1/7 | 68.5ms | 21.4ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 212.5ms | 11.4× | 4/7 | 242.1ms | 29.6ms | 27.0 MB | 4/7 | 6129302 |
| clojure | 166.5ms | 9.0× | 3/7 | 507.2ms | 340.7ms | 115.7 MB | 7/7 | 6129302 |
| elixir | 255.3ms | 13.7× | 5/7 | 440.9ms | 185.6ms | 71.9 MB | 6/7 | 6129302 |
| python | 1.369s | 73.6× | 7/7 | 1.379s | 10.4ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.2ms | 1.1× | 2/7 | 37.8ms | 17.6ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 409.4ms | 22.0× | 6/7 | 448.2ms | 38.8ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.6ms | 1.0× | 1/7 | 40.0ms | 21.4ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 92.1ms | 18.1× | 4/7 | 121.7ms | 29.6ms | 40.4 MB | 4/7 | 654353666 |
| clojure | 192.3ms | 37.7× | 5/7 | 533.0ms | 340.7ms | 118.3 MB | 7/7 | 654353666 |
| elixir | 58.3ms | 11.4× | 3/7 | 243.9ms | 185.6ms | 75.9 MB | 6/7 | 654353666 |
| python | 468.1ms | 91.8× | 7/7 | 478.5ms | 10.4ms | 10.4 MB | 1/7 | 654353666 |
| node | 15.7ms | 3.1× | 2/7 | 33.3ms | 17.6ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 289.6ms | 56.8× | 6/7 | 328.4ms | 38.8ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.1ms | 1.0× | 1/7 | 26.5ms | 21.4ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.3ms | 1.0× | 1/7 | 40.9ms | 29.6ms | 30.1 MB | 1/7 | 3388889 |
| clojure | 174.3ms | 15.4× | 7/7 | 515.0ms | 340.7ms | 168.4 MB | 6/7 | 3388889 |
| elixir | 116.0ms | 10.3× | 6/7 | 301.6ms | 185.6ms | 200.8 MB | 7/7 | 3388889 |
| python | 42.2ms | 3.7× | 3/7 | 52.6ms | 10.4ms | 39.9 MB | 2/7 | 3388889 |
| node | 65.0ms | 5.8× | 4/7 | 82.6ms | 17.6ms | 94.7 MB | 5/7 | 3388889 |
| ruby | 83.7ms | 7.4× | 5/7 | 122.5ms | 38.8ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 32.4ms | 2.9× | 2/7 | 53.8ms | 21.4ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.6ms | 3.5× | 4/7 | 137.2ms | 29.6ms | 28.1 MB | 4/7 | 374854840 |
| clojure | 282.1ms | 9.2× | 7/7 | 622.8ms | 340.7ms | 302.8 MB | 7/7 | 374854840 |
| elixir | 166.1ms | 5.4× | 5/7 | 351.7ms | 185.6ms | 73.3 MB | 6/7 | 374854840 |
| python | 170.1ms | 5.5× | 6/7 | 180.5ms | 10.4ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.8ms | 1.0× | 1/7 | 48.4ms | 17.6ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 74.2ms | 2.4× | 3/7 | 113.0ms | 38.8ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 38.3ms | 1.2× | 2/7 | 59.7ms | 21.4ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.0ms | 10.5× | 4/7 | 117.6ms | 29.6ms | 43.4 MB | 4/7 | 1638200 |
| clojure | 185.4ms | 22.1× | 7/7 | 526.1ms | 340.7ms | 150.5 MB | 7/7 | 1638200 |
| elixir | 8.4ms | 1.0× | 1/7 | 194.0ms | 185.6ms | 71.3 MB | 6/7 | 1638200 |
| python | 94.8ms | 11.3× | 5/7 | 105.2ms | 10.4ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.4ms | 2.4× | 3/7 | 38.0ms | 17.6ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 96.1ms | 11.4× | 6/7 | 134.9ms | 38.8ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 15.1ms | 1.8× | 2/7 | 36.5ms | 21.4ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.6ms | 2.3× | 5/7 | 185.2ms | 29.6ms | 154.3 MB | 6/7 | 46468819 |
| clojure | 263.4ms | 4.0× | 7/7 | 604.1ms | 340.7ms | 124.1 MB | 5/7 | 46468819 |
| elixir | 115.3ms | 1.7× | 4/7 | 300.9ms | 185.6ms | 156.6 MB | 7/7 | 46468819 |
| python | 180.3ms | 2.7× | 6/7 | 190.7ms | 10.4ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.4ms | 1.6× | 3/7 | 121.0ms | 17.6ms | 64.5 MB | 4/7 | 46468819 |
| ruby | 73.1ms | 1.1× | 2/7 | 111.9ms | 38.8ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 66.4ms | 1.0× | 1/7 | 87.8ms | 21.4ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.8ms | 18.4× | 5/7 | 132.4ms | 29.6ms | 42.2 MB | 4/7 | 724 |
| clojure | 196.6ms | 35.1× | 7/7 | 537.3ms | 340.7ms | 132.2 MB | 7/7 | 724 |
| elixir | 5.6ms | 1.0× | 1/7 | 191.2ms | 185.6ms | 72.0 MB | 6/7 | 724 |
| python | 53.2ms | 9.5× | 4/7 | 63.6ms | 10.4ms | 9.8 MB | 1/7 | 724 |
| node | 6.9ms | 1.2× | 2/7 | 24.5ms | 17.6ms | 50.1 MB | 5/7 | 724 |
| ruby | 126.4ms | 22.6× | 6/7 | 165.2ms | 38.8ms | 19.5 MB | 2/7 | 724 |
| dotnet | 21.0ms | 3.8× | 3/7 | 42.4ms | 21.4ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.9ms | 1.9× | 2/7 | 69.5ms | 29.6ms | 24.3 MB | 3/7 | 9900000 |
| clojure | 1.105s | 52.1× | 7/7 | 1.445s | 340.7ms | 371.3 MB | 7/7 | 9900000 |
| elixir | 21.2ms | 1.0× | 1/7 | 206.8ms | 185.6ms | 72.7 MB | 6/7 | 9900000 |
| python | 50.2ms | 2.4× | 3/7 | 60.6ms | 10.4ms | 9.8 MB | 1/7 | 9900000 |
| node | 579.4ms | 27.3× | 6/7 | 597.0ms | 17.6ms | 49.7 MB | 5/7 | 9900000 |
| ruby | 111.3ms | 5.2× | 4/7 | 150.1ms | 38.8ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 292.6ms | 13.8× | 5/7 | 314.0ms | 21.4ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.4ms | 6.1× | 2/7 | 81.0ms | 29.6ms | 27.4 MB | 3/7 | 2475000 |
| clojure | 1.352s | 160.9× | 7/7 | 1.692s | 340.7ms | 375.4 MB | 7/7 | 2475000 |
| elixir | 8.4ms | 1.0× | 1/7 | 194.0ms | 185.6ms | 71.1 MB | 6/7 | 2475000 |
| python | 237.7ms | 28.3× | 5/7 | 248.1ms | 10.4ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.1ms | 25.0× | 4/7 | 227.7ms | 17.6ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 114.5ms | 13.6× | 3/7 | 153.3ms | 38.8ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 700.4ms | 83.4× | 6/7 | 721.8ms | 21.4ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 7.6× | 6/7 | 61.6ms | 29.6ms | 27.4 MB | 3/7 | 155553889038886 |
| clojure | 142.2ms | 33.9× | 7/7 | 482.9ms | 340.7ms | 108.2 MB | 7/7 | 155553889038886 |
| elixir | 10.2ms | 2.4× | 5/7 | 195.8ms | 185.6ms | 74.0 MB | 6/7 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/7 | 14.6ms | 10.4ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 1.8× | 3/7 | 25.3ms | 17.6ms | 51.5 MB | 5/7 | 155553889038886 |
| ruby | 7.5ms | 1.8× | 2/7 | 46.3ms | 38.8ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.0ms | 1.9× | 4/7 | 29.4ms | 21.4ms | 28.2 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 124.2ms | 6.9× | 4/7 | 153.8ms | 29.6ms | 79.2 MB | 5/7 | 6100000 |
| clojure | 190.6ms | 10.6× | 5/7 | 531.3ms | 340.7ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 17.9ms | 1.0× | 1/7 | 203.5ms | 185.6ms | 76.0 MB | 4/7 | 6100000 |
| python | 544.4ms | 30.4× | 6/7 | 554.8ms | 10.4ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.1ms | 2.9× | 3/7 | 69.7ms | 17.6ms | 51.1 MB | 3/7 | 6100000 |
| ruby | 1.601s | 89.5× | 7/7 | 1.640s | 38.8ms | 133.3 MB | 6/7 | 6100000 |
| dotnet | 19.6ms | 1.1× | 2/7 | 41.0ms | 21.4ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 401.2ms | 11.9× | 5/7 | 430.8ms | 29.6ms | 34.2 MB | 4/7 | 31781100 |
| clojure | 214.8ms | 6.4× | 4/7 | 555.5ms | 340.7ms | 133.8 MB | 6/7 | 31781100 |
| elixir | 73.3ms | 2.2× | 2/7 | 258.9ms | 185.6ms | 71.3 MB | 5/7 | 31781100 |
| python | 689.6ms | 20.5× | 7/7 | 700.0ms | 10.4ms | 22.2 MB | 2/7 | 31781100 |
| node | 110.4ms | 3.3× | 3/7 | 128.0ms | 17.6ms | 181.3 MB | 7/7 | 31781100 |
| ruby | 430.9ms | 12.8× | 6/7 | 469.7ms | 38.8ms | 19.4 MB | 1/7 | 31781100 |
| dotnet | 33.6ms | 1.0× | 1/7 | 55.0ms | 21.4ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.3ms | 1.3× | 3/7 | 180.9ms | 29.6ms | 123.7 MB | 5/7 | 500 |
| clojure | 822.2ms | 7.1× | 7/7 | 1.163s | 340.7ms | 287.8 MB | 6/7 | 500 |
| elixir | 556.1ms | 4.8× | 6/7 | 741.7ms | 185.6ms | 499.3 MB | 7/7 | 500 |
| python | 173.1ms | 1.5× | 4/7 | 183.5ms | 10.4ms | 45.0 MB | 1/7 | 500 |
| node | 116.3ms | 1.0× | 1/7 | 133.9ms | 17.6ms | 64.2 MB | 4/7 | 500 |
| ruby | 207.9ms | 1.8× | 5/7 | 246.7ms | 38.8ms | 45.8 MB | 2/7 | 500 |
| dotnet | 146.4ms | 1.3× | 2/7 | 167.8ms | 21.4ms | 48.1 MB | 3/7 | 500 |
