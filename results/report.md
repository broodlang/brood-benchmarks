# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-12 10:14.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.1ms | 3.0× | 4/7 | 33.1ms | — | 25.1 MB | 3/7 | 0 |
| clojure | 376.8ms | 34.3× | 7/7 | 376.8ms | — | 102.6 MB | 7/7 | 0 |
| elixir | 185.4ms | 16.9× | 6/7 | 185.4ms | — | 71.2 MB | 6/7 | 0 |
| python | 11.0ms | 1.0× | 1/7 | 11.0ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.1ms | 1.6× | 2/7 | 18.1ms | — | 42.3 MB | 5/7 | 0 |
| ruby | 40.3ms | 3.7× | 5/7 | 40.3ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 25.5ms | 2.3× | 3/7 | 25.5ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 64.9ms | 1.5× | 2/7 | 98.0ms | 33.1ms | 28.9 MB | 4/7 | 9227465 |
| clojure | 252.2ms | 5.9× | 5/7 | 629.0ms | 376.8ms | 108.2 MB | 7/7 | 9227465 |
| elixir | 90.4ms | 2.1× | 4/7 | 275.8ms | 185.4ms | 72.4 MB | 6/7 | 9227465 |
| python | 783.8ms | 18.4× | 7/7 | 794.8ms | 11.0ms | 9.8 MB | 1/7 | 9227465 |
| node | 82.1ms | 1.9× | 3/7 | 100.2ms | 18.1ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 692.3ms | 16.3× | 6/7 | 732.6ms | 40.3ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 42.5ms | 1.0× | 1/7 | 68.0ms | 25.5ms | 25.7 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.4ms | 3.5× | 3/7 | 70.5ms | 33.1ms | 28.9 MB | 4/7 | 449999985000000 |
| clojure | 170.8ms | 16.1× | 5/7 | 547.6ms | 376.8ms | 108.3 MB | 7/7 | 449999985000000 |
| elixir | 63.2ms | 6.0× | 4/7 | 248.6ms | 185.4ms | 71.5 MB | 6/7 | 449999985000000 |
| python | 2.458s | 231.9× | 7/7 | 2.469s | 11.0ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 31.9ms | 3.0× | 2/7 | 50.0ms | 18.1ms | 49.7 MB | 5/7 | 449999985000000 |
| ruby | 567.3ms | 53.5× | 6/7 | 607.6ms | 40.3ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 10.6ms | 1.0× | 1/7 | 36.1ms | 25.5ms | 26.1 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.6ms | 1.4× | 2/7 | 46.7ms | 33.1ms | 25.1 MB | 3/7 | 12499997500000 |
| clojure | 384.1ms | 38.8× | 7/7 | 760.9ms | 376.8ms | 219.7 MB | 7/7 | 12499997500000 |
| elixir | 66.7ms | 6.7× | 3/7 | 252.1ms | 185.4ms | 69.8 MB | 5/7 | 12499997500000 |
| python | 129.0ms | 13.0× | 4/7 | 140.0ms | 11.0ms | 10.4 MB | 1/7 | 12499997500000 |
| node | 253.3ms | 25.6× | 5/7 | 271.4ms | 18.1ms | 89.5 MB | 6/7 | 12499997500000 |
| ruby | 255.4ms | 25.8× | 6/7 | 295.7ms | 40.3ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 9.9ms | 1.0× | 1/7 | 35.4ms | 25.5ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 7.6× | 4/7 | 76.2ms | 33.1ms | 29.7 MB | 4/7 | 13848 |
| clojure | 150.0ms | 26.3× | 7/7 | 526.8ms | 376.8ms | 108.9 MB | 7/7 | 13848 |
| elixir | 27.2ms | 4.8× | 3/7 | 212.6ms | 185.4ms | 70.4 MB | 6/7 | 13848 |
| python | 125.9ms | 22.1× | 5/7 | 136.9ms | 11.0ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.5× | 2/7 | 26.6ms | 18.1ms | 48.2 MB | 5/7 | 13848 |
| ruby | 138.4ms | 24.3× | 6/7 | 178.7ms | 40.3ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 5.7ms | 1.0× | 1/7 | 31.2ms | 25.5ms | 26.2 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.0ms | 1.9× | 2/7 | 116.1ms | 33.1ms | 29.3 MB | 4/7 | 442 |
| clojure | 492.5ms | 11.5× | 5/7 | 869.3ms | 376.8ms | 371.5 MB | 7/7 | 442 |
| elixir | 118.7ms | 2.8× | 3/7 | 304.1ms | 185.4ms | 72.2 MB | 6/7 | 442 |
| python | 2.737s | 64.1× | 7/7 | 2.748s | 11.0ms | 9.8 MB | 1/7 | 442 |
| node | 190.1ms | 4.5× | 4/7 | 208.2ms | 18.1ms | 48.0 MB | 5/7 | 442 |
| ruby | 878.8ms | 20.6× | 6/7 | 919.1ms | 40.3ms | 19.1 MB | 2/7 | 442 |
| dotnet | 42.7ms | 1.0× | 1/7 | 68.2ms | 25.5ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 235.0ms | 14.9× | 4/7 | 268.1ms | 33.1ms | 29.2 MB | 4/7 | 6129302 |
| clojure | 168.5ms | 10.7× | 3/7 | 545.3ms | 376.8ms | 115.4 MB | 7/7 | 6129302 |
| elixir | 270.7ms | 17.1× | 5/7 | 456.1ms | 185.4ms | 72.5 MB | 6/7 | 6129302 |
| python | 1.403s | 88.8× | 7/7 | 1.414s | 11.0ms | 9.9 MB | 1/7 | 6129302 |
| node | 20.7ms | 1.3× | 2/7 | 38.8ms | 18.1ms | 49.6 MB | 5/7 | 6129302 |
| ruby | 446.3ms | 28.2× | 6/7 | 486.6ms | 40.3ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 15.8ms | 1.0× | 1/7 | 41.3ms | 25.5ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 134.7ms | 112.3× | 4/7 | 167.8ms | 33.1ms | 44.1 MB | 4/7 | 654353666 |
| clojure | 465.3ms | 387.8× | 7/7 | 842.1ms | 376.8ms | 119.0 MB | 7/7 | 654353666 |
| elixir | 70.6ms | 58.8× | 3/7 | 256.0ms | 185.4ms | 75.7 MB | 6/7 | 654353666 |
| python | 457.4ms | 381.2× | 6/7 | 468.4ms | 11.0ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.8ms | 14.0× | 2/7 | 34.9ms | 18.1ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 327.3ms | 272.8× | 5/7 | 367.6ms | 40.3ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 1.2ms | 1.0× | 1/7 | 26.7ms | 25.5ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.3ms | 1.0× | 1/7 | 45.4ms | 33.1ms | 32.8 MB | 1/7 | 3388889 |
| clojure | 188.5ms | 15.3× | 7/7 | 565.3ms | 376.8ms | 168.7 MB | 6/7 | 3388889 |
| elixir | 115.9ms | 9.4× | 6/7 | 301.3ms | 185.4ms | 200.0 MB | 7/7 | 3388889 |
| python | 42.4ms | 3.4× | 3/7 | 53.4ms | 11.0ms | 39.9 MB | 2/7 | 3388889 |
| node | 70.6ms | 5.7× | 4/7 | 88.7ms | 18.1ms | 94.9 MB | 5/7 | 3388889 |
| ruby | 96.0ms | 7.8× | 5/7 | 136.3ms | 40.3ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.7ms | 2.5× | 2/7 | 56.2ms | 25.5ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 182.4ms | 5.7× | 6/7 | 215.5ms | 33.1ms | 30.0 MB | 4/7 | 374854840 |
| clojure | 289.7ms | 9.0× | 7/7 | 666.5ms | 376.8ms | 301.5 MB | 7/7 | 374854840 |
| elixir | 181.0ms | 5.6× | 4/7 | 366.4ms | 185.4ms | 72.9 MB | 6/7 | 374854840 |
| python | 182.3ms | 5.7× | 5/7 | 193.3ms | 11.0ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.1ms | 1.0× | 1/7 | 50.2ms | 18.1ms | 49.7 MB | 5/7 | 374854840 |
| ruby | 78.8ms | 2.5× | 3/7 | 119.1ms | 40.3ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 35.5ms | 1.1× | 2/7 | 61.0ms | 25.5ms | 27.0 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.1ms | 8.2× | 4/7 | 127.2ms | 33.1ms | 52.8 MB | 4/7 | 1638200 |
| clojure | 156.5ms | 13.6× | 7/7 | 533.3ms | 376.8ms | 149.7 MB | 7/7 | 1638200 |
| elixir | 15.5ms | 1.3× | 2/7 | 200.9ms | 185.4ms | 71.7 MB | 6/7 | 1638200 |
| python | 99.3ms | 8.6× | 5/7 | 110.3ms | 11.0ms | 10.0 MB | 1/7 | 1638200 |
| node | 21.5ms | 1.9× | 3/7 | 39.6ms | 18.1ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 103.6ms | 9.0× | 6/7 | 143.9ms | 40.3ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 11.5ms | 1.0× | 1/7 | 37.0ms | 25.5ms | 32.1 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.5ms | 2.2× | 5/7 | 182.6ms | 33.1ms | 144.2 MB | 6/7 | 46468819 |
| clojure | 235.6ms | 3.4× | 7/7 | 612.4ms | 376.8ms | 123.6 MB | 5/7 | 46468819 |
| elixir | 123.5ms | 1.8× | 4/7 | 308.9ms | 185.4ms | 157.8 MB | 7/7 | 46468819 |
| python | 184.9ms | 2.7× | 6/7 | 195.9ms | 11.0ms | 25.8 MB | 2/7 | 46468819 |
| node | 106.4ms | 1.5× | 3/7 | 124.5ms | 18.1ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 71.4ms | 1.0× | 2/7 | 111.7ms | 40.3ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 68.8ms | 1.0× | 1/7 | 94.3ms | 25.5ms | 29.5 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.1ms | 10.7× | 5/7 | 113.2ms | 33.1ms | 38.5 MB | 4/7 | 724 |
| clojure | 187.0ms | 24.9× | 7/7 | 563.8ms | 376.8ms | 132.3 MB | 7/7 | 724 |
| elixir | 10.1ms | 1.3× | 2/7 | 195.5ms | 185.4ms | 71.2 MB | 6/7 | 724 |
| python | 55.1ms | 7.3× | 4/7 | 66.1ms | 11.0ms | 9.8 MB | 1/7 | 724 |
| node | 7.5ms | 1.0× | 1/7 | 25.6ms | 18.1ms | 50.3 MB | 5/7 | 724 |
| ruby | 123.0ms | 16.4× | 6/7 | 163.3ms | 40.3ms | 19.4 MB | 2/7 | 724 |
| dotnet | 16.7ms | 2.2× | 3/7 | 42.2ms | 25.5ms | 29.1 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.6ms | 1.5× | 2/7 | 70.7ms | 33.1ms | 29.2 MB | 3/7 | 9900000 |
| clojure | 1.111s | 45.5× | 7/7 | 1.488s | 376.8ms | 371.2 MB | 7/7 | 9900000 |
| elixir | 24.4ms | 1.0× | 1/7 | 209.8ms | 185.4ms | 70.0 MB | 6/7 | 9900000 |
| python | 48.0ms | 2.0× | 3/7 | 59.0ms | 11.0ms | 9.8 MB | 1/7 | 9900000 |
| node | 588.7ms | 24.1× | 6/7 | 606.8ms | 18.1ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 110.9ms | 4.5× | 4/7 | 151.2ms | 40.3ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 295.3ms | 12.1× | 5/7 | 320.8ms | 25.5ms | 32.7 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.3ms | 5.9× | 2/7 | 89.4ms | 33.1ms | 29.3 MB | 3/7 | 2475000 |
| clojure | 1.512s | 157.5× | 7/7 | 1.889s | 376.8ms | 373.8 MB | 7/7 | 2475000 |
| elixir | 9.6ms | 1.0× | 1/7 | 195.0ms | 185.4ms | 70.7 MB | 6/7 | 2475000 |
| python | 238.8ms | 24.9× | 5/7 | 249.8ms | 11.0ms | 9.8 MB | 1/7 | 2475000 |
| node | 224.8ms | 23.4× | 4/7 | 242.9ms | 18.1ms | 49.9 MB | 5/7 | 2475000 |
| ruby | 117.2ms | 12.2× | 3/7 | 157.5ms | 40.3ms | 25.9 MB | 2/7 | 2475000 |
| dotnet | 710.2ms | 74.0× | 6/7 | 735.7ms | 25.5ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 8.8× | 6/7 | 64.0ms | 33.1ms | 29.2 MB | 4/7 | 155553889038886 |
| clojure | 117.2ms | 33.5× | 7/7 | 494.0ms | 376.8ms | 108.1 MB | 7/7 | 155553889038886 |
| elixir | 18.1ms | 5.2× | 4/7 | 203.5ms | 185.4ms | 72.7 MB | 6/7 | 155553889038886 |
| python | 3.5ms | 1.0× | 1/7 | 14.5ms | 11.0ms | 9.7 MB | 1/7 | 155553889038886 |
| node | 13.7ms | 3.9× | 3/7 | 31.8ms | 18.1ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 18.6ms | 5.3× | 5/7 | 58.9ms | 40.3ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 5.4ms | 1.5× | 2/7 | 30.9ms | 25.5ms | 27.8 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.043s | 15.0× | 6/7 | 4.076s | 33.1ms | 30.4 MB | 4/7 | 24558 |
| clojure | 670.7ms | 2.5× | 4/7 | 1.048s | 376.8ms | 374.6 MB | 7/7 | 24558 |
| elixir | 354.5ms | 1.3× | 2/7 | 539.9ms | 185.4ms | 70.7 MB | 6/7 | 24558 |
| python | 4.129s | 15.3× | 7/7 | 4.140s | 11.0ms | 11.0 MB | 1/7 | 24558 |
| node | 410.2ms | 1.5× | 3/7 | 428.3ms | 18.1ms | 48.1 MB | 5/7 | 24558 |
| ruby | 1.786s | 6.6× | 5/7 | 1.826s | 40.3ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 269.7ms | 1.0× | 1/7 | 295.2ms | 25.5ms | 26.1 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.269s | 1268.7× | 7/7 | 1.302s | 33.1ms | 463.2 MB | 7/7 | 78498 |
| clojure | 208.3ms | 208.3× | 6/7 | 585.1ms | 376.8ms | 108.3 MB | 6/7 | 78498 |
| elixir | 63.2ms | 63.2× | 3/7 | 248.6ms | 185.4ms | 79.0 MB | 5/7 | 78498 |
| python | 121.7ms | 121.7× | 5/7 | 132.7ms | 11.0ms | 10.8 MB | 1/7 | 78498 |
| node | 6.0ms | 6.0× | 2/7 | 24.1ms | 18.1ms | 49.3 MB | 4/7 | 78498 |
| ruby | 86.9ms | 86.9× | 4/7 | 127.2ms | 40.3ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 0.4ms | < 1× | 1/7 | 25.9ms | 25.5ms | 27.2 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 659.0ms | 34.5× | 7/7 | 692.1ms | 33.1ms | 237.6 MB | 6/7 | 30039386344 |
| clojure | 282.9ms | 14.8× | 6/7 | 659.7ms | 376.8ms | 290.9 MB | 7/7 | 30039386344 |
| elixir | 126.5ms | 6.6× | 5/7 | 311.9ms | 185.4ms | 98.2 MB | 5/7 | 30039386344 |
| python | 85.4ms | 4.5× | 4/7 | 96.4ms | 11.0ms | 14.8 MB | 1/7 | 30039386344 |
| node | 23.4ms | 1.2× | 2/7 | 41.5ms | 18.1ms | 53.8 MB | 4/7 | 30039386344 |
| ruby | 39.9ms | 2.1× | 3/7 | 80.2ms | 40.3ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 19.1ms | 1.0× | 1/7 | 44.6ms | 25.5ms | 30.1 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 7.411s | 1398.3× | 7/7 | 7.444s | 33.1ms | 41.9 MB | 4/7 | -169078071 |
| clojure | 177.3ms | 33.5× | 4/7 | 554.1ms | 376.8ms | 108.6 MB | 7/7 | -169078071 |
| elixir | 153.5ms | 29.0× | 3/7 | 338.9ms | 185.4ms | 71.6 MB | 6/7 | -169078071 |
| python | 782.4ms | 147.6× | 6/7 | 793.4ms | 11.0ms | 10.3 MB | 1/7 | -169078071 |
| node | 15.8ms | 3.0× | 2/7 | 33.9ms | 18.1ms | 50.2 MB | 5/7 | -169078071 |
| ruby | 314.8ms | 59.4× | 5/7 | 355.1ms | 40.3ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 5.3ms | 1.0× | 1/7 | 30.8ms | 25.5ms | 26.8 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 896.3ms | 597.5× | 7/7 | 929.4ms | 33.1ms | 107.3 MB | 6/7 | 1489952542 |
| clojure | 555.7ms | 370.5× | 6/7 | 932.5ms | 376.8ms | 168.6 MB | 7/7 | 1489952542 |
| elixir | 12.3ms | 8.2× | 4/7 | 197.7ms | 185.4ms | 74.5 MB | 5/7 | 1489952542 |
| python | 7.4ms | 4.9× | 3/7 | 18.4ms | 11.0ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.5ms | 1.0× | 1/7 | 19.6ms | 18.1ms | 43.9 MB | 4/7 | 1489952542 |
| ruby | 3.9ms | 2.6× | 2/7 | 44.2ms | 40.3ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 42.6ms | 28.4× | 5/7 | 68.1ms | 25.5ms | 33.9 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.443s | 678.5× | 7/7 | 2.476s | 33.1ms | 229.6 MB | 7/7 | 10000 |
| clojure | 139.9ms | 38.9× | 6/7 | 516.7ms | 376.8ms | 108.7 MB | 6/7 | 10000 |
| elixir | 13.6ms | 3.8× | 4/7 | 199.0ms | 185.4ms | 71.7 MB | 5/7 | 10000 |
| python | 14.1ms | 3.9× | 5/7 | 25.1ms | 11.0ms | 11.1 MB | 1/7 | 10000 |
| node | 3.6ms | 1.0× | 1/7 | 21.7ms | 18.1ms | 50.1 MB | 4/7 | 10000 |
| ruby | 8.8ms | 2.4× | 2/7 | 49.1ms | 40.3ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 9.3ms | 2.6× | 3/7 | 34.8ms | 25.5ms | 31.7 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.7ms | 95.5× | 6/7 | 166.8ms | 33.1ms | 105.2 MB | 6/7 | 12081249 |
| clojure | 144.1ms | 102.9× | 7/7 | 520.9ms | 376.8ms | 109.3 MB | 7/7 | 12081249 |
| elixir | 12.0ms | 8.6× | 4/7 | 197.4ms | 185.4ms | 75.4 MB | 5/7 | 12081249 |
| python | 14.3ms | 10.2× | 5/7 | 25.3ms | 11.0ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.4ms | 3.9× | 2/7 | 23.5ms | 18.1ms | 50.6 MB | 4/7 | 12081249 |
| ruby | 7.2ms | 5.1× | 3/7 | 47.5ms | 40.3ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 1.4ms | 1.0× | 1/7 | 26.9ms | 25.5ms | 27.0 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 60.7ms | 4.2× | 4/7 | 93.8ms | 33.1ms | 61.5 MB | 4/7 | 6100000 |
| clojure | 185.9ms | 12.9× | 5/7 | 562.7ms | 376.8ms | 133.7 MB | 7/7 | 6100000 |
| elixir | 23.6ms | 1.6× | 2/7 | 209.0ms | 185.4ms | 75.5 MB | 5/7 | 6100000 |
| python | 571.6ms | 39.7× | 6/7 | 582.6ms | 11.0ms | 27.9 MB | 1/7 | 6100000 |
| node | 56.8ms | 3.9× | 3/7 | 74.9ms | 18.1ms | 51.3 MB | 3/7 | 6100000 |
| ruby | 1.659s | 115.2× | 7/7 | 1.700s | 40.3ms | 132.5 MB | 6/7 | 6100000 |
| dotnet | 14.4ms | 1.0× | 1/7 | 39.9ms | 25.5ms | 30.5 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 183.8ms | 1.5× | 2/7 | 216.9ms | 33.1ms | 32.0 MB | 4/7 | 134626900 |
| clojure | 429.7ms | 3.5× | 5/7 | 806.5ms | 376.8ms | 136.1 MB | 6/7 | 134626900 |
| elixir | 352.0ms | 2.9× | 4/7 | 537.4ms | 185.4ms | 70.7 MB | 5/7 | 134626900 |
| python | 2.880s | 23.7× | 7/7 | 2.891s | 11.0ms | 21.9 MB | 2/7 | 134626900 |
| node | 343.2ms | 2.8× | 3/7 | 361.3ms | 18.1ms | 182.1 MB | 7/7 | 134626900 |
| ruby | 2.151s | 17.7× | 6/7 | 2.191s | 40.3ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 121.6ms | 1.0× | 1/7 | 147.1ms | 25.5ms | 27.9 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.4ms | 1.4× | 3/7 | 204.5ms | 33.1ms | 124.6 MB | 5/7 | 500 |
| clojure | 885.6ms | 7.0× | 7/7 | 1.262s | 376.8ms | 278.6 MB | 6/7 | 500 |
| elixir | 623.3ms | 4.9× | 6/7 | 808.7ms | 185.4ms | 475.4 MB | 7/7 | 500 |
| python | 175.8ms | 1.4× | 4/7 | 186.8ms | 11.0ms | 43.1 MB | 1/7 | 500 |
| node | 126.0ms | 1.0× | 1/7 | 144.1ms | 18.1ms | 64.9 MB | 4/7 | 500 |
| ruby | 222.5ms | 1.8× | 5/7 | 262.8ms | 40.3ms | 45.5 MB | 2/7 | 500 |
| dotnet | 150.5ms | 1.2× | 2/7 | 176.0ms | 25.5ms | 48.1 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 659.1ms | 10.7× | 5/7 | 692.2ms | 33.1ms | 104.7 MB | 6/7 | 100000 |
| clojure | 635.3ms | 10.3× | 4/7 | 1.012s | 376.8ms | 132.9 MB | 7/7 | 100000 |
| elixir | 61.7ms | 1.0× | 1/7 | 247.1ms | 185.4ms | 71.7 MB | 5/7 | 100000 |
| python | 850.8ms | 13.8× | 7/7 | 861.8ms | 11.0ms | 10.8 MB | 1/7 | 100000 |
| node | 675.9ms | 11.0× | 6/7 | 694.0ms | 18.1ms | 67.4 MB | 4/7 | 100000 |
| ruby | 625.2ms | 10.1× | 3/7 | 665.5ms | 40.3ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 187.1ms | 3.0× | 2/7 | 212.6ms | 25.5ms | 27.7 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.251s | 19.0× | 4/7 | 2.284s | 33.1ms | 331.1 MB | 6/7 | 1000000 |
| clojure | 4.579s | 38.6× | 6/7 | 4.956s | 376.8ms | 754.1 MB | 7/7 | 1000000 |
| elixir | 275.4ms | 2.3× | 2/7 | 460.8ms | 185.4ms | 70.5 MB | 5/7 | 1000000 |
| python | 4.887s | 41.2× | 7/7 | 4.898s | 11.0ms | 16.0 MB | 1/7 | 1000000 |
| node | 118.6ms | 1.0× | 1/7 | 136.7ms | 18.1ms | 65.4 MB | 4/7 | 1000000 |
| ruby | 3.654s | 30.8× | 5/7 | 3.695s | 40.3ms | 23.0 MB | 2/7 | 1000000 |
| dotnet | 918.7ms | 7.7× | 3/7 | 944.2ms | 25.5ms | 30.2 MB | 3/7 | 1000000 |
