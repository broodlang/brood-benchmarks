# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-19 07:25.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.7ms | 3.3× | 4/7 | 35.7ms | — | 25.8 MB | 3/7 | 0 |
| clojure | 354.0ms | 32.5× | 7/7 | 354.0ms | — | 102.0 MB | 7/7 | 0 |
| elixir | 189.9ms | 17.4× | 6/7 | 189.9ms | — | 70.0 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.5ms | 1.7× | 2/7 | 18.5ms | — | 44.7 MB | 5/7 | 0 |
| ruby | 40.2ms | 3.7× | 5/7 | 40.2ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.7ms | 2.0× | 3/7 | 21.7ms | — | 26.1 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 57.8ms | 1.2× | 2/7 | 93.5ms | 35.7ms | 29.4 MB | 4/7 | 9227465 |
| clojure | 233.6ms | 4.9× | 5/7 | 587.6ms | 354.0ms | 108.9 MB | 7/7 | 9227465 |
| elixir | 84.0ms | 1.8× | 4/7 | 273.9ms | 189.9ms | 72.3 MB | 6/7 | 9227465 |
| python | 772.3ms | 16.3× | 7/7 | 783.2ms | 10.9ms | 10.0 MB | 1/7 | 9227465 |
| node | 81.9ms | 1.7× | 3/7 | 100.4ms | 18.5ms | 50.4 MB | 5/7 | 9227465 |
| ruby | 657.9ms | 13.9× | 6/7 | 698.1ms | 40.2ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 47.3ms | 1.0× | 1/7 | 69.0ms | 21.7ms | 26.0 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.6ms | 2.9× | 3/7 | 76.3ms | 35.7ms | 29.8 MB | 4/7 | 449999985000000 |
| clojure | 166.0ms | 12.0× | 5/7 | 520.0ms | 354.0ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 49.0ms | 3.6× | 4/7 | 238.9ms | 189.9ms | 70.7 MB | 6/7 | 449999985000000 |
| python | 2.495s | 180.8× | 7/7 | 2.506s | 10.9ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 30.6ms | 2.2× | 2/7 | 49.1ms | 18.5ms | 52.1 MB | 5/7 | 449999985000000 |
| ruby | 621.1ms | 45.0× | 6/7 | 661.3ms | 40.2ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 13.8ms | 1.0× | 1/7 | 35.5ms | 21.7ms | 26.5 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.3ms | 1.0× | 1/7 | 40.0ms | 35.7ms | 25.8 MB | 3/7 | 12499997500000 |
| clojure | 180.7ms | 42.0× | 5/7 | 534.7ms | 354.0ms | 222.1 MB | 7/7 | 12499997500000 |
| elixir | 32.4ms | 7.5× | 3/7 | 222.3ms | 189.9ms | 71.5 MB | 5/7 | 12499997500000 |
| python | 107.8ms | 25.1× | 4/7 | 118.7ms | 10.9ms | 10.7 MB | 1/7 | 12499997500000 |
| node | 232.4ms | 54.0× | 6/7 | 250.9ms | 18.5ms | 92.2 MB | 6/7 | 12499997500000 |
| ruby | 240.2ms | 55.9× | 7/7 | 280.4ms | 40.2ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 11.9ms | 2.8× | 2/7 | 33.6ms | 21.7ms | 27.8 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.6ms | 4.9× | 4/7 | 83.3ms | 35.7ms | 30.1 MB | 4/7 | 13848 |
| clojure | 164.6ms | 17.0× | 7/7 | 518.6ms | 354.0ms | 109.5 MB | 7/7 | 13848 |
| elixir | 24.5ms | 2.5× | 3/7 | 214.4ms | 189.9ms | 72.1 MB | 6/7 | 13848 |
| python | 130.4ms | 13.4× | 6/7 | 141.3ms | 10.9ms | 10.1 MB | 1/7 | 13848 |
| node | 10.5ms | 1.1× | 2/7 | 29.0ms | 18.5ms | 50.9 MB | 5/7 | 13848 |
| ruby | 121.7ms | 12.5× | 5/7 | 161.9ms | 40.2ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 9.7ms | 1.0× | 1/7 | 31.4ms | 21.7ms | 26.6 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.4ms | 1.9× | 2/7 | 126.1ms | 35.7ms | 29.8 MB | 4/7 | 442 |
| clojure | 463.6ms | 9.5× | 5/7 | 817.6ms | 354.0ms | 370.8 MB | 7/7 | 442 |
| elixir | 109.6ms | 2.2× | 3/7 | 299.5ms | 189.9ms | 70.3 MB | 6/7 | 442 |
| python | 2.547s | 52.2× | 7/7 | 2.558s | 10.9ms | 9.9 MB | 1/7 | 442 |
| node | 180.5ms | 3.7× | 4/7 | 199.0ms | 18.5ms | 50.5 MB | 5/7 | 442 |
| ruby | 878.1ms | 18.0× | 6/7 | 918.3ms | 40.2ms | 19.3 MB | 2/7 | 442 |
| dotnet | 48.8ms | 1.0× | 1/7 | 70.5ms | 21.7ms | 26.5 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 183.4ms | 8.8× | 3/7 | 219.1ms | 35.7ms | 30.1 MB | 4/7 | 6129302 |
| clojure | 186.5ms | 8.9× | 4/7 | 540.5ms | 354.0ms | 115.2 MB | 7/7 | 6129302 |
| elixir | 303.7ms | 14.5× | 5/7 | 493.6ms | 189.9ms | 72.0 MB | 6/7 | 6129302 |
| python | 1.552s | 74.2× | 7/7 | 1.562s | 10.9ms | 10.1 MB | 1/7 | 6129302 |
| node | 22.2ms | 1.1× | 2/7 | 40.7ms | 18.5ms | 52.1 MB | 5/7 | 6129302 |
| ruby | 424.7ms | 20.3× | 6/7 | 464.9ms | 40.2ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 20.9ms | 1.0× | 1/7 | 42.6ms | 21.7ms | 26.5 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 142.2ms | 22.2× | 4/7 | 177.9ms | 35.7ms | 47.2 MB | 4/7 | 654353666 |
| clojure | 201.5ms | 31.5× | 5/7 | 555.5ms | 354.0ms | 118.5 MB | 7/7 | 654353666 |
| elixir | 71.9ms | 11.2× | 3/7 | 261.8ms | 189.9ms | 75.3 MB | 6/7 | 654353666 |
| python | 457.6ms | 71.5× | 7/7 | 468.5ms | 10.9ms | 10.4 MB | 1/7 | 654353666 |
| node | 17.5ms | 2.7× | 2/7 | 36.0ms | 18.5ms | 54.2 MB | 5/7 | 654353666 |
| ruby | 309.3ms | 48.3× | 6/7 | 349.5ms | 40.2ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 6.4ms | 1.0× | 1/7 | 28.1ms | 21.7ms | 26.9 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 14.8ms | 1.0× | 1/7 | 50.5ms | 35.7ms | 35.7 MB | 1/7 | 3388889 |
| clojure | 210.2ms | 14.2× | 7/7 | 564.2ms | 354.0ms | 170.4 MB | 6/7 | 3388889 |
| elixir | 125.6ms | 8.5× | 6/7 | 315.5ms | 189.9ms | 202.9 MB | 7/7 | 3388889 |
| python | 45.5ms | 3.1× | 3/7 | 56.4ms | 10.9ms | 40.0 MB | 2/7 | 3388889 |
| node | 67.3ms | 4.5× | 4/7 | 85.8ms | 18.5ms | 97.5 MB | 5/7 | 3388889 |
| ruby | 87.1ms | 5.9× | 5/7 | 127.3ms | 40.2ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 35.4ms | 2.4× | 2/7 | 57.1ms | 21.7ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.3ms | 1.1× | 2/7 | 72.0ms | 35.7ms | 30.9 MB | 4/7 | 374854840 |
| clojure | 276.2ms | 8.6× | 7/7 | 630.2ms | 354.0ms | 301.5 MB | 7/7 | 374854840 |
| elixir | 177.9ms | 5.6× | 5/7 | 367.8ms | 189.9ms | 73.0 MB | 6/7 | 374854840 |
| python | 181.8ms | 5.7× | 6/7 | 192.7ms | 10.9ms | 10.1 MB | 1/7 | 374854840 |
| node | 32.0ms | 1.0× | 1/7 | 50.5ms | 18.5ms | 52.3 MB | 5/7 | 374854840 |
| ruby | 69.7ms | 2.2× | 4/7 | 109.9ms | 40.2ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 38.7ms | 1.2× | 3/7 | 60.4ms | 21.7ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 100.0ms | 13.9× | 6/7 | 135.7ms | 35.7ms | 55.7 MB | 4/7 | 1638200 |
| clojure | 157.0ms | 21.8× | 7/7 | 511.0ms | 354.0ms | 150.6 MB | 7/7 | 1638200 |
| elixir | 7.2ms | 1.0× | 1/7 | 197.1ms | 189.9ms | 70.2 MB | 6/7 | 1638200 |
| python | 95.1ms | 13.2× | 4/7 | 106.0ms | 10.9ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.3ms | 3.0× | 3/7 | 39.8ms | 18.5ms | 58.4 MB | 5/7 | 1638200 |
| ruby | 96.8ms | 13.4× | 5/7 | 137.0ms | 40.2ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 14.6ms | 2.0× | 2/7 | 36.3ms | 21.7ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.9ms | 3.3× | 6/7 | 247.6ms | 35.7ms | 192.6 MB | 7/7 | 46468819 |
| clojure | 243.6ms | 3.8× | 7/7 | 597.6ms | 354.0ms | 123.2 MB | 5/7 | 46468819 |
| elixir | 105.1ms | 1.6× | 4/7 | 295.0ms | 189.9ms | 157.7 MB | 6/7 | 46468819 |
| python | 186.5ms | 2.9× | 5/7 | 197.4ms | 10.9ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.7ms | 1.6× | 3/7 | 122.2ms | 18.5ms | 67.2 MB | 4/7 | 46468819 |
| ruby | 70.9ms | 1.1× | 2/7 | 111.1ms | 40.2ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 63.8ms | 1.0× | 1/7 | 85.5ms | 21.7ms | 29.9 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.7ms | 21.8× | 5/7 | 116.4ms | 35.7ms | 46.7 MB | 4/7 | 724 |
| clojure | 221.7ms | 59.9× | 7/7 | 575.7ms | 354.0ms | 136.5 MB | 7/7 | 724 |
| elixir | 3.7ms | 1.0× | 1/7 | 193.6ms | 189.9ms | 70.2 MB | 6/7 | 724 |
| python | 54.0ms | 14.6× | 4/7 | 64.9ms | 10.9ms | 10.0 MB | 1/7 | 724 |
| node | 6.5ms | 1.8× | 2/7 | 25.0ms | 18.5ms | 52.9 MB | 5/7 | 724 |
| ruby | 124.6ms | 33.7× | 6/7 | 164.8ms | 40.2ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.2ms | 5.5× | 3/7 | 41.9ms | 21.7ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.4ms | 2.1× | 3/7 | 87.1ms | 35.7ms | 29.8 MB | 3/7 | 9900000 |
| clojure | 1.084s | 43.9× | 7/7 | 1.438s | 354.0ms | 371.3 MB | 7/7 | 9900000 |
| elixir | 24.7ms | 1.0× | 1/7 | 214.6ms | 189.9ms | 71.1 MB | 6/7 | 9900000 |
| python | 47.8ms | 1.9× | 2/7 | 58.7ms | 10.9ms | 9.9 MB | 1/7 | 9900000 |
| node | 563.2ms | 22.8× | 6/7 | 581.7ms | 18.5ms | 52.5 MB | 5/7 | 9900000 |
| ruby | 108.9ms | 4.4× | 4/7 | 149.1ms | 40.2ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 295.3ms | 12.0× | 5/7 | 317.0ms | 21.7ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.5ms | 5.6× | 2/7 | 79.2ms | 35.7ms | 30.0 MB | 3/7 | 2475000 |
| clojure | 1.306s | 169.7× | 7/7 | 1.661s | 354.0ms | 374.6 MB | 7/7 | 2475000 |
| elixir | 7.7ms | 1.0× | 1/7 | 197.6ms | 189.9ms | 72.8 MB | 6/7 | 2475000 |
| python | 232.2ms | 30.2× | 5/7 | 243.1ms | 10.9ms | 10.0 MB | 1/7 | 2475000 |
| node | 207.6ms | 27.0× | 4/7 | 226.1ms | 18.5ms | 52.5 MB | 5/7 | 2475000 |
| ruby | 109.3ms | 14.2× | 3/7 | 149.5ms | 40.2ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 668.5ms | 86.8× | 6/7 | 690.2ms | 21.7ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 9.4× | 6/7 | 66.6ms | 35.7ms | 30.0 MB | 4/7 | 155553889038886 |
| clojure | 118.8ms | 36.0× | 7/7 | 472.8ms | 354.0ms | 109.3 MB | 7/7 | 155553889038886 |
| elixir | 7.3ms | 2.2× | 3/7 | 197.2ms | 189.9ms | 70.8 MB | 6/7 | 155553889038886 |
| python | 3.3ms | 1.0× | 1/7 | 14.2ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 8.0ms | 2.4× | 5/7 | 26.5ms | 18.5ms | 54.1 MB | 5/7 | 155553889038886 |
| ruby | 6.0ms | 1.8× | 2/7 | 46.2ms | 40.2ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.4ms | 2.2× | 4/7 | 29.1ms | 21.7ms | 28.1 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 342.3ms | 1.4× | 3/7 | 378.0ms | 35.7ms | 30.2 MB | 4/7 | 24558 |
| clojure | 520.7ms | 2.1× | 5/7 | 874.7ms | 354.0ms | 375.0 MB | 7/7 | 24558 |
| elixir | 284.8ms | 1.2× | 2/7 | 474.7ms | 189.9ms | 70.3 MB | 6/7 | 24558 |
| python | 3.878s | 15.9× | 7/7 | 3.889s | 10.9ms | 11.1 MB | 1/7 | 24558 |
| node | 394.7ms | 1.6× | 4/7 | 413.2ms | 18.5ms | 50.6 MB | 5/7 | 24558 |
| ruby | 1.646s | 6.7× | 6/7 | 1.686s | 40.2ms | 19.8 MB | 2/7 | 24558 |
| dotnet | 243.9ms | 1.0× | 1/7 | 265.6ms | 21.7ms | 26.4 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 2.8× | 3/7 | 71.8ms | 35.7ms | 37.6 MB | 4/7 | 78498 |
| clojure | 183.9ms | 14.0× | 5/7 | 537.9ms | 354.0ms | 109.1 MB | 7/7 | 78498 |
| elixir | 226.4ms | 17.3× | 7/7 | 416.3ms | 189.9ms | 78.9 MB | 6/7 | 78498 |
| python | 173.7ms | 13.3× | 4/7 | 184.6ms | 10.9ms | 10.9 MB | 1/7 | 78498 |
| node | 13.1ms | 1.0× | 1/7 | 31.6ms | 18.5ms | 51.7 MB | 5/7 | 78498 |
| ruby | 199.9ms | 15.3× | 6/7 | 240.1ms | 40.2ms | 26.9 MB | 2/7 | 78498 |
| dotnet | 18.1ms | 1.4× | 2/7 | 39.8ms | 21.7ms | 27.8 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.3ms | 3.3× | 4/7 | 124.0ms | 35.7ms | 78.1 MB | 5/7 | 30039386344 |
| clojure | 389.8ms | 14.5× | 6/7 | 743.8ms | 354.0ms | 291.4 MB | 7/7 | 30039386344 |
| elixir | 570.9ms | 21.3× | 7/7 | 760.8ms | 189.9ms | 98.5 MB | 6/7 | 30039386344 |
| python | 352.7ms | 13.2× | 5/7 | 363.6ms | 10.9ms | 14.9 MB | 1/7 | 30039386344 |
| node | 76.0ms | 2.8× | 3/7 | 94.5ms | 18.5ms | 56.3 MB | 4/7 | 30039386344 |
| ruby | 74.8ms | 2.8× | 2/7 | 115.0ms | 40.2ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 26.8ms | 1.0× | 1/7 | 48.5ms | 21.7ms | 30.6 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 420.3ms | 26.1× | 6/7 | 456.0ms | 35.7ms | 59.8 MB | 5/7 | -169078071 |
| clojure | 220.5ms | 13.7× | 4/7 | 574.5ms | 354.0ms | 109.4 MB | 7/7 | -169078071 |
| elixir | 162.2ms | 10.1× | 3/7 | 352.1ms | 189.9ms | 70.4 MB | 6/7 | -169078071 |
| python | 820.4ms | 51.0× | 7/7 | 831.3ms | 10.9ms | 10.4 MB | 1/7 | -169078071 |
| node | 16.1ms | 1.0× | 1/7 | 34.6ms | 18.5ms | 52.6 MB | 4/7 | -169078071 |
| ruby | 331.4ms | 20.6× | 5/7 | 371.6ms | 40.2ms | 19.3 MB | 2/7 | -169078071 |
| dotnet | 25.6ms | 1.6× | 2/7 | 47.3ms | 21.7ms | 27.2 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 163.2ms | 96.0× | 6/7 | 198.9ms | 35.7ms | 79.7 MB | 6/7 | 1489952542 |
| clojure | 475.7ms | 279.8× | 7/7 | 829.7ms | 354.0ms | 165.3 MB | 7/7 | 1489952542 |
| elixir | 2.3ms | 1.4× | 2/7 | 192.2ms | 189.9ms | 74.8 MB | 5/7 | 1489952542 |
| python | 9.0ms | 5.3× | 4/7 | 19.9ms | 10.9ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.7ms | 1.0× | 1/7 | 20.2ms | 18.5ms | 45.9 MB | 4/7 | 1489952542 |
| ruby | 6.0ms | 3.5× | 3/7 | 46.2ms | 40.2ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 48.0ms | 28.2× | 5/7 | 69.7ms | 21.7ms | 34.5 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.7ms | 19.4× | 6/7 | 115.4ms | 35.7ms | 43.8 MB | 4/7 | 10000 |
| clojure | 146.2ms | 35.7× | 7/7 | 500.2ms | 354.0ms | 108.9 MB | 7/7 | 10000 |
| elixir | 19.4ms | 4.7× | 5/7 | 209.3ms | 189.9ms | 70.3 MB | 6/7 | 10000 |
| python | 13.4ms | 3.3× | 4/7 | 24.3ms | 10.9ms | 11.2 MB | 1/7 | 10000 |
| node | 4.1ms | 1.0× | 1/7 | 22.6ms | 18.5ms | 52.6 MB | 5/7 | 10000 |
| ruby | 8.5ms | 2.1× | 2/7 | 48.7ms | 40.2ms | 19.5 MB | 2/7 | 10000 |
| dotnet | 12.0ms | 2.9× | 3/7 | 33.7ms | 21.7ms | 32.0 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.7ms | 21.1× | 6/7 | 145.4ms | 35.7ms | 99.8 MB | 6/7 | 12081249 |
| clojure | 175.8ms | 33.8× | 7/7 | 529.8ms | 354.0ms | 108.2 MB | 7/7 | 12081249 |
| elixir | 14.5ms | 2.8× | 5/7 | 204.4ms | 189.9ms | 78.0 MB | 5/7 | 12081249 |
| python | 13.6ms | 2.6× | 4/7 | 24.5ms | 10.9ms | 10.3 MB | 1/7 | 12081249 |
| node | 5.2ms | 1.0× | 1/7 | 23.7ms | 18.5ms | 53.3 MB | 4/7 | 12081249 |
| ruby | 8.7ms | 1.7× | 3/7 | 48.9ms | 40.2ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 5.8ms | 1.1× | 2/7 | 27.5ms | 21.7ms | 27.4 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.0ms | 3.0× | 4/7 | 89.7ms | 35.7ms | 57.4 MB | 4/7 | 6100000 |
| clojure | 216.4ms | 11.9× | 5/7 | 570.4ms | 354.0ms | 134.9 MB | 7/7 | 6100000 |
| elixir | 21.1ms | 1.2× | 2/7 | 211.0ms | 189.9ms | 79.2 MB | 5/7 | 6100000 |
| python | 586.9ms | 32.2× | 6/7 | 597.8ms | 10.9ms | 28.1 MB | 1/7 | 6100000 |
| node | 53.5ms | 2.9× | 3/7 | 72.0ms | 18.5ms | 53.6 MB | 3/7 | 6100000 |
| ruby | 1.669s | 91.7× | 7/7 | 1.709s | 40.2ms | 133.7 MB | 6/7 | 6100000 |
| dotnet | 18.2ms | 1.0× | 1/7 | 39.9ms | 21.7ms | 31.2 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 188.1ms | 1.5× | 2/7 | 223.8ms | 35.7ms | 32.0 MB | 4/7 | 134626900 |
| clojure | 440.9ms | 3.5× | 5/7 | 794.9ms | 354.0ms | 135.1 MB | 6/7 | 134626900 |
| elixir | 308.9ms | 2.4× | 3/7 | 498.8ms | 189.9ms | 72.9 MB | 5/7 | 134626900 |
| python | 2.696s | 21.3× | 7/7 | 2.707s | 10.9ms | 22.4 MB | 2/7 | 134626900 |
| node | 322.5ms | 2.5× | 4/7 | 341.0ms | 18.5ms | 185.7 MB | 7/7 | 134626900 |
| ruby | 2.032s | 16.1× | 6/7 | 2.072s | 40.2ms | 19.3 MB | 1/7 | 134626900 |
| dotnet | 126.5ms | 1.0× | 1/7 | 148.2ms | 21.7ms | 28.4 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.2ms | 1.1× | 3/7 | 187.9ms | 35.7ms | 116.7 MB | 5/7 | 500 |
| clojure | 853.7ms | 6.4× | 7/7 | 1.208s | 354.0ms | 285.3 MB | 6/7 | 500 |
| elixir | 539.8ms | 4.0× | 6/7 | 729.7ms | 189.9ms | 502.1 MB | 7/7 | 500 |
| python | 172.4ms | 1.3× | 4/7 | 183.3ms | 10.9ms | 45.7 MB | 1/7 | 500 |
| node | 133.8ms | 1.0× | 1/7 | 152.3ms | 18.5ms | 67.5 MB | 4/7 | 500 |
| ruby | 209.7ms | 1.6× | 5/7 | 249.9ms | 40.2ms | 45.8 MB | 2/7 | 500 |
| dotnet | 151.6ms | 1.1× | 2/7 | 173.3ms | 21.7ms | 48.5 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 240.6ms | 4.7× | 3/7 | 276.3ms | 35.7ms | 74.6 MB | 6/7 | 100000 |
| clojure | 602.3ms | 11.7× | 4/7 | 956.3ms | 354.0ms | 133.4 MB | 7/7 | 100000 |
| elixir | 51.5ms | 1.0× | 1/7 | 241.4ms | 189.9ms | 70.4 MB | 5/7 | 100000 |
| python | 826.6ms | 16.1× | 7/7 | 837.5ms | 10.9ms | 11.0 MB | 1/7 | 100000 |
| node | 656.8ms | 12.8× | 6/7 | 675.3ms | 18.5ms | 70.2 MB | 4/7 | 100000 |
| ruby | 628.0ms | 12.2× | 5/7 | 668.2ms | 40.2ms | 19.3 MB | 2/7 | 100000 |
| dotnet | 169.9ms | 3.3× | 2/7 | 191.6ms | 21.7ms | 28.1 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.354s | 11.4× | 4/7 | 1.390s | 35.7ms | 268.3 MB | 6/7 | 1000000 |
| clojure | 4.549s | 38.2× | 6/7 | 4.903s | 354.0ms | 754.2 MB | 7/7 | 1000000 |
| elixir | 257.6ms | 2.2× | 2/7 | 447.5ms | 189.9ms | 70.2 MB | 5/7 | 1000000 |
| python | 4.815s | 40.4× | 7/7 | 4.826s | 10.9ms | 16.3 MB | 1/7 | 1000000 |
| node | 119.2ms | 1.0× | 1/7 | 137.7ms | 18.5ms | 67.7 MB | 4/7 | 1000000 |
| ruby | 3.642s | 30.6× | 5/7 | 3.682s | 40.2ms | 23.1 MB | 2/7 | 1000000 |
| dotnet | 813.3ms | 6.8× | 3/7 | 835.0ms | 21.7ms | 30.6 MB | 3/7 | 1000000 |
