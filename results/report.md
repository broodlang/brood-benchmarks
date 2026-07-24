# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-24 12:42.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 9.9ms | 1.0× | 1/7 | 9.9ms | — | 27.9 MB | 4/7 | 0 |
| clojure | 331.4ms | 33.5× | 7/7 | 331.4ms | — | 101.2 MB | 7/7 | 0 |
| elixir | 179.7ms | 18.2× | 6/7 | 179.7ms | — | 70.0 MB | 6/7 | 0 |
| python | 10.1ms | 1.0× | 2/7 | 10.1ms | — | 9.7 MB | 1/7 | 0 |
| node | 17.9ms | 1.8× | 3/7 | 17.9ms | — | 42.3 MB | 5/7 | 0 |
| ruby | 38.7ms | 3.9× | 5/7 | 38.7ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 21.8ms | 2.2× | 4/7 | 21.8ms | — | 25.8 MB | 3/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 57.4ms | 1.3× | 2/7 | 67.3ms | 9.9ms | 21.0 MB | 3/7 | 9227465 |
| clojure | 202.4ms | 4.5× | 5/7 | 533.8ms | 331.4ms | 107.7 MB | 7/7 | 9227465 |
| elixir | 74.7ms | 1.7× | 4/7 | 254.4ms | 179.7ms | 71.9 MB | 6/7 | 9227465 |
| python | 731.3ms | 16.4× | 7/7 | 741.4ms | 10.1ms | 9.9 MB | 1/7 | 9227465 |
| node | 73.3ms | 1.6× | 3/7 | 91.2ms | 17.9ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 607.1ms | 13.6× | 6/7 | 645.8ms | 38.7ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 44.6ms | 1.0× | 1/7 | 66.4ms | 21.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.5ms | 3.2× | 3/7 | 48.4ms | 9.9ms | 21.2 MB | 3/7 | 449999985000000 |
| clojure | 143.4ms | 12.1× | 5/7 | 474.8ms | 331.4ms | 107.7 MB | 7/7 | 449999985000000 |
| elixir | 51.5ms | 4.3× | 4/7 | 231.2ms | 179.7ms | 70.9 MB | 6/7 | 449999985000000 |
| python | 2.316s | 194.6× | 7/7 | 2.326s | 10.1ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.7ms | 2.5× | 2/7 | 47.6ms | 17.9ms | 49.7 MB | 5/7 | 449999985000000 |
| ruby | 590.8ms | 49.6× | 6/7 | 629.5ms | 38.7ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 11.9ms | 1.0× | 1/7 | 33.7ms | 21.8ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.9ms | 1.0× | 1/7 | 13.8ms | 9.9ms | 17.3 MB | 2/7 | 12499997500000 |
| clojure | 178.5ms | 45.8× | 5/7 | 509.9ms | 331.4ms | 220.5 MB | 7/7 | 12499997500000 |
| elixir | 33.6ms | 8.6× | 3/7 | 213.3ms | 179.7ms | 71.9 MB | 5/7 | 12499997500000 |
| python | 105.6ms | 27.1× | 4/7 | 115.7ms | 10.1ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 224.6ms | 57.6× | 6/7 | 242.5ms | 17.9ms | 89.8 MB | 6/7 | 12499997500000 |
| ruby | 228.5ms | 58.6× | 7/7 | 267.2ms | 38.7ms | 19.2 MB | 3/7 | 12499997500000 |
| dotnet | 11.4ms | 2.9× | 2/7 | 33.2ms | 21.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.9ms | 5.4× | 4/7 | 53.8ms | 9.9ms | 22.4 MB | 3/7 | 13848 |
| clojure | 144.5ms | 17.6× | 7/7 | 475.9ms | 331.4ms | 109.3 MB | 7/7 | 13848 |
| elixir | 19.9ms | 2.4× | 3/7 | 199.6ms | 179.7ms | 69.6 MB | 6/7 | 13848 |
| python | 120.8ms | 14.7× | 6/7 | 130.9ms | 10.1ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.0× | 2/7 | 26.4ms | 17.9ms | 48.4 MB | 5/7 | 13848 |
| ruby | 115.6ms | 14.1× | 5/7 | 154.3ms | 38.7ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.2ms | 1.0× | 1/7 | 30.0ms | 21.8ms | 26.4 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.7ms | 1.8× | 2/7 | 93.6ms | 9.9ms | 22.0 MB | 3/7 | 442 |
| clojure | 420.5ms | 9.0× | 5/7 | 751.9ms | 331.4ms | 370.8 MB | 7/7 | 442 |
| elixir | 103.9ms | 2.2× | 3/7 | 283.6ms | 179.7ms | 70.6 MB | 6/7 | 442 |
| python | 2.635s | 56.7× | 7/7 | 2.646s | 10.1ms | 9.9 MB | 1/7 | 442 |
| node | 174.4ms | 3.8× | 4/7 | 192.3ms | 17.9ms | 47.9 MB | 5/7 | 442 |
| ruby | 853.7ms | 18.4× | 6/7 | 892.4ms | 38.7ms | 19.2 MB | 2/7 | 442 |
| dotnet | 46.5ms | 1.0× | 1/7 | 68.3ms | 21.8ms | 26.2 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 170.4ms | 9.3× | 4/7 | 180.3ms | 9.9ms | 22.1 MB | 3/7 | 6129302 |
| clojure | 157.5ms | 8.6× | 3/7 | 488.9ms | 331.4ms | 115.6 MB | 7/7 | 6129302 |
| elixir | 255.6ms | 14.0× | 5/7 | 435.3ms | 179.7ms | 71.6 MB | 6/7 | 6129302 |
| python | 1.371s | 74.9× | 7/7 | 1.382s | 10.1ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.3ms | 1.2× | 2/7 | 39.2ms | 17.9ms | 49.6 MB | 5/7 | 6129302 |
| ruby | 408.3ms | 22.3× | 6/7 | 447.0ms | 38.7ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 18.3ms | 1.0× | 1/7 | 40.1ms | 21.8ms | 26.4 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 134.5ms | 32.0× | 4/7 | 144.4ms | 9.9ms | 45.0 MB | 4/7 | 654353666 |
| clojure | 194.3ms | 46.3× | 5/7 | 525.7ms | 331.4ms | 118.4 MB | 7/7 | 654353666 |
| elixir | 63.8ms | 15.2× | 3/7 | 243.5ms | 179.7ms | 74.9 MB | 6/7 | 654353666 |
| python | 449.8ms | 107.1× | 7/7 | 459.9ms | 10.1ms | 10.3 MB | 1/7 | 654353666 |
| node | 17.1ms | 4.1× | 2/7 | 35.0ms | 17.9ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 280.3ms | 66.7× | 6/7 | 319.0ms | 38.7ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.2ms | 1.0× | 1/7 | 26.0ms | 21.8ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.5ms | 1.0× | 1/7 | 22.4ms | 9.9ms | 27.6 MB | 1/7 | 3388889 |
| clojure | 158.3ms | 12.7× | 7/7 | 489.7ms | 331.4ms | 169.7 MB | 6/7 | 3388889 |
| elixir | 118.4ms | 9.5× | 6/7 | 298.1ms | 179.7ms | 200.4 MB | 7/7 | 3388889 |
| python | 42.6ms | 3.4× | 3/7 | 52.7ms | 10.1ms | 40.0 MB | 2/7 | 3388889 |
| node | 64.7ms | 5.2× | 4/7 | 82.6ms | 17.9ms | 95.0 MB | 5/7 | 3388889 |
| ruby | 82.7ms | 6.6× | 5/7 | 121.4ms | 38.7ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 31.0ms | 2.5× | 2/7 | 52.8ms | 21.8ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.7ms | 1.2× | 2/7 | 45.6ms | 9.9ms | 23.3 MB | 3/7 | 374854840 |
| clojure | 268.5ms | 9.0× | 7/7 | 599.9ms | 331.4ms | 302.9 MB | 7/7 | 374854840 |
| elixir | 157.9ms | 5.3× | 5/7 | 337.6ms | 179.7ms | 73.2 MB | 6/7 | 374854840 |
| python | 177.5ms | 5.9× | 6/7 | 187.6ms | 10.1ms | 10.0 MB | 1/7 | 374854840 |
| node | 29.9ms | 1.0× | 1/7 | 47.8ms | 17.9ms | 49.8 MB | 5/7 | 374854840 |
| ruby | 71.3ms | 2.4× | 4/7 | 110.0ms | 38.7ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 36.6ms | 1.2× | 3/7 | 58.4ms | 21.8ms | 27.4 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.1ms | 9.8× | 6/7 | 112.0ms | 9.9ms | 51.5 MB | 4/7 | 1638200 |
| clojure | 171.3ms | 16.5× | 7/7 | 502.7ms | 331.4ms | 150.2 MB | 7/7 | 1638200 |
| elixir | 10.4ms | 1.0× | 1/7 | 190.1ms | 179.7ms | 72.6 MB | 6/7 | 1638200 |
| python | 97.9ms | 9.4× | 5/7 | 108.0ms | 10.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.4ms | 2.0× | 3/7 | 38.3ms | 17.9ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 95.9ms | 9.2× | 4/7 | 134.6ms | 38.7ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 12.8ms | 1.2× | 2/7 | 34.6ms | 21.8ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 213.5ms | 3.4× | 6/7 | 223.4ms | 9.9ms | 185.7 MB | 7/7 | 46468819 |
| clojure | 246.0ms | 3.9× | 7/7 | 577.4ms | 331.4ms | 123.7 MB | 5/7 | 46468819 |
| elixir | 108.1ms | 1.7× | 4/7 | 287.8ms | 179.7ms | 159.0 MB | 6/7 | 46468819 |
| python | 180.2ms | 2.9× | 5/7 | 190.3ms | 10.1ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.1ms | 1.6× | 3/7 | 121.0ms | 17.9ms | 64.8 MB | 4/7 | 46468819 |
| ruby | 70.6ms | 1.1× | 2/7 | 109.3ms | 38.7ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 63.2ms | 1.0× | 1/7 | 85.0ms | 21.8ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.9ms | 9.5× | 5/7 | 92.8ms | 9.9ms | 40.5 MB | 4/7 | 724 |
| clojure | 202.5ms | 23.3× | 7/7 | 533.9ms | 331.4ms | 135.9 MB | 7/7 | 724 |
| elixir | 9.0ms | 1.0× | 2/7 | 188.7ms | 179.7ms | 70.1 MB | 6/7 | 724 |
| python | 53.8ms | 6.2× | 4/7 | 63.9ms | 10.1ms | 9.9 MB | 1/7 | 724 |
| node | 8.7ms | 1.0× | 1/7 | 26.6ms | 17.9ms | 50.3 MB | 5/7 | 724 |
| ruby | 122.4ms | 14.1× | 6/7 | 161.1ms | 38.7ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.3ms | 2.2× | 3/7 | 41.1ms | 21.8ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.9ms | 2.3× | 2/7 | 55.8ms | 9.9ms | 21.7 MB | 2/7 | 9900000 |
| clojure | 1.088s | 54.1× | 7/7 | 1.420s | 331.4ms | 370.7 MB | 7/7 | 9900000 |
| elixir | 20.1ms | 1.0× | 1/7 | 199.8ms | 179.7ms | 71.6 MB | 6/7 | 9900000 |
| python | 51.1ms | 2.5× | 3/7 | 61.2ms | 10.1ms | 9.9 MB | 1/7 | 9900000 |
| node | 560.7ms | 27.9× | 6/7 | 578.6ms | 17.9ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 109.9ms | 5.5× | 4/7 | 148.6ms | 38.7ms | 21.8 MB | 3/7 | 9900000 |
| dotnet | 285.0ms | 14.2× | 5/7 | 306.8ms | 21.8ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.9ms | 7.5× | 2/7 | 52.8ms | 9.9ms | 21.8 MB | 2/7 | 2475000 |
| clojure | 1.304s | 228.8× | 7/7 | 1.635s | 331.4ms | 375.1 MB | 7/7 | 2475000 |
| elixir | 5.7ms | 1.0× | 1/7 | 185.4ms | 179.7ms | 73.0 MB | 6/7 | 2475000 |
| python | 233.9ms | 41.0× | 5/7 | 244.0ms | 10.1ms | 9.9 MB | 1/7 | 2475000 |
| node | 212.6ms | 37.3× | 4/7 | 230.5ms | 17.9ms | 49.8 MB | 5/7 | 2475000 |
| ruby | 110.4ms | 19.4× | 3/7 | 149.1ms | 38.7ms | 26.0 MB | 3/7 | 2475000 |
| dotnet | 688.2ms | 120.7× | 6/7 | 710.0ms | 21.8ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.2ms | 7.9× | 6/7 | 42.1ms | 9.9ms | 22.0 MB | 3/7 | 155553889038886 |
| clojure | 130.1ms | 31.7× | 7/7 | 461.5ms | 331.4ms | 108.2 MB | 7/7 | 155553889038886 |
| elixir | 8.9ms | 2.2× | 5/7 | 188.6ms | 179.7ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 4.1ms | 1.0× | 1/7 | 14.2ms | 10.1ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 7.6ms | 1.9× | 3/7 | 25.5ms | 17.9ms | 51.7 MB | 5/7 | 155553889038886 |
| ruby | 7.8ms | 1.9× | 4/7 | 46.5ms | 38.7ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 7.2ms | 1.8× | 2/7 | 29.0ms | 21.8ms | 28.1 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 342.1ms | 1.3× | 3/7 | 352.0ms | 9.9ms | 22.5 MB | 3/7 | 24558 |
| clojure | 557.1ms | 2.1× | 5/7 | 888.5ms | 331.4ms | 377.3 MB | 7/7 | 24558 |
| elixir | 282.7ms | 1.0× | 2/7 | 462.4ms | 179.7ms | 70.6 MB | 6/7 | 24558 |
| python | 3.804s | 14.0× | 7/7 | 3.814s | 10.1ms | 11.1 MB | 1/7 | 24558 |
| node | 391.9ms | 1.4× | 4/7 | 409.8ms | 17.9ms | 48.2 MB | 5/7 | 24558 |
| ruby | 1.663s | 6.1× | 6/7 | 1.701s | 38.7ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 271.7ms | 1.0× | 1/7 | 293.5ms | 21.8ms | 26.3 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.3ms | 12.2× | 3/7 | 45.2ms | 9.9ms | 29.6 MB | 4/7 | 78498 |
| clojure | 134.1ms | 46.2× | 7/7 | 465.5ms | 331.4ms | 108.7 MB | 7/7 | 78498 |
| elixir | 55.0ms | 19.0× | 4/7 | 234.7ms | 179.7ms | 79.4 MB | 6/7 | 78498 |
| python | 118.2ms | 40.8× | 6/7 | 128.3ms | 10.1ms | 10.8 MB | 1/7 | 78498 |
| node | 6.0ms | 2.1× | 2/7 | 23.9ms | 17.9ms | 49.3 MB | 5/7 | 78498 |
| ruby | 82.8ms | 28.6× | 5/7 | 121.5ms | 38.7ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.9ms | 1.0× | 1/7 | 24.7ms | 21.8ms | 27.5 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 60.9ms | 2.8× | 4/7 | 70.8ms | 9.9ms | 69.8 MB | 5/7 | 30039386344 |
| clojure | 293.7ms | 13.4× | 7/7 | 625.1ms | 331.4ms | 291.5 MB | 7/7 | 30039386344 |
| elixir | 116.3ms | 5.3× | 6/7 | 296.0ms | 179.7ms | 98.1 MB | 6/7 | 30039386344 |
| python | 79.2ms | 3.6× | 5/7 | 89.3ms | 10.1ms | 14.9 MB | 1/7 | 30039386344 |
| node | 22.8ms | 1.0× | 2/7 | 40.7ms | 17.9ms | 53.8 MB | 4/7 | 30039386344 |
| ruby | 38.3ms | 1.7× | 3/7 | 77.0ms | 38.7ms | 21.7 MB | 2/7 | 30039386344 |
| dotnet | 21.9ms | 1.0× | 1/7 | 43.7ms | 21.8ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 307.5ms | 48.0× | 6/7 | 317.4ms | 9.9ms | 56.5 MB | 5/7 | -169078071 |
| clojure | 184.8ms | 28.9× | 4/7 | 516.2ms | 331.4ms | 108.6 MB | 7/7 | -169078071 |
| elixir | 138.2ms | 21.6× | 3/7 | 317.9ms | 179.7ms | 70.4 MB | 6/7 | -169078071 |
| python | 717.1ms | 112.0× | 7/7 | 727.2ms | 10.1ms | 10.3 MB | 1/7 | -169078071 |
| node | 12.6ms | 2.0× | 2/7 | 30.5ms | 17.9ms | 49.9 MB | 4/7 | -169078071 |
| ruby | 289.1ms | 45.2× | 5/7 | 327.8ms | 38.7ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.4ms | 1.0× | 1/7 | 28.2ms | 21.8ms | 27.1 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.3ms | 80.8× | 6/7 | 147.2ms | 9.9ms | 72.5 MB | 5/7 | 1489952542 |
| clojure | 379.7ms | 223.4× | 7/7 | 711.1ms | 331.4ms | 166.2 MB | 7/7 | 1489952542 |
| elixir | 3.9ms | 2.3× | 2/7 | 183.6ms | 179.7ms | 75.1 MB | 6/7 | 1489952542 |
| python | 8.2ms | 4.8× | 4/7 | 18.3ms | 10.1ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.7ms | 1.0× | 1/7 | 19.6ms | 17.9ms | 43.8 MB | 4/7 | 1489952542 |
| ruby | 4.2ms | 2.5× | 3/7 | 42.9ms | 38.7ms | 19.9 MB | 2/7 | 1489952542 |
| dotnet | 41.9ms | 24.6× | 5/7 | 63.7ms | 21.8ms | 34.2 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.5ms | 23.2× | 6/7 | 93.4ms | 9.9ms | 38.9 MB | 4/7 | 10000 |
| clojure | 140.5ms | 39.0× | 7/7 | 471.9ms | 331.4ms | 108.8 MB | 7/7 | 10000 |
| elixir | 12.6ms | 3.5× | 4/7 | 192.3ms | 179.7ms | 72.6 MB | 6/7 | 10000 |
| python | 13.0ms | 3.6× | 5/7 | 23.1ms | 10.1ms | 11.2 MB | 1/7 | 10000 |
| node | 3.6ms | 1.0× | 1/7 | 21.5ms | 17.9ms | 50.1 MB | 5/7 | 10000 |
| ruby | 7.1ms | 2.0× | 2/7 | 45.8ms | 38.7ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.6ms | 3.5× | 3/7 | 34.4ms | 21.8ms | 32.0 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.9ms | 27.8× | 6/7 | 112.8ms | 9.9ms | 97.6 MB | 6/7 | 12081249 |
| clojure | 168.6ms | 45.6× | 7/7 | 500.0ms | 331.4ms | 109.2 MB | 7/7 | 12081249 |
| elixir | 8.9ms | 2.4× | 4/7 | 188.6ms | 179.7ms | 76.0 MB | 5/7 | 12081249 |
| python | 12.8ms | 3.5× | 5/7 | 22.9ms | 10.1ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.3ms | 1.4× | 2/7 | 23.2ms | 17.9ms | 50.7 MB | 4/7 | 12081249 |
| ruby | 7.8ms | 2.1× | 3/7 | 46.5ms | 38.7ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 3.7ms | 1.0× | 1/7 | 25.5ms | 21.8ms | 27.3 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 48.2ms | 2.7× | 3/7 | 58.1ms | 9.9ms | 52.5 MB | 4/7 | 6100000 |
| clojure | 192.0ms | 10.7× | 5/7 | 523.4ms | 331.4ms | 134.1 MB | 7/7 | 6100000 |
| elixir | 23.0ms | 1.3× | 2/7 | 202.7ms | 179.7ms | 76.3 MB | 5/7 | 6100000 |
| python | 545.2ms | 30.5× | 6/7 | 555.3ms | 10.1ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.6ms | 2.9× | 4/7 | 70.5ms | 17.9ms | 51.3 MB | 3/7 | 6100000 |
| ruby | 1.550s | 86.6× | 7/7 | 1.589s | 38.7ms | 134.0 MB | 6/7 | 6100000 |
| dotnet | 17.9ms | 1.0× | 1/7 | 39.7ms | 21.8ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.2ms | 1.5× | 2/7 | 174.1ms | 9.9ms | 24.4 MB | 3/7 | 134626900 |
| clojure | 378.7ms | 3.6× | 5/7 | 710.1ms | 331.4ms | 135.6 MB | 6/7 | 134626900 |
| elixir | 281.7ms | 2.6× | 3/7 | 461.4ms | 179.7ms | 71.3 MB | 5/7 | 134626900 |
| python | 2.422s | 22.7× | 7/7 | 2.432s | 10.1ms | 21.9 MB | 2/7 | 134626900 |
| node | 284.8ms | 2.7× | 4/7 | 302.7ms | 17.9ms | 181.7 MB | 7/7 | 134626900 |
| ruby | 1.775s | 16.6× | 6/7 | 1.813s | 38.7ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 106.6ms | 1.0× | 1/7 | 128.4ms | 21.8ms | 28.3 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.2ms | 1.3× | 3/7 | 159.1ms | 9.9ms | 78.7 MB | 5/7 | 500 |
| clojure | 775.4ms | 6.6× | 7/7 | 1.107s | 331.4ms | 282.9 MB | 6/7 | 500 |
| elixir | 537.3ms | 4.6× | 6/7 | 717.0ms | 179.7ms | 485.8 MB | 7/7 | 500 |
| python | 171.1ms | 1.5× | 4/7 | 181.2ms | 10.1ms | 45.8 MB | 2/7 | 500 |
| node | 116.9ms | 1.0× | 1/7 | 134.8ms | 17.9ms | 64.9 MB | 4/7 | 500 |
| ruby | 208.6ms | 1.8× | 5/7 | 247.3ms | 38.7ms | 45.6 MB | 1/7 | 500 |
| dotnet | 146.0ms | 1.2× | 2/7 | 167.8ms | 21.8ms | 48.3 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 247.1ms | 4.7× | 3/7 | 257.0ms | 9.9ms | 70.5 MB | 5/7 | 100000 |
| clojure | 572.6ms | 10.8× | 4/7 | 904.0ms | 331.4ms | 132.6 MB | 7/7 | 100000 |
| elixir | 53.0ms | 1.0× | 1/7 | 232.7ms | 179.7ms | 72.3 MB | 6/7 | 100000 |
| python | 776.5ms | 14.7× | 7/7 | 786.6ms | 10.1ms | 10.9 MB | 1/7 | 100000 |
| node | 628.7ms | 11.9× | 6/7 | 646.6ms | 17.9ms | 67.1 MB | 4/7 | 100000 |
| ruby | 575.5ms | 10.9× | 5/7 | 614.2ms | 38.7ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 163.4ms | 3.1× | 2/7 | 185.2ms | 21.8ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.381s | 12.0× | 4/7 | 1.391s | 9.9ms | 259.1 MB | 6/7 | 1000000 |
| clojure | 4.394s | 38.3× | 6/7 | 4.725s | 331.4ms | 860.4 MB | 7/7 | 1000000 |
| elixir | 257.9ms | 2.2× | 2/7 | 437.6ms | 179.7ms | 71.1 MB | 5/7 | 1000000 |
| python | 4.629s | 40.3× | 7/7 | 4.639s | 10.1ms | 16.2 MB | 1/7 | 1000000 |
| node | 114.8ms | 1.0× | 1/7 | 132.7ms | 17.9ms | 65.4 MB | 4/7 | 1000000 |
| ruby | 3.446s | 30.0× | 5/7 | 3.485s | 38.7ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 829.8ms | 7.2× | 3/7 | 851.6ms | 21.8ms | 30.5 MB | 3/7 | 1000000 |
