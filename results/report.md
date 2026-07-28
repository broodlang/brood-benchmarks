# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-28 14:55.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.5ms | 1.1× | 2/7 | 12.5ms | — | 20.1 MB | 3/7 | 0 |
| clojure | 348.5ms | 32.0× | 7/7 | 348.5ms | — | 103.5 MB | 7/7 | 0 |
| elixir | 185.0ms | 17.0× | 6/7 | 185.0ms | — | 72.9 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.8ms | 1.7× | 3/7 | 18.8ms | — | 42.5 MB | 5/7 | 0 |
| ruby | 41.0ms | 3.8× | 5/7 | 41.0ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 22.5ms | 2.1× | 4/7 | 22.5ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.2ms | 1.3× | 2/7 | 74.7ms | 12.5ms | 23.9 MB | 3/7 | 9227465 |
| clojure | 206.7ms | 4.3× | 5/7 | 555.2ms | 348.5ms | 109.3 MB | 7/7 | 9227465 |
| elixir | 88.0ms | 1.8× | 4/7 | 273.0ms | 185.0ms | 69.9 MB | 6/7 | 9227465 |
| python | 803.3ms | 16.7× | 7/7 | 814.2ms | 10.9ms | 9.9 MB | 1/7 | 9227465 |
| node | 78.7ms | 1.6× | 3/7 | 97.5ms | 18.8ms | 47.8 MB | 5/7 | 9227465 |
| ruby | 637.7ms | 13.3× | 6/7 | 678.7ms | 41.0ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 48.1ms | 1.0× | 1/7 | 70.6ms | 22.5ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.4ms | 3.8× | 3/7 | 57.9ms | 12.5ms | 24.1 MB | 3/7 | 449999985000000 |
| clojure | 158.8ms | 13.1× | 5/7 | 507.3ms | 348.5ms | 108.8 MB | 7/7 | 449999985000000 |
| elixir | 55.8ms | 4.6× | 4/7 | 240.8ms | 185.0ms | 70.9 MB | 6/7 | 449999985000000 |
| python | 2.447s | 202.2× | 7/7 | 2.458s | 10.9ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.8ms | 2.5× | 2/7 | 48.6ms | 18.8ms | 51.9 MB | 5/7 | 449999985000000 |
| ruby | 594.1ms | 49.1× | 6/7 | 635.1ms | 41.0ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 34.6ms | 22.5ms | 26.4 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.7ms | 1.0× | 1/7 | 16.2ms | 12.5ms | 19.8 MB | 3/7 | 12499997500000 |
| clojure | 169.4ms | 45.8× | 5/7 | 517.9ms | 348.5ms | 220.9 MB | 7/7 | 12499997500000 |
| elixir | 33.1ms | 8.9× | 3/7 | 218.1ms | 185.0ms | 72.0 MB | 5/7 | 12499997500000 |
| python | 105.7ms | 28.6× | 4/7 | 116.6ms | 10.9ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 220.4ms | 59.6× | 6/7 | 239.2ms | 18.8ms | 92.0 MB | 6/7 | 12499997500000 |
| ruby | 222.2ms | 60.1× | 7/7 | 263.2ms | 41.0ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.9ms | 3.2× | 2/7 | 34.4ms | 22.5ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.3ms | 5.1× | 4/7 | 53.8ms | 12.5ms | 23.8 MB | 3/7 | 13848 |
| clojure | 143.2ms | 17.7× | 7/7 | 491.7ms | 348.5ms | 109.2 MB | 7/7 | 13848 |
| elixir | 18.5ms | 2.3× | 3/7 | 203.5ms | 185.0ms | 70.4 MB | 6/7 | 13848 |
| python | 124.1ms | 15.3× | 6/7 | 135.0ms | 10.9ms | 9.9 MB | 1/7 | 13848 |
| node | 8.8ms | 1.1× | 2/7 | 27.6ms | 18.8ms | 50.6 MB | 5/7 | 13848 |
| ruby | 118.7ms | 14.7× | 5/7 | 159.7ms | 41.0ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.1ms | 1.0× | 1/7 | 30.6ms | 22.5ms | 26.4 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.1ms | 1.8× | 2/7 | 95.6ms | 12.5ms | 23.8 MB | 3/7 | 442 |
| clojure | 418.3ms | 9.0× | 5/7 | 766.8ms | 348.5ms | 370.6 MB | 7/7 | 442 |
| elixir | 107.5ms | 2.3× | 3/7 | 292.5ms | 185.0ms | 70.7 MB | 6/7 | 442 |
| python | 2.559s | 55.3× | 7/7 | 2.570s | 10.9ms | 10.0 MB | 1/7 | 442 |
| node | 175.4ms | 3.8× | 4/7 | 194.2ms | 18.8ms | 50.3 MB | 5/7 | 442 |
| ruby | 850.0ms | 18.4× | 6/7 | 891.0ms | 41.0ms | 19.2 MB | 2/7 | 442 |
| dotnet | 46.3ms | 1.0× | 1/7 | 68.8ms | 22.5ms | 26.2 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 168.4ms | 9.3× | 4/7 | 180.9ms | 12.5ms | 24.0 MB | 3/7 | 6129302 |
| clojure | 158.2ms | 8.7× | 3/7 | 506.7ms | 348.5ms | 115.6 MB | 7/7 | 6129302 |
| elixir | 258.8ms | 14.2× | 5/7 | 443.8ms | 185.0ms | 72.6 MB | 6/7 | 6129302 |
| python | 1.270s | 69.8× | 7/7 | 1.281s | 10.9ms | 10.1 MB | 1/7 | 6129302 |
| node | 20.6ms | 1.1× | 2/7 | 39.4ms | 18.8ms | 51.9 MB | 5/7 | 6129302 |
| ruby | 410.8ms | 22.6× | 6/7 | 451.8ms | 41.0ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.2ms | 1.0× | 1/7 | 40.7ms | 22.5ms | 26.4 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.2ms | 34.6× | 4/7 | 140.7ms | 12.5ms | 44.0 MB | 4/7 | 654353666 |
| clojure | 190.6ms | 51.5× | 5/7 | 539.1ms | 348.5ms | 118.3 MB | 7/7 | 654353666 |
| elixir | 66.6ms | 18.0× | 3/7 | 251.6ms | 185.0ms | 77.5 MB | 6/7 | 654353666 |
| python | 445.9ms | 120.5× | 7/7 | 456.8ms | 10.9ms | 10.4 MB | 1/7 | 654353666 |
| node | 17.2ms | 4.6× | 2/7 | 36.0ms | 18.8ms | 53.9 MB | 5/7 | 654353666 |
| ruby | 274.9ms | 74.3× | 6/7 | 315.9ms | 41.0ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 3.7ms | 1.0× | 1/7 | 26.2ms | 22.5ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.0ms | 1.0× | 1/7 | 25.5ms | 12.5ms | 30.2 MB | 1/7 | 3388889 |
| clojure | 159.8ms | 12.3× | 7/7 | 508.3ms | 348.5ms | 168.3 MB | 6/7 | 3388889 |
| elixir | 124.1ms | 9.5× | 6/7 | 309.1ms | 185.0ms | 201.8 MB | 7/7 | 3388889 |
| python | 42.4ms | 3.3× | 3/7 | 53.3ms | 10.9ms | 40.0 MB | 2/7 | 3388889 |
| node | 65.3ms | 5.0× | 4/7 | 84.1ms | 18.8ms | 97.2 MB | 5/7 | 3388889 |
| ruby | 82.0ms | 6.3× | 5/7 | 123.0ms | 41.0ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.8ms | 2.4× | 2/7 | 53.3ms | 22.5ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.8ms | 1.1× | 2/7 | 46.3ms | 12.5ms | 24.7 MB | 3/7 | 374854840 |
| clojure | 274.4ms | 9.2× | 7/7 | 622.9ms | 348.5ms | 302.4 MB | 7/7 | 374854840 |
| elixir | 162.5ms | 5.5× | 5/7 | 347.5ms | 185.0ms | 70.3 MB | 6/7 | 374854840 |
| python | 171.7ms | 5.8× | 6/7 | 182.6ms | 10.9ms | 10.0 MB | 1/7 | 374854840 |
| node | 29.8ms | 1.0× | 1/7 | 48.6ms | 18.8ms | 52.3 MB | 5/7 | 374854840 |
| ruby | 70.4ms | 2.4× | 4/7 | 111.4ms | 41.0ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 38.4ms | 1.3× | 3/7 | 60.9ms | 22.5ms | 27.2 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.1ms | 8.4× | 6/7 | 115.6ms | 12.5ms | 53.4 MB | 4/7 | 1638200 |
| clojure | 161.9ms | 13.2× | 7/7 | 510.4ms | 348.5ms | 150.1 MB | 7/7 | 1638200 |
| elixir | 12.3ms | 1.0× | 1/7 | 197.3ms | 185.0ms | 73.4 MB | 6/7 | 1638200 |
| python | 99.8ms | 8.1× | 5/7 | 110.7ms | 10.9ms | 10.2 MB | 1/7 | 1638200 |
| node | 21.4ms | 1.7× | 3/7 | 40.2ms | 18.8ms | 58.0 MB | 5/7 | 1638200 |
| ruby | 98.1ms | 8.0× | 4/7 | 139.1ms | 41.0ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 14.6ms | 1.2× | 2/7 | 37.1ms | 22.5ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.4ms | 2.1× | 5/7 | 149.9ms | 12.5ms | 200.7 MB | 7/7 | 46468819 |
| clojure | 243.4ms | 3.8× | 7/7 | 591.9ms | 348.5ms | 123.6 MB | 5/7 | 46468819 |
| elixir | 116.8ms | 1.8× | 4/7 | 301.8ms | 185.0ms | 157.8 MB | 6/7 | 46468819 |
| python | 184.6ms | 2.9× | 6/7 | 195.5ms | 10.9ms | 25.9 MB | 2/7 | 46468819 |
| node | 104.1ms | 1.6× | 3/7 | 122.9ms | 18.8ms | 67.0 MB | 4/7 | 46468819 |
| ruby | 70.8ms | 1.1× | 2/7 | 111.8ms | 41.0ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 64.6ms | 1.0× | 1/7 | 87.1ms | 22.5ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.5ms | 11.8× | 5/7 | 94.0ms | 12.5ms | 44.3 MB | 4/7 | 724 |
| clojure | 190.7ms | 27.6× | 7/7 | 539.2ms | 348.5ms | 136.2 MB | 7/7 | 724 |
| elixir | 10.4ms | 1.5× | 2/7 | 195.4ms | 185.0ms | 71.2 MB | 6/7 | 724 |
| python | 54.8ms | 7.9× | 4/7 | 65.7ms | 10.9ms | 9.9 MB | 1/7 | 724 |
| node | 6.9ms | 1.0× | 1/7 | 25.7ms | 18.8ms | 52.6 MB | 5/7 | 724 |
| ruby | 121.7ms | 17.6× | 6/7 | 162.7ms | 41.0ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.2ms | 2.8× | 3/7 | 41.7ms | 22.5ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.2ms | 2.1× | 2/7 | 56.7ms | 12.5ms | 23.5 MB | 3/7 | 9900000 |
| clojure | 1.088s | 51.6× | 7/7 | 1.436s | 348.5ms | 370.3 MB | 7/7 | 9900000 |
| elixir | 21.1ms | 1.0× | 1/7 | 206.1ms | 185.0ms | 70.6 MB | 6/7 | 9900000 |
| python | 46.9ms | 2.2× | 3/7 | 57.8ms | 10.9ms | 10.0 MB | 1/7 | 9900000 |
| node | 594.7ms | 28.2× | 6/7 | 613.5ms | 18.8ms | 52.4 MB | 5/7 | 9900000 |
| ruby | 108.5ms | 5.1× | 4/7 | 149.5ms | 41.0ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 296.2ms | 14.0× | 5/7 | 318.7ms | 22.5ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.6ms | 5.0× | 2/7 | 54.1ms | 12.5ms | 23.7 MB | 2/7 | 2475000 |
| clojure | 1.333s | 160.6× | 7/7 | 1.682s | 348.5ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 8.3ms | 1.0× | 1/7 | 193.3ms | 185.0ms | 72.5 MB | 6/7 | 2475000 |
| python | 233.1ms | 28.1× | 5/7 | 244.0ms | 10.9ms | 9.9 MB | 1/7 | 2475000 |
| node | 211.6ms | 25.5× | 4/7 | 230.4ms | 18.8ms | 52.2 MB | 5/7 | 2475000 |
| ruby | 111.2ms | 13.4× | 3/7 | 152.2ms | 41.0ms | 26.0 MB | 3/7 | 2475000 |
| dotnet | 668.5ms | 80.5× | 6/7 | 691.0ms | 22.5ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 8.4× | 6/7 | 44.5ms | 12.5ms | 24.0 MB | 3/7 | 155553889038886 |
| clojure | 130.2ms | 34.3× | 7/7 | 478.7ms | 348.5ms | 108.1 MB | 7/7 | 155553889038886 |
| elixir | 5.5ms | 1.4× | 2/7 | 190.5ms | 185.0ms | 72.5 MB | 6/7 | 155553889038886 |
| python | 3.8ms | 1.0× | 1/7 | 14.7ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 7.8ms | 2.1× | 5/7 | 26.6ms | 18.8ms | 53.8 MB | 5/7 | 155553889038886 |
| ruby | 6.3ms | 1.7× | 3/7 | 47.3ms | 41.0ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 6.7ms | 1.8× | 4/7 | 29.2ms | 22.5ms | 28.0 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 361.6ms | 1.5× | 3/7 | 374.1ms | 12.5ms | 23.9 MB | 3/7 | 24558 |
| clojure | 553.0ms | 2.3× | 5/7 | 901.5ms | 348.5ms | 374.7 MB | 7/7 | 24558 |
| elixir | 290.9ms | 1.2× | 2/7 | 475.9ms | 185.0ms | 71.7 MB | 6/7 | 24558 |
| python | 3.876s | 15.8× | 7/7 | 3.887s | 10.9ms | 11.1 MB | 1/7 | 24558 |
| node | 397.7ms | 1.6× | 4/7 | 416.5ms | 18.8ms | 50.3 MB | 5/7 | 24558 |
| ruby | 1.680s | 6.9× | 6/7 | 1.721s | 41.0ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 245.0ms | 1.0× | 1/7 | 267.5ms | 22.5ms | 26.2 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.6ms | 11.3× | 3/7 | 44.1ms | 12.5ms | 31.6 MB | 4/7 | 78498 |
| clojure | 132.9ms | 47.5× | 7/7 | 481.4ms | 348.5ms | 108.9 MB | 7/7 | 78498 |
| elixir | 59.9ms | 21.4× | 4/7 | 244.9ms | 185.0ms | 79.7 MB | 6/7 | 78498 |
| python | 114.8ms | 41.0× | 6/7 | 125.7ms | 10.9ms | 10.9 MB | 1/7 | 78498 |
| node | 6.0ms | 2.1× | 2/7 | 24.8ms | 18.8ms | 51.5 MB | 5/7 | 78498 |
| ruby | 83.7ms | 29.9× | 5/7 | 124.7ms | 41.0ms | 26.9 MB | 2/7 | 78498 |
| dotnet | 2.8ms | 1.0× | 1/7 | 25.3ms | 22.5ms | 27.5 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 61.5ms | 2.7× | 4/7 | 74.0ms | 12.5ms | 71.9 MB | 5/7 | 30039386344 |
| clojure | 298.3ms | 13.2× | 7/7 | 646.8ms | 348.5ms | 291.8 MB | 7/7 | 30039386344 |
| elixir | 120.0ms | 5.3× | 6/7 | 305.0ms | 185.0ms | 97.8 MB | 6/7 | 30039386344 |
| python | 81.9ms | 3.6× | 5/7 | 92.8ms | 10.9ms | 14.9 MB | 1/7 | 30039386344 |
| node | 22.8ms | 1.0× | 2/7 | 41.6ms | 18.8ms | 56.1 MB | 4/7 | 30039386344 |
| ruby | 38.3ms | 1.7× | 3/7 | 79.3ms | 41.0ms | 21.7 MB | 2/7 | 30039386344 |
| dotnet | 22.6ms | 1.0× | 1/7 | 45.1ms | 22.5ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 322.6ms | 50.4× | 6/7 | 335.1ms | 12.5ms | 55.3 MB | 5/7 | -169078071 |
| clojure | 174.0ms | 27.2× | 4/7 | 522.5ms | 348.5ms | 109.7 MB | 7/7 | -169078071 |
| elixir | 151.2ms | 23.6× | 3/7 | 336.2ms | 185.0ms | 71.0 MB | 6/7 | -169078071 |
| python | 693.8ms | 108.4× | 7/7 | 704.7ms | 10.9ms | 10.5 MB | 1/7 | -169078071 |
| node | 14.1ms | 2.2× | 2/7 | 32.9ms | 18.8ms | 52.5 MB | 4/7 | -169078071 |
| ruby | 292.8ms | 45.8× | 5/7 | 333.8ms | 41.0ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.4ms | 1.0× | 1/7 | 28.9ms | 22.5ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.7ms | 121.4× | 6/7 | 158.2ms | 12.5ms | 69.1 MB | 5/7 | 1489952542 |
| clojure | 403.4ms | 336.2× | 7/7 | 751.9ms | 348.5ms | 164.7 MB | 7/7 | 1489952542 |
| elixir | 6.3ms | 5.3× | 3/7 | 191.3ms | 185.0ms | 74.6 MB | 6/7 | 1489952542 |
| python | 7.9ms | 6.6× | 4/7 | 18.8ms | 10.9ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.2ms | 1.0× | 1/7 | 20.0ms | 18.8ms | 45.7 MB | 4/7 | 1489952542 |
| ruby | 2.3ms | 1.9× | 2/7 | 43.3ms | 41.0ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 43.1ms | 35.9× | 5/7 | 65.6ms | 22.5ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.8ms | 20.7× | 6/7 | 93.3ms | 12.5ms | 42.3 MB | 4/7 | 10000 |
| clojure | 130.1ms | 33.4× | 7/7 | 478.6ms | 348.5ms | 108.4 MB | 7/7 | 10000 |
| elixir | 16.1ms | 4.1× | 5/7 | 201.1ms | 185.0ms | 71.5 MB | 6/7 | 10000 |
| python | 12.6ms | 3.2× | 4/7 | 23.5ms | 10.9ms | 11.2 MB | 1/7 | 10000 |
| node | 3.9ms | 1.0× | 1/7 | 22.7ms | 18.8ms | 52.3 MB | 5/7 | 10000 |
| ruby | 5.9ms | 1.5× | 2/7 | 46.9ms | 41.0ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 12.1ms | 3.1× | 3/7 | 34.6ms | 22.5ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 99.2ms | 23.1× | 6/7 | 111.7ms | 12.5ms | 92.2 MB | 6/7 | 12081249 |
| clojure | 163.2ms | 38.0× | 7/7 | 511.7ms | 348.5ms | 109.5 MB | 7/7 | 12081249 |
| elixir | 16.2ms | 3.8× | 5/7 | 201.2ms | 185.0ms | 77.4 MB | 5/7 | 12081249 |
| python | 12.7ms | 3.0× | 4/7 | 23.6ms | 10.9ms | 10.3 MB | 1/7 | 12081249 |
| node | 5.7ms | 1.3× | 2/7 | 24.5ms | 18.8ms | 52.9 MB | 4/7 | 12081249 |
| ruby | 7.8ms | 1.8× | 3/7 | 48.8ms | 41.0ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 4.3ms | 1.0× | 1/7 | 26.8ms | 22.5ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.7ms | 2.5× | 3/7 | 57.2ms | 12.5ms | 45.6 MB | 3/7 | 6100000 |
| clojure | 187.7ms | 10.5× | 5/7 | 536.2ms | 348.5ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 18.6ms | 1.0× | 2/7 | 203.6ms | 185.0ms | 77.3 MB | 5/7 | 6100000 |
| python | 555.3ms | 31.2× | 6/7 | 566.2ms | 10.9ms | 28.0 MB | 1/7 | 6100000 |
| node | 53.4ms | 3.0× | 4/7 | 72.2ms | 18.8ms | 53.4 MB | 4/7 | 6100000 |
| ruby | 1.578s | 88.6× | 7/7 | 1.619s | 41.0ms | 133.0 MB | 6/7 | 6100000 |
| dotnet | 17.8ms | 1.0× | 1/7 | 40.3ms | 22.5ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.0ms | 1.6× | 2/7 | 184.5ms | 12.5ms | 27.0 MB | 3/7 | 134626900 |
| clojure | 366.6ms | 3.3× | 5/7 | 715.1ms | 348.5ms | 135.8 MB | 6/7 | 134626900 |
| elixir | 297.0ms | 2.7× | 4/7 | 482.0ms | 185.0ms | 72.0 MB | 5/7 | 134626900 |
| python | 2.424s | 21.9× | 7/7 | 2.434s | 10.9ms | 21.9 MB | 2/7 | 134626900 |
| node | 287.3ms | 2.6× | 3/7 | 306.1ms | 18.8ms | 184.8 MB | 7/7 | 134626900 |
| ruby | 1.795s | 16.2× | 6/7 | 1.836s | 41.0ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 110.6ms | 1.0× | 1/7 | 133.1ms | 22.5ms | 28.3 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 160.5ms | 1.3× | 3/7 | 173.0ms | 12.5ms | 82.8 MB | 5/7 | 500 |
| clojure | 785.0ms | 6.5× | 7/7 | 1.133s | 348.5ms | 299.2 MB | 6/7 | 500 |
| elixir | 560.6ms | 4.7× | 6/7 | 745.6ms | 185.0ms | 484.3 MB | 7/7 | 500 |
| python | 172.9ms | 1.4× | 4/7 | 183.8ms | 10.9ms | 45.3 MB | 1/7 | 500 |
| node | 120.4ms | 1.0× | 1/7 | 139.2ms | 18.8ms | 67.3 MB | 4/7 | 500 |
| ruby | 204.3ms | 1.7× | 5/7 | 245.3ms | 41.0ms | 45.8 MB | 2/7 | 500 |
| dotnet | 146.3ms | 1.2× | 2/7 | 168.8ms | 22.5ms | 48.4 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 194.5ms | 3.8× | 3/7 | 207.0ms | 12.5ms | 48.0 MB | 4/7 | 100000 |
| clojure | 567.5ms | 11.0× | 4/7 | 916.0ms | 348.5ms | 134.4 MB | 7/7 | 100000 |
| elixir | 51.7ms | 1.0× | 1/7 | 236.7ms | 185.0ms | 71.3 MB | 6/7 | 100000 |
| python | 813.8ms | 15.7× | 7/7 | 824.7ms | 10.9ms | 10.9 MB | 1/7 | 100000 |
| node | 635.6ms | 12.3× | 6/7 | 654.4ms | 18.8ms | 69.6 MB | 5/7 | 100000 |
| ruby | 596.9ms | 11.5× | 5/7 | 637.9ms | 41.0ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 161.7ms | 3.1× | 2/7 | 184.2ms | 22.5ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 725.6ms | 6.0× | 3/7 | 738.1ms | 12.5ms | 91.1 MB | 6/7 | 1000000 |
| clojure | 4.317s | 35.9× | 6/7 | 4.665s | 348.5ms | 737.2 MB | 7/7 | 1000000 |
| elixir | 265.6ms | 2.2× | 2/7 | 450.6ms | 185.0ms | 70.3 MB | 5/7 | 1000000 |
| python | 4.598s | 38.2× | 7/7 | 4.609s | 10.9ms | 16.3 MB | 1/7 | 1000000 |
| node | 120.4ms | 1.0× | 1/7 | 139.2ms | 18.8ms | 67.4 MB | 4/7 | 1000000 |
| ruby | 3.380s | 28.1× | 5/7 | 3.421s | 41.0ms | 23.3 MB | 2/7 | 1000000 |
| dotnet | 772.9ms | 6.4× | 4/7 | 795.4ms | 22.5ms | 30.7 MB | 3/7 | 1000000 |
