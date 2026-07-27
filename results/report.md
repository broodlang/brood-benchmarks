# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-27 12:24.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.6ms | 1.2× | 2/7 | 12.6ms | — | 20.1 MB | 3/7 | 0 |
| clojure | 344.5ms | 34.1× | 7/7 | 344.5ms | — | 103.5 MB | 7/7 | 0 |
| elixir | 183.3ms | 18.1× | 6/7 | 183.3ms | — | 70.1 MB | 6/7 | 0 |
| python | 10.1ms | 1.0× | 1/7 | 10.1ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.4ms | 1.8× | 3/7 | 18.4ms | — | 42.3 MB | 5/7 | 0 |
| ruby | 39.2ms | 3.9× | 5/7 | 39.2ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 21.8ms | 2.2× | 4/7 | 21.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 58.7ms | 1.4× | 2/7 | 71.3ms | 12.6ms | 24.1 MB | 3/7 | 9227465 |
| clojure | 197.0ms | 4.5× | 5/7 | 541.5ms | 344.5ms | 108.5 MB | 7/7 | 9227465 |
| elixir | 78.5ms | 1.8× | 4/7 | 261.8ms | 183.3ms | 73.0 MB | 6/7 | 9227465 |
| python | 780.5ms | 18.0× | 7/7 | 790.6ms | 10.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.8ms | 1.7× | 3/7 | 92.2ms | 18.4ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 607.4ms | 14.0× | 6/7 | 646.6ms | 39.2ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 43.4ms | 1.0× | 1/7 | 65.2ms | 21.8ms | 25.8 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.0ms | 3.5× | 3/7 | 53.6ms | 12.6ms | 24.1 MB | 3/7 | 449999985000000 |
| clojure | 142.8ms | 12.1× | 5/7 | 487.3ms | 344.5ms | 108.3 MB | 7/7 | 449999985000000 |
| elixir | 50.5ms | 4.3× | 4/7 | 233.8ms | 183.3ms | 72.2 MB | 6/7 | 449999985000000 |
| python | 2.556s | 216.6× | 7/7 | 2.566s | 10.1ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.9ms | 2.5× | 2/7 | 48.3ms | 18.4ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 583.7ms | 49.5× | 6/7 | 622.9ms | 39.2ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 11.8ms | 1.0× | 1/7 | 33.6ms | 21.8ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.2ms | 1.0× | 1/7 | 15.8ms | 12.6ms | 20.4 MB | 3/7 | 12499997500000 |
| clojure | 171.3ms | 53.5× | 5/7 | 515.8ms | 344.5ms | 220.7 MB | 7/7 | 12499997500000 |
| elixir | 29.9ms | 9.3× | 3/7 | 213.2ms | 183.3ms | 70.5 MB | 5/7 | 12499997500000 |
| python | 106.2ms | 33.2× | 4/7 | 116.3ms | 10.1ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 222.2ms | 69.4× | 6/7 | 240.6ms | 18.4ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 223.4ms | 69.8× | 7/7 | 262.6ms | 39.2ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.8ms | 3.7× | 2/7 | 33.6ms | 21.8ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.6ms | 5.5× | 4/7 | 58.2ms | 12.6ms | 25.5 MB | 3/7 | 13848 |
| clojure | 144.8ms | 17.4× | 7/7 | 489.3ms | 344.5ms | 109.1 MB | 7/7 | 13848 |
| elixir | 20.2ms | 2.4× | 3/7 | 203.5ms | 183.3ms | 72.8 MB | 6/7 | 13848 |
| python | 122.7ms | 14.8× | 6/7 | 132.8ms | 10.1ms | 9.9 MB | 1/7 | 13848 |
| node | 8.3ms | 1.0× | 1/7 | 26.7ms | 18.4ms | 48.3 MB | 5/7 | 13848 |
| ruby | 113.8ms | 13.7× | 5/7 | 153.0ms | 39.2ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.3ms | 1.0× | 2/7 | 30.1ms | 21.8ms | 26.1 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.2ms | 1.9× | 2/7 | 97.8ms | 12.6ms | 25.3 MB | 3/7 | 442 |
| clojure | 433.2ms | 9.5× | 5/7 | 777.7ms | 344.5ms | 371.3 MB | 7/7 | 442 |
| elixir | 104.7ms | 2.3× | 3/7 | 288.0ms | 183.3ms | 70.4 MB | 6/7 | 442 |
| python | 2.541s | 55.5× | 7/7 | 2.551s | 10.1ms | 9.8 MB | 1/7 | 442 |
| node | 173.3ms | 3.8× | 4/7 | 191.7ms | 18.4ms | 47.9 MB | 5/7 | 442 |
| ruby | 845.5ms | 18.5× | 6/7 | 884.7ms | 39.2ms | 19.2 MB | 2/7 | 442 |
| dotnet | 45.8ms | 1.0× | 1/7 | 67.6ms | 21.8ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 177.6ms | 9.6× | 4/7 | 190.2ms | 12.6ms | 25.2 MB | 3/7 | 6129302 |
| clojure | 155.1ms | 8.4× | 3/7 | 499.6ms | 344.5ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 253.9ms | 13.7× | 5/7 | 437.2ms | 183.3ms | 71.9 MB | 6/7 | 6129302 |
| python | 1.433s | 77.5× | 7/7 | 1.443s | 10.1ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.9ms | 1.1× | 2/7 | 39.3ms | 18.4ms | 49.5 MB | 5/7 | 6129302 |
| ruby | 415.3ms | 22.4× | 6/7 | 454.5ms | 39.2ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.5ms | 1.0× | 1/7 | 40.3ms | 21.8ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.8ms | 31.9× | 4/7 | 146.4ms | 12.6ms | 44.7 MB | 4/7 | 654353666 |
| clojure | 177.8ms | 42.3× | 5/7 | 522.3ms | 344.5ms | 118.6 MB | 7/7 | 654353666 |
| elixir | 58.9ms | 14.0× | 3/7 | 242.2ms | 183.3ms | 74.4 MB | 6/7 | 654353666 |
| python | 452.3ms | 107.7× | 7/7 | 462.4ms | 10.1ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.8ms | 4.0× | 2/7 | 35.2ms | 18.4ms | 51.7 MB | 5/7 | 654353666 |
| ruby | 276.9ms | 65.9× | 6/7 | 316.1ms | 39.2ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.2ms | 1.0× | 1/7 | 26.0ms | 21.8ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.0ms | 1.0× | 1/7 | 25.6ms | 12.6ms | 30.7 MB | 1/7 | 3388889 |
| clojure | 154.6ms | 11.9× | 7/7 | 499.1ms | 344.5ms | 168.5 MB | 6/7 | 3388889 |
| elixir | 118.4ms | 9.1× | 6/7 | 301.7ms | 183.3ms | 201.3 MB | 7/7 | 3388889 |
| python | 43.0ms | 3.3× | 3/7 | 53.1ms | 10.1ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.2ms | 4.9× | 4/7 | 82.6ms | 18.4ms | 94.9 MB | 5/7 | 3388889 |
| ruby | 82.9ms | 6.4× | 5/7 | 122.1ms | 39.2ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.8ms | 2.4× | 2/7 | 52.6ms | 21.8ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.1ms | 1.2× | 2/7 | 47.7ms | 12.6ms | 26.0 MB | 3/7 | 374854840 |
| clojure | 260.3ms | 8.9× | 7/7 | 604.8ms | 344.5ms | 302.6 MB | 7/7 | 374854840 |
| elixir | 155.1ms | 5.3× | 5/7 | 338.4ms | 183.3ms | 72.1 MB | 6/7 | 374854840 |
| python | 175.4ms | 6.0× | 6/7 | 185.5ms | 10.1ms | 10.0 MB | 1/7 | 374854840 |
| node | 29.4ms | 1.0× | 1/7 | 47.8ms | 18.4ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 70.2ms | 2.4× | 4/7 | 109.4ms | 39.2ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 36.4ms | 1.2× | 3/7 | 58.2ms | 21.8ms | 27.2 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 108.3ms | 12.0× | 6/7 | 120.9ms | 12.6ms | 56.0 MB | 5/7 | 1638200 |
| clojure | 167.8ms | 18.6× | 7/7 | 512.3ms | 344.5ms | 149.6 MB | 7/7 | 1638200 |
| elixir | 9.0ms | 1.0× | 1/7 | 192.3ms | 183.3ms | 72.6 MB | 6/7 | 1638200 |
| python | 96.1ms | 10.7× | 4/7 | 106.2ms | 10.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.2ms | 2.4× | 3/7 | 39.6ms | 18.4ms | 55.6 MB | 4/7 | 1638200 |
| ruby | 96.8ms | 10.8× | 5/7 | 136.0ms | 39.2ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 12.6ms | 1.4× | 2/7 | 34.4ms | 21.8ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 191.9ms | 3.0× | 6/7 | 204.5ms | 12.6ms | 200.4 MB | 7/7 | 46468819 |
| clojure | 241.4ms | 3.8× | 7/7 | 585.9ms | 344.5ms | 123.4 MB | 5/7 | 46468819 |
| elixir | 105.5ms | 1.7× | 4/7 | 288.8ms | 183.3ms | 157.1 MB | 6/7 | 46468819 |
| python | 186.2ms | 2.9× | 5/7 | 196.3ms | 10.1ms | 25.8 MB | 2/7 | 46468819 |
| node | 102.8ms | 1.6× | 3/7 | 121.2ms | 18.4ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 71.8ms | 1.1× | 2/7 | 111.0ms | 39.2ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 63.8ms | 1.0× | 1/7 | 85.6ms | 21.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.5ms | 23.6× | 5/7 | 95.1ms | 12.6ms | 43.8 MB | 4/7 | 724 |
| clojure | 234.0ms | 66.9× | 7/7 | 578.5ms | 344.5ms | 136.0 MB | 7/7 | 724 |
| elixir | 3.5ms | 1.0× | 1/7 | 186.8ms | 183.3ms | 70.2 MB | 6/7 | 724 |
| python | 53.7ms | 15.3× | 4/7 | 63.8ms | 10.1ms | 9.9 MB | 1/7 | 724 |
| node | 6.8ms | 1.9× | 2/7 | 25.2ms | 18.4ms | 50.4 MB | 5/7 | 724 |
| ruby | 123.5ms | 35.3× | 6/7 | 162.7ms | 39.2ms | 19.4 MB | 2/7 | 724 |
| dotnet | 19.3ms | 5.5× | 3/7 | 41.1ms | 21.8ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.2ms | 2.4× | 2/7 | 59.8ms | 12.6ms | 25.5 MB | 3/7 | 9900000 |
| clojure | 1.085s | 55.6× | 7/7 | 1.430s | 344.5ms | 371.4 MB | 7/7 | 9900000 |
| elixir | 19.5ms | 1.0× | 1/7 | 202.8ms | 183.3ms | 69.9 MB | 6/7 | 9900000 |
| python | 48.1ms | 2.5× | 3/7 | 58.2ms | 10.1ms | 9.9 MB | 1/7 | 9900000 |
| node | 564.1ms | 28.9× | 6/7 | 582.5ms | 18.4ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 107.5ms | 5.5× | 4/7 | 146.7ms | 39.2ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 288.3ms | 14.8× | 5/7 | 310.1ms | 21.8ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.9ms | 6.4× | 2/7 | 58.5ms | 12.6ms | 25.2 MB | 2/7 | 2475000 |
| clojure | 1.327s | 184.3× | 7/7 | 1.672s | 344.5ms | 375.7 MB | 7/7 | 2475000 |
| elixir | 7.2ms | 1.0× | 1/7 | 190.5ms | 183.3ms | 71.7 MB | 6/7 | 2475000 |
| python | 225.3ms | 31.3× | 5/7 | 235.4ms | 10.1ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.5ms | 29.2× | 4/7 | 228.9ms | 18.4ms | 49.9 MB | 5/7 | 2475000 |
| ruby | 112.7ms | 15.7× | 3/7 | 151.9ms | 39.2ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 663.4ms | 92.1× | 6/7 | 685.2ms | 21.8ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.3ms | 7.2× | 6/7 | 44.9ms | 12.6ms | 25.1 MB | 3/7 | 155553889038886 |
| clojure | 125.2ms | 27.8× | 7/7 | 469.7ms | 344.5ms | 108.9 MB | 7/7 | 155553889038886 |
| elixir | 10.4ms | 2.3× | 5/7 | 193.7ms | 183.3ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 1.0× | 1/7 | 14.6ms | 10.1ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.3ms | 1.6× | 4/7 | 25.7ms | 18.4ms | 51.7 MB | 5/7 | 155553889038886 |
| ruby | 7.2ms | 1.6× | 3/7 | 46.4ms | 39.2ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 7.0ms | 1.6× | 2/7 | 28.8ms | 21.8ms | 27.9 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 350.7ms | 1.4× | 3/7 | 363.3ms | 12.6ms | 25.5 MB | 3/7 | 24558 |
| clojure | 550.7ms | 2.3× | 5/7 | 895.2ms | 344.5ms | 374.5 MB | 7/7 | 24558 |
| elixir | 288.1ms | 1.2× | 2/7 | 471.4ms | 183.3ms | 71.3 MB | 6/7 | 24558 |
| python | 3.850s | 15.8× | 7/7 | 3.860s | 10.1ms | 11.0 MB | 1/7 | 24558 |
| node | 394.0ms | 1.6× | 4/7 | 412.4ms | 18.4ms | 48.1 MB | 5/7 | 24558 |
| ruby | 1.665s | 6.8× | 6/7 | 1.704s | 39.2ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 243.6ms | 1.0× | 1/7 | 265.4ms | 21.8ms | 26.1 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.7ms | 12.7× | 3/7 | 48.3ms | 12.6ms | 32.8 MB | 4/7 | 78498 |
| clojure | 129.3ms | 46.2× | 7/7 | 473.8ms | 344.5ms | 108.0 MB | 7/7 | 78498 |
| elixir | 52.7ms | 18.8× | 4/7 | 236.0ms | 183.3ms | 78.0 MB | 6/7 | 78498 |
| python | 114.2ms | 40.8× | 6/7 | 124.3ms | 10.1ms | 10.9 MB | 1/7 | 78498 |
| node | 7.1ms | 2.5× | 2/7 | 25.5ms | 18.4ms | 49.2 MB | 5/7 | 78498 |
| ruby | 83.9ms | 30.0× | 5/7 | 123.1ms | 39.2ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.8ms | 1.0× | 1/7 | 24.6ms | 21.8ms | 27.3 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 61.8ms | 2.8× | 4/7 | 74.4ms | 12.6ms | 72.5 MB | 5/7 | 30039386344 |
| clojure | 287.4ms | 13.0× | 7/7 | 631.9ms | 344.5ms | 291.2 MB | 7/7 | 30039386344 |
| elixir | 120.3ms | 5.4× | 6/7 | 303.6ms | 183.3ms | 99.3 MB | 6/7 | 30039386344 |
| python | 79.0ms | 3.6× | 5/7 | 89.1ms | 10.1ms | 14.9 MB | 1/7 | 30039386344 |
| node | 23.0ms | 1.0× | 2/7 | 41.4ms | 18.4ms | 53.6 MB | 4/7 | 30039386344 |
| ruby | 38.2ms | 1.7× | 3/7 | 77.4ms | 39.2ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 22.1ms | 1.0× | 1/7 | 43.9ms | 21.8ms | 30.3 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 314.1ms | 46.2× | 6/7 | 326.7ms | 12.6ms | 54.4 MB | 5/7 | -169078071 |
| clojure | 177.4ms | 26.1× | 4/7 | 521.9ms | 344.5ms | 107.8 MB | 7/7 | -169078071 |
| elixir | 140.5ms | 20.7× | 3/7 | 323.8ms | 183.3ms | 69.7 MB | 6/7 | -169078071 |
| python | 698.3ms | 102.7× | 7/7 | 708.4ms | 10.1ms | 10.4 MB | 1/7 | -169078071 |
| node | 12.3ms | 1.8× | 2/7 | 30.7ms | 18.4ms | 50.1 MB | 4/7 | -169078071 |
| ruby | 299.6ms | 44.1× | 5/7 | 338.8ms | 39.2ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.8ms | 1.0× | 1/7 | 28.6ms | 21.8ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.8ms | 145.8× | 6/7 | 158.4ms | 12.6ms | 77.3 MB | 6/7 | 1489952542 |
| clojure | 378.5ms | 378.5× | 7/7 | 723.0ms | 344.5ms | 158.1 MB | 7/7 | 1489952542 |
| elixir | 2.5ms | 2.5× | 2/7 | 185.8ms | 183.3ms | 73.8 MB | 5/7 | 1489952542 |
| python | 8.4ms | 8.4× | 4/7 | 18.5ms | 10.1ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.0ms | 1.0× | 1/7 | 19.4ms | 18.4ms | 43.8 MB | 4/7 | 1489952542 |
| ruby | 4.2ms | 4.2× | 3/7 | 43.4ms | 39.2ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 43.0ms | 43.0× | 5/7 | 64.8ms | 21.8ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.1ms | 23.3× | 6/7 | 91.7ms | 12.6ms | 43.0 MB | 4/7 | 10000 |
| clojure | 122.8ms | 36.1× | 7/7 | 467.3ms | 344.5ms | 107.7 MB | 7/7 | 10000 |
| elixir | 14.0ms | 4.1× | 5/7 | 197.3ms | 183.3ms | 70.5 MB | 6/7 | 10000 |
| python | 13.1ms | 3.9× | 4/7 | 23.2ms | 10.1ms | 11.2 MB | 1/7 | 10000 |
| node | 3.4ms | 1.0× | 1/7 | 21.8ms | 18.4ms | 50.0 MB | 5/7 | 10000 |
| ruby | 7.3ms | 2.1× | 2/7 | 46.5ms | 39.2ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 12.7ms | 3.7× | 3/7 | 34.5ms | 21.8ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 104.2ms | 27.4× | 6/7 | 116.8ms | 12.6ms | 100.3 MB | 6/7 | 12081249 |
| clojure | 149.0ms | 39.2× | 7/7 | 493.5ms | 344.5ms | 109.7 MB | 7/7 | 12081249 |
| elixir | 10.0ms | 2.6× | 4/7 | 193.3ms | 183.3ms | 75.8 MB | 5/7 | 12081249 |
| python | 13.2ms | 3.5× | 5/7 | 23.3ms | 10.1ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.3ms | 1.4× | 2/7 | 23.7ms | 18.4ms | 50.5 MB | 4/7 | 12081249 |
| ruby | 7.7ms | 2.0× | 3/7 | 46.9ms | 39.2ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 3.8ms | 1.0× | 1/7 | 25.6ms | 21.8ms | 27.1 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.5ms | 2.6× | 3/7 | 58.1ms | 12.6ms | 46.6 MB | 3/7 | 6100000 |
| clojure | 176.4ms | 10.0× | 5/7 | 520.9ms | 344.5ms | 134.7 MB | 7/7 | 6100000 |
| elixir | 19.9ms | 1.1× | 2/7 | 203.2ms | 183.3ms | 76.8 MB | 5/7 | 6100000 |
| python | 547.7ms | 30.9× | 6/7 | 557.8ms | 10.1ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.7ms | 3.0× | 4/7 | 71.1ms | 18.4ms | 51.3 MB | 4/7 | 6100000 |
| ruby | 1.567s | 88.5× | 7/7 | 1.606s | 39.2ms | 133.8 MB | 6/7 | 6100000 |
| dotnet | 17.7ms | 1.0× | 1/7 | 39.5ms | 21.8ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.6ms | 1.5× | 2/7 | 184.2ms | 12.6ms | 27.2 MB | 3/7 | 134626900 |
| clojure | 370.6ms | 3.3× | 5/7 | 715.1ms | 344.5ms | 136.4 MB | 6/7 | 134626900 |
| elixir | 289.4ms | 2.6× | 3/7 | 472.7ms | 183.3ms | 70.8 MB | 5/7 | 134626900 |
| python | 2.430s | 21.5× | 7/7 | 2.440s | 10.1ms | 21.9 MB | 2/7 | 134626900 |
| node | 289.7ms | 2.6× | 4/7 | 308.1ms | 18.4ms | 181.7 MB | 7/7 | 134626900 |
| ruby | 1.838s | 16.2× | 6/7 | 1.877s | 39.2ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 113.1ms | 1.0× | 1/7 | 134.9ms | 21.8ms | 28.1 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 168.2ms | 1.3× | 3/7 | 180.8ms | 12.6ms | 83.7 MB | 5/7 | 500 |
| clojure | 781.4ms | 6.3× | 7/7 | 1.126s | 344.5ms | 321.1 MB | 6/7 | 500 |
| elixir | 543.0ms | 4.3× | 6/7 | 726.3ms | 183.3ms | 520.9 MB | 7/7 | 500 |
| python | 173.2ms | 1.4× | 4/7 | 183.3ms | 10.1ms | 45.4 MB | 1/7 | 500 |
| node | 124.9ms | 1.0× | 1/7 | 143.3ms | 18.4ms | 64.7 MB | 4/7 | 500 |
| ruby | 201.5ms | 1.6× | 5/7 | 240.7ms | 39.2ms | 45.8 MB | 2/7 | 500 |
| dotnet | 148.6ms | 1.2× | 2/7 | 170.4ms | 21.8ms | 47.9 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 197.4ms | 3.5× | 3/7 | 210.0ms | 12.6ms | 48.0 MB | 4/7 | 100000 |
| clojure | 567.9ms | 10.2× | 4/7 | 912.4ms | 344.5ms | 133.0 MB | 7/7 | 100000 |
| elixir | 55.9ms | 1.0× | 1/7 | 239.2ms | 183.3ms | 70.8 MB | 6/7 | 100000 |
| python | 814.7ms | 14.6× | 7/7 | 824.8ms | 10.1ms | 10.9 MB | 1/7 | 100000 |
| node | 633.8ms | 11.3× | 6/7 | 652.2ms | 18.4ms | 67.1 MB | 5/7 | 100000 |
| ruby | 592.8ms | 10.6× | 5/7 | 632.0ms | 39.2ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 162.5ms | 2.9× | 2/7 | 184.3ms | 21.8ms | 27.9 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 729.5ms | 6.3× | 4/7 | 742.1ms | 12.6ms | 93.6 MB | 6/7 | 1000000 |
| clojure | 4.321s | 37.6× | 6/7 | 4.666s | 344.5ms | 744.1 MB | 7/7 | 1000000 |
| elixir | 253.5ms | 2.2× | 2/7 | 436.8ms | 183.3ms | 71.0 MB | 5/7 | 1000000 |
| python | 4.637s | 40.4× | 7/7 | 4.647s | 10.1ms | 16.1 MB | 1/7 | 1000000 |
| node | 114.9ms | 1.0× | 1/7 | 133.3ms | 18.4ms | 65.3 MB | 4/7 | 1000000 |
| ruby | 3.438s | 29.9× | 5/7 | 3.477s | 39.2ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 727.0ms | 6.3× | 3/7 | 748.8ms | 21.8ms | 30.4 MB | 3/7 | 1000000 |
