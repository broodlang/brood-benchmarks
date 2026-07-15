# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-15 22:03.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.3ms | 2.9× | 4/7 | 31.3ms | — | 20.0 MB | 3/7 | 0 |
| clojure | 332.7ms | 31.1× | 7/7 | 332.7ms | — | 101.5 MB | 7/7 | 0 |
| elixir | 187.2ms | 17.5× | 6/7 | 187.2ms | — | 71.8 MB | 6/7 | 0 |
| python | 10.7ms | 1.0× | 1/7 | 10.7ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.9ms | 1.7× | 2/7 | 17.9ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 39.7ms | 3.7× | 5/7 | 39.7ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 22.0ms | 2.1× | 3/7 | 22.0ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.7ms | 1.3× | 2/7 | 88.0ms | 31.3ms | 23.3 MB | 3/7 | 9227465 |
| clojure | 212.1ms | 4.9× | 5/7 | 544.8ms | 332.7ms | 109.2 MB | 7/7 | 9227465 |
| elixir | 71.7ms | 1.6× | 3/7 | 258.9ms | 187.2ms | 71.9 MB | 6/7 | 9227465 |
| python | 733.3ms | 16.8× | 7/7 | 744.0ms | 10.7ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.9ms | 1.7× | 4/7 | 91.8ms | 17.9ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 601.9ms | 13.8× | 6/7 | 641.6ms | 39.7ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 43.6ms | 1.0× | 1/7 | 65.6ms | 22.0ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 250.0ms | 20.8× | 5/7 | 281.3ms | 31.3ms | 23.3 MB | 3/7 | 449999985000000 |
| clojure | 145.4ms | 12.1× | 4/7 | 478.1ms | 332.7ms | 109.3 MB | 7/7 | 449999985000000 |
| elixir | 48.5ms | 4.0× | 3/7 | 235.7ms | 187.2ms | 71.8 MB | 6/7 | 449999985000000 |
| python | 2.289s | 190.7× | 7/7 | 2.299s | 10.7ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.4ms | 2.5× | 2/7 | 48.3ms | 17.9ms | 49.9 MB | 5/7 | 449999985000000 |
| ruby | 572.9ms | 47.7× | 6/7 | 612.6ms | 39.7ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 12.0ms | 1.0× | 1/7 | 34.0ms | 22.0ms | 26.4 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 34.6ms | 31.3ms | 19.7 MB | 3/7 | 12499997500000 |
| clojure | 183.8ms | 55.7× | 5/7 | 516.5ms | 332.7ms | 220.1 MB | 7/7 | 12499997500000 |
| elixir | 26.2ms | 7.9× | 3/7 | 213.4ms | 187.2ms | 71.4 MB | 5/7 | 12499997500000 |
| python | 105.9ms | 32.1× | 4/7 | 116.6ms | 10.7ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 220.4ms | 66.8× | 6/7 | 238.3ms | 17.9ms | 90.2 MB | 6/7 | 12499997500000 |
| ruby | 223.1ms | 67.6× | 7/7 | 262.8ms | 39.7ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 11.6ms | 3.5× | 2/7 | 33.6ms | 22.0ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.2ms | 5.0× | 4/7 | 75.5ms | 31.3ms | 23.7 MB | 3/7 | 13848 |
| clojure | 155.2ms | 17.4× | 7/7 | 487.9ms | 332.7ms | 108.8 MB | 7/7 | 13848 |
| elixir | 14.7ms | 1.7× | 3/7 | 201.9ms | 187.2ms | 71.4 MB | 6/7 | 13848 |
| python | 121.5ms | 13.7× | 6/7 | 132.2ms | 10.7ms | 9.9 MB | 1/7 | 13848 |
| node | 8.9ms | 1.0× | 1/7 | 26.8ms | 17.9ms | 48.9 MB | 5/7 | 13848 |
| ruby | 115.8ms | 13.0× | 5/7 | 155.5ms | 39.7ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 9.5ms | 1.1× | 2/7 | 31.5ms | 22.0ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.3ms | 1.9× | 2/7 | 119.6ms | 31.3ms | 23.7 MB | 3/7 | 442 |
| clojure | 439.3ms | 9.4× | 5/7 | 772.0ms | 332.7ms | 372.0 MB | 7/7 | 442 |
| elixir | 100.7ms | 2.2× | 3/7 | 287.9ms | 187.2ms | 72.6 MB | 6/7 | 442 |
| python | 2.861s | 61.1× | 7/7 | 2.872s | 10.7ms | 9.8 MB | 1/7 | 442 |
| node | 174.0ms | 3.7× | 4/7 | 191.9ms | 17.9ms | 48.6 MB | 5/7 | 442 |
| ruby | 843.9ms | 18.0× | 6/7 | 883.6ms | 39.7ms | 19.1 MB | 2/7 | 442 |
| dotnet | 46.8ms | 1.0× | 1/7 | 68.8ms | 22.0ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.4ms | 9.1× | 3/7 | 203.7ms | 31.3ms | 23.7 MB | 3/7 | 6129302 |
| clojure | 180.1ms | 9.5× | 4/7 | 512.8ms | 332.7ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 240.8ms | 12.7× | 5/7 | 428.0ms | 187.2ms | 71.5 MB | 6/7 | 6129302 |
| python | 1.331s | 70.0× | 7/7 | 1.341s | 10.7ms | 9.9 MB | 1/7 | 6129302 |
| node | 21.1ms | 1.1× | 2/7 | 39.0ms | 17.9ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 424.4ms | 22.3× | 6/7 | 464.1ms | 39.7ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 19.0ms | 1.0× | 1/7 | 41.0ms | 22.0ms | 26.4 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 125.5ms | 27.9× | 4/7 | 156.8ms | 31.3ms | 40.4 MB | 4/7 | 654353666 |
| clojure | 197.4ms | 43.9× | 5/7 | 530.1ms | 332.7ms | 117.3 MB | 7/7 | 654353666 |
| elixir | 59.1ms | 13.1× | 3/7 | 246.3ms | 187.2ms | 74.1 MB | 6/7 | 654353666 |
| python | 458.9ms | 102.0× | 7/7 | 469.6ms | 10.7ms | 10.3 MB | 1/7 | 654353666 |
| node | 18.0ms | 4.0× | 2/7 | 35.9ms | 17.9ms | 52.4 MB | 5/7 | 654353666 |
| ruby | 273.0ms | 60.7× | 6/7 | 312.7ms | 39.7ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 26.5ms | 22.0ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.2ms | 1.0× | 1/7 | 44.5ms | 31.3ms | 30.1 MB | 1/7 | 3388889 |
| clojure | 173.3ms | 13.1× | 7/7 | 506.0ms | 332.7ms | 167.7 MB | 6/7 | 3388889 |
| elixir | 118.3ms | 9.0× | 6/7 | 305.5ms | 187.2ms | 202.2 MB | 7/7 | 3388889 |
| python | 42.5ms | 3.2× | 3/7 | 53.2ms | 10.7ms | 39.9 MB | 2/7 | 3388889 |
| node | 65.6ms | 5.0× | 4/7 | 83.5ms | 17.9ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 83.0ms | 6.3× | 5/7 | 122.7ms | 39.7ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.6ms | 2.3× | 2/7 | 52.6ms | 22.0ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.6ms | 1.6× | 3/7 | 81.9ms | 31.3ms | 24.6 MB | 3/7 | 374854840 |
| clojure | 279.8ms | 8.7× | 7/7 | 612.5ms | 332.7ms | 302.3 MB | 7/7 | 374854840 |
| elixir | 174.4ms | 5.5× | 6/7 | 361.6ms | 187.2ms | 71.2 MB | 6/7 | 374854840 |
| python | 172.0ms | 5.4× | 5/7 | 182.7ms | 10.7ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.0ms | 1.0× | 1/7 | 49.9ms | 17.9ms | 50.1 MB | 5/7 | 374854840 |
| ruby | 72.1ms | 2.3× | 4/7 | 111.8ms | 39.7ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 37.5ms | 1.2× | 2/7 | 59.5ms | 22.0ms | 27.2 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.4ms | 9.0× | 6/7 | 134.7ms | 31.3ms | 50.2 MB | 4/7 | 1638200 |
| clojure | 180.9ms | 15.7× | 7/7 | 513.6ms | 332.7ms | 149.8 MB | 7/7 | 1638200 |
| elixir | 11.5ms | 1.0× | 1/7 | 198.7ms | 187.2ms | 70.7 MB | 6/7 | 1638200 |
| python | 95.5ms | 8.3× | 4/7 | 106.2ms | 10.7ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.1ms | 1.8× | 3/7 | 39.0ms | 17.9ms | 56.1 MB | 5/7 | 1638200 |
| ruby | 95.6ms | 8.3× | 5/7 | 135.3ms | 39.7ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.1ms | 1.2× | 2/7 | 36.1ms | 22.0ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.9ms | 3.3× | 6/7 | 243.2ms | 31.3ms | 183.2 MB | 7/7 | 46468819 |
| clojure | 264.6ms | 4.1× | 7/7 | 597.3ms | 332.7ms | 124.5 MB | 5/7 | 46468819 |
| elixir | 119.3ms | 1.9× | 4/7 | 306.5ms | 187.2ms | 159.5 MB | 6/7 | 46468819 |
| python | 200.3ms | 3.1× | 5/7 | 211.0ms | 10.7ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.3ms | 1.6× | 3/7 | 122.2ms | 17.9ms | 64.9 MB | 4/7 | 46468819 |
| ruby | 71.0ms | 1.1× | 2/7 | 110.7ms | 39.7ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 64.2ms | 1.0× | 1/7 | 86.2ms | 22.0ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 135.4ms | 27.6× | 6/7 | 166.7ms | 31.3ms | 42.8 MB | 4/7 | 724 |
| clojure | 276.0ms | 56.3× | 7/7 | 608.7ms | 332.7ms | 136.2 MB | 7/7 | 724 |
| elixir | 4.9ms | 1.0× | 1/7 | 192.1ms | 187.2ms | 73.3 MB | 6/7 | 724 |
| python | 54.2ms | 11.1× | 4/7 | 64.9ms | 10.7ms | 9.8 MB | 1/7 | 724 |
| node | 7.6ms | 1.6× | 2/7 | 25.5ms | 17.9ms | 50.5 MB | 5/7 | 724 |
| ruby | 123.2ms | 25.1× | 5/7 | 162.9ms | 39.7ms | 19.4 MB | 2/7 | 724 |
| dotnet | 19.8ms | 4.0× | 3/7 | 41.8ms | 22.0ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.9ms | 2.0× | 2/7 | 71.2ms | 31.3ms | 23.6 MB | 3/7 | 9900000 |
| clojure | 1.094s | 53.6× | 7/7 | 1.427s | 332.7ms | 370.7 MB | 7/7 | 9900000 |
| elixir | 20.4ms | 1.0× | 1/7 | 207.6ms | 187.2ms | 70.4 MB | 6/7 | 9900000 |
| python | 46.5ms | 2.3× | 3/7 | 57.2ms | 10.7ms | 9.8 MB | 1/7 | 9900000 |
| node | 625.1ms | 30.6× | 6/7 | 643.0ms | 17.9ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 111.8ms | 5.5× | 4/7 | 151.5ms | 39.7ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 292.0ms | 14.3× | 5/7 | 314.0ms | 22.0ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.5ms | 5.3× | 2/7 | 70.8ms | 31.3ms | 23.7 MB | 2/7 | 2475000 |
| clojure | 1.328s | 177.1× | 7/7 | 1.661s | 332.7ms | 373.7 MB | 7/7 | 2475000 |
| elixir | 7.5ms | 1.0× | 1/7 | 194.7ms | 187.2ms | 72.0 MB | 6/7 | 2475000 |
| python | 246.0ms | 32.8× | 5/7 | 256.7ms | 10.7ms | 9.8 MB | 1/7 | 2475000 |
| node | 212.5ms | 28.3× | 4/7 | 230.4ms | 17.9ms | 50.2 MB | 5/7 | 2475000 |
| ruby | 118.1ms | 15.7× | 3/7 | 157.8ms | 39.7ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 683.0ms | 91.1× | 6/7 | 705.0ms | 22.0ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.9ms | 9.7× | 6/7 | 68.2ms | 31.3ms | 23.7 MB | 3/7 | 155553889038886 |
| clojure | 139.3ms | 36.7× | 7/7 | 472.0ms | 332.7ms | 108.9 MB | 7/7 | 155553889038886 |
| elixir | 5.6ms | 1.5× | 2/7 | 192.8ms | 187.2ms | 72.4 MB | 6/7 | 155553889038886 |
| python | 3.8ms | 1.0× | 1/7 | 14.5ms | 10.7ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.8ms | 2.1× | 5/7 | 25.7ms | 17.9ms | 52.0 MB | 5/7 | 155553889038886 |
| ruby | 7.1ms | 1.9× | 3/7 | 46.8ms | 39.7ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 7.2ms | 1.9× | 4/7 | 29.2ms | 22.0ms | 28.0 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 342.4ms | 1.2× | 3/7 | 373.7ms | 31.3ms | 24.2 MB | 3/7 | 24558 |
| clojure | 576.2ms | 2.1× | 5/7 | 908.9ms | 332.7ms | 377.0 MB | 7/7 | 24558 |
| elixir | 276.8ms | 1.0× | 2/7 | 464.0ms | 187.2ms | 73.4 MB | 6/7 | 24558 |
| python | 3.899s | 14.1× | 7/7 | 3.910s | 10.7ms | 11.0 MB | 1/7 | 24558 |
| node | 408.9ms | 1.5× | 4/7 | 426.8ms | 17.9ms | 48.4 MB | 5/7 | 24558 |
| ruby | 1.636s | 5.9× | 6/7 | 1.676s | 39.7ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 275.6ms | 1.0× | 1/7 | 297.6ms | 22.0ms | 26.2 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 124.1ms | 40.0× | 6/7 | 155.4ms | 31.3ms | 59.3 MB | 5/7 | 78498 |
| clojure | 150.5ms | 48.5× | 7/7 | 483.2ms | 332.7ms | 108.9 MB | 7/7 | 78498 |
| elixir | 52.8ms | 17.0× | 3/7 | 240.0ms | 187.2ms | 79.2 MB | 6/7 | 78498 |
| python | 122.8ms | 39.6× | 5/7 | 133.5ms | 10.7ms | 10.8 MB | 1/7 | 78498 |
| node | 6.0ms | 1.9× | 2/7 | 23.9ms | 17.9ms | 49.5 MB | 4/7 | 78498 |
| ruby | 84.7ms | 27.3× | 4/7 | 124.4ms | 39.7ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 3.1ms | 1.0× | 1/7 | 25.1ms | 22.0ms | 27.3 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.8ms | 4.8× | 5/7 | 139.1ms | 31.3ms | 76.3 MB | 5/7 | 30039386344 |
| clojure | 308.6ms | 13.7× | 7/7 | 641.3ms | 332.7ms | 291.8 MB | 7/7 | 30039386344 |
| elixir | 117.4ms | 5.2× | 6/7 | 304.6ms | 187.2ms | 99.2 MB | 6/7 | 30039386344 |
| python | 80.4ms | 3.6× | 4/7 | 91.1ms | 10.7ms | 14.8 MB | 1/7 | 30039386344 |
| node | 22.5ms | 1.0× | 1/7 | 40.4ms | 17.9ms | 54.6 MB | 4/7 | 30039386344 |
| ruby | 39.7ms | 1.8× | 3/7 | 79.4ms | 39.7ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 23.7ms | 1.1× | 2/7 | 45.7ms | 22.0ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 442.8ms | 66.1× | 6/7 | 474.1ms | 31.3ms | 40.5 MB | 4/7 | -169078071 |
| clojure | 200.2ms | 29.9× | 4/7 | 532.9ms | 332.7ms | 109.3 MB | 7/7 | -169078071 |
| elixir | 145.3ms | 21.7× | 3/7 | 332.5ms | 187.2ms | 70.3 MB | 6/7 | -169078071 |
| python | 771.0ms | 115.1× | 7/7 | 781.7ms | 10.7ms | 10.3 MB | 1/7 | -169078071 |
| node | 15.1ms | 2.3× | 2/7 | 33.0ms | 17.9ms | 50.5 MB | 5/7 | -169078071 |
| ruby | 302.8ms | 45.2× | 5/7 | 342.5ms | 39.7ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 6.7ms | 1.0× | 1/7 | 28.7ms | 22.0ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 267.9ms | 267.9× | 6/7 | 299.2ms | 31.3ms | 112.5 MB | 6/7 | 1489952542 |
| clojure | 397.3ms | 397.3× | 7/7 | 730.0ms | 332.7ms | 165.2 MB | 7/7 | 1489952542 |
| elixir | 0.6ms | < 1× | 1/7 | 187.8ms | 187.2ms | 75.9 MB | 5/7 | 1489952542 |
| python | 7.6ms | 7.6× | 4/7 | 18.3ms | 10.7ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.7ms | 1.7× | 2/7 | 19.6ms | 17.9ms | 44.0 MB | 4/7 | 1489952542 |
| ruby | 3.5ms | 3.5× | 3/7 | 43.2ms | 39.7ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 42.6ms | 42.6× | 5/7 | 64.6ms | 22.0ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 269.9ms | 67.5× | 7/7 | 301.2ms | 31.3ms | 63.8 MB | 5/7 | 10000 |
| clojure | 144.4ms | 36.1× | 6/7 | 477.1ms | 332.7ms | 108.5 MB | 7/7 | 10000 |
| elixir | 9.9ms | 2.5× | 3/7 | 197.1ms | 187.2ms | 69.8 MB | 6/7 | 10000 |
| python | 12.4ms | 3.1× | 5/7 | 23.1ms | 10.7ms | 11.1 MB | 1/7 | 10000 |
| node | 4.0ms | 1.0× | 1/7 | 21.9ms | 17.9ms | 50.3 MB | 4/7 | 10000 |
| ruby | 6.7ms | 1.7× | 2/7 | 46.4ms | 39.7ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.3ms | 3.1× | 4/7 | 34.3ms | 22.0ms | 31.8 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.6ms | 31.1× | 6/7 | 164.9ms | 31.3ms | 99.5 MB | 6/7 | 12081249 |
| clojure | 172.1ms | 40.0× | 7/7 | 504.8ms | 332.7ms | 108.7 MB | 7/7 | 12081249 |
| elixir | 8.6ms | 2.0× | 4/7 | 195.8ms | 187.2ms | 77.0 MB | 5/7 | 12081249 |
| python | 12.0ms | 2.8× | 5/7 | 22.7ms | 10.7ms | 10.2 MB | 1/7 | 12081249 |
| node | 6.6ms | 1.5× | 2/7 | 24.5ms | 17.9ms | 50.9 MB | 4/7 | 12081249 |
| ruby | 8.1ms | 1.9× | 3/7 | 47.8ms | 39.7ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 4.3ms | 1.0× | 1/7 | 26.3ms | 22.0ms | 27.1 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.3ms | 3.2× | 3/7 | 82.6ms | 31.3ms | 52.0 MB | 4/7 | 6100000 |
| clojure | 196.0ms | 12.2× | 5/7 | 528.7ms | 332.7ms | 134.0 MB | 7/7 | 6100000 |
| elixir | 16.1ms | 1.0× | 1/7 | 203.3ms | 187.2ms | 75.3 MB | 5/7 | 6100000 |
| python | 557.1ms | 34.6× | 6/7 | 567.8ms | 10.7ms | 27.8 MB | 1/7 | 6100000 |
| node | 52.4ms | 3.3× | 4/7 | 70.3ms | 17.9ms | 51.5 MB | 3/7 | 6100000 |
| ruby | 1.588s | 98.7× | 7/7 | 1.628s | 39.7ms | 133.9 MB | 6/7 | 6100000 |
| dotnet | 18.0ms | 1.1× | 2/7 | 40.0ms | 22.0ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 202.8ms | 1.7× | 2/7 | 234.1ms | 31.3ms | 25.9 MB | 3/7 | 134626900 |
| clojure | 407.6ms | 3.5× | 5/7 | 740.3ms | 332.7ms | 135.9 MB | 6/7 | 134626900 |
| elixir | 287.1ms | 2.5× | 3/7 | 474.3ms | 187.2ms | 71.3 MB | 5/7 | 134626900 |
| python | 2.502s | 21.5× | 7/7 | 2.512s | 10.7ms | 21.9 MB | 2/7 | 134626900 |
| node | 304.1ms | 2.6× | 4/7 | 322.0ms | 17.9ms | 181.8 MB | 7/7 | 134626900 |
| ruby | 1.894s | 16.3× | 6/7 | 1.934s | 39.7ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 116.5ms | 1.0× | 1/7 | 138.5ms | 22.0ms | 28.2 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 159.0ms | 1.3× | 3/7 | 190.3ms | 31.3ms | 105.1 MB | 5/7 | 500 |
| clojure | 839.1ms | 6.9× | 7/7 | 1.172s | 332.7ms | 294.3 MB | 6/7 | 500 |
| elixir | 586.4ms | 4.8× | 6/7 | 773.6ms | 187.2ms | 484.1 MB | 7/7 | 500 |
| python | 174.1ms | 1.4× | 4/7 | 184.8ms | 10.7ms | 45.1 MB | 1/7 | 500 |
| node | 122.1ms | 1.0× | 1/7 | 140.0ms | 17.9ms | 64.6 MB | 4/7 | 500 |
| ruby | 206.6ms | 1.7× | 5/7 | 246.3ms | 39.7ms | 45.7 MB | 2/7 | 500 |
| dotnet | 147.4ms | 1.2× | 2/7 | 169.4ms | 22.0ms | 48.1 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 258.8ms | 4.9× | 3/7 | 290.1ms | 31.3ms | 98.2 MB | 6/7 | 100000 |
| clojure | 614.0ms | 11.7× | 5/7 | 946.7ms | 332.7ms | 132.4 MB | 7/7 | 100000 |
| elixir | 52.5ms | 1.0× | 1/7 | 239.7ms | 187.2ms | 71.3 MB | 5/7 | 100000 |
| python | 842.4ms | 16.0× | 7/7 | 853.1ms | 10.7ms | 10.8 MB | 1/7 | 100000 |
| node | 654.4ms | 12.5× | 6/7 | 672.3ms | 17.9ms | 66.9 MB | 4/7 | 100000 |
| ruby | 585.6ms | 11.2× | 4/7 | 625.3ms | 39.7ms | 19.1 MB | 2/7 | 100000 |
| dotnet | 160.5ms | 3.1× | 2/7 | 182.5ms | 22.0ms | 27.9 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.380s | 11.9× | 4/7 | 1.411s | 31.3ms | 291.9 MB | 6/7 | 1000000 |
| clojure | 4.512s | 38.9× | 6/7 | 4.845s | 332.7ms | 770.3 MB | 7/7 | 1000000 |
| elixir | 254.2ms | 2.2× | 2/7 | 441.4ms | 187.2ms | 72.0 MB | 5/7 | 1000000 |
| python | 4.809s | 41.5× | 7/7 | 4.819s | 10.7ms | 16.2 MB | 1/7 | 1000000 |
| node | 115.9ms | 1.0× | 1/7 | 133.8ms | 17.9ms | 65.4 MB | 4/7 | 1000000 |
| ruby | 3.581s | 30.9× | 5/7 | 3.621s | 39.7ms | 23.1 MB | 2/7 | 1000000 |
| dotnet | 857.2ms | 7.4× | 3/7 | 879.2ms | 22.0ms | 30.3 MB | 3/7 | 1000000 |
