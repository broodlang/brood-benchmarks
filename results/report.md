# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-28 20:09.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.7ms | 1.2× | 2/7 | 12.7ms | — | 19.9 MB | 3/7 | 0 |
| clojure | 351.6ms | 33.8× | 7/7 | 351.6ms | — | 103.6 MB | 7/7 | 0 |
| elixir | 188.0ms | 18.1× | 6/7 | 188.0ms | — | 71.9 MB | 6/7 | 0 |
| python | 10.4ms | 1.0× | 1/7 | 10.4ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.2ms | 1.7× | 3/7 | 18.2ms | — | 44.6 MB | 5/7 | 0 |
| ruby | 39.6ms | 3.8× | 5/7 | 39.6ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 21.9ms | 2.1× | 4/7 | 21.9ms | — | 26.0 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 60.3ms | 1.3× | 2/7 | 73.0ms | 12.7ms | 23.5 MB | 3/7 | 9227465 |
| clojure | 199.3ms | 4.4× | 5/7 | 550.9ms | 351.6ms | 109.5 MB | 7/7 | 9227465 |
| elixir | 79.7ms | 1.7× | 4/7 | 267.7ms | 188.0ms | 73.1 MB | 6/7 | 9227465 |
| python | 757.7ms | 16.6× | 7/7 | 768.1ms | 10.4ms | 9.9 MB | 1/7 | 9227465 |
| node | 77.2ms | 1.7× | 3/7 | 95.4ms | 18.2ms | 50.2 MB | 5/7 | 9227465 |
| ruby | 627.9ms | 13.8× | 6/7 | 667.5ms | 39.6ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 45.6ms | 1.0× | 1/7 | 67.5ms | 21.9ms | 26.0 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 3.6× | 3/7 | 55.8ms | 12.7ms | 23.5 MB | 3/7 | 449999985000000 |
| clojure | 146.4ms | 12.2× | 5/7 | 498.0ms | 351.6ms | 109.0 MB | 7/7 | 449999985000000 |
| elixir | 50.6ms | 4.2× | 4/7 | 238.6ms | 188.0ms | 71.6 MB | 6/7 | 449999985000000 |
| python | 2.365s | 197.0× | 7/7 | 2.375s | 10.4ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 30.6ms | 2.5× | 2/7 | 48.8ms | 18.2ms | 51.9 MB | 5/7 | 449999985000000 |
| ruby | 605.0ms | 50.4× | 6/7 | 644.6ms | 39.6ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 12.0ms | 1.0× | 1/7 | 33.9ms | 21.9ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.7ms | 1.0× | 1/7 | 17.4ms | 12.7ms | 20.0 MB | 3/7 | 12499997500000 |
| clojure | 169.7ms | 36.1× | 5/7 | 521.3ms | 351.6ms | 224.1 MB | 7/7 | 12499997500000 |
| elixir | 30.7ms | 6.5× | 3/7 | 218.7ms | 188.0ms | 70.1 MB | 5/7 | 12499997500000 |
| python | 112.4ms | 23.9× | 4/7 | 122.8ms | 10.4ms | 10.7 MB | 1/7 | 12499997500000 |
| node | 228.8ms | 48.7× | 6/7 | 247.0ms | 18.2ms | 92.2 MB | 6/7 | 12499997500000 |
| ruby | 241.7ms | 51.4× | 7/7 | 281.3ms | 39.6ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 12.7ms | 2.7× | 2/7 | 34.6ms | 21.9ms | 27.7 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.7ms | 4.6× | 4/7 | 54.4ms | 12.7ms | 23.9 MB | 3/7 | 13848 |
| clojure | 144.9ms | 16.1× | 7/7 | 496.5ms | 351.6ms | 108.7 MB | 7/7 | 13848 |
| elixir | 16.7ms | 1.9× | 3/7 | 204.7ms | 188.0ms | 70.2 MB | 6/7 | 13848 |
| python | 123.4ms | 13.7× | 6/7 | 133.8ms | 10.4ms | 10.0 MB | 1/7 | 13848 |
| node | 9.5ms | 1.1× | 2/7 | 27.7ms | 18.2ms | 50.7 MB | 5/7 | 13848 |
| ruby | 121.5ms | 13.5× | 5/7 | 161.1ms | 39.6ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 9.0ms | 1.0× | 1/7 | 30.9ms | 21.9ms | 26.4 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.8ms | 1.7× | 2/7 | 95.5ms | 12.7ms | 23.9 MB | 3/7 | 442 |
| clojure | 429.7ms | 9.0× | 5/7 | 781.3ms | 351.6ms | 370.4 MB | 7/7 | 442 |
| elixir | 107.9ms | 2.3× | 3/7 | 295.9ms | 188.0ms | 72.7 MB | 6/7 | 442 |
| python | 2.558s | 53.7× | 7/7 | 2.568s | 10.4ms | 9.9 MB | 1/7 | 442 |
| node | 180.1ms | 3.8× | 4/7 | 198.3ms | 18.2ms | 50.4 MB | 5/7 | 442 |
| ruby | 857.3ms | 18.0× | 6/7 | 896.9ms | 39.6ms | 19.2 MB | 2/7 | 442 |
| dotnet | 47.6ms | 1.0× | 1/7 | 69.5ms | 21.9ms | 26.4 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.9ms | 8.8× | 4/7 | 186.6ms | 12.7ms | 24.1 MB | 3/7 | 6129302 |
| clojure | 158.6ms | 8.1× | 3/7 | 510.2ms | 351.6ms | 114.7 MB | 7/7 | 6129302 |
| elixir | 254.7ms | 12.9× | 5/7 | 442.7ms | 188.0ms | 72.0 MB | 6/7 | 6129302 |
| python | 1.392s | 70.7× | 7/7 | 1.403s | 10.4ms | 10.1 MB | 1/7 | 6129302 |
| node | 21.3ms | 1.1× | 2/7 | 39.5ms | 18.2ms | 51.9 MB | 5/7 | 6129302 |
| ruby | 425.5ms | 21.6× | 6/7 | 465.1ms | 39.6ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 19.7ms | 1.0× | 1/7 | 41.6ms | 21.9ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 131.1ms | 23.0× | 4/7 | 143.8ms | 12.7ms | 44.4 MB | 4/7 | 654353666 |
| clojure | 191.0ms | 33.5× | 5/7 | 542.6ms | 351.6ms | 116.4 MB | 7/7 | 654353666 |
| elixir | 63.8ms | 11.2× | 3/7 | 251.8ms | 188.0ms | 75.8 MB | 6/7 | 654353666 |
| python | 439.1ms | 77.0× | 7/7 | 449.5ms | 10.4ms | 10.4 MB | 1/7 | 654353666 |
| node | 18.0ms | 3.2× | 2/7 | 36.2ms | 18.2ms | 54.0 MB | 5/7 | 654353666 |
| ruby | 295.8ms | 51.9× | 6/7 | 335.4ms | 39.6ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.7ms | 1.0× | 1/7 | 27.6ms | 21.9ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 14.2ms | 1.0× | 1/7 | 26.9ms | 12.7ms | 30.4 MB | 1/7 | 3388889 |
| clojure | 168.6ms | 11.9× | 7/7 | 520.2ms | 351.6ms | 168.9 MB | 6/7 | 3388889 |
| elixir | 122.0ms | 8.6× | 6/7 | 310.0ms | 188.0ms | 201.5 MB | 7/7 | 3388889 |
| python | 44.5ms | 3.1× | 3/7 | 54.9ms | 10.4ms | 40.0 MB | 2/7 | 3388889 |
| node | 66.7ms | 4.7× | 4/7 | 84.9ms | 18.2ms | 97.3 MB | 5/7 | 3388889 |
| ruby | 85.4ms | 6.0× | 5/7 | 125.0ms | 39.6ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.9ms | 2.2× | 2/7 | 53.8ms | 21.9ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.4ms | 1.1× | 2/7 | 47.1ms | 12.7ms | 24.7 MB | 3/7 | 374854840 |
| clojure | 281.5ms | 9.1× | 7/7 | 633.1ms | 351.6ms | 302.7 MB | 7/7 | 374854840 |
| elixir | 173.5ms | 5.6× | 5/7 | 361.5ms | 188.0ms | 72.3 MB | 6/7 | 374854840 |
| python | 179.0ms | 5.8× | 6/7 | 189.4ms | 10.4ms | 10.0 MB | 1/7 | 374854840 |
| node | 31.1ms | 1.0× | 1/7 | 49.3ms | 18.2ms | 52.3 MB | 5/7 | 374854840 |
| ruby | 72.3ms | 2.3× | 4/7 | 111.9ms | 39.6ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 38.0ms | 1.2× | 3/7 | 59.9ms | 21.9ms | 27.4 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.3ms | 6.8× | 6/7 | 118.0ms | 12.7ms | 53.7 MB | 4/7 | 1638200 |
| clojure | 165.4ms | 10.7× | 7/7 | 517.0ms | 351.6ms | 150.4 MB | 7/7 | 1638200 |
| elixir | 16.0ms | 1.0× | 2/7 | 204.0ms | 188.0ms | 73.3 MB | 6/7 | 1638200 |
| python | 101.1ms | 6.5× | 5/7 | 111.5ms | 10.4ms | 10.2 MB | 1/7 | 1638200 |
| node | 23.5ms | 1.5× | 3/7 | 41.7ms | 18.2ms | 58.2 MB | 5/7 | 1638200 |
| ruby | 100.4ms | 6.5× | 4/7 | 140.0ms | 39.6ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 15.5ms | 1.0× | 1/7 | 37.4ms | 21.9ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 140.1ms | 2.1× | 5/7 | 152.8ms | 12.7ms | 200.6 MB | 7/7 | 46468819 |
| clojure | 248.2ms | 3.8× | 7/7 | 599.8ms | 351.6ms | 123.5 MB | 5/7 | 46468819 |
| elixir | 119.3ms | 1.8× | 4/7 | 307.3ms | 188.0ms | 159.4 MB | 6/7 | 46468819 |
| python | 189.9ms | 2.9× | 6/7 | 200.3ms | 10.4ms | 25.9 MB | 2/7 | 46468819 |
| node | 109.1ms | 1.7× | 3/7 | 127.3ms | 18.2ms | 67.2 MB | 4/7 | 46468819 |
| ruby | 74.4ms | 1.1× | 2/7 | 114.0ms | 39.6ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 65.6ms | 1.0× | 1/7 | 87.5ms | 21.9ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.9ms | 22.3× | 5/7 | 97.6ms | 12.7ms | 44.1 MB | 4/7 | 724 |
| clojure | 210.7ms | 55.4× | 7/7 | 562.3ms | 351.6ms | 132.2 MB | 7/7 | 724 |
| elixir | 3.8ms | 1.0× | 1/7 | 191.8ms | 188.0ms | 71.6 MB | 6/7 | 724 |
| python | 55.3ms | 14.6× | 4/7 | 65.7ms | 10.4ms | 9.9 MB | 1/7 | 724 |
| node | 8.3ms | 2.2× | 2/7 | 26.5ms | 18.2ms | 52.9 MB | 5/7 | 724 |
| ruby | 130.6ms | 34.4× | 6/7 | 170.2ms | 39.6ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.9ms | 5.2× | 3/7 | 41.8ms | 21.9ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 1.7× | 2/7 | 55.8ms | 12.7ms | 23.6 MB | 3/7 | 9900000 |
| clojure | 1.115s | 44.3× | 7/7 | 1.467s | 351.6ms | 370.3 MB | 7/7 | 9900000 |
| elixir | 25.2ms | 1.0× | 1/7 | 213.2ms | 188.0ms | 73.4 MB | 6/7 | 9900000 |
| python | 48.9ms | 1.9× | 3/7 | 59.3ms | 10.4ms | 9.9 MB | 1/7 | 9900000 |
| node | 588.2ms | 23.3× | 6/7 | 606.4ms | 18.2ms | 52.5 MB | 5/7 | 9900000 |
| ruby | 116.2ms | 4.6× | 4/7 | 155.8ms | 39.6ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 300.2ms | 11.9× | 5/7 | 322.1ms | 21.9ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.7ms | 4.0× | 2/7 | 54.4ms | 12.7ms | 23.7 MB | 2/7 | 2475000 |
| clojure | 1.372s | 130.7× | 7/7 | 1.724s | 351.6ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 10.5ms | 1.0× | 1/7 | 198.5ms | 188.0ms | 72.7 MB | 6/7 | 2475000 |
| python | 236.3ms | 22.5× | 5/7 | 246.7ms | 10.4ms | 9.9 MB | 1/7 | 2475000 |
| node | 214.5ms | 20.4× | 4/7 | 232.7ms | 18.2ms | 52.4 MB | 5/7 | 2475000 |
| ruby | 116.7ms | 11.1× | 3/7 | 156.3ms | 39.6ms | 26.0 MB | 3/7 | 2475000 |
| dotnet | 692.2ms | 65.9× | 6/7 | 714.1ms | 21.9ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.3ms | 7.9× | 6/7 | 46.0ms | 12.7ms | 24.1 MB | 3/7 | 155553889038886 |
| clojure | 125.9ms | 30.0× | 7/7 | 477.5ms | 351.6ms | 108.1 MB | 7/7 | 155553889038886 |
| elixir | 5.2ms | 1.2× | 2/7 | 193.2ms | 188.0ms | 73.2 MB | 6/7 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/7 | 14.6ms | 10.4ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.0ms | 2.4× | 5/7 | 28.2ms | 18.2ms | 54.1 MB | 5/7 | 155553889038886 |
| ruby | 8.3ms | 2.0× | 4/7 | 47.9ms | 39.6ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.8ms | 1.9× | 3/7 | 29.7ms | 21.9ms | 28.1 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 359.1ms | 1.5× | 3/7 | 371.8ms | 12.7ms | 23.7 MB | 3/7 | 24558 |
| clojure | 543.4ms | 2.2× | 5/7 | 895.0ms | 351.6ms | 375.4 MB | 7/7 | 24558 |
| elixir | 286.8ms | 1.2× | 2/7 | 474.8ms | 188.0ms | 70.3 MB | 6/7 | 24558 |
| python | 3.993s | 16.2× | 7/7 | 4.003s | 10.4ms | 11.2 MB | 1/7 | 24558 |
| node | 407.5ms | 1.7× | 4/7 | 425.7ms | 18.2ms | 50.4 MB | 5/7 | 24558 |
| ruby | 1.823s | 7.4× | 6/7 | 1.863s | 39.6ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 246.5ms | 1.0× | 1/7 | 268.4ms | 21.9ms | 26.4 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.2ms | 8.9× | 3/7 | 43.9ms | 12.7ms | 31.3 MB | 4/7 | 78498 |
| clojure | 131.5ms | 37.6× | 7/7 | 483.1ms | 351.6ms | 107.4 MB | 7/7 | 78498 |
| elixir | 58.5ms | 16.7× | 4/7 | 246.5ms | 188.0ms | 77.8 MB | 6/7 | 78498 |
| python | 124.4ms | 35.5× | 6/7 | 134.8ms | 10.4ms | 10.9 MB | 1/7 | 78498 |
| node | 6.4ms | 1.8× | 2/7 | 24.6ms | 18.2ms | 51.5 MB | 5/7 | 78498 |
| ruby | 89.7ms | 25.6× | 5/7 | 129.3ms | 39.6ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 3.5ms | 1.0× | 1/7 | 25.4ms | 21.9ms | 27.5 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 61.2ms | 2.5× | 4/7 | 73.9ms | 12.7ms | 72.4 MB | 5/7 | 30039386344 |
| clojure | 300.8ms | 12.4× | 7/7 | 652.4ms | 351.6ms | 291.8 MB | 7/7 | 30039386344 |
| elixir | 126.9ms | 5.2× | 6/7 | 314.9ms | 188.0ms | 97.1 MB | 6/7 | 30039386344 |
| python | 94.2ms | 3.9× | 5/7 | 104.6ms | 10.4ms | 14.9 MB | 1/7 | 30039386344 |
| node | 24.2ms | 1.0× | 1/7 | 42.4ms | 18.2ms | 56.2 MB | 4/7 | 30039386344 |
| ruby | 41.5ms | 1.7× | 3/7 | 81.1ms | 39.6ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 24.2ms | 1.0× | 2/7 | 46.1ms | 21.9ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 330.0ms | 41.2× | 6/7 | 342.7ms | 12.7ms | 55.4 MB | 5/7 | -169078071 |
| clojure | 192.4ms | 24.0× | 4/7 | 544.0ms | 351.6ms | 109.9 MB | 7/7 | -169078071 |
| elixir | 145.5ms | 18.2× | 3/7 | 333.5ms | 188.0ms | 72.3 MB | 6/7 | -169078071 |
| python | 722.4ms | 90.3× | 7/7 | 732.8ms | 10.4ms | 10.4 MB | 1/7 | -169078071 |
| node | 15.9ms | 2.0× | 2/7 | 34.1ms | 18.2ms | 52.6 MB | 4/7 | -169078071 |
| ruby | 301.2ms | 37.6× | 5/7 | 340.8ms | 39.6ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 8.0ms | 1.0× | 1/7 | 29.9ms | 21.9ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.0ms | 79.5× | 6/7 | 163.7ms | 12.7ms | 71.7 MB | 5/7 | 1489952542 |
| clojure | 402.8ms | 212.0× | 7/7 | 754.4ms | 351.6ms | 172.0 MB | 7/7 | 1489952542 |
| elixir | 3.7ms | 1.9× | 2/7 | 191.7ms | 188.0ms | 75.1 MB | 6/7 | 1489952542 |
| python | 8.3ms | 4.4× | 4/7 | 18.7ms | 10.4ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.9ms | 1.0× | 1/7 | 20.1ms | 18.2ms | 46.0 MB | 4/7 | 1489952542 |
| ruby | 6.2ms | 3.3× | 3/7 | 45.8ms | 39.6ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 46.1ms | 24.3× | 5/7 | 68.0ms | 21.9ms | 34.2 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.6ms | 19.9× | 6/7 | 100.3ms | 12.7ms | 42.2 MB | 4/7 | 10000 |
| clojure | 132.4ms | 30.1× | 7/7 | 484.0ms | 351.6ms | 108.1 MB | 7/7 | 10000 |
| elixir | 13.6ms | 3.1× | 4/7 | 201.6ms | 188.0ms | 71.0 MB | 6/7 | 10000 |
| python | 13.4ms | 3.0× | 3/7 | 23.8ms | 10.4ms | 11.2 MB | 1/7 | 10000 |
| node | 4.4ms | 1.0× | 1/7 | 22.6ms | 18.2ms | 52.4 MB | 5/7 | 10000 |
| ruby | 8.7ms | 2.0× | 2/7 | 48.3ms | 39.6ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 14.2ms | 3.2× | 5/7 | 36.1ms | 21.9ms | 32.1 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.7ms | 21.6× | 6/7 | 114.4ms | 12.7ms | 92.1 MB | 6/7 | 12081249 |
| clojure | 165.3ms | 35.2× | 7/7 | 516.9ms | 351.6ms | 109.3 MB | 7/7 | 12081249 |
| elixir | 8.7ms | 1.9× | 4/7 | 196.7ms | 188.0ms | 79.5 MB | 5/7 | 12081249 |
| python | 13.2ms | 2.8× | 5/7 | 23.6ms | 10.4ms | 10.3 MB | 1/7 | 12081249 |
| node | 6.6ms | 1.4× | 2/7 | 24.8ms | 18.2ms | 53.3 MB | 4/7 | 12081249 |
| ruby | 8.5ms | 1.8× | 3/7 | 48.1ms | 39.6ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 4.7ms | 1.0× | 1/7 | 26.6ms | 21.9ms | 27.3 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.0ms | 2.6× | 3/7 | 58.7ms | 12.7ms | 46.0 MB | 3/7 | 6100000 |
| clojure | 190.5ms | 10.7× | 5/7 | 542.1ms | 351.6ms | 133.4 MB | 7/7 | 6100000 |
| elixir | 25.7ms | 1.4× | 2/7 | 213.7ms | 188.0ms | 77.6 MB | 5/7 | 6100000 |
| python | 559.3ms | 31.4× | 6/7 | 569.7ms | 10.4ms | 27.9 MB | 1/7 | 6100000 |
| node | 54.3ms | 3.1× | 4/7 | 72.5ms | 18.2ms | 53.5 MB | 4/7 | 6100000 |
| ruby | 1.594s | 89.6× | 7/7 | 1.634s | 39.6ms | 133.0 MB | 6/7 | 6100000 |
| dotnet | 17.8ms | 1.0× | 1/7 | 39.7ms | 21.9ms | 31.1 MB | 2/7 | 6100000 |

## spawn-live — hold N processes alive, then wake each  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.706s | 2.7× | 2/2 | 1.719s | 12.7ms | 1835.8 MB | 2/2 | 300000 |
| elixir | 631.9ms | 1.0× | 1/2 | 819.9ms | 188.0ms | 914.4 MB | 1/2 | 300000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 178.3ms | 1.6× | 2/7 | 191.0ms | 12.7ms | 27.0 MB | 3/7 | 134626900 |
| clojure | 369.2ms | 3.2× | 5/7 | 720.8ms | 351.6ms | 136.1 MB | 6/7 | 134626900 |
| elixir | 296.7ms | 2.6× | 4/7 | 484.7ms | 188.0ms | 72.8 MB | 5/7 | 134626900 |
| python | 2.501s | 21.8× | 7/7 | 2.511s | 10.4ms | 21.9 MB | 2/7 | 134626900 |
| node | 295.2ms | 2.6× | 3/7 | 313.4ms | 18.2ms | 185.6 MB | 7/7 | 134626900 |
| ruby | 1.850s | 16.1× | 6/7 | 1.889s | 39.6ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 114.7ms | 1.0× | 1/7 | 136.6ms | 21.9ms | 28.2 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.8ms | 1.3× | 3/7 | 177.5ms | 12.7ms | 87.1 MB | 5/7 | 500 |
| clojure | 805.5ms | 6.4× | 7/7 | 1.157s | 351.6ms | 292.2 MB | 6/7 | 500 |
| elixir | 574.2ms | 4.6× | 6/7 | 762.2ms | 188.0ms | 481.3 MB | 7/7 | 500 |
| python | 176.1ms | 1.4× | 4/7 | 186.5ms | 10.4ms | 43.6 MB | 1/7 | 500 |
| node | 125.9ms | 1.0× | 1/7 | 144.1ms | 18.2ms | 67.6 MB | 4/7 | 500 |
| ruby | 209.8ms | 1.7× | 5/7 | 249.4ms | 39.6ms | 46.1 MB | 2/7 | 500 |
| dotnet | 150.1ms | 1.2× | 2/7 | 172.0ms | 21.9ms | 47.7 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 201.7ms | 4.0× | 3/7 | 214.4ms | 12.7ms | 48.5 MB | 4/7 | 100000 |
| clojure | 588.1ms | 11.6× | 4/7 | 939.7ms | 351.6ms | 133.0 MB | 7/7 | 100000 |
| elixir | 50.9ms | 1.0× | 1/7 | 238.9ms | 188.0ms | 71.9 MB | 6/7 | 100000 |
| python | 814.3ms | 16.0× | 7/7 | 824.7ms | 10.4ms | 10.9 MB | 1/7 | 100000 |
| node | 644.1ms | 12.7× | 6/7 | 662.3ms | 18.2ms | 70.2 MB | 5/7 | 100000 |
| ruby | 608.3ms | 12.0× | 5/7 | 647.9ms | 39.6ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 164.5ms | 3.2× | 2/7 | 186.4ms | 21.9ms | 28.0 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 744.2ms | 5.8× | 3/7 | 756.9ms | 12.7ms | 72.8 MB | 6/7 | 1000000 |
| clojure | 4.396s | 34.3× | 6/7 | 4.748s | 351.6ms | 729.6 MB | 7/7 | 1000000 |
| elixir | 259.0ms | 2.0× | 2/7 | 447.0ms | 188.0ms | 70.2 MB | 5/7 | 1000000 |
| python | 4.703s | 36.7× | 7/7 | 4.714s | 10.4ms | 16.3 MB | 1/7 | 1000000 |
| node | 128.1ms | 1.0× | 1/7 | 146.3ms | 18.2ms | 67.5 MB | 4/7 | 1000000 |
| ruby | 3.447s | 26.9× | 5/7 | 3.487s | 39.6ms | 23.4 MB | 2/7 | 1000000 |
| dotnet | 839.4ms | 6.6× | 4/7 | 861.3ms | 21.9ms | 30.4 MB | 3/7 | 1000000 |
