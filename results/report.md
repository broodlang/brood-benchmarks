# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-26 19:47.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.1ms | 1.1× | 2/7 | 11.1ms | — | 16.2 MB | 2/7 | 0 |
| clojure | 336.8ms | 33.0× | 7/7 | 336.8ms | — | 103.8 MB | 7/7 | 0 |
| elixir | 180.4ms | 17.7× | 6/7 | 180.4ms | — | 72.3 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.8 MB | 1/7 | 0 |
| node | 17.7ms | 1.7× | 3/7 | 17.7ms | — | 42.9 MB | 5/7 | 0 |
| ruby | 38.6ms | 3.8× | 5/7 | 38.6ms | — | 19.2 MB | 3/7 | 0 |
| dotnet | 22.0ms | 2.2× | 4/7 | 22.0ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.6ms | 1.3× | 2/7 | 67.7ms | 11.1ms | 19.6 MB | 3/7 | 9227465 |
| clojure | 196.0ms | 4.5× | 5/7 | 532.8ms | 336.8ms | 109.2 MB | 7/7 | 9227465 |
| elixir | 77.0ms | 1.8× | 4/7 | 257.4ms | 180.4ms | 70.1 MB | 6/7 | 9227465 |
| python | 750.4ms | 17.2× | 7/7 | 760.6ms | 10.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.9ms | 1.7× | 3/7 | 91.6ms | 17.7ms | 48.2 MB | 5/7 | 9227465 |
| ruby | 603.8ms | 13.8× | 6/7 | 642.4ms | 38.6ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 43.6ms | 1.0× | 1/7 | 65.6ms | 22.0ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.6ms | 3.6× | 3/7 | 48.7ms | 11.1ms | 20.0 MB | 3/7 | 449999985000000 |
| clojure | 143.2ms | 13.8× | 5/7 | 480.0ms | 336.8ms | 108.4 MB | 7/7 | 449999985000000 |
| elixir | 50.5ms | 4.9× | 4/7 | 230.9ms | 180.4ms | 71.7 MB | 6/7 | 449999985000000 |
| python | 2.554s | 245.5× | 7/7 | 2.564s | 10.2ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 30.4ms | 2.9× | 2/7 | 48.1ms | 17.7ms | 50.2 MB | 5/7 | 449999985000000 |
| ruby | 560.5ms | 53.9× | 6/7 | 599.1ms | 38.6ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 10.4ms | 1.0× | 1/7 | 32.4ms | 22.0ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.5ms | 1.0× | 1/7 | 14.6ms | 11.1ms | 16.2 MB | 2/7 | 12499997500000 |
| clojure | 178.0ms | 50.9× | 5/7 | 514.8ms | 336.8ms | 223.5 MB | 7/7 | 12499997500000 |
| elixir | 31.5ms | 9.0× | 3/7 | 211.9ms | 180.4ms | 72.0 MB | 5/7 | 12499997500000 |
| python | 105.5ms | 30.1× | 4/7 | 115.7ms | 10.2ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 218.3ms | 62.4× | 6/7 | 236.0ms | 17.7ms | 90.2 MB | 6/7 | 12499997500000 |
| ruby | 222.1ms | 63.5× | 7/7 | 260.7ms | 38.6ms | 19.2 MB | 3/7 | 12499997500000 |
| dotnet | 12.1ms | 3.5× | 2/7 | 34.1ms | 22.0ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.0ms | 5.2× | 4/7 | 55.1ms | 11.1ms | 20.9 MB | 3/7 | 13848 |
| clojure | 143.3ms | 17.1× | 7/7 | 480.1ms | 336.8ms | 109.8 MB | 7/7 | 13848 |
| elixir | 20.4ms | 2.4× | 3/7 | 200.8ms | 180.4ms | 71.6 MB | 6/7 | 13848 |
| python | 120.1ms | 14.3× | 6/7 | 130.3ms | 10.2ms | 9.9 MB | 1/7 | 13848 |
| node | 8.7ms | 1.0× | 2/7 | 26.4ms | 17.7ms | 48.7 MB | 5/7 | 13848 |
| ruby | 118.5ms | 14.1× | 5/7 | 157.1ms | 38.6ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.4ms | 1.0× | 1/7 | 30.4ms | 22.0ms | 26.4 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.0ms | 1.9× | 2/7 | 95.1ms | 11.1ms | 20.9 MB | 3/7 | 442 |
| clojure | 426.0ms | 9.4× | 5/7 | 762.8ms | 336.8ms | 371.1 MB | 7/7 | 442 |
| elixir | 105.3ms | 2.3× | 3/7 | 285.7ms | 180.4ms | 70.1 MB | 6/7 | 442 |
| python | 2.380s | 52.7× | 7/7 | 2.390s | 10.2ms | 9.8 MB | 1/7 | 442 |
| node | 172.3ms | 3.8× | 4/7 | 190.0ms | 17.7ms | 48.5 MB | 5/7 | 442 |
| ruby | 848.2ms | 18.8× | 6/7 | 886.8ms | 38.6ms | 19.2 MB | 2/7 | 442 |
| dotnet | 45.2ms | 1.0× | 1/7 | 67.2ms | 22.0ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 169.2ms | 9.5× | 4/7 | 180.3ms | 11.1ms | 21.3 MB | 3/7 | 6129302 |
| clojure | 155.1ms | 8.7× | 3/7 | 491.9ms | 336.8ms | 114.6 MB | 7/7 | 6129302 |
| elixir | 245.4ms | 13.7× | 5/7 | 425.8ms | 180.4ms | 72.2 MB | 6/7 | 6129302 |
| python | 1.277s | 71.3× | 7/7 | 1.287s | 10.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.4ms | 1.2× | 2/7 | 39.1ms | 17.7ms | 50.0 MB | 5/7 | 6129302 |
| ruby | 417.4ms | 23.3× | 6/7 | 456.0ms | 38.6ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 17.9ms | 1.0× | 1/7 | 39.9ms | 22.0ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 130.7ms | 29.7× | 4/7 | 141.8ms | 11.1ms | 39.6 MB | 4/7 | 654353666 |
| clojure | 187.0ms | 42.5× | 5/7 | 523.8ms | 336.8ms | 118.3 MB | 7/7 | 654353666 |
| elixir | 60.8ms | 13.8× | 3/7 | 241.2ms | 180.4ms | 77.8 MB | 6/7 | 654353666 |
| python | 434.2ms | 98.7× | 7/7 | 444.4ms | 10.2ms | 10.3 MB | 1/7 | 654353666 |
| node | 17.1ms | 3.9× | 2/7 | 34.8ms | 17.7ms | 52.1 MB | 5/7 | 654353666 |
| ruby | 275.4ms | 62.6× | 6/7 | 314.0ms | 38.6ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.4ms | 1.0× | 1/7 | 26.4ms | 22.0ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.7ms | 1.0× | 1/7 | 23.8ms | 11.1ms | 26.7 MB | 1/7 | 3388889 |
| clojure | 155.7ms | 12.3× | 7/7 | 492.5ms | 336.8ms | 167.6 MB | 6/7 | 3388889 |
| elixir | 120.4ms | 9.5× | 6/7 | 300.8ms | 180.4ms | 199.8 MB | 7/7 | 3388889 |
| python | 42.3ms | 3.3× | 3/7 | 52.5ms | 10.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.7ms | 5.1× | 4/7 | 82.4ms | 17.7ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 82.4ms | 6.5× | 5/7 | 121.0ms | 38.6ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 31.0ms | 2.4× | 2/7 | 53.0ms | 22.0ms | 56.7 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.2ms | 1.2× | 2/7 | 46.3ms | 11.1ms | 22.0 MB | 3/7 | 374854840 |
| clojure | 263.9ms | 8.9× | 7/7 | 600.7ms | 336.8ms | 302.2 MB | 7/7 | 374854840 |
| elixir | 155.7ms | 5.2× | 5/7 | 336.1ms | 180.4ms | 70.1 MB | 6/7 | 374854840 |
| python | 169.3ms | 5.7× | 6/7 | 179.5ms | 10.2ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.7ms | 1.0× | 1/7 | 47.4ms | 17.7ms | 50.2 MB | 5/7 | 374854840 |
| ruby | 69.1ms | 2.3× | 4/7 | 107.7ms | 38.6ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 35.8ms | 1.2× | 3/7 | 57.8ms | 22.0ms | 27.2 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.9ms | 8.7× | 6/7 | 114.0ms | 11.1ms | 46.9 MB | 4/7 | 1638200 |
| clojure | 167.5ms | 14.2× | 7/7 | 504.3ms | 336.8ms | 150.0 MB | 7/7 | 1638200 |
| elixir | 11.8ms | 1.0× | 1/7 | 192.2ms | 180.4ms | 72.7 MB | 6/7 | 1638200 |
| python | 94.4ms | 8.0× | 4/7 | 104.6ms | 10.2ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.5ms | 1.7× | 3/7 | 38.2ms | 17.7ms | 56.1 MB | 5/7 | 1638200 |
| ruby | 98.0ms | 8.3× | 5/7 | 136.6ms | 38.6ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 13.7ms | 1.2× | 2/7 | 35.7ms | 22.0ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.2ms | 3.3× | 6/7 | 222.3ms | 11.1ms | 185.2 MB | 7/7 | 46468819 |
| clojure | 243.0ms | 3.9× | 7/7 | 579.8ms | 336.8ms | 123.3 MB | 5/7 | 46468819 |
| elixir | 107.9ms | 1.7× | 4/7 | 288.3ms | 180.4ms | 159.4 MB | 6/7 | 46468819 |
| python | 182.4ms | 2.9× | 5/7 | 192.6ms | 10.2ms | 26.0 MB | 2/7 | 46468819 |
| node | 103.0ms | 1.6× | 3/7 | 120.7ms | 17.7ms | 64.9 MB | 4/7 | 46468819 |
| ruby | 70.4ms | 1.1× | 2/7 | 109.0ms | 38.6ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 63.1ms | 1.0× | 1/7 | 85.1ms | 22.0ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.2ms | 11.4× | 5/7 | 92.3ms | 11.1ms | 38.7 MB | 4/7 | 724 |
| clojure | 214.8ms | 30.3× | 7/7 | 551.6ms | 336.8ms | 133.1 MB | 7/7 | 724 |
| elixir | 7.9ms | 1.1× | 2/7 | 188.3ms | 180.4ms | 72.0 MB | 6/7 | 724 |
| python | 53.5ms | 7.5× | 4/7 | 63.7ms | 10.2ms | 9.8 MB | 1/7 | 724 |
| node | 7.1ms | 1.0× | 1/7 | 24.8ms | 17.7ms | 50.7 MB | 5/7 | 724 |
| ruby | 122.3ms | 17.2× | 6/7 | 160.9ms | 38.6ms | 19.4 MB | 2/7 | 724 |
| dotnet | 18.6ms | 2.6× | 3/7 | 40.6ms | 22.0ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.9ms | 2.2× | 2/7 | 57.0ms | 11.1ms | 20.6 MB | 2/7 | 9900000 |
| clojure | 1.077s | 52.0× | 7/7 | 1.413s | 336.8ms | 371.4 MB | 7/7 | 9900000 |
| elixir | 20.7ms | 1.0× | 1/7 | 201.1ms | 180.4ms | 69.8 MB | 6/7 | 9900000 |
| python | 49.1ms | 2.4× | 3/7 | 59.3ms | 10.2ms | 9.8 MB | 1/7 | 9900000 |
| node | 554.0ms | 26.8× | 6/7 | 571.7ms | 17.7ms | 50.2 MB | 5/7 | 9900000 |
| ruby | 109.2ms | 5.3× | 4/7 | 147.8ms | 38.6ms | 21.8 MB | 3/7 | 9900000 |
| dotnet | 288.1ms | 13.9× | 5/7 | 310.1ms | 22.0ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.5ms | 5.6× | 2/7 | 54.6ms | 11.1ms | 20.5 MB | 2/7 | 2475000 |
| clojure | 1.316s | 170.9× | 7/7 | 1.653s | 336.8ms | 374.5 MB | 7/7 | 2475000 |
| elixir | 7.7ms | 1.0× | 1/7 | 188.1ms | 180.4ms | 71.8 MB | 6/7 | 2475000 |
| python | 227.3ms | 29.5× | 5/7 | 237.5ms | 10.2ms | 9.9 MB | 1/7 | 2475000 |
| node | 207.3ms | 26.9× | 4/7 | 225.0ms | 17.7ms | 50.1 MB | 5/7 | 2475000 |
| ruby | 107.2ms | 13.9× | 3/7 | 145.8ms | 38.6ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 650.7ms | 84.5× | 6/7 | 672.7ms | 22.0ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.4ms | 7.8× | 6/7 | 42.5ms | 11.1ms | 20.9 MB | 3/7 | 155553889038886 |
| clojure | 122.9ms | 30.7× | 7/7 | 459.7ms | 336.8ms | 108.5 MB | 7/7 | 155553889038886 |
| elixir | 8.5ms | 2.1× | 5/7 | 188.9ms | 180.4ms | 70.7 MB | 6/7 | 155553889038886 |
| python | 4.0ms | 1.0× | 1/7 | 14.2ms | 10.2ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 8.3ms | 2.1× | 4/7 | 26.0ms | 17.7ms | 52.1 MB | 5/7 | 155553889038886 |
| ruby | 7.7ms | 1.9× | 3/7 | 46.3ms | 38.6ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 6.4ms | 1.6× | 2/7 | 28.4ms | 22.0ms | 27.9 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 341.9ms | 1.4× | 3/7 | 353.0ms | 11.1ms | 20.9 MB | 3/7 | 24558 |
| clojure | 548.8ms | 2.3× | 5/7 | 885.6ms | 336.8ms | 374.3 MB | 7/7 | 24558 |
| elixir | 286.6ms | 1.2× | 2/7 | 467.0ms | 180.4ms | 72.0 MB | 6/7 | 24558 |
| python | 3.805s | 15.7× | 7/7 | 3.816s | 10.2ms | 11.0 MB | 1/7 | 24558 |
| node | 391.2ms | 1.6× | 4/7 | 408.9ms | 17.7ms | 48.5 MB | 5/7 | 24558 |
| ruby | 1.634s | 6.7× | 6/7 | 1.673s | 38.6ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 242.1ms | 1.0× | 1/7 | 264.1ms | 22.0ms | 26.2 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.9ms | 13.4× | 3/7 | 46.0ms | 11.1ms | 28.6 MB | 4/7 | 78498 |
| clojure | 131.1ms | 50.4× | 7/7 | 467.9ms | 336.8ms | 108.6 MB | 7/7 | 78498 |
| elixir | 53.5ms | 20.6× | 4/7 | 233.9ms | 180.4ms | 78.7 MB | 6/7 | 78498 |
| python | 118.1ms | 45.4× | 6/7 | 128.3ms | 10.2ms | 10.8 MB | 1/7 | 78498 |
| node | 6.2ms | 2.4× | 2/7 | 23.9ms | 17.7ms | 49.6 MB | 5/7 | 78498 |
| ruby | 83.5ms | 32.1× | 5/7 | 122.1ms | 38.6ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.6ms | 1.0× | 1/7 | 24.6ms | 22.0ms | 27.4 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 61.0ms | 2.9× | 4/7 | 72.1ms | 11.1ms | 66.9 MB | 5/7 | 30039386344 |
| clojure | 285.1ms | 13.4× | 7/7 | 621.9ms | 336.8ms | 289.6 MB | 7/7 | 30039386344 |
| elixir | 113.9ms | 5.3× | 6/7 | 294.3ms | 180.4ms | 96.8 MB | 6/7 | 30039386344 |
| python | 80.0ms | 3.8× | 5/7 | 90.2ms | 10.2ms | 15.0 MB | 1/7 | 30039386344 |
| node | 23.2ms | 1.1× | 2/7 | 40.9ms | 17.7ms | 54.1 MB | 4/7 | 30039386344 |
| ruby | 39.9ms | 1.9× | 3/7 | 78.5ms | 38.6ms | 21.7 MB | 2/7 | 30039386344 |
| dotnet | 21.3ms | 1.0× | 1/7 | 43.3ms | 22.0ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 311.6ms | 52.8× | 6/7 | 322.7ms | 11.1ms | 51.3 MB | 5/7 | -169078071 |
| clojure | 181.1ms | 30.7× | 4/7 | 517.9ms | 336.8ms | 109.1 MB | 7/7 | -169078071 |
| elixir | 143.7ms | 24.4× | 3/7 | 324.1ms | 180.4ms | 70.2 MB | 6/7 | -169078071 |
| python | 693.7ms | 117.6× | 7/7 | 703.9ms | 10.2ms | 10.4 MB | 1/7 | -169078071 |
| node | 14.4ms | 2.4× | 2/7 | 32.1ms | 17.7ms | 50.6 MB | 4/7 | -169078071 |
| ruby | 290.8ms | 49.3× | 5/7 | 329.4ms | 38.6ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 5.9ms | 1.0× | 1/7 | 27.9ms | 22.0ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.2ms | 76.2× | 6/7 | 148.3ms | 11.1ms | 70.4 MB | 5/7 | 1489952542 |
| clojure | 378.8ms | 210.4× | 7/7 | 715.6ms | 336.8ms | 160.1 MB | 7/7 | 1489952542 |
| elixir | 3.9ms | 2.2× | 2/7 | 184.3ms | 180.4ms | 75.6 MB | 6/7 | 1489952542 |
| python | 7.9ms | 4.4× | 4/7 | 18.1ms | 10.2ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.8ms | 1.0× | 1/7 | 19.5ms | 17.7ms | 44.2 MB | 4/7 | 1489952542 |
| ruby | 5.4ms | 3.0× | 3/7 | 44.0ms | 38.6ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 41.3ms | 22.9× | 5/7 | 63.3ms | 22.0ms | 34.1 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.5ms | 22.3× | 6/7 | 93.6ms | 11.1ms | 38.2 MB | 4/7 | 10000 |
| clojure | 130.1ms | 35.2× | 7/7 | 466.9ms | 336.8ms | 108.6 MB | 7/7 | 10000 |
| elixir | 14.2ms | 3.8× | 5/7 | 194.6ms | 180.4ms | 72.4 MB | 6/7 | 10000 |
| python | 12.9ms | 3.5× | 4/7 | 23.1ms | 10.2ms | 11.1 MB | 1/7 | 10000 |
| node | 3.7ms | 1.0× | 1/7 | 21.4ms | 17.7ms | 50.4 MB | 5/7 | 10000 |
| ruby | 8.0ms | 2.2× | 2/7 | 46.6ms | 38.6ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 11.2ms | 3.0× | 3/7 | 33.2ms | 22.0ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.9ms | 28.1× | 6/7 | 115.0ms | 11.1ms | 95.2 MB | 6/7 | 12081249 |
| clojure | 155.1ms | 41.9× | 7/7 | 491.9ms | 336.8ms | 108.4 MB | 7/7 | 12081249 |
| elixir | 9.3ms | 2.5× | 4/7 | 189.7ms | 180.4ms | 76.8 MB | 5/7 | 12081249 |
| python | 12.4ms | 3.4× | 5/7 | 22.6ms | 10.2ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.4ms | 1.5× | 2/7 | 23.1ms | 17.7ms | 51.0 MB | 4/7 | 12081249 |
| ruby | 8.1ms | 2.2× | 3/7 | 46.7ms | 38.6ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 3.7ms | 1.0× | 1/7 | 25.7ms | 22.0ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.5ms | 2.9× | 3/7 | 56.6ms | 11.1ms | 40.4 MB | 3/7 | 6100000 |
| clojure | 182.4ms | 11.5× | 5/7 | 519.2ms | 336.8ms | 134.6 MB | 7/7 | 6100000 |
| elixir | 22.1ms | 1.4× | 2/7 | 202.5ms | 180.4ms | 76.5 MB | 5/7 | 6100000 |
| python | 549.3ms | 34.8× | 6/7 | 559.5ms | 10.2ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.5ms | 3.3× | 4/7 | 70.2ms | 17.7ms | 51.7 MB | 4/7 | 6100000 |
| ruby | 1.564s | 99.0× | 7/7 | 1.603s | 38.6ms | 133.3 MB | 6/7 | 6100000 |
| dotnet | 15.8ms | 1.0× | 1/7 | 37.8ms | 22.0ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 163.7ms | 1.5× | 2/7 | 174.8ms | 11.1ms | 22.7 MB | 3/7 | 134626900 |
| clojure | 368.2ms | 3.4× | 5/7 | 705.0ms | 336.8ms | 137.2 MB | 6/7 | 134626900 |
| elixir | 311.2ms | 2.9× | 4/7 | 491.6ms | 180.4ms | 71.1 MB | 5/7 | 134626900 |
| python | 2.396s | 22.4× | 7/7 | 2.406s | 10.2ms | 22.0 MB | 2/7 | 134626900 |
| node | 284.5ms | 2.7× | 3/7 | 302.2ms | 17.7ms | 181.8 MB | 7/7 | 134626900 |
| ruby | 1.779s | 16.6× | 6/7 | 1.817s | 38.6ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 107.2ms | 1.0× | 1/7 | 129.2ms | 22.0ms | 28.1 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 161.8ms | 1.4× | 3/7 | 172.9ms | 11.1ms | 79.8 MB | 5/7 | 500 |
| clojure | 777.9ms | 6.7× | 7/7 | 1.115s | 336.8ms | 280.6 MB | 6/7 | 500 |
| elixir | 559.7ms | 4.8× | 6/7 | 740.1ms | 180.4ms | 472.6 MB | 7/7 | 500 |
| python | 171.4ms | 1.5× | 4/7 | 181.6ms | 10.2ms | 44.5 MB | 1/7 | 500 |
| node | 116.5ms | 1.0× | 1/7 | 134.2ms | 17.7ms | 65.2 MB | 4/7 | 500 |
| ruby | 203.0ms | 1.7× | 5/7 | 241.6ms | 38.6ms | 45.6 MB | 2/7 | 500 |
| dotnet | 150.4ms | 1.3× | 2/7 | 172.4ms | 22.0ms | 48.3 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 180.7ms | 3.5× | 3/7 | 191.8ms | 11.1ms | 41.1 MB | 4/7 | 100000 |
| clojure | 560.6ms | 11.0× | 5/7 | 897.4ms | 336.8ms | 133.4 MB | 7/7 | 100000 |
| elixir | 51.0ms | 1.0× | 1/7 | 231.4ms | 180.4ms | 71.8 MB | 6/7 | 100000 |
| python | 802.2ms | 15.7× | 7/7 | 812.4ms | 10.2ms | 10.9 MB | 1/7 | 100000 |
| node | 643.6ms | 12.6× | 6/7 | 661.3ms | 17.7ms | 67.2 MB | 5/7 | 100000 |
| ruby | 553.1ms | 10.8× | 4/7 | 591.7ms | 38.6ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 160.5ms | 3.1× | 2/7 | 182.5ms | 22.0ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 701.3ms | 6.2× | 3/7 | 712.4ms | 11.1ms | 91.1 MB | 6/7 | 1000000 |
| clojure | 4.419s | 38.8× | 6/7 | 4.756s | 336.8ms | 762.4 MB | 7/7 | 1000000 |
| elixir | 257.4ms | 2.3× | 2/7 | 437.8ms | 180.4ms | 72.5 MB | 5/7 | 1000000 |
| python | 4.678s | 41.1× | 7/7 | 4.688s | 10.2ms | 16.1 MB | 1/7 | 1000000 |
| node | 113.9ms | 1.0× | 1/7 | 131.6ms | 17.7ms | 65.6 MB | 4/7 | 1000000 |
| ruby | 3.457s | 30.3× | 5/7 | 3.495s | 38.6ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 746.0ms | 6.5× | 4/7 | 768.0ms | 22.0ms | 30.4 MB | 3/7 | 1000000 |
