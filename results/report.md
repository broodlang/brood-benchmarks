# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-17 13:45.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.8ms | 3.3× | 4/7 | 36.8ms | — | 25.7 MB | 3/7 | 0 |
| clojure | 359.9ms | 32.7× | 7/7 | 359.9ms | — | 102.9 MB | 7/7 | 0 |
| elixir | 191.9ms | 17.4× | 6/7 | 191.9ms | — | 70.9 MB | 6/7 | 0 |
| python | 11.0ms | 1.0× | 1/7 | 11.0ms | — | 9.8 MB | 1/7 | 0 |
| node | 20.0ms | 1.8× | 2/7 | 20.0ms | — | 44.0 MB | 5/7 | 0 |
| ruby | 42.7ms | 3.9× | 5/7 | 42.7ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 22.3ms | 2.0× | 3/7 | 22.3ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 55.7ms | 1.3× | 2/7 | 92.5ms | 36.8ms | 28.6 MB | 4/7 | 9227465 |
| clojure | 220.3ms | 5.0× | 5/7 | 580.2ms | 359.9ms | 108.1 MB | 7/7 | 9227465 |
| elixir | 74.3ms | 1.7× | 4/7 | 266.2ms | 191.9ms | 72.6 MB | 6/7 | 9227465 |
| python | 733.7ms | 16.6× | 7/7 | 744.7ms | 11.0ms | 9.8 MB | 1/7 | 9227465 |
| node | 72.2ms | 1.6× | 3/7 | 92.2ms | 20.0ms | 50.8 MB | 5/7 | 9227465 |
| ruby | 588.8ms | 13.4× | 6/7 | 631.5ms | 42.7ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 44.1ms | 1.0× | 1/7 | 66.4ms | 22.3ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.0ms | 2.9× | 3/7 | 72.8ms | 36.8ms | 28.9 MB | 4/7 | 449999985000000 |
| clojure | 131.6ms | 10.4× | 5/7 | 491.5ms | 359.9ms | 108.2 MB | 7/7 | 449999985000000 |
| elixir | 48.1ms | 3.8× | 4/7 | 240.0ms | 191.9ms | 70.0 MB | 6/7 | 449999985000000 |
| python | 2.267s | 180.0× | 7/7 | 2.278s | 11.0ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 28.8ms | 2.3× | 2/7 | 48.8ms | 20.0ms | 52.7 MB | 5/7 | 449999985000000 |
| ruby | 581.7ms | 46.2× | 6/7 | 624.4ms | 42.7ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 12.6ms | 1.0× | 1/7 | 34.9ms | 22.3ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.2ms | 1.0× | 1/7 | 38.0ms | 36.8ms | 25.2 MB | 3/7 | 12499997500000 |
| clojure | 164.1ms | 136.7× | 5/7 | 524.0ms | 359.9ms | 220.4 MB | 7/7 | 12499997500000 |
| elixir | 31.2ms | 26.0× | 3/7 | 223.1ms | 191.9ms | 72.3 MB | 5/7 | 12499997500000 |
| python | 104.6ms | 87.2× | 4/7 | 115.6ms | 11.0ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 218.5ms | 182.1× | 6/7 | 238.5ms | 20.0ms | 92.9 MB | 6/7 | 12499997500000 |
| ruby | 227.8ms | 189.8× | 7/7 | 270.5ms | 42.7ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.7ms | 9.7× | 2/7 | 34.0ms | 22.3ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.4ms | 6.5× | 4/7 | 78.2ms | 36.8ms | 29.3 MB | 4/7 | 13848 |
| clojure | 125.2ms | 19.6× | 7/7 | 485.1ms | 359.9ms | 109.6 MB | 7/7 | 13848 |
| elixir | 13.8ms | 2.2× | 3/7 | 205.7ms | 191.9ms | 72.0 MB | 6/7 | 13848 |
| python | 122.2ms | 19.1× | 6/7 | 133.2ms | 11.0ms | 9.9 MB | 1/7 | 13848 |
| node | 6.4ms | 1.0× | 1/7 | 26.4ms | 20.0ms | 51.3 MB | 5/7 | 13848 |
| ruby | 114.9ms | 18.0× | 5/7 | 157.6ms | 42.7ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.4ms | 1.3× | 2/7 | 30.7ms | 22.3ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.1ms | 1.7× | 2/7 | 117.9ms | 36.8ms | 28.9 MB | 4/7 | 442 |
| clojure | 417.6ms | 9.0× | 5/7 | 777.5ms | 359.9ms | 370.8 MB | 7/7 | 442 |
| elixir | 105.8ms | 2.3× | 3/7 | 297.7ms | 191.9ms | 70.7 MB | 6/7 | 442 |
| python | 2.607s | 56.1× | 7/7 | 2.618s | 11.0ms | 9.8 MB | 1/7 | 442 |
| node | 171.6ms | 3.7× | 4/7 | 191.6ms | 20.0ms | 51.0 MB | 5/7 | 442 |
| ruby | 845.4ms | 18.2× | 6/7 | 888.1ms | 42.7ms | 19.2 MB | 2/7 | 442 |
| dotnet | 46.5ms | 1.0× | 1/7 | 68.8ms | 22.3ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 170.8ms | 9.4× | 4/7 | 207.6ms | 36.8ms | 29.4 MB | 4/7 | 6129302 |
| clojure | 143.0ms | 7.9× | 3/7 | 502.9ms | 359.9ms | 116.0 MB | 7/7 | 6129302 |
| elixir | 258.3ms | 14.3× | 5/7 | 450.2ms | 191.9ms | 71.0 MB | 6/7 | 6129302 |
| python | 1.325s | 73.2× | 7/7 | 1.335s | 11.0ms | 9.9 MB | 1/7 | 6129302 |
| node | 18.7ms | 1.0× | 2/7 | 38.7ms | 20.0ms | 52.5 MB | 5/7 | 6129302 |
| ruby | 424.8ms | 23.5× | 6/7 | 467.5ms | 42.7ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 18.1ms | 1.0× | 1/7 | 40.4ms | 22.3ms | 26.2 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 129.5ms | 31.6× | 4/7 | 166.3ms | 36.8ms | 43.9 MB | 4/7 | 654353666 |
| clojure | 197.9ms | 48.3× | 5/7 | 557.8ms | 359.9ms | 117.6 MB | 7/7 | 654353666 |
| elixir | 58.9ms | 14.4× | 3/7 | 250.8ms | 191.9ms | 78.9 MB | 6/7 | 654353666 |
| python | 468.1ms | 114.2× | 7/7 | 479.1ms | 11.0ms | 10.3 MB | 1/7 | 654353666 |
| node | 15.7ms | 3.8× | 2/7 | 35.7ms | 20.0ms | 55.1 MB | 5/7 | 654353666 |
| ruby | 289.7ms | 70.7× | 6/7 | 332.4ms | 42.7ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.1ms | 1.0× | 1/7 | 26.4ms | 22.3ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.8ms | 1.0× | 1/7 | 47.6ms | 36.8ms | 35.2 MB | 1/7 | 3388889 |
| clojure | 155.3ms | 14.4× | 7/7 | 515.2ms | 359.9ms | 168.8 MB | 6/7 | 3388889 |
| elixir | 114.6ms | 10.6× | 6/7 | 306.5ms | 191.9ms | 203.0 MB | 7/7 | 3388889 |
| python | 42.9ms | 4.0× | 3/7 | 53.9ms | 11.0ms | 39.9 MB | 2/7 | 3388889 |
| node | 63.6ms | 5.9× | 4/7 | 83.6ms | 20.0ms | 97.9 MB | 5/7 | 3388889 |
| ruby | 80.6ms | 7.5× | 5/7 | 123.3ms | 42.7ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 32.0ms | 3.0× | 2/7 | 54.3ms | 22.3ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 1.1× | 2/7 | 67.7ms | 36.8ms | 30.2 MB | 4/7 | 374854840 |
| clojure | 252.7ms | 8.7× | 7/7 | 612.6ms | 359.9ms | 302.2 MB | 7/7 | 374854840 |
| elixir | 172.9ms | 6.0× | 5/7 | 364.8ms | 191.9ms | 70.4 MB | 6/7 | 374854840 |
| python | 175.2ms | 6.1× | 6/7 | 186.2ms | 11.0ms | 9.9 MB | 1/7 | 374854840 |
| node | 28.9ms | 1.0× | 1/7 | 48.9ms | 20.0ms | 53.0 MB | 5/7 | 374854840 |
| ruby | 70.4ms | 2.4× | 4/7 | 113.1ms | 42.7ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 37.1ms | 1.3× | 3/7 | 59.4ms | 22.3ms | 27.2 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.7ms | 22.9× | 6/7 | 146.5ms | 36.8ms | 59.1 MB | 5/7 | 1638200 |
| clojure | 153.7ms | 32.0× | 7/7 | 513.6ms | 359.9ms | 149.5 MB | 7/7 | 1638200 |
| elixir | 4.8ms | 1.0× | 1/7 | 196.7ms | 191.9ms | 72.3 MB | 6/7 | 1638200 |
| python | 97.6ms | 20.3× | 5/7 | 108.6ms | 11.0ms | 10.1 MB | 1/7 | 1638200 |
| node | 18.7ms | 3.9× | 3/7 | 38.7ms | 20.0ms | 58.8 MB | 4/7 | 1638200 |
| ruby | 95.9ms | 20.0× | 4/7 | 138.6ms | 42.7ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 14.9ms | 3.1× | 2/7 | 37.2ms | 22.3ms | 32.5 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 203.4ms | 3.1× | 6/7 | 240.2ms | 36.8ms | 192.2 MB | 7/7 | 46468819 |
| clojure | 237.3ms | 3.6× | 7/7 | 597.2ms | 359.9ms | 123.0 MB | 5/7 | 46468819 |
| elixir | 112.6ms | 1.7× | 4/7 | 304.5ms | 191.9ms | 159.7 MB | 6/7 | 46468819 |
| python | 189.8ms | 2.9× | 5/7 | 200.8ms | 11.0ms | 26.0 MB | 2/7 | 46468819 |
| node | 103.6ms | 1.6× | 3/7 | 123.6ms | 20.0ms | 67.8 MB | 4/7 | 46468819 |
| ruby | 67.4ms | 1.0× | 2/7 | 110.1ms | 42.7ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 65.3ms | 1.0× | 1/7 | 87.6ms | 22.3ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.4ms | 23.6× | 5/7 | 117.2ms | 36.8ms | 47.4 MB | 4/7 | 724 |
| clojure | 191.4ms | 56.3× | 7/7 | 551.3ms | 359.9ms | 136.0 MB | 7/7 | 724 |
| elixir | 3.4ms | 1.0× | 1/7 | 195.3ms | 191.9ms | 70.2 MB | 6/7 | 724 |
| python | 53.5ms | 15.7× | 4/7 | 64.5ms | 11.0ms | 9.8 MB | 1/7 | 724 |
| node | 5.3ms | 1.6× | 2/7 | 25.3ms | 20.0ms | 53.4 MB | 5/7 | 724 |
| ruby | 126.5ms | 37.2× | 6/7 | 169.2ms | 42.7ms | 19.4 MB | 2/7 | 724 |
| dotnet | 19.0ms | 5.6× | 3/7 | 41.3ms | 22.3ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.0ms | 2.7× | 2/7 | 78.8ms | 36.8ms | 29.3 MB | 3/7 | 9900000 |
| clojure | 1.083s | 69.0× | 7/7 | 1.443s | 359.9ms | 370.4 MB | 7/7 | 9900000 |
| elixir | 15.7ms | 1.0× | 1/7 | 207.6ms | 191.9ms | 71.4 MB | 6/7 | 9900000 |
| python | 47.4ms | 3.0× | 3/7 | 58.4ms | 11.0ms | 9.8 MB | 1/7 | 9900000 |
| node | 563.6ms | 35.9× | 6/7 | 583.6ms | 20.0ms | 53.2 MB | 5/7 | 9900000 |
| ruby | 117.7ms | 7.5× | 4/7 | 160.4ms | 42.7ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 295.6ms | 18.8× | 5/7 | 317.9ms | 22.3ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.2ms | 7.3× | 2/7 | 76.0ms | 36.8ms | 29.3 MB | 3/7 | 2475000 |
| clojure | 1.312s | 243.0× | 7/7 | 1.672s | 359.9ms | 375.3 MB | 7/7 | 2475000 |
| elixir | 5.4ms | 1.0× | 1/7 | 197.3ms | 191.9ms | 73.0 MB | 6/7 | 2475000 |
| python | 234.0ms | 43.3× | 5/7 | 245.0ms | 11.0ms | 9.9 MB | 1/7 | 2475000 |
| node | 205.7ms | 38.1× | 4/7 | 225.7ms | 20.0ms | 52.9 MB | 5/7 | 2475000 |
| ruby | 109.8ms | 20.3× | 3/7 | 152.5ms | 42.7ms | 25.9 MB | 2/7 | 2475000 |
| dotnet | 666.1ms | 123.4× | 6/7 | 688.4ms | 22.3ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.8ms | 17.1× | 6/7 | 67.6ms | 36.8ms | 28.9 MB | 4/7 | 155553889038886 |
| clojure | 120.9ms | 67.2× | 7/7 | 480.8ms | 359.9ms | 108.7 MB | 7/7 | 155553889038886 |
| elixir | 1.8ms | 1.0× | 1/7 | 193.7ms | 191.9ms | 70.9 MB | 6/7 | 155553889038886 |
| python | 3.7ms | 2.1× | 2/7 | 14.7ms | 11.0ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 6.6ms | 3.7× | 4/7 | 26.6ms | 20.0ms | 54.7 MB | 5/7 | 155553889038886 |
| ruby | 4.6ms | 2.6× | 3/7 | 47.3ms | 42.7ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 7.1ms | 3.9× | 5/7 | 29.4ms | 22.3ms | 28.0 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 342.2ms | 1.3× | 3/7 | 379.0ms | 36.8ms | 29.9 MB | 4/7 | 24558 |
| clojure | 538.9ms | 2.0× | 5/7 | 898.8ms | 359.9ms | 374.3 MB | 7/7 | 24558 |
| elixir | 278.7ms | 1.0× | 2/7 | 470.6ms | 191.9ms | 70.2 MB | 6/7 | 24558 |
| python | 3.868s | 14.1× | 7/7 | 3.879s | 11.0ms | 11.0 MB | 1/7 | 24558 |
| node | 392.2ms | 1.4× | 4/7 | 412.2ms | 20.0ms | 51.1 MB | 5/7 | 24558 |
| ruby | 1.658s | 6.1× | 6/7 | 1.701s | 42.7ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 273.6ms | 1.0× | 1/7 | 295.9ms | 22.3ms | 26.3 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.7ms | 9.6× | 3/7 | 70.5ms | 36.8ms | 36.5 MB | 4/7 | 78498 |
| clojure | 126.0ms | 36.0× | 7/7 | 485.9ms | 359.9ms | 108.8 MB | 7/7 | 78498 |
| elixir | 60.2ms | 17.2× | 4/7 | 252.1ms | 191.9ms | 78.0 MB | 6/7 | 78498 |
| python | 117.9ms | 33.7× | 6/7 | 128.9ms | 11.0ms | 10.8 MB | 1/7 | 78498 |
| node | 4.7ms | 1.3× | 2/7 | 24.7ms | 20.0ms | 52.1 MB | 5/7 | 78498 |
| ruby | 82.5ms | 23.6× | 5/7 | 125.2ms | 42.7ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 3.5ms | 1.0× | 1/7 | 25.8ms | 22.3ms | 27.3 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.2ms | 3.5× | 4/7 | 112.0ms | 36.8ms | 77.8 MB | 5/7 | 30039386344 |
| clojure | 282.1ms | 13.2× | 7/7 | 642.0ms | 359.9ms | 291.5 MB | 7/7 | 30039386344 |
| elixir | 120.5ms | 5.7× | 6/7 | 312.4ms | 191.9ms | 97.0 MB | 6/7 | 30039386344 |
| python | 91.5ms | 4.3× | 5/7 | 102.5ms | 11.0ms | 15.0 MB | 1/7 | 30039386344 |
| node | 21.3ms | 1.0× | 1/7 | 41.3ms | 20.0ms | 56.9 MB | 4/7 | 30039386344 |
| ruby | 39.6ms | 1.9× | 3/7 | 82.3ms | 42.7ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 23.0ms | 1.1× | 2/7 | 45.3ms | 22.3ms | 30.3 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 318.8ms | 56.9× | 6/7 | 355.6ms | 36.8ms | 49.0 MB | 4/7 | -169078071 |
| clojure | 172.2ms | 30.8× | 4/7 | 532.1ms | 359.9ms | 109.4 MB | 7/7 | -169078071 |
| elixir | 145.8ms | 26.0× | 3/7 | 337.7ms | 191.9ms | 70.7 MB | 6/7 | -169078071 |
| python | 680.1ms | 121.4× | 7/7 | 691.1ms | 11.0ms | 10.4 MB | 1/7 | -169078071 |
| node | 10.4ms | 1.9× | 2/7 | 30.4ms | 20.0ms | 53.2 MB | 5/7 | -169078071 |
| ruby | 288.2ms | 51.5× | 5/7 | 330.9ms | 42.7ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 5.6ms | 1.0× | 1/7 | 27.9ms | 22.3ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.1ms | 144.1× | 6/7 | 180.9ms | 36.8ms | 72.0 MB | 5/7 | 1489952542 |
| clojure | 414.8ms | 414.8× | 7/7 | 774.7ms | 359.9ms | 171.2 MB | 7/7 | 1489952542 |
| elixir | 4.8ms | 4.8× | 3/7 | 196.7ms | 191.9ms | 75.4 MB | 6/7 | 1489952542 |
| python | 9.0ms | 9.0× | 4/7 | 20.0ms | 11.0ms | 12.3 MB | 1/7 | 1489952542 |
| node | 0.0ms | < 1× | 1/7 | 19.7ms | 20.0ms | 45.8 MB | 4/7 | 1489952542 |
| ruby | 0.9ms | < 1× | 2/7 | 43.6ms | 42.7ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 43.7ms | 43.7× | 5/7 | 66.0ms | 22.3ms | 34.2 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 77.5ms | 43.1× | 6/7 | 114.3ms | 36.8ms | 48.2 MB | 4/7 | 10000 |
| clojure | 127.7ms | 70.9× | 7/7 | 487.6ms | 359.9ms | 108.0 MB | 7/7 | 10000 |
| elixir | 12.2ms | 6.8× | 4/7 | 204.1ms | 191.9ms | 70.1 MB | 6/7 | 10000 |
| python | 12.3ms | 6.8× | 5/7 | 23.3ms | 11.0ms | 11.1 MB | 1/7 | 10000 |
| node | 1.8ms | 1.0× | 1/7 | 21.8ms | 20.0ms | 53.2 MB | 5/7 | 10000 |
| ruby | 4.7ms | 2.6× | 2/7 | 47.4ms | 42.7ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 11.8ms | 6.6× | 3/7 | 34.1ms | 22.3ms | 31.8 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 97.5ms | 24.4× | 6/7 | 134.3ms | 36.8ms | 90.4 MB | 6/7 | 12081249 |
| clojure | 151.4ms | 37.9× | 7/7 | 511.3ms | 359.9ms | 108.4 MB | 7/7 | 12081249 |
| elixir | 7.9ms | 2.0× | 4/7 | 199.8ms | 191.9ms | 76.3 MB | 5/7 | 12081249 |
| python | 12.4ms | 3.1× | 5/7 | 23.4ms | 11.0ms | 10.2 MB | 1/7 | 12081249 |
| node | 4.0ms | 1.0× | 1/7 | 24.0ms | 20.0ms | 53.8 MB | 4/7 | 12081249 |
| ruby | 5.0ms | 1.2× | 3/7 | 47.7ms | 42.7ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 4.0ms | 1.0× | 2/7 | 26.3ms | 22.3ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.1ms | 2.8× | 3/7 | 82.9ms | 36.8ms | 58.0 MB | 4/7 | 6100000 |
| clojure | 177.7ms | 10.6× | 5/7 | 537.6ms | 359.9ms | 133.8 MB | 7/7 | 6100000 |
| elixir | 16.7ms | 1.0× | 1/7 | 208.6ms | 191.9ms | 77.4 MB | 5/7 | 6100000 |
| python | 560.6ms | 33.6× | 6/7 | 571.6ms | 11.0ms | 28.0 MB | 1/7 | 6100000 |
| node | 50.8ms | 3.0× | 4/7 | 70.8ms | 20.0ms | 54.3 MB | 3/7 | 6100000 |
| ruby | 1.599s | 95.7× | 7/7 | 1.641s | 42.7ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 17.2ms | 1.0× | 2/7 | 39.5ms | 22.3ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 170.5ms | 1.5× | 2/7 | 207.3ms | 36.8ms | 30.9 MB | 4/7 | 134626900 |
| clojure | 379.7ms | 3.2× | 5/7 | 739.6ms | 359.9ms | 135.6 MB | 6/7 | 134626900 |
| elixir | 310.2ms | 2.7× | 4/7 | 502.1ms | 191.9ms | 70.7 MB | 5/7 | 134626900 |
| python | 2.590s | 22.2× | 7/7 | 2.601s | 11.0ms | 21.7 MB | 2/7 | 134626900 |
| node | 304.7ms | 2.6× | 3/7 | 324.7ms | 20.0ms | 186.2 MB | 7/7 | 134626900 |
| ruby | 1.957s | 16.7× | 6/7 | 2.000s | 42.7ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 116.9ms | 1.0× | 1/7 | 139.2ms | 22.3ms | 28.3 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.2ms | 1.2× | 2/7 | 185.0ms | 36.8ms | 108.2 MB | 5/7 | 500 |
| clojure | 799.0ms | 6.5× | 7/7 | 1.159s | 359.9ms | 291.7 MB | 6/7 | 500 |
| elixir | 590.0ms | 4.8× | 6/7 | 781.9ms | 191.9ms | 461.2 MB | 7/7 | 500 |
| python | 173.5ms | 1.4× | 4/7 | 184.5ms | 11.0ms | 43.4 MB | 1/7 | 500 |
| node | 122.7ms | 1.0× | 1/7 | 142.7ms | 20.0ms | 68.4 MB | 4/7 | 500 |
| ruby | 203.8ms | 1.7× | 5/7 | 246.5ms | 42.7ms | 46.0 MB | 2/7 | 500 |
| dotnet | 149.1ms | 1.2× | 3/7 | 171.4ms | 22.3ms | 48.1 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 256.6ms | 5.2× | 3/7 | 293.4ms | 36.8ms | 107.6 MB | 6/7 | 100000 |
| clojure | 599.3ms | 12.1× | 4/7 | 959.2ms | 359.9ms | 132.3 MB | 7/7 | 100000 |
| elixir | 49.5ms | 1.0× | 1/7 | 241.4ms | 191.9ms | 72.2 MB | 5/7 | 100000 |
| python | 839.0ms | 16.9× | 7/7 | 850.0ms | 11.0ms | 10.9 MB | 1/7 | 100000 |
| node | 659.7ms | 13.3× | 6/7 | 679.7ms | 20.0ms | 70.9 MB | 4/7 | 100000 |
| ruby | 609.6ms | 12.3× | 5/7 | 652.3ms | 42.7ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 164.8ms | 3.3× | 2/7 | 187.1ms | 22.3ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.397s | 12.1× | 4/7 | 1.433s | 36.8ms | 283.7 MB | 6/7 | 1000000 |
| clojure | 4.546s | 39.3× | 6/7 | 4.906s | 359.9ms | 750.1 MB | 7/7 | 1000000 |
| elixir | 262.0ms | 2.3× | 2/7 | 453.9ms | 191.9ms | 72.6 MB | 5/7 | 1000000 |
| python | 4.826s | 41.7× | 7/7 | 4.837s | 11.0ms | 16.1 MB | 1/7 | 1000000 |
| node | 115.7ms | 1.0× | 1/7 | 135.7ms | 20.0ms | 68.3 MB | 4/7 | 1000000 |
| ruby | 3.579s | 30.9× | 5/7 | 3.621s | 42.7ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 853.0ms | 7.4× | 3/7 | 875.3ms | 22.3ms | 30.4 MB | 3/7 | 1000000 |
