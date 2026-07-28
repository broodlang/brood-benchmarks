# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-28 10:33.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; startup best of 9; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.3ms | 1.2× | 2/7 | 12.3ms | — | 20.3 MB | 3/7 | 0 |
| clojure | 333.9ms | 33.4× | 7/7 | 333.9ms | — | 101.7 MB | 7/7 | 0 |
| elixir | 181.8ms | 18.2× | 6/7 | 181.8ms | — | 72.2 MB | 6/7 | 0 |
| python | 10.0ms | 1.0× | 1/7 | 10.0ms | — | 9.7 MB | 1/7 | 0 |
| node | 17.8ms | 1.8× | 3/7 | 17.8ms | — | 44.5 MB | 5/7 | 0 |
| ruby | 38.7ms | 3.9× | 5/7 | 38.7ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 21.8ms | 2.2× | 4/7 | 21.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 59.4ms | 1.3× | 2/7 | 71.7ms | 12.3ms | 24.2 MB | 3/7 | 9227465 |
| clojure | 205.8ms | 4.5× | 5/7 | 539.7ms | 333.9ms | 109.4 MB | 7/7 | 9227465 |
| elixir | 81.2ms | 1.8× | 4/7 | 263.0ms | 181.8ms | 71.9 MB | 6/7 | 9227465 |
| python | 744.7ms | 16.3× | 7/7 | 754.7ms | 10.0ms | 9.9 MB | 1/7 | 9227465 |
| node | 74.1ms | 1.6× | 3/7 | 91.9ms | 17.8ms | 50.2 MB | 5/7 | 9227465 |
| ruby | 635.0ms | 13.9× | 6/7 | 673.7ms | 38.7ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 45.6ms | 1.0× | 1/7 | 67.4ms | 21.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.5ms | 3.4× | 3/7 | 53.8ms | 12.3ms | 24.3 MB | 3/7 | 449999985000000 |
| clojure | 151.7ms | 12.5× | 5/7 | 485.6ms | 333.9ms | 108.8 MB | 7/7 | 449999985000000 |
| elixir | 51.3ms | 4.2× | 4/7 | 233.1ms | 181.8ms | 70.1 MB | 6/7 | 449999985000000 |
| python | 2.317s | 191.5× | 7/7 | 2.327s | 10.0ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 30.4ms | 2.5× | 2/7 | 48.2ms | 17.8ms | 51.9 MB | 5/7 | 449999985000000 |
| ruby | 592.7ms | 49.0× | 6/7 | 631.4ms | 38.7ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 33.9ms | 21.8ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.4ms | 1.0× | 1/7 | 15.7ms | 12.3ms | 20.3 MB | 3/7 | 12499997500000 |
| clojure | 174.1ms | 51.2× | 5/7 | 508.0ms | 333.9ms | 221.6 MB | 7/7 | 12499997500000 |
| elixir | 33.7ms | 9.9× | 3/7 | 215.5ms | 181.8ms | 70.2 MB | 5/7 | 12499997500000 |
| python | 105.6ms | 31.1× | 4/7 | 115.6ms | 10.0ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 219.7ms | 64.6× | 6/7 | 237.5ms | 17.8ms | 92.2 MB | 6/7 | 12499997500000 |
| ruby | 222.2ms | 65.4× | 7/7 | 260.9ms | 38.7ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 12.5ms | 3.7× | 2/7 | 34.3ms | 21.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.4ms | 4.7× | 4/7 | 53.7ms | 12.3ms | 24.4 MB | 3/7 | 13848 |
| clojure | 149.8ms | 16.8× | 7/7 | 483.7ms | 333.9ms | 108.9 MB | 7/7 | 13848 |
| elixir | 21.8ms | 2.4× | 3/7 | 203.6ms | 181.8ms | 70.4 MB | 6/7 | 13848 |
| python | 123.2ms | 13.8× | 6/7 | 133.2ms | 10.0ms | 10.0 MB | 1/7 | 13848 |
| node | 9.4ms | 1.1× | 2/7 | 27.2ms | 17.8ms | 50.7 MB | 5/7 | 13848 |
| ruby | 118.7ms | 13.3× | 5/7 | 157.4ms | 38.7ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.9ms | 1.0× | 1/7 | 30.7ms | 21.8ms | 26.2 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.7ms | 1.6× | 2/7 | 96.0ms | 12.3ms | 24.3 MB | 3/7 | 442 |
| clojure | 454.4ms | 8.9× | 5/7 | 788.3ms | 333.9ms | 370.9 MB | 7/7 | 442 |
| elixir | 119.3ms | 2.3× | 3/7 | 301.1ms | 181.8ms | 73.2 MB | 6/7 | 442 |
| python | 2.604s | 51.0× | 7/7 | 2.614s | 10.0ms | 9.9 MB | 1/7 | 442 |
| node | 189.1ms | 3.7× | 4/7 | 206.9ms | 17.8ms | 50.3 MB | 5/7 | 442 |
| ruby | 879.2ms | 17.2× | 6/7 | 917.9ms | 38.7ms | 19.2 MB | 2/7 | 442 |
| dotnet | 51.1ms | 1.0× | 1/7 | 72.9ms | 21.8ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 180.1ms | 9.5× | 3/7 | 192.4ms | 12.3ms | 24.4 MB | 3/7 | 6129302 |
| clojure | 181.4ms | 9.6× | 4/7 | 515.3ms | 333.9ms | 114.6 MB | 7/7 | 6129302 |
| elixir | 252.6ms | 13.4× | 5/7 | 434.4ms | 181.8ms | 70.7 MB | 6/7 | 6129302 |
| python | 1.390s | 73.6× | 7/7 | 1.400s | 10.0ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.7ms | 1.1× | 2/7 | 39.5ms | 17.8ms | 51.9 MB | 5/7 | 6129302 |
| ruby | 415.4ms | 22.0× | 6/7 | 454.1ms | 38.7ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.9ms | 1.0× | 1/7 | 40.7ms | 21.8ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.4ms | 28.5× | 4/7 | 140.7ms | 12.3ms | 43.8 MB | 4/7 | 654353666 |
| clojure | 200.8ms | 44.6× | 5/7 | 534.7ms | 333.9ms | 118.4 MB | 7/7 | 654353666 |
| elixir | 69.4ms | 15.4× | 3/7 | 251.2ms | 181.8ms | 78.1 MB | 6/7 | 654353666 |
| python | 462.9ms | 102.9× | 7/7 | 472.9ms | 10.0ms | 10.4 MB | 1/7 | 654353666 |
| node | 17.2ms | 3.8× | 2/7 | 35.0ms | 17.8ms | 54.3 MB | 5/7 | 654353666 |
| ruby | 274.1ms | 60.9× | 6/7 | 312.8ms | 38.7ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 26.3ms | 21.8ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.5ms | 1.0× | 1/7 | 24.8ms | 12.3ms | 30.6 MB | 1/7 | 3388889 |
| clojure | 177.9ms | 14.2× | 7/7 | 511.8ms | 333.9ms | 168.2 MB | 6/7 | 3388889 |
| elixir | 128.3ms | 10.3× | 6/7 | 310.1ms | 181.8ms | 199.4 MB | 7/7 | 3388889 |
| python | 43.4ms | 3.5× | 3/7 | 53.4ms | 10.0ms | 40.0 MB | 2/7 | 3388889 |
| node | 65.4ms | 5.2× | 4/7 | 83.2ms | 17.8ms | 97.4 MB | 5/7 | 3388889 |
| ruby | 85.0ms | 6.8× | 5/7 | 123.7ms | 38.7ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.4ms | 2.5× | 2/7 | 53.2ms | 21.8ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.5ms | 1.1× | 2/7 | 45.8ms | 12.3ms | 25.2 MB | 3/7 | 374854840 |
| clojure | 289.9ms | 9.6× | 7/7 | 623.8ms | 333.9ms | 302.3 MB | 7/7 | 374854840 |
| elixir | 175.3ms | 5.8× | 6/7 | 357.1ms | 181.8ms | 72.7 MB | 6/7 | 374854840 |
| python | 172.0ms | 5.7× | 5/7 | 182.0ms | 10.0ms | 10.0 MB | 1/7 | 374854840 |
| node | 30.3ms | 1.0× | 1/7 | 48.1ms | 17.8ms | 52.2 MB | 5/7 | 374854840 |
| ruby | 70.8ms | 2.3× | 4/7 | 109.5ms | 38.7ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 37.3ms | 1.2× | 3/7 | 59.1ms | 21.8ms | 27.3 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.7ms | 10.6× | 6/7 | 116.0ms | 12.3ms | 51.5 MB | 4/7 | 1638200 |
| clojure | 172.0ms | 17.6× | 7/7 | 505.9ms | 333.9ms | 150.5 MB | 7/7 | 1638200 |
| elixir | 9.8ms | 1.0× | 1/7 | 191.6ms | 181.8ms | 70.0 MB | 6/7 | 1638200 |
| python | 98.5ms | 10.1× | 5/7 | 108.5ms | 10.0ms | 10.2 MB | 1/7 | 1638200 |
| node | 21.4ms | 2.2× | 3/7 | 39.2ms | 17.8ms | 58.0 MB | 5/7 | 1638200 |
| ruby | 97.2ms | 9.9× | 4/7 | 135.9ms | 38.7ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 15.1ms | 1.5× | 2/7 | 36.9ms | 21.8ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.0ms | 3.0× | 6/7 | 205.3ms | 12.3ms | 194.0 MB | 7/7 | 46468819 |
| clojure | 247.7ms | 3.8× | 7/7 | 581.6ms | 333.9ms | 123.9 MB | 5/7 | 46468819 |
| elixir | 114.5ms | 1.8× | 4/7 | 296.3ms | 181.8ms | 157.4 MB | 6/7 | 46468819 |
| python | 185.7ms | 2.9× | 5/7 | 195.7ms | 10.0ms | 25.9 MB | 2/7 | 46468819 |
| node | 105.4ms | 1.6× | 3/7 | 123.2ms | 17.8ms | 67.1 MB | 4/7 | 46468819 |
| ruby | 72.3ms | 1.1× | 2/7 | 111.0ms | 38.7ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 64.4ms | 1.0× | 1/7 | 86.2ms | 21.8ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.3ms | 10.6× | 5/7 | 91.6ms | 12.3ms | 41.4 MB | 4/7 | 724 |
| clojure | 203.4ms | 27.1× | 7/7 | 537.3ms | 333.9ms | 132.3 MB | 7/7 | 724 |
| elixir | 15.0ms | 2.0× | 2/7 | 196.8ms | 181.8ms | 70.3 MB | 6/7 | 724 |
| python | 53.9ms | 7.2× | 4/7 | 63.9ms | 10.0ms | 9.9 MB | 1/7 | 724 |
| node | 7.5ms | 1.0× | 1/7 | 25.3ms | 17.8ms | 52.7 MB | 5/7 | 724 |
| ruby | 123.5ms | 16.5× | 6/7 | 162.2ms | 38.7ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.0ms | 2.7× | 3/7 | 41.8ms | 21.8ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.6ms | 1.6× | 2/7 | 56.9ms | 12.3ms | 24.1 MB | 3/7 | 9900000 |
| clojure | 1.095s | 40.0× | 7/7 | 1.429s | 333.9ms | 371.4 MB | 7/7 | 9900000 |
| elixir | 27.4ms | 1.0× | 1/7 | 209.2ms | 181.8ms | 73.0 MB | 6/7 | 9900000 |
| python | 48.1ms | 1.8× | 3/7 | 58.1ms | 10.0ms | 9.9 MB | 1/7 | 9900000 |
| node | 564.3ms | 20.6× | 6/7 | 582.1ms | 17.8ms | 52.4 MB | 5/7 | 9900000 |
| ruby | 110.5ms | 4.0× | 4/7 | 149.2ms | 38.7ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 287.0ms | 10.5× | 5/7 | 308.8ms | 21.8ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.0ms | 3.6× | 2/7 | 53.3ms | 12.3ms | 24.3 MB | 2/7 | 2475000 |
| clojure | 1.339s | 116.4× | 7/7 | 1.673s | 333.9ms | 375.4 MB | 7/7 | 2475000 |
| elixir | 11.5ms | 1.0× | 1/7 | 193.3ms | 181.8ms | 70.0 MB | 6/7 | 2475000 |
| python | 226.0ms | 19.7× | 5/7 | 236.0ms | 10.0ms | 9.9 MB | 1/7 | 2475000 |
| node | 206.8ms | 18.0× | 4/7 | 224.6ms | 17.8ms | 52.3 MB | 5/7 | 2475000 |
| ruby | 110.9ms | 9.6× | 3/7 | 149.6ms | 38.7ms | 26.0 MB | 3/7 | 2475000 |
| dotnet | 697.1ms | 60.6× | 6/7 | 718.9ms | 21.8ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 7.4× | 6/7 | 44.3ms | 12.3ms | 24.8 MB | 3/7 | 155553889038886 |
| clojure | 135.1ms | 31.4× | 7/7 | 469.0ms | 333.9ms | 109.0 MB | 7/7 | 155553889038886 |
| elixir | 11.1ms | 2.6× | 5/7 | 192.9ms | 181.8ms | 74.0 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.0× | 1/7 | 14.3ms | 10.0ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 9.4ms | 2.2× | 4/7 | 27.2ms | 17.8ms | 54.0 MB | 5/7 | 155553889038886 |
| ruby | 7.9ms | 1.8× | 2/7 | 46.6ms | 38.7ms | 19.7 MB | 2/7 | 155553889038886 |
| dotnet | 9.3ms | 2.2× | 3/7 | 31.1ms | 21.8ms | 27.9 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 348.8ms | 1.4× | 3/7 | 361.1ms | 12.3ms | 24.4 MB | 3/7 | 24558 |
| clojure | 548.3ms | 2.2× | 5/7 | 882.2ms | 333.9ms | 374.5 MB | 7/7 | 24558 |
| elixir | 288.4ms | 1.2× | 2/7 | 470.2ms | 181.8ms | 70.3 MB | 6/7 | 24558 |
| python | 3.901s | 15.9× | 7/7 | 3.912s | 10.0ms | 11.1 MB | 1/7 | 24558 |
| node | 395.6ms | 1.6× | 4/7 | 413.4ms | 17.8ms | 50.4 MB | 5/7 | 24558 |
| ruby | 1.661s | 6.8× | 6/7 | 1.700s | 38.7ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 244.8ms | 1.0× | 1/7 | 266.6ms | 21.8ms | 26.2 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.1ms | 9.1× | 3/7 | 43.4ms | 12.3ms | 31.7 MB | 4/7 | 78498 |
| clojure | 146.2ms | 43.0× | 7/7 | 480.1ms | 333.9ms | 108.3 MB | 7/7 | 78498 |
| elixir | 60.8ms | 17.9× | 4/7 | 242.6ms | 181.8ms | 77.6 MB | 6/7 | 78498 |
| python | 125.9ms | 37.0× | 6/7 | 135.9ms | 10.0ms | 10.8 MB | 1/7 | 78498 |
| node | 6.2ms | 1.8× | 2/7 | 24.0ms | 17.8ms | 51.5 MB | 5/7 | 78498 |
| ruby | 85.0ms | 25.0× | 5/7 | 123.7ms | 38.7ms | 26.9 MB | 2/7 | 78498 |
| dotnet | 3.4ms | 1.0× | 1/7 | 25.2ms | 21.8ms | 27.4 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 63.5ms | 2.9× | 4/7 | 75.8ms | 12.3ms | 72.0 MB | 5/7 | 30039386344 |
| clojure | 297.8ms | 13.5× | 7/7 | 631.7ms | 333.9ms | 291.7 MB | 7/7 | 30039386344 |
| elixir | 121.8ms | 5.5× | 6/7 | 303.6ms | 181.8ms | 99.3 MB | 6/7 | 30039386344 |
| python | 79.1ms | 3.6× | 5/7 | 89.1ms | 10.0ms | 14.9 MB | 1/7 | 30039386344 |
| node | 23.2ms | 1.0× | 2/7 | 41.0ms | 17.8ms | 56.1 MB | 4/7 | 30039386344 |
| ruby | 39.6ms | 1.8× | 3/7 | 78.3ms | 38.7ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 22.1ms | 1.0× | 1/7 | 43.9ms | 21.8ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 316.1ms | 48.6× | 6/7 | 328.4ms | 12.3ms | 54.9 MB | 5/7 | -169078071 |
| clojure | 189.6ms | 29.2× | 4/7 | 523.5ms | 333.9ms | 109.4 MB | 7/7 | -169078071 |
| elixir | 151.6ms | 23.3× | 3/7 | 333.4ms | 181.8ms | 72.7 MB | 6/7 | -169078071 |
| python | 676.3ms | 104.0× | 7/7 | 686.3ms | 10.0ms | 10.4 MB | 1/7 | -169078071 |
| node | 14.7ms | 2.3× | 2/7 | 32.5ms | 17.8ms | 52.2 MB | 4/7 | -169078071 |
| ruby | 293.6ms | 45.2× | 5/7 | 332.3ms | 38.7ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.5ms | 1.0× | 1/7 | 28.3ms | 21.8ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.2ms | 82.9× | 6/7 | 161.5ms | 12.3ms | 78.1 MB | 6/7 | 1489952542 |
| clojure | 392.0ms | 217.8× | 7/7 | 725.9ms | 333.9ms | 182.6 MB | 7/7 | 1489952542 |
| elixir | 12.1ms | 6.7× | 4/7 | 193.9ms | 181.8ms | 75.9 MB | 5/7 | 1489952542 |
| python | 8.7ms | 4.8× | 3/7 | 18.7ms | 10.0ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.8ms | 1.0× | 1/7 | 19.6ms | 17.8ms | 45.8 MB | 4/7 | 1489952542 |
| ruby | 4.6ms | 2.6× | 2/7 | 43.3ms | 38.7ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 43.0ms | 23.9× | 5/7 | 64.8ms | 21.8ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.1ms | 19.8× | 6/7 | 93.4ms | 12.3ms | 42.7 MB | 4/7 | 10000 |
| clojure | 136.2ms | 33.2× | 7/7 | 470.1ms | 333.9ms | 108.5 MB | 7/7 | 10000 |
| elixir | 17.3ms | 4.2× | 5/7 | 199.1ms | 181.8ms | 72.7 MB | 6/7 | 10000 |
| python | 13.2ms | 3.2× | 4/7 | 23.2ms | 10.0ms | 11.2 MB | 1/7 | 10000 |
| node | 4.1ms | 1.0× | 1/7 | 21.9ms | 17.8ms | 52.4 MB | 5/7 | 10000 |
| ruby | 8.2ms | 2.0× | 2/7 | 46.9ms | 38.7ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 12.6ms | 3.1× | 3/7 | 34.4ms | 21.8ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 108.5ms | 22.1× | 6/7 | 120.8ms | 12.3ms | 100.4 MB | 6/7 | 12081249 |
| clojure | 164.2ms | 33.5× | 7/7 | 498.1ms | 333.9ms | 108.9 MB | 7/7 | 12081249 |
| elixir | 11.6ms | 2.4× | 4/7 | 193.4ms | 181.8ms | 79.1 MB | 5/7 | 12081249 |
| python | 13.0ms | 2.7× | 5/7 | 23.0ms | 10.0ms | 10.3 MB | 1/7 | 12081249 |
| node | 6.4ms | 1.3× | 2/7 | 24.2ms | 17.8ms | 53.0 MB | 4/7 | 12081249 |
| ruby | 8.7ms | 1.8× | 3/7 | 47.4ms | 38.7ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 4.9ms | 1.0× | 1/7 | 26.7ms | 21.8ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.3ms | 2.6× | 3/7 | 59.6ms | 12.3ms | 47.6 MB | 3/7 | 6100000 |
| clojure | 194.4ms | 10.7× | 5/7 | 528.3ms | 333.9ms | 137.7 MB | 7/7 | 6100000 |
| elixir | 24.7ms | 1.4× | 2/7 | 206.5ms | 181.8ms | 76.4 MB | 5/7 | 6100000 |
| python | 544.5ms | 29.9× | 6/7 | 554.5ms | 10.0ms | 28.1 MB | 1/7 | 6100000 |
| node | 53.3ms | 2.9× | 4/7 | 71.1ms | 17.8ms | 53.4 MB | 4/7 | 6100000 |
| ruby | 1.573s | 86.4× | 7/7 | 1.611s | 38.7ms | 132.2 MB | 6/7 | 6100000 |
| dotnet | 18.2ms | 1.0× | 1/7 | 40.0ms | 21.8ms | 30.6 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.2ms | 1.6× | 2/7 | 185.5ms | 12.3ms | 27.5 MB | 3/7 | 134626900 |
| clojure | 382.0ms | 3.4× | 5/7 | 715.9ms | 333.9ms | 136.3 MB | 6/7 | 134626900 |
| elixir | 294.4ms | 2.6× | 4/7 | 476.2ms | 181.8ms | 72.3 MB | 5/7 | 134626900 |
| python | 2.415s | 21.7× | 7/7 | 2.425s | 10.0ms | 22.2 MB | 2/7 | 134626900 |
| node | 290.4ms | 2.6× | 3/7 | 308.2ms | 17.8ms | 184.9 MB | 7/7 | 134626900 |
| ruby | 1.798s | 16.1× | 6/7 | 1.837s | 38.7ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 111.5ms | 1.0× | 1/7 | 133.3ms | 21.8ms | 28.1 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 168.4ms | 1.4× | 3/7 | 180.7ms | 12.3ms | 81.9 MB | 5/7 | 500 |
| clojure | 804.8ms | 6.7× | 7/7 | 1.139s | 333.9ms | 286.3 MB | 6/7 | 500 |
| elixir | 557.8ms | 4.7× | 6/7 | 739.6ms | 181.8ms | 496.8 MB | 7/7 | 500 |
| python | 176.2ms | 1.5× | 4/7 | 186.2ms | 10.0ms | 44.2 MB | 1/7 | 500 |
| node | 119.5ms | 1.0× | 1/7 | 137.3ms | 17.8ms | 67.2 MB | 4/7 | 500 |
| ruby | 212.6ms | 1.8× | 5/7 | 251.3ms | 38.7ms | 45.9 MB | 2/7 | 500 |
| dotnet | 146.4ms | 1.2× | 2/7 | 168.2ms | 21.8ms | 48.5 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 188.5ms | 3.5× | 3/7 | 200.8ms | 12.3ms | 45.4 MB | 4/7 | 100000 |
| clojure | 590.3ms | 11.0× | 5/7 | 924.2ms | 333.9ms | 133.7 MB | 7/7 | 100000 |
| elixir | 53.5ms | 1.0× | 1/7 | 235.3ms | 181.8ms | 71.3 MB | 6/7 | 100000 |
| python | 807.9ms | 15.1× | 7/7 | 817.9ms | 10.0ms | 10.9 MB | 1/7 | 100000 |
| node | 637.7ms | 11.9× | 6/7 | 655.5ms | 17.8ms | 69.8 MB | 5/7 | 100000 |
| ruby | 589.9ms | 11.0× | 4/7 | 628.6ms | 38.7ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 164.7ms | 3.1× | 2/7 | 186.5ms | 21.8ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 722.1ms | 6.1× | 3/7 | 734.4ms | 12.3ms | 94.2 MB | 6/7 | 1000000 |
| clojure | 4.307s | 36.6× | 6/7 | 4.641s | 333.9ms | 755.0 MB | 7/7 | 1000000 |
| elixir | 260.7ms | 2.2× | 2/7 | 442.5ms | 181.8ms | 72.1 MB | 5/7 | 1000000 |
| python | 4.601s | 39.1× | 7/7 | 4.611s | 10.0ms | 16.2 MB | 1/7 | 1000000 |
| node | 117.6ms | 1.0× | 1/7 | 135.4ms | 17.8ms | 67.4 MB | 4/7 | 1000000 |
| ruby | 3.371s | 28.7× | 5/7 | 3.410s | 38.7ms | 23.4 MB | 2/7 | 1000000 |
| dotnet | 778.3ms | 6.6× | 4/7 | 800.1ms | 21.8ms | 30.4 MB | 3/7 | 1000000 |
