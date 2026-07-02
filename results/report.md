# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 10:12.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.3ms | 2.9× | 4/7 | 29.3ms | — | 23.5 MB | 3/7 | 0 |
| clojure | 336.3ms | 33.0× | 7/7 | 336.3ms | — | 101.8 MB | 7/7 | 0 |
| elixir | 185.6ms | 18.2× | 6/7 | 185.6ms | — | 72.5 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.6ms | 1.7× | 2/7 | 17.6ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.8× | 5/7 | 38.8ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.7ms | 2.1× | 3/7 | 21.7ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.3ms | 5.5× | 5/7 | 253.6ms | 29.3ms | 27.2 MB | 4/7 | 9227465 |
| clojure | 199.8ms | 4.9× | 4/7 | 536.1ms | 336.3ms | 108.7 MB | 7/7 | 9227465 |
| elixir | 73.1ms | 1.8× | 3/7 | 258.7ms | 185.6ms | 72.7 MB | 6/7 | 9227465 |
| python | 737.7ms | 18.0× | 7/7 | 747.9ms | 10.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 72.9ms | 1.8× | 2/7 | 90.5ms | 17.6ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 602.8ms | 14.7× | 6/7 | 641.6ms | 38.8ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 40.9ms | 1.0× | 1/7 | 62.6ms | 21.7ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.8ms | 3.1× | 3/7 | 66.1ms | 29.3ms | 26.6 MB | 4/7 | 449999985000000 |
| clojure | 144.9ms | 12.2× | 5/7 | 481.2ms | 336.3ms | 108.9 MB | 7/7 | 449999985000000 |
| elixir | 51.2ms | 4.3× | 4/7 | 236.8ms | 185.6ms | 70.5 MB | 6/7 | 449999985000000 |
| python | 2.302s | 193.5× | 7/7 | 2.313s | 10.2ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.8ms | 2.5× | 2/7 | 47.4ms | 17.6ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 558.4ms | 46.9× | 6/7 | 597.2ms | 38.8ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 11.9ms | 1.0× | 1/7 | 33.6ms | 21.7ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.9ms | 1.0× | 1/7 | 32.2ms | 29.3ms | 23.4 MB | 3/7 | 12499997500000 |
| clojure | 176.6ms | 60.9× | 5/7 | 512.9ms | 336.3ms | 219.9 MB | 7/7 | 12499997500000 |
| elixir | 30.6ms | 10.6× | 3/7 | 216.2ms | 185.6ms | 70.6 MB | 5/7 | 12499997500000 |
| python | 105.3ms | 36.3× | 4/7 | 115.5ms | 10.2ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 219.6ms | 75.7× | 6/7 | 237.2ms | 17.6ms | 89.6 MB | 6/7 | 12499997500000 |
| ruby | 223.1ms | 76.9× | 7/7 | 261.9ms | 38.8ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 10.9ms | 3.8× | 2/7 | 32.6ms | 21.7ms | 27.7 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.6ms | 4.0× | 4/7 | 62.9ms | 29.3ms | 27.2 MB | 4/7 | 13848 |
| clojure | 148.5ms | 17.5× | 7/7 | 484.8ms | 336.3ms | 108.6 MB | 7/7 | 13848 |
| elixir | 17.7ms | 2.1× | 3/7 | 203.3ms | 185.6ms | 70.2 MB | 6/7 | 13848 |
| python | 122.0ms | 14.4× | 6/7 | 132.2ms | 10.2ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.0× | 1/7 | 26.1ms | 17.6ms | 48.2 MB | 5/7 | 13848 |
| ruby | 118.8ms | 14.0× | 5/7 | 157.6ms | 38.8ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.9ms | 1.0× | 2/7 | 30.6ms | 21.7ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.1ms | 1.6× | 2/7 | 104.4ms | 29.3ms | 27.1 MB | 4/7 | 442 |
| clojure | 436.1ms | 9.5× | 5/7 | 772.4ms | 336.3ms | 371.6 MB | 7/7 | 442 |
| elixir | 98.0ms | 2.1× | 3/7 | 283.6ms | 185.6ms | 71.4 MB | 6/7 | 442 |
| python | 2.742s | 60.0× | 7/7 | 2.752s | 10.2ms | 9.8 MB | 1/7 | 442 |
| node | 172.5ms | 3.8× | 4/7 | 190.1ms | 17.6ms | 48.0 MB | 5/7 | 442 |
| ruby | 857.1ms | 18.8× | 6/7 | 895.9ms | 38.8ms | 19.3 MB | 2/7 | 442 |
| dotnet | 45.7ms | 1.0× | 1/7 | 67.4ms | 21.7ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 214.7ms | 11.6× | 4/7 | 244.0ms | 29.3ms | 27.2 MB | 4/7 | 6129302 |
| clojure | 170.4ms | 9.2× | 3/7 | 506.7ms | 336.3ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 252.0ms | 13.6× | 5/7 | 437.6ms | 185.6ms | 73.2 MB | 6/7 | 6129302 |
| python | 1.401s | 75.7× | 7/7 | 1.411s | 10.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.6ms | 1.1× | 2/7 | 38.2ms | 17.6ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 416.4ms | 22.5× | 6/7 | 455.2ms | 38.8ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.5ms | 1.0× | 1/7 | 40.2ms | 21.7ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 93.7ms | 18.0× | 4/7 | 123.0ms | 29.3ms | 39.9 MB | 4/7 | 654353666 |
| clojure | 200.0ms | 38.5× | 5/7 | 536.3ms | 336.3ms | 118.3 MB | 7/7 | 654353666 |
| elixir | 60.5ms | 11.6× | 3/7 | 246.1ms | 185.6ms | 77.4 MB | 6/7 | 654353666 |
| python | 445.2ms | 85.6× | 7/7 | 455.4ms | 10.2ms | 10.4 MB | 1/7 | 654353666 |
| node | 15.0ms | 2.9× | 2/7 | 32.6ms | 17.6ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 288.0ms | 55.4× | 6/7 | 326.8ms | 38.8ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.2ms | 1.0× | 1/7 | 26.9ms | 21.7ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.7ms | 1.0× | 1/7 | 40.0ms | 29.3ms | 29.6 MB | 1/7 | 3388889 |
| clojure | 178.3ms | 16.7× | 7/7 | 514.6ms | 336.3ms | 168.6 MB | 6/7 | 3388889 |
| elixir | 116.1ms | 10.9× | 6/7 | 301.7ms | 185.6ms | 200.0 MB | 7/7 | 3388889 |
| python | 42.9ms | 4.0× | 3/7 | 53.1ms | 10.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.2ms | 6.0× | 4/7 | 81.8ms | 17.6ms | 94.7 MB | 5/7 | 3388889 |
| ruby | 83.4ms | 7.8× | 5/7 | 122.2ms | 38.8ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.3ms | 2.8× | 2/7 | 52.0ms | 21.7ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.1ms | 3.8× | 4/7 | 139.4ms | 29.3ms | 27.8 MB | 4/7 | 374854840 |
| clojure | 302.9ms | 10.4× | 7/7 | 639.2ms | 336.3ms | 302.5 MB | 7/7 | 374854840 |
| elixir | 164.4ms | 5.6× | 5/7 | 350.0ms | 185.6ms | 71.6 MB | 6/7 | 374854840 |
| python | 174.9ms | 6.0× | 6/7 | 185.1ms | 10.2ms | 10.0 MB | 1/7 | 374854840 |
| node | 29.1ms | 1.0× | 1/7 | 46.7ms | 17.6ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 71.0ms | 2.4× | 3/7 | 109.8ms | 38.8ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.4ms | 1.3× | 2/7 | 58.1ms | 21.7ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.5ms | 9.2× | 4/7 | 116.8ms | 29.3ms | 43.6 MB | 4/7 | 1638200 |
| clojure | 183.2ms | 19.3× | 7/7 | 519.5ms | 336.3ms | 150.4 MB | 7/7 | 1638200 |
| elixir | 9.5ms | 1.0× | 1/7 | 195.1ms | 185.6ms | 70.9 MB | 6/7 | 1638200 |
| python | 94.5ms | 9.9× | 5/7 | 104.7ms | 10.2ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.4ms | 2.1× | 3/7 | 38.0ms | 17.6ms | 55.5 MB | 5/7 | 1638200 |
| ruby | 98.8ms | 10.4× | 6/7 | 137.6ms | 38.8ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.4ms | 1.5× | 2/7 | 36.1ms | 21.7ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.9ms | 2.3× | 5/7 | 181.2ms | 29.3ms | 153.5 MB | 6/7 | 46468819 |
| clojure | 255.4ms | 3.9× | 7/7 | 591.7ms | 336.3ms | 123.3 MB | 5/7 | 46468819 |
| elixir | 109.9ms | 1.7× | 4/7 | 295.5ms | 185.6ms | 157.8 MB | 7/7 | 46468819 |
| python | 192.4ms | 2.9× | 6/7 | 202.6ms | 10.2ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.3ms | 1.6× | 3/7 | 121.9ms | 17.6ms | 64.4 MB | 4/7 | 46468819 |
| ruby | 72.2ms | 1.1× | 2/7 | 111.0ms | 38.8ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 65.6ms | 1.0× | 1/7 | 87.3ms | 21.7ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.4ms | 13.7× | 5/7 | 131.7ms | 29.3ms | 42.0 MB | 4/7 | 724 |
| clojure | 210.8ms | 28.1× | 7/7 | 547.1ms | 336.3ms | 132.4 MB | 7/7 | 724 |
| elixir | 9.4ms | 1.3× | 2/7 | 195.0ms | 185.6ms | 71.2 MB | 6/7 | 724 |
| python | 54.4ms | 7.3× | 4/7 | 64.6ms | 10.2ms | 9.8 MB | 1/7 | 724 |
| node | 7.5ms | 1.0× | 1/7 | 25.1ms | 17.6ms | 50.1 MB | 5/7 | 724 |
| ruby | 126.0ms | 16.8× | 6/7 | 164.8ms | 38.8ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.4ms | 2.6× | 3/7 | 41.1ms | 21.7ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 2.1× | 2/7 | 68.2ms | 29.3ms | 24.5 MB | 3/7 | 9900000 |
| clojure | 1.139s | 60.6× | 7/7 | 1.475s | 336.3ms | 371.1 MB | 7/7 | 9900000 |
| elixir | 18.8ms | 1.0× | 1/7 | 204.4ms | 185.6ms | 70.1 MB | 6/7 | 9900000 |
| python | 47.0ms | 2.5× | 3/7 | 57.2ms | 10.2ms | 9.8 MB | 1/7 | 9900000 |
| node | 625.5ms | 33.3× | 6/7 | 643.1ms | 17.6ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 110.5ms | 5.9× | 4/7 | 149.3ms | 38.8ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 287.5ms | 15.3× | 5/7 | 309.2ms | 21.7ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.2ms | 11.1× | 2/7 | 81.5ms | 29.3ms | 26.8 MB | 3/7 | 2475000 |
| clojure | 1.345s | 286.3× | 7/7 | 1.682s | 336.3ms | 373.9 MB | 7/7 | 2475000 |
| elixir | 4.7ms | 1.0× | 1/7 | 190.3ms | 185.6ms | 70.3 MB | 6/7 | 2475000 |
| python | 219.9ms | 46.8× | 5/7 | 230.1ms | 10.2ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.4ms | 44.8× | 4/7 | 228.0ms | 17.6ms | 49.5 MB | 5/7 | 2475000 |
| ruby | 122.0ms | 26.0× | 3/7 | 160.8ms | 38.8ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 696.0ms | 148.1× | 6/7 | 717.7ms | 21.7ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.5ms | 7.8× | 6/7 | 62.8ms | 29.3ms | 27.3 MB | 3/7 | 155553889038886 |
| clojure | 144.1ms | 33.5× | 7/7 | 480.4ms | 336.3ms | 107.7 MB | 7/7 | 155553889038886 |
| elixir | 8.5ms | 2.0× | 4/7 | 194.1ms | 185.6ms | 72.5 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.0× | 1/7 | 14.5ms | 10.2ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 1.8× | 2/7 | 25.3ms | 17.6ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 8.0ms | 1.9× | 3/7 | 46.8ms | 38.8ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.5ms | 2.0× | 5/7 | 30.2ms | 21.7ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 130.9ms | 7.9× | 4/7 | 160.2ms | 29.3ms | 87.8 MB | 5/7 | 6100000 |
| clojure | 195.8ms | 11.8× | 5/7 | 532.1ms | 336.3ms | 133.4 MB | 7/7 | 6100000 |
| elixir | 16.6ms | 1.0× | 1/7 | 202.2ms | 185.6ms | 75.4 MB | 4/7 | 6100000 |
| python | 550.6ms | 33.2× | 6/7 | 560.8ms | 10.2ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.5ms | 3.2× | 3/7 | 70.1ms | 17.6ms | 51.0 MB | 3/7 | 6100000 |
| ruby | 1.606s | 96.8× | 7/7 | 1.645s | 38.8ms | 132.2 MB | 6/7 | 6100000 |
| dotnet | 17.9ms | 1.1× | 2/7 | 39.6ms | 21.7ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 399.2ms | 12.2× | 5/7 | 428.5ms | 29.3ms | 34.0 MB | 4/7 | 31781100 |
| clojure | 215.5ms | 6.6× | 4/7 | 551.8ms | 336.3ms | 133.3 MB | 6/7 | 31781100 |
| elixir | 75.6ms | 2.3× | 2/7 | 261.2ms | 185.6ms | 71.7 MB | 5/7 | 31781100 |
| python | 687.2ms | 21.0× | 7/7 | 697.4ms | 10.2ms | 22.3 MB | 2/7 | 31781100 |
| node | 109.0ms | 3.3× | 3/7 | 126.6ms | 17.6ms | 181.2 MB | 7/7 | 31781100 |
| ruby | 430.8ms | 13.1× | 6/7 | 469.6ms | 38.8ms | 19.4 MB | 1/7 | 31781100 |
| dotnet | 32.8ms | 1.0× | 1/7 | 54.5ms | 21.7ms | 28.2 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.1ms | 1.2× | 2/7 | 174.4ms | 29.3ms | 126.3 MB | 5/7 | 500 |
| clojure | 825.0ms | 6.9× | 7/7 | 1.161s | 336.3ms | 282.8 MB | 6/7 | 500 |
| elixir | 582.3ms | 4.9× | 6/7 | 767.9ms | 185.6ms | 444.8 MB | 7/7 | 500 |
| python | 175.0ms | 1.5× | 4/7 | 185.2ms | 10.2ms | 45.9 MB | 1/7 | 500 |
| node | 119.0ms | 1.0× | 1/7 | 136.6ms | 17.6ms | 64.7 MB | 4/7 | 500 |
| ruby | 208.3ms | 1.8× | 5/7 | 247.1ms | 38.8ms | 46.2 MB | 2/7 | 500 |
| dotnet | 145.3ms | 1.2× | 3/7 | 167.0ms | 21.7ms | 48.4 MB | 3/7 | 500 |
