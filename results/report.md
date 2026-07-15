# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-15 14:39.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.5ms | 3.1× | 4/7 | 31.5ms | — | 19.9 MB | 3/7 | 0 |
| clojure | 334.6ms | 32.5× | 7/7 | 334.6ms | — | 102.6 MB | 7/7 | 0 |
| elixir | 188.9ms | 18.3× | 6/7 | 188.9ms | — | 70.7 MB | 6/7 | 0 |
| python | 10.3ms | 1.0× | 1/7 | 10.3ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.7ms | 1.8× | 2/7 | 18.7ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.8× | 5/7 | 38.8ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 22.5ms | 2.2× | 3/7 | 22.5ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 57.3ms | 1.3× | 2/7 | 88.8ms | 31.5ms | 23.1 MB | 3/7 | 9227465 |
| clojure | 209.2ms | 4.8× | 5/7 | 543.8ms | 334.6ms | 108.1 MB | 7/7 | 9227465 |
| elixir | 67.7ms | 1.6× | 3/7 | 256.6ms | 188.9ms | 70.5 MB | 6/7 | 9227465 |
| python | 730.6ms | 16.8× | 7/7 | 740.9ms | 10.3ms | 9.8 MB | 1/7 | 9227465 |
| node | 71.8ms | 1.6× | 4/7 | 90.5ms | 18.7ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 593.8ms | 13.6× | 6/7 | 632.6ms | 38.8ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 43.6ms | 1.0× | 1/7 | 66.1ms | 22.5ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 279.6ms | 24.3× | 5/7 | 311.1ms | 31.5ms | 23.1 MB | 3/7 | 449999985000000 |
| clojure | 147.7ms | 12.8× | 4/7 | 482.3ms | 334.6ms | 108.2 MB | 7/7 | 449999985000000 |
| elixir | 43.2ms | 3.8× | 3/7 | 232.1ms | 188.9ms | 72.4 MB | 6/7 | 449999985000000 |
| python | 2.330s | 202.6× | 7/7 | 2.340s | 10.3ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.0ms | 2.5× | 2/7 | 47.7ms | 18.7ms | 49.9 MB | 5/7 | 449999985000000 |
| ruby | 590.4ms | 51.3× | 6/7 | 629.2ms | 38.8ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 11.5ms | 1.0× | 1/7 | 34.0ms | 22.5ms | 26.4 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.4ms | 1.0× | 1/7 | 34.9ms | 31.5ms | 19.8 MB | 3/7 | 12499997500000 |
| clojure | 174.2ms | 51.2× | 5/7 | 508.8ms | 334.6ms | 219.6 MB | 7/7 | 12499997500000 |
| elixir | 26.6ms | 7.8× | 3/7 | 215.5ms | 188.9ms | 70.5 MB | 5/7 | 12499997500000 |
| python | 104.9ms | 30.9× | 4/7 | 115.2ms | 10.3ms | 10.4 MB | 1/7 | 12499997500000 |
| node | 217.3ms | 63.9× | 6/7 | 236.0ms | 18.7ms | 90.1 MB | 6/7 | 12499997500000 |
| ruby | 223.2ms | 65.6× | 7/7 | 262.0ms | 38.8ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 11.4ms | 3.4× | 2/7 | 33.9ms | 22.5ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 48.9ms | 6.3× | 4/7 | 80.4ms | 31.5ms | 23.8 MB | 3/7 | 13848 |
| clojure | 142.5ms | 18.3× | 7/7 | 477.1ms | 334.6ms | 108.4 MB | 7/7 | 13848 |
| elixir | 8.2ms | 1.1× | 2/7 | 197.1ms | 188.9ms | 70.8 MB | 6/7 | 13848 |
| python | 122.6ms | 15.7× | 6/7 | 132.9ms | 10.3ms | 9.9 MB | 1/7 | 13848 |
| node | 7.8ms | 1.0× | 1/7 | 26.5ms | 18.7ms | 48.5 MB | 5/7 | 13848 |
| ruby | 117.3ms | 15.0× | 5/7 | 156.1ms | 38.8ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 8.5ms | 1.1× | 3/7 | 31.0ms | 22.5ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.3ms | 3.0× | 3/7 | 168.8ms | 31.5ms | 23.6 MB | 3/7 | 442 |
| clojure | 432.4ms | 9.4× | 5/7 | 767.0ms | 334.6ms | 370.7 MB | 7/7 | 442 |
| elixir | 96.6ms | 2.1× | 2/7 | 285.5ms | 188.9ms | 70.2 MB | 6/7 | 442 |
| python | 2.407s | 52.4× | 7/7 | 2.417s | 10.3ms | 9.8 MB | 1/7 | 442 |
| node | 172.0ms | 3.7× | 4/7 | 190.7ms | 18.7ms | 48.4 MB | 5/7 | 442 |
| ruby | 835.2ms | 18.2× | 6/7 | 874.0ms | 38.8ms | 19.1 MB | 2/7 | 442 |
| dotnet | 45.9ms | 1.0× | 1/7 | 68.4ms | 22.5ms | 26.4 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 253.0ms | 14.1× | 5/7 | 284.5ms | 31.5ms | 23.7 MB | 3/7 | 6129302 |
| clojure | 157.0ms | 8.7× | 3/7 | 491.6ms | 334.6ms | 115.8 MB | 7/7 | 6129302 |
| elixir | 249.8ms | 13.9× | 4/7 | 438.7ms | 188.9ms | 72.7 MB | 6/7 | 6129302 |
| python | 1.330s | 73.9× | 7/7 | 1.341s | 10.3ms | 9.9 MB | 1/7 | 6129302 |
| node | 20.2ms | 1.1× | 2/7 | 38.9ms | 18.7ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 410.3ms | 22.8× | 6/7 | 449.1ms | 38.8ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 18.0ms | 1.0× | 1/7 | 40.5ms | 22.5ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 130.1ms | 33.4× | 4/7 | 161.6ms | 31.5ms | 30.0 MB | 4/7 | 654353666 |
| clojure | 200.2ms | 51.3× | 5/7 | 534.8ms | 334.6ms | 118.7 MB | 7/7 | 654353666 |
| elixir | 54.8ms | 14.1× | 3/7 | 243.7ms | 188.9ms | 76.9 MB | 6/7 | 654353666 |
| python | 436.6ms | 111.9× | 7/7 | 446.9ms | 10.3ms | 10.3 MB | 1/7 | 654353666 |
| node | 14.9ms | 3.8× | 2/7 | 33.6ms | 18.7ms | 52.2 MB | 5/7 | 654353666 |
| ruby | 276.2ms | 70.8× | 6/7 | 315.0ms | 38.8ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 3.9ms | 1.0× | 1/7 | 26.4ms | 22.5ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.4ms | 1.0× | 1/7 | 43.9ms | 31.5ms | 30.1 MB | 1/7 | 3388889 |
| clojure | 174.5ms | 14.1× | 7/7 | 509.1ms | 334.6ms | 167.9 MB | 6/7 | 3388889 |
| elixir | 111.8ms | 9.0× | 6/7 | 300.7ms | 188.9ms | 199.8 MB | 7/7 | 3388889 |
| python | 44.0ms | 3.5× | 3/7 | 54.3ms | 10.3ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.1ms | 5.2× | 4/7 | 82.8ms | 18.7ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 81.7ms | 6.6× | 5/7 | 120.5ms | 38.8ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.4ms | 2.5× | 2/7 | 52.9ms | 22.5ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.3ms | 1.7× | 3/7 | 82.8ms | 31.5ms | 24.7 MB | 3/7 | 374854840 |
| clojure | 286.1ms | 9.4× | 7/7 | 620.7ms | 334.6ms | 301.9 MB | 7/7 | 374854840 |
| elixir | 149.5ms | 4.9× | 5/7 | 338.4ms | 188.9ms | 71.4 MB | 6/7 | 374854840 |
| python | 178.0ms | 5.8× | 6/7 | 188.3ms | 10.3ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.5ms | 1.0× | 1/7 | 49.2ms | 18.7ms | 50.1 MB | 5/7 | 374854840 |
| ruby | 69.7ms | 2.3× | 4/7 | 108.5ms | 38.8ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 36.7ms | 1.2× | 2/7 | 59.2ms | 22.5ms | 27.2 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 104.3ms | 32.6× | 6/7 | 135.8ms | 31.5ms | 47.7 MB | 4/7 | 1638200 |
| clojure | 171.7ms | 53.7× | 7/7 | 506.3ms | 334.6ms | 150.1 MB | 7/7 | 1638200 |
| elixir | 3.2ms | 1.0× | 1/7 | 192.1ms | 188.9ms | 69.7 MB | 6/7 | 1638200 |
| python | 95.9ms | 30.0× | 5/7 | 106.2ms | 10.3ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.6ms | 6.4× | 3/7 | 39.3ms | 18.7ms | 56.0 MB | 5/7 | 1638200 |
| ruby | 95.9ms | 30.0× | 4/7 | 134.7ms | 38.8ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 13.3ms | 4.2× | 2/7 | 35.8ms | 22.5ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 216.9ms | 3.2× | 6/7 | 248.4ms | 31.5ms | 183.6 MB | 7/7 | 46468819 |
| clojure | 258.1ms | 3.8× | 7/7 | 592.7ms | 334.6ms | 123.0 MB | 5/7 | 46468819 |
| elixir | 104.9ms | 1.5× | 4/7 | 293.8ms | 188.9ms | 159.1 MB | 6/7 | 46468819 |
| python | 184.8ms | 2.7× | 5/7 | 195.1ms | 10.3ms | 25.8 MB | 2/7 | 46468819 |
| node | 101.6ms | 1.5× | 3/7 | 120.3ms | 18.7ms | 64.8 MB | 4/7 | 46468819 |
| ruby | 71.9ms | 1.1× | 2/7 | 110.7ms | 38.8ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 68.4ms | 1.0× | 1/7 | 90.9ms | 22.5ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.2ms | 45.9× | 6/7 | 164.7ms | 31.5ms | 42.3 MB | 4/7 | 724 |
| clojure | 256.6ms | 88.5× | 7/7 | 591.2ms | 334.6ms | 132.4 MB | 7/7 | 724 |
| elixir | 2.9ms | 1.0× | 1/7 | 191.8ms | 188.9ms | 71.9 MB | 6/7 | 724 |
| python | 54.3ms | 18.7× | 4/7 | 64.6ms | 10.3ms | 9.8 MB | 1/7 | 724 |
| node | 6.3ms | 2.2× | 2/7 | 25.0ms | 18.7ms | 50.5 MB | 5/7 | 724 |
| ruby | 126.9ms | 43.8× | 5/7 | 165.7ms | 38.8ms | 19.4 MB | 2/7 | 724 |
| dotnet | 18.8ms | 6.5× | 3/7 | 41.3ms | 22.5ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.8ms | 2.4× | 2/7 | 70.3ms | 31.5ms | 23.9 MB | 3/7 | 9900000 |
| clojure | 1.102s | 68.9× | 7/7 | 1.437s | 334.6ms | 370.9 MB | 7/7 | 9900000 |
| elixir | 16.0ms | 1.0× | 1/7 | 204.9ms | 188.9ms | 70.2 MB | 6/7 | 9900000 |
| python | 48.3ms | 3.0× | 3/7 | 58.6ms | 10.3ms | 9.8 MB | 1/7 | 9900000 |
| node | 569.5ms | 35.6× | 6/7 | 588.2ms | 18.7ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 111.5ms | 7.0× | 4/7 | 150.3ms | 38.8ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 283.1ms | 17.7× | 5/7 | 305.6ms | 22.5ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.1ms | 40.1× | 2/7 | 71.6ms | 31.5ms | 23.5 MB | 2/7 | 2475000 |
| clojure | 1.322s | 1322.4× | 7/7 | 1.657s | 334.6ms | 374.6 MB | 7/7 | 2475000 |
| elixir | 0.1ms | < 1× | 1/7 | 189.0ms | 188.9ms | 70.2 MB | 6/7 | 2475000 |
| python | 236.6ms | 236.6× | 5/7 | 246.9ms | 10.3ms | 9.8 MB | 1/7 | 2475000 |
| node | 206.0ms | 206.0× | 4/7 | 224.7ms | 18.7ms | 50.1 MB | 5/7 | 2475000 |
| ruby | 115.9ms | 115.9× | 3/7 | 154.7ms | 38.8ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 665.7ms | 665.7× | 6/7 | 688.2ms | 22.5ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.3ms | 18.1× | 6/7 | 67.8ms | 31.5ms | 24.0 MB | 3/7 | 155553889038886 |
| clojure | 132.2ms | 66.1× | 7/7 | 466.8ms | 334.6ms | 108.4 MB | 7/7 | 155553889038886 |
| elixir | 2.0ms | 1.0× | 1/7 | 190.9ms | 188.9ms | 71.7 MB | 6/7 | 155553889038886 |
| python | 3.7ms | 1.8× | 2/7 | 14.0ms | 10.3ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 6.9ms | 3.5× | 4/7 | 25.6ms | 18.7ms | 51.9 MB | 5/7 | 155553889038886 |
| ruby | 7.3ms | 3.7× | 5/7 | 46.1ms | 38.8ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 6.8ms | 3.4× | 3/7 | 29.3ms | 22.5ms | 27.9 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 340.7ms | 1.4× | 3/7 | 372.2ms | 31.5ms | 23.8 MB | 3/7 | 24558 |
| clojure | 541.4ms | 2.2× | 5/7 | 876.0ms | 334.6ms | 374.7 MB | 7/7 | 24558 |
| elixir | 271.7ms | 1.1× | 2/7 | 460.6ms | 188.9ms | 73.0 MB | 6/7 | 24558 |
| python | 3.904s | 16.1× | 7/7 | 3.915s | 10.3ms | 11.0 MB | 1/7 | 24558 |
| node | 390.5ms | 1.6× | 4/7 | 409.2ms | 18.7ms | 48.3 MB | 5/7 | 24558 |
| ruby | 1.637s | 6.7× | 6/7 | 1.676s | 38.8ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 242.9ms | 1.0× | 1/7 | 265.4ms | 22.5ms | 26.1 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 122.3ms | 48.9× | 6/7 | 153.8ms | 31.5ms | 58.6 MB | 5/7 | 78498 |
| clojure | 143.4ms | 57.4× | 7/7 | 478.0ms | 334.6ms | 108.9 MB | 7/7 | 78498 |
| elixir | 48.0ms | 19.2× | 3/7 | 236.9ms | 188.9ms | 80.0 MB | 6/7 | 78498 |
| python | 117.3ms | 46.9× | 5/7 | 127.6ms | 10.3ms | 10.8 MB | 1/7 | 78498 |
| node | 6.2ms | 2.5× | 2/7 | 24.9ms | 18.7ms | 49.5 MB | 4/7 | 78498 |
| ruby | 83.5ms | 33.4× | 4/7 | 122.3ms | 38.8ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.5ms | 1.0× | 1/7 | 25.0ms | 22.5ms | 27.3 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.6ms | 4.8× | 5/7 | 137.1ms | 31.5ms | 75.3 MB | 5/7 | 30039386344 |
| clojure | 305.6ms | 14.0× | 7/7 | 640.2ms | 334.6ms | 291.9 MB | 7/7 | 30039386344 |
| elixir | 109.6ms | 5.0× | 6/7 | 298.5ms | 188.9ms | 97.2 MB | 6/7 | 30039386344 |
| python | 78.6ms | 3.6× | 4/7 | 88.9ms | 10.3ms | 14.8 MB | 1/7 | 30039386344 |
| node | 22.3ms | 1.0× | 2/7 | 41.0ms | 18.7ms | 53.9 MB | 4/7 | 30039386344 |
| ruby | 39.9ms | 1.8× | 3/7 | 78.7ms | 38.8ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 21.9ms | 1.0× | 1/7 | 44.4ms | 22.5ms | 30.3 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 719.7ms | 124.1× | 7/7 | 751.2ms | 31.5ms | 43.2 MB | 4/7 | -169078071 |
| clojure | 193.1ms | 33.3× | 4/7 | 527.7ms | 334.6ms | 109.2 MB | 7/7 | -169078071 |
| elixir | 133.1ms | 22.9× | 3/7 | 322.0ms | 188.9ms | 72.8 MB | 6/7 | -169078071 |
| python | 704.4ms | 121.4× | 6/7 | 714.7ms | 10.3ms | 10.3 MB | 1/7 | -169078071 |
| node | 13.2ms | 2.3× | 2/7 | 31.9ms | 18.7ms | 50.1 MB | 5/7 | -169078071 |
| ruby | 295.5ms | 50.9× | 5/7 | 334.3ms | 38.8ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 5.8ms | 1.0× | 1/7 | 28.3ms | 22.5ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 363.5ms | 302.9× | 6/7 | 395.0ms | 31.5ms | 100.6 MB | 6/7 | 1489952542 |
| clojure | 409.5ms | 341.3× | 7/7 | 744.1ms | 334.6ms | 165.2 MB | 7/7 | 1489952542 |
| elixir | 4.1ms | 3.4× | 2/7 | 193.0ms | 188.9ms | 74.1 MB | 5/7 | 1489952542 |
| python | 8.2ms | 6.8× | 4/7 | 18.5ms | 10.3ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.2ms | 1.0× | 1/7 | 19.9ms | 18.7ms | 43.9 MB | 4/7 | 1489952542 |
| ruby | 4.9ms | 4.1× | 3/7 | 43.7ms | 38.8ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 43.6ms | 36.3× | 5/7 | 66.1ms | 22.5ms | 34.0 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 548.5ms | 176.9× | 7/7 | 580.0ms | 31.5ms | 178.1 MB | 7/7 | 10000 |
| clojure | 141.3ms | 45.6× | 6/7 | 475.9ms | 334.6ms | 109.0 MB | 6/7 | 10000 |
| elixir | 10.5ms | 3.4× | 3/7 | 199.4ms | 188.9ms | 70.4 MB | 5/7 | 10000 |
| python | 12.6ms | 4.1× | 5/7 | 22.9ms | 10.3ms | 11.1 MB | 1/7 | 10000 |
| node | 3.1ms | 1.0× | 1/7 | 21.8ms | 18.7ms | 50.3 MB | 4/7 | 10000 |
| ruby | 7.9ms | 2.5× | 2/7 | 46.7ms | 38.8ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 11.0ms | 3.5× | 4/7 | 33.5ms | 22.5ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.9ms | 35.9× | 6/7 | 164.4ms | 31.5ms | 104.7 MB | 6/7 | 12081249 |
| clojure | 160.4ms | 43.4× | 7/7 | 495.0ms | 334.6ms | 110.1 MB | 7/7 | 12081249 |
| elixir | 3.8ms | 1.0× | 2/7 | 192.7ms | 188.9ms | 76.3 MB | 5/7 | 12081249 |
| python | 12.7ms | 3.4× | 5/7 | 23.0ms | 10.3ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.2ms | 1.4× | 3/7 | 23.9ms | 18.7ms | 50.8 MB | 4/7 | 12081249 |
| ruby | 8.9ms | 2.4× | 4/7 | 47.7ms | 38.8ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 3.7ms | 1.0× | 1/7 | 26.2ms | 22.5ms | 27.1 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.1ms | 2.9× | 3/7 | 81.6ms | 31.5ms | 52.7 MB | 4/7 | 6100000 |
| clojure | 180.6ms | 10.4× | 5/7 | 515.2ms | 334.6ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 19.5ms | 1.1× | 2/7 | 208.4ms | 188.9ms | 77.1 MB | 5/7 | 6100000 |
| python | 558.9ms | 32.3× | 6/7 | 569.2ms | 10.3ms | 27.8 MB | 1/7 | 6100000 |
| node | 51.7ms | 3.0× | 4/7 | 70.4ms | 18.7ms | 51.6 MB | 3/7 | 6100000 |
| ruby | 1.576s | 91.1× | 7/7 | 1.615s | 38.8ms | 133.2 MB | 6/7 | 6100000 |
| dotnet | 17.3ms | 1.0× | 1/7 | 39.8ms | 22.5ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 215.1ms | 1.9× | 2/7 | 246.6ms | 31.5ms | 26.0 MB | 3/7 | 134626900 |
| clojure | 406.1ms | 3.6× | 5/7 | 740.7ms | 334.6ms | 135.7 MB | 6/7 | 134626900 |
| elixir | 287.2ms | 2.6× | 3/7 | 476.1ms | 188.9ms | 71.2 MB | 5/7 | 134626900 |
| python | 2.524s | 22.6× | 7/7 | 2.535s | 10.3ms | 21.8 MB | 2/7 | 134626900 |
| node | 297.5ms | 2.7× | 4/7 | 316.2ms | 18.7ms | 181.3 MB | 7/7 | 134626900 |
| ruby | 1.940s | 17.4× | 6/7 | 1.979s | 38.8ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 111.5ms | 1.0× | 1/7 | 134.0ms | 22.5ms | 28.3 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 153.3ms | 1.3× | 3/7 | 184.8ms | 31.5ms | 106.3 MB | 5/7 | 500 |
| clojure | 820.2ms | 7.1× | 7/7 | 1.155s | 334.6ms | 283.4 MB | 6/7 | 500 |
| elixir | 587.1ms | 5.1× | 6/7 | 776.0ms | 188.9ms | 496.4 MB | 7/7 | 500 |
| python | 172.2ms | 1.5× | 4/7 | 182.5ms | 10.3ms | 45.0 MB | 1/7 | 500 |
| node | 115.4ms | 1.0× | 1/7 | 134.1ms | 18.7ms | 64.7 MB | 4/7 | 500 |
| ruby | 201.7ms | 1.7× | 5/7 | 240.5ms | 38.8ms | 45.9 MB | 2/7 | 500 |
| dotnet | 148.8ms | 1.3× | 2/7 | 171.3ms | 22.5ms | 47.8 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 249.6ms | 5.3× | 3/7 | 281.1ms | 31.5ms | 96.9 MB | 6/7 | 100000 |
| clojure | 612.1ms | 13.0× | 5/7 | 946.7ms | 334.6ms | 133.3 MB | 7/7 | 100000 |
| elixir | 47.2ms | 1.0× | 1/7 | 236.1ms | 188.9ms | 72.0 MB | 5/7 | 100000 |
| python | 831.9ms | 17.6× | 7/7 | 842.2ms | 10.3ms | 10.8 MB | 1/7 | 100000 |
| node | 637.5ms | 13.5× | 6/7 | 656.2ms | 18.7ms | 67.5 MB | 4/7 | 100000 |
| ruby | 578.3ms | 12.3× | 4/7 | 617.1ms | 38.8ms | 19.1 MB | 2/7 | 100000 |
| dotnet | 161.6ms | 3.4× | 2/7 | 184.1ms | 22.5ms | 27.9 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.318s | 10.8× | 4/7 | 1.349s | 31.5ms | 274.0 MB | 6/7 | 1000000 |
| clojure | 4.505s | 36.9× | 6/7 | 4.840s | 334.6ms | 769.4 MB | 7/7 | 1000000 |
| elixir | 248.8ms | 2.0× | 2/7 | 437.7ms | 188.9ms | 71.9 MB | 5/7 | 1000000 |
| python | 4.734s | 38.8× | 7/7 | 4.744s | 10.3ms | 16.1 MB | 1/7 | 1000000 |
| node | 122.1ms | 1.0× | 1/7 | 140.8ms | 18.7ms | 65.4 MB | 4/7 | 1000000 |
| ruby | 3.535s | 29.0× | 5/7 | 3.574s | 38.8ms | 23.0 MB | 2/7 | 1000000 |
| dotnet | 853.5ms | 7.0× | 3/7 | 876.0ms | 22.5ms | 30.4 MB | 3/7 | 1000000 |
