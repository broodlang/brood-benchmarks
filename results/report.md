# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-11 18:02.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.3ms | 3.0× | 4/7 | 32.3ms | — | 24.6 MB | 3/7 | 0 |
| clojure | 349.9ms | 32.7× | 7/7 | 349.9ms | — | 103.2 MB | 7/7 | 0 |
| elixir | 194.9ms | 18.2× | 6/7 | 194.9ms | — | 71.1 MB | 6/7 | 0 |
| python | 10.7ms | 1.0× | 1/7 | 10.7ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.7ms | 1.7× | 2/7 | 18.7ms | — | 42.6 MB | 5/7 | 0 |
| ruby | 39.8ms | 3.7× | 5/7 | 39.8ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 22.6ms | 2.1× | 3/7 | 22.6ms | — | 25.6 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.5ms | 1.2× | 2/7 | 84.8ms | 32.3ms | 27.9 MB | 4/7 | 9227465 |
| clojure | 209.0ms | 4.8× | 5/7 | 558.9ms | 349.9ms | 108.9 MB | 7/7 | 9227465 |
| elixir | 72.4ms | 1.7× | 3/7 | 267.3ms | 194.9ms | 70.8 MB | 6/7 | 9227465 |
| python | 784.9ms | 18.2× | 7/7 | 795.6ms | 10.7ms | 9.8 MB | 1/7 | 9227465 |
| node | 82.5ms | 1.9× | 4/7 | 101.2ms | 18.7ms | 48.0 MB | 5/7 | 9227465 |
| ruby | 645.1ms | 14.9× | 6/7 | 684.9ms | 39.8ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 43.2ms | 1.0× | 1/7 | 65.8ms | 22.6ms | 25.6 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.1ms | 3.5× | 3/7 | 71.4ms | 32.3ms | 27.7 MB | 4/7 | 449999985000000 |
| clojure | 153.3ms | 13.6× | 5/7 | 503.2ms | 349.9ms | 107.8 MB | 7/7 | 449999985000000 |
| elixir | 40.0ms | 3.5× | 4/7 | 234.9ms | 194.9ms | 72.4 MB | 6/7 | 449999985000000 |
| python | 2.368s | 209.5× | 7/7 | 2.378s | 10.7ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.0ms | 2.7× | 2/7 | 48.7ms | 18.7ms | 49.8 MB | 5/7 | 449999985000000 |
| ruby | 595.4ms | 52.7× | 6/7 | 635.2ms | 39.8ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 11.3ms | 1.0× | 1/7 | 33.9ms | 22.6ms | 26.1 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 35.6ms | 32.3ms | 24.5 MB | 3/7 | 12499997500000 |
| clojure | 170.5ms | 51.7× | 5/7 | 520.4ms | 349.9ms | 221.0 MB | 7/7 | 12499997500000 |
| elixir | 15.8ms | 4.8× | 3/7 | 210.7ms | 194.9ms | 70.1 MB | 5/7 | 12499997500000 |
| python | 110.0ms | 33.3× | 4/7 | 120.7ms | 10.7ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 223.1ms | 67.6× | 6/7 | 241.8ms | 18.7ms | 90.0 MB | 6/7 | 12499997500000 |
| ruby | 252.0ms | 76.4× | 7/7 | 291.8ms | 39.8ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 11.6ms | 3.5× | 2/7 | 34.2ms | 22.6ms | 27.2 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.5ms | 4.9× | 4/7 | 70.8ms | 32.3ms | 28.1 MB | 4/7 | 13848 |
| clojure | 137.5ms | 17.4× | 7/7 | 487.4ms | 349.9ms | 108.2 MB | 7/7 | 13848 |
| elixir | 8.8ms | 1.1× | 3/7 | 203.7ms | 194.9ms | 72.3 MB | 6/7 | 13848 |
| python | 123.3ms | 15.6× | 6/7 | 134.0ms | 10.7ms | 9.9 MB | 1/7 | 13848 |
| node | 8.7ms | 1.1× | 2/7 | 27.4ms | 18.7ms | 48.5 MB | 5/7 | 13848 |
| ruby | 115.5ms | 14.6× | 5/7 | 155.3ms | 39.8ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 7.9ms | 1.0× | 1/7 | 30.5ms | 22.6ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 78.2ms | 1.8× | 2/7 | 110.5ms | 32.3ms | 28.3 MB | 4/7 | 442 |
| clojure | 422.9ms | 9.5× | 5/7 | 772.8ms | 349.9ms | 370.0 MB | 7/7 | 442 |
| elixir | 94.3ms | 2.1× | 3/7 | 289.2ms | 194.9ms | 72.2 MB | 6/7 | 442 |
| python | 2.673s | 59.9× | 7/7 | 2.683s | 10.7ms | 9.8 MB | 1/7 | 442 |
| node | 177.1ms | 4.0× | 4/7 | 195.8ms | 18.7ms | 48.3 MB | 5/7 | 442 |
| ruby | 885.7ms | 19.9× | 6/7 | 925.5ms | 39.8ms | 19.0 MB | 2/7 | 442 |
| dotnet | 44.6ms | 1.0× | 1/7 | 67.2ms | 22.6ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.2ms | 11.4× | 4/7 | 250.5ms | 32.3ms | 28.0 MB | 4/7 | 6129302 |
| clojure | 157.9ms | 8.3× | 3/7 | 507.8ms | 349.9ms | 115.4 MB | 7/7 | 6129302 |
| elixir | 261.8ms | 13.7× | 5/7 | 456.7ms | 194.9ms | 69.9 MB | 6/7 | 6129302 |
| python | 1.382s | 72.4× | 7/7 | 1.393s | 10.7ms | 9.9 MB | 1/7 | 6129302 |
| node | 20.8ms | 1.1× | 2/7 | 39.5ms | 18.7ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 430.7ms | 22.5× | 6/7 | 470.5ms | 39.8ms | 19.2 MB | 2/7 | 6129302 |
| dotnet | 19.1ms | 1.0× | 1/7 | 41.7ms | 22.6ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.2ms | 24.2× | 4/7 | 160.5ms | 32.3ms | 42.4 MB | 4/7 | 654353666 |
| clojure | 230.0ms | 43.4× | 5/7 | 579.9ms | 349.9ms | 118.0 MB | 7/7 | 654353666 |
| elixir | 82.2ms | 15.5× | 3/7 | 277.1ms | 194.9ms | 77.0 MB | 6/7 | 654353666 |
| python | 493.5ms | 93.1× | 7/7 | 504.2ms | 10.7ms | 10.3 MB | 1/7 | 654353666 |
| node | 22.5ms | 4.2× | 2/7 | 41.2ms | 18.7ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 291.2ms | 54.9× | 6/7 | 331.0ms | 39.8ms | 19.3 MB | 2/7 | 654353666 |
| dotnet | 5.3ms | 1.0× | 1/7 | 27.9ms | 22.6ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 11.0ms | 1.0× | 1/7 | 43.3ms | 32.3ms | 31.2 MB | 1/7 | 3388889 |
| clojure | 176.4ms | 16.0× | 7/7 | 526.3ms | 349.9ms | 167.7 MB | 6/7 | 3388889 |
| elixir | 124.3ms | 11.3× | 6/7 | 319.2ms | 194.9ms | 202.4 MB | 7/7 | 3388889 |
| python | 43.3ms | 3.9× | 3/7 | 54.0ms | 10.7ms | 39.8 MB | 2/7 | 3388889 |
| node | 65.1ms | 5.9× | 4/7 | 83.8ms | 18.7ms | 95.1 MB | 5/7 | 3388889 |
| ruby | 82.1ms | 7.5× | 5/7 | 121.9ms | 39.8ms | 47.7 MB | 3/7 | 3388889 |
| dotnet | 30.5ms | 2.8× | 2/7 | 53.1ms | 22.6ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.2ms | 3.5× | 4/7 | 145.5ms | 32.3ms | 28.7 MB | 4/7 | 374854840 |
| clojure | 281.0ms | 8.7× | 7/7 | 630.9ms | 349.9ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 165.7ms | 5.1× | 5/7 | 360.6ms | 194.9ms | 70.0 MB | 6/7 | 374854840 |
| python | 173.4ms | 5.4× | 6/7 | 184.1ms | 10.7ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.3ms | 1.0× | 1/7 | 51.0ms | 18.7ms | 49.9 MB | 5/7 | 374854840 |
| ruby | 75.8ms | 2.3× | 3/7 | 115.6ms | 39.8ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 37.6ms | 1.2× | 2/7 | 60.2ms | 22.6ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.5ms | 36.6× | 4/7 | 123.8ms | 32.3ms | 51.5 MB | 4/7 | 1638200 |
| clojure | 183.5ms | 73.4× | 7/7 | 533.4ms | 349.9ms | 150.7 MB | 7/7 | 1638200 |
| elixir | 2.5ms | 1.0× | 1/7 | 197.4ms | 194.9ms | 71.0 MB | 6/7 | 1638200 |
| python | 105.5ms | 42.2× | 6/7 | 116.2ms | 10.7ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.3ms | 8.5× | 3/7 | 40.0ms | 18.7ms | 56.0 MB | 5/7 | 1638200 |
| ruby | 101.1ms | 40.4× | 5/7 | 140.9ms | 39.8ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.7ms | 5.9× | 2/7 | 37.3ms | 22.6ms | 32.1 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 160.5ms | 2.5× | 5/7 | 192.8ms | 32.3ms | 164.7 MB | 7/7 | 46468819 |
| clojure | 311.7ms | 4.8× | 7/7 | 661.6ms | 349.9ms | 123.1 MB | 5/7 | 46468819 |
| elixir | 102.3ms | 1.6× | 3/7 | 297.2ms | 194.9ms | 158.9 MB | 6/7 | 46468819 |
| python | 186.2ms | 2.9× | 6/7 | 196.9ms | 10.7ms | 25.8 MB | 2/7 | 46468819 |
| node | 102.7ms | 1.6× | 4/7 | 121.4ms | 18.7ms | 64.8 MB | 4/7 | 46468819 |
| ruby | 71.5ms | 1.1× | 2/7 | 111.3ms | 39.8ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 65.2ms | 1.0× | 1/7 | 87.8ms | 22.6ms | 29.5 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 82.0ms | 82.0× | 5/7 | 114.3ms | 32.3ms | 37.8 MB | 4/7 | 724 |
| clojure | 217.1ms | 217.1× | 7/7 | 567.0ms | 349.9ms | 136.2 MB | 7/7 | 724 |
| elixir | 0.0ms | < 1× | 1/7 | 188.1ms | 194.9ms | 71.6 MB | 6/7 | 724 |
| python | 54.3ms | 54.3× | 4/7 | 65.0ms | 10.7ms | 9.8 MB | 1/7 | 724 |
| node | 6.5ms | 6.5× | 2/7 | 25.2ms | 18.7ms | 50.4 MB | 5/7 | 724 |
| ruby | 124.1ms | 124.1× | 6/7 | 163.9ms | 39.8ms | 19.3 MB | 2/7 | 724 |
| dotnet | 20.4ms | 20.4× | 3/7 | 43.0ms | 22.6ms | 29.1 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.6ms | 1.8× | 2/7 | 68.9ms | 32.3ms | 27.9 MB | 3/7 | 9900000 |
| clojure | 1.118s | 54.0× | 7/7 | 1.468s | 349.9ms | 370.6 MB | 7/7 | 9900000 |
| elixir | 20.7ms | 1.0× | 1/7 | 215.6ms | 194.9ms | 72.3 MB | 6/7 | 9900000 |
| python | 49.2ms | 2.4× | 3/7 | 59.9ms | 10.7ms | 9.8 MB | 1/7 | 9900000 |
| node | 572.9ms | 27.7× | 6/7 | 591.6ms | 18.7ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 111.4ms | 5.4× | 4/7 | 151.2ms | 39.8ms | 21.6 MB | 2/7 | 9900000 |
| dotnet | 285.2ms | 13.8× | 5/7 | 307.8ms | 22.6ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.2ms | 53.2× | 2/7 | 85.5ms | 32.3ms | 28.4 MB | 3/7 | 2475000 |
| clojure | 1.364s | 1363.9× | 7/7 | 1.714s | 349.9ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 0.0ms | < 1× | 1/7 | 192.4ms | 194.9ms | 70.0 MB | 6/7 | 2475000 |
| python | 235.9ms | 235.9× | 5/7 | 246.6ms | 10.7ms | 9.8 MB | 1/7 | 2475000 |
| node | 210.3ms | 210.3× | 4/7 | 229.0ms | 18.7ms | 50.1 MB | 5/7 | 2475000 |
| ruby | 112.5ms | 112.5× | 3/7 | 152.3ms | 39.8ms | 25.8 MB | 2/7 | 2475000 |
| dotnet | 677.7ms | 677.7× | 6/7 | 700.3ms | 22.6ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 30.0× | 6/7 | 62.3ms | 32.3ms | 28.5 MB | 4/7 | 155553889038886 |
| clojure | 129.7ms | 129.7× | 7/7 | 479.6ms | 349.9ms | 108.4 MB | 7/7 | 155553889038886 |
| elixir | 0.0ms | < 1× | 1/7 | 189.4ms | 194.9ms | 70.8 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 3.9× | 2/7 | 14.6ms | 10.7ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.2ms | 7.2× | 4/7 | 25.9ms | 18.7ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 7.3ms | 7.3× | 5/7 | 47.1ms | 39.8ms | 19.7 MB | 2/7 | 155553889038886 |
| dotnet | 6.9ms | 6.9× | 3/7 | 29.5ms | 22.6ms | 27.8 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.418s | 194.3× | 6/7 | 1.451s | 32.3ms | 121.4 MB | 5/7 | 6100000 |
| clojure | 190.7ms | 26.1× | 4/7 | 540.6ms | 349.9ms | 133.2 MB | 7/7 | 6100000 |
| elixir | 7.3ms | 1.0× | 1/7 | 202.2ms | 194.9ms | 75.1 MB | 4/7 | 6100000 |
| python | 552.9ms | 75.7× | 5/7 | 563.6ms | 10.7ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.8ms | 7.2× | 3/7 | 71.5ms | 18.7ms | 51.4 MB | 3/7 | 6100000 |
| ruby | 1.581s | 216.6× | 7/7 | 1.621s | 39.8ms | 132.9 MB | 6/7 | 6100000 |
| dotnet | 16.6ms | 2.3× | 2/7 | 39.2ms | 22.6ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 165.2ms | 1.5× | 2/7 | 197.5ms | 32.3ms | 31.3 MB | 4/7 | 134626900 |
| clojure | 372.6ms | 3.3× | 5/7 | 722.5ms | 349.9ms | 136.9 MB | 6/7 | 134626900 |
| elixir | 311.0ms | 2.8× | 4/7 | 505.9ms | 194.9ms | 71.2 MB | 5/7 | 134626900 |
| python | 2.492s | 22.2× | 7/7 | 2.503s | 10.7ms | 22.0 MB | 2/7 | 134626900 |
| node | 296.3ms | 2.6× | 3/7 | 315.0ms | 18.7ms | 181.5 MB | 7/7 | 134626900 |
| ruby | 1.864s | 16.6× | 6/7 | 1.904s | 39.8ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 112.3ms | 1.0× | 1/7 | 134.9ms | 22.6ms | 27.9 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.0ms | 1.3× | 3/7 | 183.3ms | 32.3ms | 125.1 MB | 5/7 | 500 |
| clojure | 800.2ms | 6.7× | 7/7 | 1.150s | 349.9ms | 292.8 MB | 6/7 | 500 |
| elixir | 575.0ms | 4.8× | 6/7 | 769.9ms | 194.9ms | 490.2 MB | 7/7 | 500 |
| python | 175.3ms | 1.5× | 4/7 | 186.0ms | 10.7ms | 44.9 MB | 1/7 | 500 |
| node | 119.4ms | 1.0× | 1/7 | 138.1ms | 18.7ms | 65.0 MB | 4/7 | 500 |
| ruby | 197.8ms | 1.7× | 5/7 | 237.6ms | 39.8ms | 45.7 MB | 2/7 | 500 |
| dotnet | 150.3ms | 1.3× | 2/7 | 172.9ms | 22.6ms | 48.2 MB | 3/7 | 500 |
