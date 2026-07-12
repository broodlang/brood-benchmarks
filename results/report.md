# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-12 08:20.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.1ms | 3.2× | 4/7 | 33.1ms | — | 24.4 MB | 3/7 | 0 |
| clojure | 341.6ms | 33.5× | 7/7 | 341.6ms | — | 101.2 MB | 7/7 | 0 |
| elixir | 190.2ms | 18.6× | 6/7 | 190.2ms | — | 73.2 MB | 6/7 | 0 |
| python | 10.2ms | 1.0× | 1/7 | 10.2ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.1ms | 1.8× | 2/7 | 18.1ms | — | 42.8 MB | 5/7 | 0 |
| ruby | 40.0ms | 3.9× | 5/7 | 40.0ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 22.4ms | 2.2× | 3/7 | 22.4ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.0ms | 1.1× | 2/7 | 84.1ms | 33.1ms | 28.3 MB | 4/7 | 9227465 |
| clojure | 209.5ms | 4.6× | 5/7 | 551.1ms | 341.6ms | 108.5 MB | 7/7 | 9227465 |
| elixir | 80.7ms | 1.8× | 4/7 | 270.9ms | 190.2ms | 72.2 MB | 6/7 | 9227465 |
| python | 762.5ms | 16.9× | 7/7 | 772.7ms | 10.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 77.1ms | 1.7× | 3/7 | 95.2ms | 18.1ms | 48.2 MB | 5/7 | 9227465 |
| ruby | 638.1ms | 14.1× | 6/7 | 678.1ms | 40.0ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 45.1ms | 1.0× | 1/7 | 67.5ms | 22.4ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.9ms | 1.4× | 3/7 | 69.0ms | 33.1ms | 28.1 MB | 4/7 | 449999985000000 |
| clojure | 153.8ms | 6.0× | 5/7 | 495.4ms | 341.6ms | 107.9 MB | 7/7 | 449999985000000 |
| elixir | 57.0ms | 2.2× | 4/7 | 247.2ms | 190.2ms | 72.4 MB | 6/7 | 449999985000000 |
| python | 2.351s | 91.5× | 7/7 | 2.361s | 10.2ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 31.9ms | 1.2× | 2/7 | 50.0ms | 18.1ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 599.9ms | 23.3× | 6/7 | 639.9ms | 40.0ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 25.7ms | 1.0× | 1/7 | 48.1ms | 22.4ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.3ms | 1.1× | 2/7 | 46.4ms | 33.1ms | 24.4 MB | 3/7 | 12499997500000 |
| clojure | 198.6ms | 16.4× | 5/7 | 540.2ms | 341.6ms | 220.4 MB | 7/7 | 12499997500000 |
| elixir | 28.2ms | 2.3× | 3/7 | 218.4ms | 190.2ms | 71.1 MB | 5/7 | 12499997500000 |
| python | 107.4ms | 8.9× | 4/7 | 117.6ms | 10.2ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 220.4ms | 18.2× | 6/7 | 238.5ms | 18.1ms | 90.3 MB | 6/7 | 12499997500000 |
| ruby | 226.3ms | 18.7× | 7/7 | 266.3ms | 40.0ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 34.5ms | 22.4ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.8ms | 5.0× | 4/7 | 71.9ms | 33.1ms | 28.4 MB | 4/7 | 13848 |
| clojure | 172.9ms | 22.2× | 7/7 | 514.5ms | 341.6ms | 108.6 MB | 7/7 | 13848 |
| elixir | 15.0ms | 1.9× | 3/7 | 205.2ms | 190.2ms | 70.0 MB | 6/7 | 13848 |
| python | 123.0ms | 15.8× | 6/7 | 133.2ms | 10.2ms | 9.9 MB | 1/7 | 13848 |
| node | 10.3ms | 1.3× | 2/7 | 28.4ms | 18.1ms | 48.7 MB | 5/7 | 13848 |
| ruby | 118.6ms | 15.2× | 5/7 | 158.6ms | 40.0ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 7.8ms | 1.0× | 1/7 | 30.2ms | 22.4ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.2ms | 1.7× | 2/7 | 112.3ms | 33.1ms | 28.3 MB | 4/7 | 442 |
| clojure | 444.3ms | 9.5× | 5/7 | 785.9ms | 341.6ms | 369.9 MB | 7/7 | 442 |
| elixir | 109.3ms | 2.3× | 3/7 | 299.5ms | 190.2ms | 70.7 MB | 6/7 | 442 |
| python | 2.455s | 52.2× | 7/7 | 2.465s | 10.2ms | 9.8 MB | 1/7 | 442 |
| node | 190.4ms | 4.1× | 4/7 | 208.5ms | 18.1ms | 48.4 MB | 5/7 | 442 |
| ruby | 857.4ms | 18.2× | 6/7 | 897.4ms | 40.0ms | 19.0 MB | 2/7 | 442 |
| dotnet | 47.0ms | 1.0× | 1/7 | 69.4ms | 22.4ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 215.9ms | 11.1× | 4/7 | 249.0ms | 33.1ms | 28.3 MB | 4/7 | 6129302 |
| clojure | 173.2ms | 8.9× | 3/7 | 514.8ms | 341.6ms | 115.8 MB | 7/7 | 6129302 |
| elixir | 266.7ms | 13.7× | 5/7 | 456.9ms | 190.2ms | 71.6 MB | 6/7 | 6129302 |
| python | 1.423s | 73.4× | 7/7 | 1.434s | 10.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.8ms | 1.1× | 2/7 | 39.9ms | 18.1ms | 50.0 MB | 5/7 | 6129302 |
| ruby | 418.8ms | 21.6× | 6/7 | 458.8ms | 40.0ms | 19.1 MB | 2/7 | 6129302 |
| dotnet | 19.4ms | 1.0× | 1/7 | 41.8ms | 22.4ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 127.9ms | 29.1× | 4/7 | 161.0ms | 33.1ms | 42.7 MB | 4/7 | 654353666 |
| clojure | 213.4ms | 48.5× | 5/7 | 555.0ms | 341.6ms | 118.1 MB | 7/7 | 654353666 |
| elixir | 53.8ms | 12.2× | 3/7 | 244.0ms | 190.2ms | 75.1 MB | 6/7 | 654353666 |
| python | 461.2ms | 104.8× | 7/7 | 471.4ms | 10.2ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.8ms | 3.8× | 2/7 | 34.9ms | 18.1ms | 52.2 MB | 5/7 | 654353666 |
| ruby | 295.6ms | 67.2× | 6/7 | 335.6ms | 40.0ms | 19.3 MB | 2/7 | 654353666 |
| dotnet | 4.4ms | 1.0× | 1/7 | 26.8ms | 22.4ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.3ms | 1.0× | 1/7 | 43.4ms | 33.1ms | 31.5 MB | 1/7 | 3388889 |
| clojure | 181.9ms | 17.7× | 7/7 | 523.5ms | 341.6ms | 168.1 MB | 6/7 | 3388889 |
| elixir | 118.6ms | 11.5× | 6/7 | 308.8ms | 190.2ms | 200.8 MB | 7/7 | 3388889 |
| python | 43.4ms | 4.2× | 3/7 | 53.6ms | 10.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 66.4ms | 6.4× | 4/7 | 84.5ms | 18.1ms | 95.4 MB | 5/7 | 3388889 |
| ruby | 85.4ms | 8.3× | 5/7 | 125.4ms | 40.0ms | 47.6 MB | 3/7 | 3388889 |
| dotnet | 31.3ms | 3.0× | 2/7 | 53.7ms | 22.4ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.0ms | 3.5× | 4/7 | 146.1ms | 33.1ms | 28.7 MB | 4/7 | 374854840 |
| clojure | 296.9ms | 9.2× | 7/7 | 638.5ms | 341.6ms | 302.2 MB | 7/7 | 374854840 |
| elixir | 162.6ms | 5.1× | 5/7 | 352.8ms | 190.2ms | 70.2 MB | 6/7 | 374854840 |
| python | 177.3ms | 5.5× | 6/7 | 187.5ms | 10.2ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.1ms | 1.0× | 1/7 | 50.2ms | 18.1ms | 50.2 MB | 5/7 | 374854840 |
| ruby | 73.9ms | 2.3× | 3/7 | 113.9ms | 40.0ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 37.1ms | 1.2× | 2/7 | 59.5ms | 22.4ms | 27.2 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.2ms | 7.4× | 4/7 | 127.3ms | 33.1ms | 50.3 MB | 4/7 | 1638200 |
| clojure | 187.7ms | 14.7× | 7/7 | 529.3ms | 341.6ms | 149.6 MB | 7/7 | 1638200 |
| elixir | 12.8ms | 1.0× | 1/7 | 203.0ms | 190.2ms | 72.9 MB | 6/7 | 1638200 |
| python | 99.5ms | 7.8× | 6/7 | 109.7ms | 10.2ms | 10.0 MB | 1/7 | 1638200 |
| node | 22.3ms | 1.7× | 3/7 | 40.4ms | 18.1ms | 56.2 MB | 5/7 | 1638200 |
| ruby | 98.1ms | 7.7× | 5/7 | 138.1ms | 40.0ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 13.4ms | 1.0× | 2/7 | 35.8ms | 22.4ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 158.5ms | 2.5× | 5/7 | 191.6ms | 33.1ms | 165.0 MB | 7/7 | 46468819 |
| clojure | 302.3ms | 4.7× | 7/7 | 643.9ms | 341.6ms | 123.3 MB | 5/7 | 46468819 |
| elixir | 111.4ms | 1.7× | 4/7 | 301.6ms | 190.2ms | 160.2 MB | 6/7 | 46468819 |
| python | 199.9ms | 3.1× | 6/7 | 210.1ms | 10.2ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.6ms | 1.6× | 3/7 | 122.7ms | 18.1ms | 65.0 MB | 4/7 | 46468819 |
| ruby | 73.2ms | 1.1× | 2/7 | 113.2ms | 40.0ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 64.2ms | 1.0× | 1/7 | 86.6ms | 22.4ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.9ms | 15.2× | 5/7 | 115.0ms | 33.1ms | 38.1 MB | 4/7 | 724 |
| clojure | 273.2ms | 50.6× | 7/7 | 614.8ms | 341.6ms | 136.2 MB | 7/7 | 724 |
| elixir | 5.4ms | 1.0× | 1/7 | 195.6ms | 190.2ms | 72.2 MB | 6/7 | 724 |
| python | 55.9ms | 10.4× | 4/7 | 66.1ms | 10.2ms | 9.8 MB | 1/7 | 724 |
| node | 7.9ms | 1.5× | 2/7 | 26.0ms | 18.1ms | 50.6 MB | 5/7 | 724 |
| ruby | 142.9ms | 26.5× | 6/7 | 182.9ms | 40.0ms | 19.3 MB | 2/7 | 724 |
| dotnet | 20.2ms | 3.7× | 3/7 | 42.6ms | 22.4ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.6ms | 2.2× | 2/7 | 72.7ms | 33.1ms | 28.5 MB | 3/7 | 9900000 |
| clojure | 1.210s | 66.5× | 7/7 | 1.552s | 341.6ms | 370.1 MB | 7/7 | 9900000 |
| elixir | 18.2ms | 1.0× | 1/7 | 208.4ms | 190.2ms | 71.6 MB | 6/7 | 9900000 |
| python | 51.9ms | 2.9× | 3/7 | 62.1ms | 10.2ms | 9.8 MB | 1/7 | 9900000 |
| node | 602.1ms | 33.1× | 6/7 | 620.2ms | 18.1ms | 50.4 MB | 5/7 | 9900000 |
| ruby | 111.0ms | 6.1× | 4/7 | 151.0ms | 40.0ms | 21.6 MB | 2/7 | 9900000 |
| dotnet | 292.8ms | 16.1× | 5/7 | 315.2ms | 22.4ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.8ms | 9.4× | 2/7 | 86.9ms | 33.1ms | 28.6 MB | 3/7 | 2475000 |
| clojure | 1.466s | 257.1× | 7/7 | 1.807s | 341.6ms | 373.5 MB | 7/7 | 2475000 |
| elixir | 5.7ms | 1.0× | 1/7 | 195.9ms | 190.2ms | 72.3 MB | 6/7 | 2475000 |
| python | 232.2ms | 40.7× | 5/7 | 242.4ms | 10.2ms | 9.8 MB | 1/7 | 2475000 |
| node | 222.1ms | 39.0× | 4/7 | 240.2ms | 18.1ms | 50.1 MB | 5/7 | 2475000 |
| ruby | 115.6ms | 20.3× | 3/7 | 155.6ms | 40.0ms | 25.8 MB | 2/7 | 2475000 |
| dotnet | 730.9ms | 128.2× | 6/7 | 753.3ms | 22.4ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.3ms | 6.0× | 6/7 | 65.4ms | 33.1ms | 28.5 MB | 4/7 | 155553889038886 |
| clojure | 164.3ms | 30.4× | 7/7 | 505.9ms | 341.6ms | 107.8 MB | 7/7 | 155553889038886 |
| elixir | 15.2ms | 2.8× | 5/7 | 205.4ms | 190.2ms | 72.0 MB | 6/7 | 155553889038886 |
| python | 5.4ms | 1.0× | 1/7 | 15.6ms | 10.2ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.7ms | 1.6× | 2/7 | 26.8ms | 18.1ms | 52.1 MB | 5/7 | 155553889038886 |
| ruby | 9.8ms | 1.8× | 4/7 | 49.8ms | 40.0ms | 19.6 MB | 2/7 | 155553889038886 |
| dotnet | 9.0ms | 1.7× | 3/7 | 31.4ms | 22.4ms | 27.9 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.056s | 16.5× | 6/7 | 4.089s | 33.1ms | 29.7 MB | 4/7 | 24558 |
| clojure | 601.3ms | 2.5× | 4/7 | 942.9ms | 341.6ms | 374.3 MB | 7/7 | 24558 |
| elixir | 285.0ms | 1.2× | 2/7 | 475.2ms | 190.2ms | 71.7 MB | 6/7 | 24558 |
| python | 4.194s | 17.1× | 7/7 | 4.204s | 10.2ms | 11.0 MB | 1/7 | 24558 |
| node | 407.3ms | 1.7× | 3/7 | 425.4ms | 18.1ms | 48.5 MB | 5/7 | 24558 |
| ruby | 2.018s | 8.2× | 5/7 | 2.058s | 40.0ms | 19.5 MB | 2/7 | 24558 |
| dotnet | 245.4ms | 1.0× | 1/7 | 267.8ms | 22.4ms | 26.1 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.296s | 316.0× | 7/7 | 1.329s | 33.1ms | 463.2 MB | 7/7 | 78498 |
| clojure | 169.7ms | 41.4× | 6/7 | 511.3ms | 341.6ms | 108.9 MB | 6/7 | 78498 |
| elixir | 58.6ms | 14.3× | 3/7 | 248.8ms | 190.2ms | 79.1 MB | 5/7 | 78498 |
| python | 119.6ms | 29.2× | 5/7 | 129.8ms | 10.2ms | 10.8 MB | 1/7 | 78498 |
| node | 7.2ms | 1.8× | 2/7 | 25.3ms | 18.1ms | 49.6 MB | 4/7 | 78498 |
| ruby | 101.7ms | 24.8× | 4/7 | 141.7ms | 40.0ms | 26.6 MB | 2/7 | 78498 |
| dotnet | 4.1ms | 1.0× | 1/7 | 26.5ms | 22.4ms | 27.3 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 672.2ms | 30.7× | 7/7 | 705.3ms | 33.1ms | 241.8 MB | 6/7 | 30039386344 |
| clojure | 338.1ms | 15.4× | 6/7 | 679.7ms | 341.6ms | 291.5 MB | 7/7 | 30039386344 |
| elixir | 129.0ms | 5.9× | 5/7 | 319.2ms | 190.2ms | 98.2 MB | 5/7 | 30039386344 |
| python | 101.3ms | 4.6× | 4/7 | 111.5ms | 10.2ms | 14.9 MB | 1/7 | 30039386344 |
| node | 25.7ms | 1.2× | 2/7 | 43.8ms | 18.1ms | 54.0 MB | 4/7 | 30039386344 |
| ruby | 42.6ms | 1.9× | 3/7 | 82.6ms | 40.0ms | 21.4 MB | 2/7 | 30039386344 |
| dotnet | 21.9ms | 1.0× | 1/7 | 44.3ms | 22.4ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 7.209s | 858.2× | 7/7 | 7.242s | 33.1ms | 41.5 MB | 4/7 | -169078071 |
| clojure | 200.1ms | 23.8× | 4/7 | 541.7ms | 341.6ms | 108.5 MB | 7/7 | -169078071 |
| elixir | 142.8ms | 17.0× | 3/7 | 333.0ms | 190.2ms | 70.1 MB | 6/7 | -169078071 |
| python | 762.2ms | 90.7× | 6/7 | 772.4ms | 10.2ms | 10.5 MB | 1/7 | -169078071 |
| node | 15.7ms | 1.9× | 2/7 | 33.8ms | 18.1ms | 50.5 MB | 5/7 | -169078071 |
| ruby | 302.1ms | 36.0× | 5/7 | 342.1ms | 40.0ms | 19.0 MB | 2/7 | -169078071 |
| dotnet | 8.4ms | 1.0× | 1/7 | 30.8ms | 22.4ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.525s | 1402.8× | 7/7 | 2.558s | 33.1ms | 39.9 MB | 4/7 | 1489952542 |
| clojure | 425.1ms | 236.2× | 6/7 | 766.7ms | 341.6ms | 165.9 MB | 7/7 | 1489952542 |
| elixir | 7.3ms | 4.1× | 3/7 | 197.5ms | 190.2ms | 76.2 MB | 6/7 | 1489952542 |
| python | 8.9ms | 4.9× | 4/7 | 19.1ms | 10.2ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.8ms | 1.0× | 1/7 | 19.9ms | 18.1ms | 44.1 MB | 5/7 | 1489952542 |
| ruby | 5.2ms | 2.9× | 2/7 | 45.2ms | 40.0ms | 19.6 MB | 2/7 | 1489952542 |
| dotnet | 42.9ms | 23.8× | 5/7 | 65.3ms | 22.4ms | 34.2 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.595s | 603.5× | 7/7 | 2.628s | 33.1ms | 240.9 MB | 7/7 | 10000 |
| clojure | 141.5ms | 32.9× | 6/7 | 483.1ms | 341.6ms | 108.3 MB | 6/7 | 10000 |
| elixir | 11.9ms | 2.8× | 3/7 | 202.1ms | 190.2ms | 70.6 MB | 5/7 | 10000 |
| python | 13.6ms | 3.2× | 5/7 | 23.8ms | 10.2ms | 11.2 MB | 1/7 | 10000 |
| node | 4.3ms | 1.0× | 1/7 | 22.4ms | 18.1ms | 50.4 MB | 4/7 | 10000 |
| ruby | 6.9ms | 1.6× | 2/7 | 46.9ms | 40.0ms | 19.3 MB | 2/7 | 10000 |
| dotnet | 12.8ms | 3.0× | 4/7 | 35.2ms | 22.4ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.549s | 430.2× | 7/7 | 1.582s | 33.1ms | 1321.0 MB | 7/7 | 12081249 |
| clojure | 200.2ms | 55.6× | 6/7 | 541.8ms | 341.6ms | 108.5 MB | 6/7 | 12081249 |
| elixir | 4.2ms | 1.2× | 2/7 | 194.4ms | 190.2ms | 76.8 MB | 5/7 | 12081249 |
| python | 13.4ms | 3.7× | 5/7 | 23.6ms | 10.2ms | 10.1 MB | 1/7 | 12081249 |
| node | 6.1ms | 1.7× | 3/7 | 24.2ms | 18.1ms | 51.2 MB | 4/7 | 12081249 |
| ruby | 7.6ms | 2.1× | 4/7 | 47.6ms | 40.0ms | 19.4 MB | 2/7 | 12081249 |
| dotnet | 3.6ms | 1.0× | 1/7 | 26.0ms | 22.4ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.5ms | 3.0× | 3/7 | 84.6ms | 33.1ms | 60.6 MB | 4/7 | 6100000 |
| clojure | 218.2ms | 12.7× | 5/7 | 559.8ms | 341.6ms | 133.9 MB | 7/7 | 6100000 |
| elixir | 17.2ms | 1.0× | 1/7 | 207.4ms | 190.2ms | 76.3 MB | 5/7 | 6100000 |
| python | 558.5ms | 32.5× | 6/7 | 568.7ms | 10.2ms | 27.9 MB | 1/7 | 6100000 |
| node | 53.1ms | 3.1× | 4/7 | 71.2ms | 18.1ms | 51.5 MB | 3/7 | 6100000 |
| ruby | 1.651s | 96.0× | 7/7 | 1.691s | 40.0ms | 132.7 MB | 6/7 | 6100000 |
| dotnet | 19.0ms | 1.1× | 2/7 | 41.4ms | 22.4ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.8ms | 1.4× | 2/7 | 206.9ms | 33.1ms | 31.3 MB | 4/7 | 134626900 |
| clojure | 435.0ms | 3.6× | 5/7 | 776.6ms | 341.6ms | 135.5 MB | 6/7 | 134626900 |
| elixir | 332.0ms | 2.8× | 4/7 | 522.2ms | 190.2ms | 71.4 MB | 5/7 | 134626900 |
| python | 2.497s | 20.8× | 7/7 | 2.507s | 10.2ms | 21.7 MB | 2/7 | 134626900 |
| node | 311.4ms | 2.6× | 3/7 | 329.5ms | 18.1ms | 183.0 MB | 7/7 | 134626900 |
| ruby | 2.008s | 16.7× | 6/7 | 2.048s | 40.0ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 120.1ms | 1.0× | 1/7 | 142.5ms | 22.4ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 162.0ms | 1.4× | 3/7 | 195.1ms | 33.1ms | 123.0 MB | 5/7 | 500 |
| clojure | 864.9ms | 7.2× | 7/7 | 1.206s | 341.6ms | 272.4 MB | 6/7 | 500 |
| elixir | 611.5ms | 5.1× | 6/7 | 801.7ms | 190.2ms | 467.4 MB | 7/7 | 500 |
| python | 176.4ms | 1.5× | 4/7 | 186.6ms | 10.2ms | 44.2 MB | 1/7 | 500 |
| node | 119.6ms | 1.0× | 1/7 | 137.7ms | 18.1ms | 65.1 MB | 4/7 | 500 |
| ruby | 216.9ms | 1.8× | 5/7 | 256.9ms | 40.0ms | 46.0 MB | 2/7 | 500 |
| dotnet | 154.9ms | 1.3× | 2/7 | 177.3ms | 22.4ms | 48.1 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 663.3ms | 14.1× | 5/7 | 696.4ms | 33.1ms | 113.7 MB | 6/7 | 100000 |
| clojure | 648.0ms | 13.8× | 4/7 | 989.6ms | 341.6ms | 132.9 MB | 7/7 | 100000 |
| elixir | 46.9ms | 1.0× | 1/7 | 237.1ms | 190.2ms | 70.8 MB | 5/7 | 100000 |
| python | 840.9ms | 17.9× | 7/7 | 851.1ms | 10.2ms | 10.7 MB | 1/7 | 100000 |
| node | 676.7ms | 14.4× | 6/7 | 694.8ms | 18.1ms | 67.6 MB | 4/7 | 100000 |
| ruby | 617.7ms | 13.2× | 3/7 | 657.7ms | 40.0ms | 19.0 MB | 2/7 | 100000 |
| dotnet | 171.7ms | 3.7× | 2/7 | 194.1ms | 22.4ms | 27.8 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.232s | 18.9× | 4/7 | 2.265s | 33.1ms | 320.3 MB | 6/7 | 1000000 |
| clojure | 4.589s | 38.8× | 6/7 | 4.931s | 341.6ms | 778.4 MB | 7/7 | 1000000 |
| elixir | 262.2ms | 2.2× | 2/7 | 452.4ms | 190.2ms | 71.9 MB | 5/7 | 1000000 |
| python | 4.898s | 41.4× | 7/7 | 4.908s | 10.2ms | 16.0 MB | 1/7 | 1000000 |
| node | 118.4ms | 1.0× | 1/7 | 136.5ms | 18.1ms | 65.4 MB | 4/7 | 1000000 |
| ruby | 3.642s | 30.8× | 5/7 | 3.682s | 40.0ms | 23.0 MB | 2/7 | 1000000 |
| dotnet | 884.7ms | 7.5× | 3/7 | 907.1ms | 22.4ms | 30.5 MB | 3/7 | 1000000 |
