# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-26 21:43.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.7ms | 1.1× | 2/7 | 11.7ms | — | 19.2 MB | 2/7 | 0 |
| clojure | 331.6ms | 32.5× | 7/7 | 331.6ms | — | 102.5 MB | 7/7 | 0 |
| elixir | 180.6ms | 17.7× | 6/7 | 180.6ms | — | 70.0 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.7 MB | 1/7 | 0 |
| node | 17.7ms | 1.7× | 3/7 | 17.7ms | — | 42.9 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.8× | 5/7 | 38.8ms | — | 19.2 MB | 3/7 | 0 |
| dotnet | 21.8ms | 2.1× | 4/7 | 21.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 57.4ms | 1.3× | 2/7 | 69.1ms | 11.7ms | 23.1 MB | 3/7 | 9227465 |
| clojure | 196.8ms | 4.5× | 5/7 | 528.4ms | 331.6ms | 109.4 MB | 7/7 | 9227465 |
| elixir | 71.9ms | 1.7× | 3/7 | 252.5ms | 180.6ms | 72.3 MB | 6/7 | 9227465 |
| python | 724.5ms | 16.7× | 7/7 | 734.7ms | 10.2ms | 9.9 MB | 1/7 | 9227465 |
| node | 72.7ms | 1.7× | 4/7 | 90.4ms | 17.7ms | 48.3 MB | 5/7 | 9227465 |
| ruby | 598.7ms | 13.8× | 6/7 | 637.5ms | 38.8ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 43.4ms | 1.0× | 1/7 | 65.2ms | 21.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.4ms | 3.2× | 3/7 | 49.1ms | 11.7ms | 23.5 MB | 3/7 | 449999985000000 |
| clojure | 142.6ms | 12.1× | 5/7 | 474.2ms | 331.6ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 47.4ms | 4.0× | 4/7 | 228.0ms | 180.6ms | 72.6 MB | 6/7 | 449999985000000 |
| python | 2.299s | 194.8× | 7/7 | 2.309s | 10.2ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.7ms | 2.5× | 2/7 | 47.4ms | 17.7ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 573.9ms | 48.6× | 6/7 | 612.7ms | 38.8ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 11.8ms | 1.0× | 1/7 | 33.6ms | 21.8ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.6ms | 1.0× | 1/7 | 15.3ms | 11.7ms | 19.3 MB | 3/7 | 12499997500000 |
| clojure | 173.7ms | 48.2× | 5/7 | 505.3ms | 331.6ms | 219.2 MB | 7/7 | 12499997500000 |
| elixir | 29.6ms | 8.2× | 3/7 | 210.2ms | 180.6ms | 70.1 MB | 5/7 | 12499997500000 |
| python | 103.6ms | 28.8× | 4/7 | 113.8ms | 10.2ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 218.3ms | 60.6× | 6/7 | 236.0ms | 17.7ms | 90.3 MB | 6/7 | 12499997500000 |
| ruby | 219.0ms | 60.8× | 7/7 | 257.8ms | 38.8ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.1ms | 3.1× | 2/7 | 32.9ms | 21.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.4ms | 5.0× | 4/7 | 55.1ms | 11.7ms | 23.8 MB | 3/7 | 13848 |
| clojure | 139.7ms | 16.2× | 7/7 | 471.3ms | 331.6ms | 108.1 MB | 7/7 | 13848 |
| elixir | 15.6ms | 1.8× | 3/7 | 196.2ms | 180.6ms | 72.8 MB | 6/7 | 13848 |
| python | 119.5ms | 13.9× | 6/7 | 129.7ms | 10.2ms | 10.0 MB | 1/7 | 13848 |
| node | 8.8ms | 1.0× | 2/7 | 26.5ms | 17.7ms | 48.8 MB | 5/7 | 13848 |
| ruby | 114.4ms | 13.3× | 5/7 | 153.2ms | 38.8ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.6ms | 1.0× | 1/7 | 30.4ms | 21.8ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.8ms | 1.8× | 2/7 | 94.5ms | 11.7ms | 24.3 MB | 3/7 | 442 |
| clojure | 413.2ms | 9.0× | 5/7 | 744.8ms | 331.6ms | 371.1 MB | 7/7 | 442 |
| elixir | 103.0ms | 2.2× | 3/7 | 283.6ms | 180.6ms | 69.7 MB | 6/7 | 442 |
| python | 2.368s | 51.5× | 7/7 | 2.378s | 10.2ms | 9.9 MB | 1/7 | 442 |
| node | 171.9ms | 3.7× | 4/7 | 189.6ms | 17.7ms | 48.5 MB | 5/7 | 442 |
| ruby | 839.9ms | 18.3× | 6/7 | 878.7ms | 38.8ms | 19.2 MB | 2/7 | 442 |
| dotnet | 46.0ms | 1.0× | 1/7 | 67.8ms | 21.8ms | 26.4 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.4ms | 9.5× | 4/7 | 183.1ms | 11.7ms | 23.6 MB | 3/7 | 6129302 |
| clojure | 158.3ms | 8.8× | 3/7 | 489.9ms | 331.6ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 244.1ms | 13.6× | 5/7 | 424.7ms | 180.6ms | 70.4 MB | 6/7 | 6129302 |
| python | 1.367s | 76.0× | 7/7 | 1.377s | 10.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.2ms | 1.2× | 2/7 | 38.9ms | 17.7ms | 50.1 MB | 5/7 | 6129302 |
| ruby | 404.2ms | 22.5× | 6/7 | 443.0ms | 38.8ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.0ms | 1.0× | 1/7 | 39.8ms | 21.8ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 129.7ms | 30.9× | 4/7 | 141.4ms | 11.7ms | 44.2 MB | 4/7 | 654353666 |
| clojure | 190.8ms | 45.4× | 5/7 | 522.4ms | 331.6ms | 118.4 MB | 7/7 | 654353666 |
| elixir | 60.8ms | 14.5× | 3/7 | 241.4ms | 180.6ms | 76.9 MB | 6/7 | 654353666 |
| python | 447.9ms | 106.6× | 7/7 | 458.1ms | 10.2ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.8ms | 4.0× | 2/7 | 34.5ms | 17.7ms | 52.4 MB | 5/7 | 654353666 |
| ruby | 280.8ms | 66.9× | 6/7 | 319.6ms | 38.8ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.2ms | 1.0× | 1/7 | 26.0ms | 21.8ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.1ms | 1.0× | 1/7 | 23.8ms | 11.7ms | 29.7 MB | 1/7 | 3388889 |
| clojure | 158.9ms | 13.1× | 7/7 | 490.5ms | 331.6ms | 167.4 MB | 6/7 | 3388889 |
| elixir | 113.5ms | 9.4× | 6/7 | 294.1ms | 180.6ms | 199.6 MB | 7/7 | 3388889 |
| python | 42.6ms | 3.5× | 3/7 | 52.8ms | 10.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 63.9ms | 5.3× | 4/7 | 81.6ms | 17.7ms | 95.4 MB | 5/7 | 3388889 |
| ruby | 83.0ms | 6.9× | 5/7 | 121.8ms | 38.8ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 31.2ms | 2.6× | 2/7 | 53.0ms | 21.8ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.8ms | 1.2× | 2/7 | 46.5ms | 11.7ms | 24.8 MB | 3/7 | 374854840 |
| clojure | 270.6ms | 9.0× | 7/7 | 602.2ms | 331.6ms | 302.5 MB | 7/7 | 374854840 |
| elixir | 159.9ms | 5.3× | 5/7 | 340.5ms | 180.6ms | 70.2 MB | 6/7 | 374854840 |
| python | 175.8ms | 5.9× | 6/7 | 186.0ms | 10.2ms | 10.0 MB | 1/7 | 374854840 |
| node | 30.0ms | 1.0× | 1/7 | 47.7ms | 17.7ms | 50.3 MB | 5/7 | 374854840 |
| ruby | 69.8ms | 2.3× | 4/7 | 108.6ms | 38.8ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 36.0ms | 1.2× | 3/7 | 57.8ms | 21.8ms | 27.3 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.2ms | 11.3× | 6/7 | 116.9ms | 11.7ms | 53.3 MB | 4/7 | 1638200 |
| clojure | 170.4ms | 18.3× | 7/7 | 502.0ms | 331.6ms | 150.5 MB | 7/7 | 1638200 |
| elixir | 9.3ms | 1.0× | 1/7 | 189.9ms | 180.6ms | 70.4 MB | 6/7 | 1638200 |
| python | 96.9ms | 10.4× | 5/7 | 107.1ms | 10.2ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.3ms | 2.3× | 3/7 | 39.0ms | 17.7ms | 56.3 MB | 5/7 | 1638200 |
| ruby | 95.0ms | 10.2× | 4/7 | 133.8ms | 38.8ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.2ms | 1.5× | 2/7 | 36.0ms | 21.8ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 208.3ms | 3.3× | 6/7 | 220.0ms | 11.7ms | 173.8 MB | 7/7 | 46468819 |
| clojure | 244.6ms | 3.8× | 7/7 | 576.2ms | 331.6ms | 123.8 MB | 5/7 | 46468819 |
| elixir | 106.5ms | 1.7× | 4/7 | 287.1ms | 180.6ms | 157.8 MB | 6/7 | 46468819 |
| python | 177.3ms | 2.8× | 5/7 | 187.5ms | 10.2ms | 25.9 MB | 2/7 | 46468819 |
| node | 102.3ms | 1.6× | 3/7 | 120.0ms | 17.7ms | 65.1 MB | 4/7 | 46468819 |
| ruby | 69.6ms | 1.1× | 2/7 | 108.4ms | 38.8ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 63.6ms | 1.0× | 1/7 | 85.4ms | 21.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.1ms | 11.4× | 5/7 | 92.8ms | 11.7ms | 41.6 MB | 4/7 | 724 |
| clojure | 274.0ms | 38.6× | 7/7 | 605.6ms | 331.6ms | 136.1 MB | 7/7 | 724 |
| elixir | 8.1ms | 1.1× | 2/7 | 188.7ms | 180.6ms | 72.9 MB | 6/7 | 724 |
| python | 53.4ms | 7.5× | 4/7 | 63.6ms | 10.2ms | 9.9 MB | 1/7 | 724 |
| node | 7.1ms | 1.0× | 1/7 | 24.8ms | 17.7ms | 50.8 MB | 5/7 | 724 |
| ruby | 118.2ms | 16.6× | 6/7 | 157.0ms | 38.8ms | 19.6 MB | 2/7 | 724 |
| dotnet | 18.9ms | 2.7× | 3/7 | 40.7ms | 21.8ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.8ms | 2.9× | 2/7 | 58.5ms | 11.7ms | 23.4 MB | 3/7 | 9900000 |
| clojure | 1.072s | 67.4× | 7/7 | 1.404s | 331.6ms | 370.2 MB | 7/7 | 9900000 |
| elixir | 15.9ms | 1.0× | 1/7 | 196.5ms | 180.6ms | 70.0 MB | 6/7 | 9900000 |
| python | 50.1ms | 3.2× | 3/7 | 60.3ms | 10.2ms | 9.9 MB | 1/7 | 9900000 |
| node | 557.4ms | 35.1× | 6/7 | 575.1ms | 17.7ms | 50.5 MB | 5/7 | 9900000 |
| ruby | 110.0ms | 6.9× | 4/7 | 148.8ms | 38.8ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 292.0ms | 18.4× | 5/7 | 313.8ms | 21.8ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.1ms | 6.1× | 2/7 | 55.8ms | 11.7ms | 24.1 MB | 2/7 | 2475000 |
| clojure | 1.317s | 183.0× | 7/7 | 1.649s | 331.6ms | 373.7 MB | 7/7 | 2475000 |
| elixir | 7.2ms | 1.0× | 1/7 | 187.8ms | 180.6ms | 72.4 MB | 6/7 | 2475000 |
| python | 231.0ms | 32.1× | 5/7 | 241.2ms | 10.2ms | 9.9 MB | 1/7 | 2475000 |
| node | 205.1ms | 28.5× | 4/7 | 222.8ms | 17.7ms | 50.3 MB | 5/7 | 2475000 |
| ruby | 114.7ms | 15.9× | 3/7 | 153.5ms | 38.8ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 688.3ms | 95.6× | 6/7 | 710.1ms | 21.8ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.5ms | 8.1× | 6/7 | 43.2ms | 11.7ms | 23.8 MB | 3/7 | 155553889038886 |
| clojure | 129.6ms | 33.2× | 7/7 | 461.2ms | 331.6ms | 109.1 MB | 7/7 | 155553889038886 |
| elixir | 6.5ms | 1.7× | 2/7 | 187.1ms | 180.6ms | 72.5 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 1.0× | 1/7 | 14.1ms | 10.2ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 7.9ms | 2.0× | 5/7 | 25.6ms | 17.7ms | 52.2 MB | 5/7 | 155553889038886 |
| ruby | 7.5ms | 1.9× | 4/7 | 46.3ms | 38.8ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 6.7ms | 1.7× | 3/7 | 28.5ms | 21.8ms | 28.0 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 341.8ms | 1.3× | 3/7 | 353.5ms | 11.7ms | 24.3 MB | 3/7 | 24558 |
| clojure | 556.2ms | 2.0× | 5/7 | 887.8ms | 331.6ms | 374.5 MB | 7/7 | 24558 |
| elixir | 288.7ms | 1.1× | 2/7 | 469.3ms | 180.6ms | 72.2 MB | 6/7 | 24558 |
| python | 3.887s | 14.3× | 7/7 | 3.897s | 10.2ms | 11.0 MB | 1/7 | 24558 |
| node | 391.1ms | 1.4× | 4/7 | 408.8ms | 17.7ms | 48.6 MB | 5/7 | 24558 |
| ruby | 1.684s | 6.2× | 6/7 | 1.723s | 38.8ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 272.6ms | 1.0× | 1/7 | 294.4ms | 21.8ms | 26.2 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.4ms | 12.2× | 3/7 | 47.1ms | 11.7ms | 31.9 MB | 4/7 | 78498 |
| clojure | 137.7ms | 47.5× | 7/7 | 469.3ms | 331.6ms | 108.3 MB | 7/7 | 78498 |
| elixir | 57.1ms | 19.7× | 4/7 | 237.7ms | 180.6ms | 80.0 MB | 6/7 | 78498 |
| python | 115.2ms | 39.7× | 6/7 | 125.4ms | 10.2ms | 10.9 MB | 1/7 | 78498 |
| node | 6.4ms | 2.2× | 2/7 | 24.1ms | 17.7ms | 49.7 MB | 5/7 | 78498 |
| ruby | 82.8ms | 28.6× | 5/7 | 121.6ms | 38.8ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.9ms | 1.0× | 1/7 | 24.7ms | 21.8ms | 27.4 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 60.9ms | 2.8× | 4/7 | 72.6ms | 11.7ms | 68.0 MB | 5/7 | 30039386344 |
| clojure | 296.9ms | 13.5× | 7/7 | 628.5ms | 331.6ms | 291.1 MB | 7/7 | 30039386344 |
| elixir | 113.9ms | 5.2× | 6/7 | 294.5ms | 180.6ms | 96.4 MB | 6/7 | 30039386344 |
| python | 79.3ms | 3.6× | 5/7 | 89.5ms | 10.2ms | 14.9 MB | 1/7 | 30039386344 |
| node | 22.5ms | 1.0× | 2/7 | 40.2ms | 17.7ms | 54.2 MB | 4/7 | 30039386344 |
| ruby | 38.3ms | 1.7× | 3/7 | 77.1ms | 38.8ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 22.0ms | 1.0× | 1/7 | 43.8ms | 21.8ms | 30.3 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 311.4ms | 51.9× | 6/7 | 323.1ms | 11.7ms | 48.7 MB | 4/7 | -169078071 |
| clojure | 185.5ms | 30.9× | 4/7 | 517.1ms | 331.6ms | 109.8 MB | 7/7 | -169078071 |
| elixir | 141.1ms | 23.5× | 3/7 | 321.7ms | 180.6ms | 71.9 MB | 6/7 | -169078071 |
| python | 730.6ms | 121.8× | 7/7 | 740.8ms | 10.2ms | 10.4 MB | 1/7 | -169078071 |
| node | 12.6ms | 2.1× | 2/7 | 30.3ms | 17.7ms | 50.4 MB | 5/7 | -169078071 |
| ruby | 295.7ms | 49.3× | 5/7 | 334.5ms | 38.8ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.0ms | 1.0× | 1/7 | 27.8ms | 21.8ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 139.3ms | 81.9× | 6/7 | 151.0ms | 11.7ms | 76.8 MB | 6/7 | 1489952542 |
| clojure | 394.7ms | 232.2× | 7/7 | 726.3ms | 331.6ms | 159.0 MB | 7/7 | 1489952542 |
| elixir | 5.2ms | 3.1× | 3/7 | 185.8ms | 180.6ms | 76.0 MB | 5/7 | 1489952542 |
| python | 8.0ms | 4.7× | 4/7 | 18.2ms | 10.2ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.7ms | 1.0× | 1/7 | 19.4ms | 17.7ms | 44.2 MB | 4/7 | 1489952542 |
| ruby | 3.8ms | 2.2× | 2/7 | 42.6ms | 38.8ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 42.1ms | 24.8× | 5/7 | 63.9ms | 21.8ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.5ms | 22.0× | 6/7 | 95.2ms | 11.7ms | 42.7 MB | 4/7 | 10000 |
| clojure | 138.0ms | 36.3× | 7/7 | 469.6ms | 331.6ms | 108.4 MB | 7/7 | 10000 |
| elixir | 14.4ms | 3.8× | 5/7 | 195.0ms | 180.6ms | 70.2 MB | 6/7 | 10000 |
| python | 12.6ms | 3.3× | 4/7 | 22.8ms | 10.2ms | 11.1 MB | 1/7 | 10000 |
| node | 3.8ms | 1.0× | 1/7 | 21.5ms | 17.7ms | 50.5 MB | 5/7 | 10000 |
| ruby | 6.9ms | 1.8× | 2/7 | 45.7ms | 38.8ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 11.7ms | 3.1× | 3/7 | 33.5ms | 21.8ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.0ms | 29.1× | 6/7 | 113.7ms | 11.7ms | 99.1 MB | 6/7 | 12081249 |
| clojure | 158.6ms | 45.3× | 7/7 | 490.2ms | 331.6ms | 108.9 MB | 7/7 | 12081249 |
| elixir | 4.5ms | 1.3× | 2/7 | 185.1ms | 180.6ms | 76.4 MB | 5/7 | 12081249 |
| python | 12.7ms | 3.6× | 5/7 | 22.9ms | 10.2ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.5ms | 1.6× | 3/7 | 23.2ms | 17.7ms | 51.0 MB | 4/7 | 12081249 |
| ruby | 7.7ms | 2.2× | 4/7 | 46.5ms | 38.8ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 3.5ms | 1.0× | 1/7 | 25.3ms | 21.8ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.7ms | 2.8× | 3/7 | 57.4ms | 11.7ms | 45.1 MB | 3/7 | 6100000 |
| clojure | 192.2ms | 11.6× | 5/7 | 523.8ms | 331.6ms | 133.7 MB | 7/7 | 6100000 |
| elixir | 21.2ms | 1.3× | 2/7 | 201.8ms | 180.6ms | 76.0 MB | 5/7 | 6100000 |
| python | 544.7ms | 33.0× | 6/7 | 554.9ms | 10.2ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.9ms | 3.2× | 4/7 | 70.6ms | 17.7ms | 51.7 MB | 4/7 | 6100000 |
| ruby | 1.570s | 95.1× | 7/7 | 1.609s | 38.8ms | 133.4 MB | 6/7 | 6100000 |
| dotnet | 16.5ms | 1.0× | 1/7 | 38.3ms | 21.8ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.7ms | 1.5× | 2/7 | 176.4ms | 11.7ms | 25.8 MB | 3/7 | 134626900 |
| clojure | 364.2ms | 3.4× | 5/7 | 695.8ms | 331.6ms | 138.2 MB | 6/7 | 134626900 |
| elixir | 288.9ms | 2.7× | 4/7 | 469.5ms | 180.6ms | 71.1 MB | 5/7 | 134626900 |
| python | 2.405s | 22.3× | 7/7 | 2.415s | 10.2ms | 21.9 MB | 2/7 | 134626900 |
| node | 287.7ms | 2.7× | 3/7 | 305.4ms | 17.7ms | 182.0 MB | 7/7 | 134626900 |
| ruby | 1.815s | 16.8× | 6/7 | 1.853s | 38.8ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 107.8ms | 1.0× | 1/7 | 129.6ms | 21.8ms | 28.1 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 161.3ms | 1.4× | 3/7 | 173.0ms | 11.7ms | 74.4 MB | 5/7 | 500 |
| clojure | 812.4ms | 7.0× | 7/7 | 1.144s | 331.6ms | 285.1 MB | 6/7 | 500 |
| elixir | 570.2ms | 4.9× | 6/7 | 750.8ms | 180.6ms | 504.0 MB | 7/7 | 500 |
| python | 172.7ms | 1.5× | 4/7 | 182.9ms | 10.2ms | 46.1 MB | 2/7 | 500 |
| node | 115.5ms | 1.0× | 1/7 | 133.2ms | 17.7ms | 65.0 MB | 4/7 | 500 |
| ruby | 203.3ms | 1.8× | 5/7 | 242.1ms | 38.8ms | 45.8 MB | 1/7 | 500 |
| dotnet | 142.2ms | 1.2× | 2/7 | 164.0ms | 21.8ms | 48.4 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 189.2ms | 3.8× | 3/7 | 200.9ms | 11.7ms | 45.3 MB | 4/7 | 100000 |
| clojure | 566.9ms | 11.3× | 4/7 | 898.5ms | 331.6ms | 133.0 MB | 7/7 | 100000 |
| elixir | 50.0ms | 1.0× | 1/7 | 230.6ms | 180.6ms | 72.3 MB | 6/7 | 100000 |
| python | 811.9ms | 16.2× | 7/7 | 822.1ms | 10.2ms | 10.9 MB | 1/7 | 100000 |
| node | 631.7ms | 12.6× | 6/7 | 649.4ms | 17.7ms | 67.5 MB | 5/7 | 100000 |
| ruby | 571.9ms | 11.4× | 5/7 | 610.7ms | 38.8ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 161.6ms | 3.2× | 2/7 | 183.4ms | 21.8ms | 27.7 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 703.2ms | 6.2× | 3/7 | 714.9ms | 11.7ms | 95.0 MB | 6/7 | 1000000 |
| clojure | 4.361s | 38.6× | 6/7 | 4.692s | 331.6ms | 895.0 MB | 7/7 | 1000000 |
| elixir | 255.8ms | 2.3× | 2/7 | 436.4ms | 180.6ms | 70.5 MB | 5/7 | 1000000 |
| python | 4.610s | 40.8× | 7/7 | 4.620s | 10.2ms | 16.4 MB | 1/7 | 1000000 |
| node | 112.9ms | 1.0× | 1/7 | 130.6ms | 17.7ms | 65.6 MB | 4/7 | 1000000 |
| ruby | 3.477s | 30.8× | 5/7 | 3.516s | 38.8ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 773.6ms | 6.9× | 4/7 | 795.4ms | 21.8ms | 30.4 MB | 3/7 | 1000000 |
