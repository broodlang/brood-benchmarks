# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-11 19:19.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.1ms | 3.1× | 4/7 | 34.1ms | — | 24.3 MB | 3/7 | 0 |
| clojure | 376.7ms | 34.2× | 7/7 | 376.7ms | — | 103.0 MB | 7/7 | 0 |
| elixir | 189.0ms | 17.2× | 6/7 | 189.0ms | — | 71.2 MB | 6/7 | 0 |
| python | 11.0ms | 1.0× | 1/7 | 11.0ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.9ms | 1.7× | 2/7 | 18.9ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.7ms | 3.6× | 5/7 | 39.7ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 22.7ms | 2.1× | 3/7 | 22.7ms | — | 25.5 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.9ms | 1.3× | 2/7 | 89.0ms | 34.1ms | 28.0 MB | 4/7 | 9227465 |
| clojure | 229.3ms | 5.6× | 5/7 | 606.0ms | 376.7ms | 108.8 MB | 7/7 | 9227465 |
| elixir | 79.4ms | 1.9× | 4/7 | 268.4ms | 189.0ms | 71.8 MB | 6/7 | 9227465 |
| python | 786.8ms | 19.2× | 7/7 | 797.8ms | 11.0ms | 9.7 MB | 1/7 | 9227465 |
| node | 77.1ms | 1.9× | 3/7 | 96.0ms | 18.9ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 695.0ms | 17.0× | 6/7 | 734.7ms | 39.7ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 40.9ms | 1.0× | 1/7 | 63.6ms | 22.7ms | 25.6 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.2ms | 3.3× | 3/7 | 71.3ms | 34.1ms | 28.0 MB | 4/7 | 449999985000000 |
| clojure | 143.6ms | 12.6× | 5/7 | 520.3ms | 376.7ms | 108.4 MB | 7/7 | 449999985000000 |
| elixir | 50.0ms | 4.4× | 4/7 | 239.0ms | 189.0ms | 72.2 MB | 6/7 | 449999985000000 |
| python | 2.469s | 216.6× | 7/7 | 2.480s | 11.0ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 29.3ms | 2.6× | 2/7 | 48.2ms | 18.9ms | 49.7 MB | 5/7 | 449999985000000 |
| ruby | 596.5ms | 52.3× | 6/7 | 636.2ms | 39.7ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 11.4ms | 1.0× | 1/7 | 34.1ms | 22.7ms | 26.0 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.8ms | 1.0× | 1/7 | 35.9ms | 34.1ms | 24.2 MB | 3/7 | 12499997500000 |
| clojure | 174.8ms | 97.1× | 5/7 | 551.5ms | 376.7ms | 220.0 MB | 7/7 | 12499997500000 |
| elixir | 28.8ms | 16.0× | 3/7 | 217.8ms | 189.0ms | 70.1 MB | 5/7 | 12499997500000 |
| python | 115.8ms | 64.3× | 4/7 | 126.8ms | 11.0ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 241.1ms | 133.9× | 7/7 | 260.0ms | 18.9ms | 89.8 MB | 6/7 | 12499997500000 |
| ruby | 239.8ms | 133.2× | 6/7 | 279.5ms | 39.7ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 11.4ms | 6.3× | 2/7 | 34.1ms | 22.7ms | 27.3 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.8ms | 5.3× | 4/7 | 72.9ms | 34.1ms | 28.4 MB | 4/7 | 13848 |
| clojure | 129.8ms | 17.8× | 6/7 | 506.5ms | 376.7ms | 108.3 MB | 7/7 | 13848 |
| elixir | 15.9ms | 2.2× | 3/7 | 204.9ms | 189.0ms | 71.2 MB | 6/7 | 13848 |
| python | 125.3ms | 17.2× | 5/7 | 136.3ms | 11.0ms | 9.9 MB | 1/7 | 13848 |
| node | 8.2ms | 1.1× | 2/7 | 27.1ms | 18.9ms | 48.4 MB | 5/7 | 13848 |
| ruby | 134.1ms | 18.4× | 7/7 | 173.8ms | 39.7ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 7.3ms | 1.0× | 1/7 | 30.0ms | 22.7ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.3ms | 1.8× | 2/7 | 114.4ms | 34.1ms | 28.3 MB | 4/7 | 442 |
| clojure | 430.9ms | 9.6× | 5/7 | 807.6ms | 376.7ms | 370.9 MB | 7/7 | 442 |
| elixir | 108.8ms | 2.4× | 3/7 | 297.8ms | 189.0ms | 71.3 MB | 6/7 | 442 |
| python | 2.716s | 60.2× | 7/7 | 2.727s | 11.0ms | 9.7 MB | 1/7 | 442 |
| node | 186.9ms | 4.1× | 4/7 | 205.8ms | 18.9ms | 47.9 MB | 5/7 | 442 |
| ruby | 897.0ms | 19.9× | 6/7 | 936.7ms | 39.7ms | 19.0 MB | 2/7 | 442 |
| dotnet | 45.1ms | 1.0× | 1/7 | 67.8ms | 22.7ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 222.3ms | 12.1× | 4/7 | 256.4ms | 34.1ms | 28.1 MB | 4/7 | 6129302 |
| clojure | 161.0ms | 8.8× | 3/7 | 537.7ms | 376.7ms | 114.7 MB | 7/7 | 6129302 |
| elixir | 284.0ms | 15.4× | 5/7 | 473.0ms | 189.0ms | 71.8 MB | 6/7 | 6129302 |
| python | 1.600s | 87.0× | 7/7 | 1.611s | 11.0ms | 9.9 MB | 1/7 | 6129302 |
| node | 23.1ms | 1.3× | 2/7 | 42.0ms | 18.9ms | 49.5 MB | 5/7 | 6129302 |
| ruby | 479.9ms | 26.1× | 6/7 | 519.6ms | 39.7ms | 19.2 MB | 2/7 | 6129302 |
| dotnet | 18.4ms | 1.0× | 1/7 | 41.1ms | 22.7ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.2ms | 39.3× | 4/7 | 183.3ms | 34.1ms | 42.3 MB | 4/7 | 654353666 |
| clojure | 188.6ms | 49.6× | 5/7 | 565.3ms | 376.7ms | 116.5 MB | 7/7 | 654353666 |
| elixir | 60.1ms | 15.8× | 3/7 | 249.1ms | 189.0ms | 74.5 MB | 6/7 | 654353666 |
| python | 494.9ms | 130.2× | 7/7 | 505.9ms | 11.0ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.4ms | 4.3× | 2/7 | 35.3ms | 18.9ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 306.7ms | 80.7× | 6/7 | 346.4ms | 39.7ms | 19.2 MB | 2/7 | 654353666 |
| dotnet | 3.8ms | 1.0× | 1/7 | 26.5ms | 22.7ms | 26.4 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 9.8ms | 1.0× | 1/7 | 43.9ms | 34.1ms | 31.3 MB | 1/7 | 3388889 |
| clojure | 161.3ms | 16.5× | 7/7 | 538.0ms | 376.7ms | 167.6 MB | 6/7 | 3388889 |
| elixir | 113.4ms | 11.6× | 6/7 | 302.4ms | 189.0ms | 200.0 MB | 7/7 | 3388889 |
| python | 43.2ms | 4.4× | 3/7 | 54.2ms | 11.0ms | 39.8 MB | 2/7 | 3388889 |
| node | 66.0ms | 6.7× | 4/7 | 84.9ms | 18.9ms | 94.9 MB | 5/7 | 3388889 |
| ruby | 87.2ms | 8.9× | 5/7 | 126.9ms | 39.7ms | 47.6 MB | 3/7 | 3388889 |
| dotnet | 30.1ms | 3.1× | 2/7 | 52.8ms | 22.7ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 114.5ms | 3.5× | 4/7 | 148.6ms | 34.1ms | 28.6 MB | 4/7 | 374854840 |
| clojure | 267.8ms | 8.1× | 7/7 | 644.5ms | 376.7ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 174.8ms | 5.3× | 5/7 | 363.8ms | 189.0ms | 69.9 MB | 6/7 | 374854840 |
| python | 178.3ms | 5.4× | 6/7 | 189.3ms | 11.0ms | 9.8 MB | 1/7 | 374854840 |
| node | 32.9ms | 1.0× | 1/7 | 51.8ms | 18.9ms | 49.7 MB | 5/7 | 374854840 |
| ruby | 85.3ms | 2.6× | 3/7 | 125.0ms | 39.7ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 42.0ms | 1.3× | 2/7 | 64.7ms | 22.7ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.7ms | 13.1× | 4/7 | 129.8ms | 34.1ms | 50.0 MB | 4/7 | 1638200 |
| clojure | 173.8ms | 23.8× | 7/7 | 550.5ms | 376.7ms | 149.9 MB | 7/7 | 1638200 |
| elixir | 7.3ms | 1.0× | 1/7 | 196.3ms | 189.0ms | 72.5 MB | 6/7 | 1638200 |
| python | 98.8ms | 13.5× | 5/7 | 109.8ms | 11.0ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.8ms | 2.8× | 3/7 | 39.7ms | 18.9ms | 55.7 MB | 5/7 | 1638200 |
| ruby | 100.5ms | 13.8× | 6/7 | 140.2ms | 39.7ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.0ms | 1.9× | 2/7 | 36.7ms | 22.7ms | 32.0 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 160.1ms | 2.4× | 5/7 | 194.2ms | 34.1ms | 165.1 MB | 7/7 | 46468819 |
| clojure | 243.7ms | 3.6× | 7/7 | 620.4ms | 376.7ms | 123.7 MB | 5/7 | 46468819 |
| elixir | 110.3ms | 1.6× | 4/7 | 299.3ms | 189.0ms | 156.9 MB | 6/7 | 46468819 |
| python | 190.9ms | 2.8× | 6/7 | 201.9ms | 11.0ms | 26.0 MB | 2/7 | 46468819 |
| node | 104.6ms | 1.6× | 3/7 | 123.5ms | 18.9ms | 64.8 MB | 4/7 | 46468819 |
| ruby | 77.3ms | 1.2× | 2/7 | 117.0ms | 39.7ms | 24.7 MB | 1/7 | 46468819 |
| dotnet | 67.1ms | 1.0× | 1/7 | 89.8ms | 22.7ms | 29.4 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.6ms | 12.7× | 5/7 | 115.7ms | 34.1ms | 37.7 MB | 4/7 | 724 |
| clojure | 209.6ms | 32.7× | 7/7 | 586.3ms | 376.7ms | 132.5 MB | 7/7 | 724 |
| elixir | 10.2ms | 1.6× | 2/7 | 199.2ms | 189.0ms | 72.2 MB | 6/7 | 724 |
| python | 58.2ms | 9.1× | 4/7 | 69.2ms | 11.0ms | 9.8 MB | 1/7 | 724 |
| node | 6.4ms | 1.0× | 1/7 | 25.3ms | 18.9ms | 50.4 MB | 5/7 | 724 |
| ruby | 128.6ms | 20.1× | 6/7 | 168.3ms | 39.7ms | 19.2 MB | 2/7 | 724 |
| dotnet | 20.0ms | 3.1× | 3/7 | 42.7ms | 22.7ms | 29.0 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.8ms | 1.8× | 2/7 | 75.9ms | 34.1ms | 28.1 MB | 3/7 | 9900000 |
| clojure | 1.134s | 50.2× | 7/7 | 1.510s | 376.7ms | 370.7 MB | 7/7 | 9900000 |
| elixir | 22.6ms | 1.0× | 1/7 | 211.6ms | 189.0ms | 70.4 MB | 6/7 | 9900000 |
| python | 51.2ms | 2.3× | 3/7 | 62.2ms | 11.0ms | 9.7 MB | 1/7 | 9900000 |
| node | 639.0ms | 28.3× | 6/7 | 657.9ms | 18.9ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 121.5ms | 5.4× | 4/7 | 161.2ms | 39.7ms | 21.6 MB | 2/7 | 9900000 |
| dotnet | 294.2ms | 13.0× | 5/7 | 316.9ms | 22.7ms | 32.7 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.7ms | 54.7× | 2/7 | 88.8ms | 34.1ms | 28.4 MB | 3/7 | 2475000 |
| clojure | 1.396s | 1396.4× | 7/7 | 1.773s | 376.7ms | 374.5 MB | 7/7 | 2475000 |
| elixir | 0.0ms | < 1× | 1/7 | 188.7ms | 189.0ms | 71.9 MB | 6/7 | 2475000 |
| python | 243.2ms | 243.2× | 5/7 | 254.2ms | 11.0ms | 9.9 MB | 1/7 | 2475000 |
| node | 231.4ms | 231.4× | 4/7 | 250.3ms | 18.9ms | 49.8 MB | 5/7 | 2475000 |
| ruby | 120.9ms | 120.9× | 3/7 | 160.6ms | 39.7ms | 25.7 MB | 2/7 | 2475000 |
| dotnet | 721.4ms | 721.4× | 6/7 | 744.1ms | 22.7ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.7ms | 8.0× | 6/7 | 62.8ms | 34.1ms | 28.3 MB | 4/7 | 155553889038886 |
| clojure | 127.1ms | 35.3× | 7/7 | 503.8ms | 376.7ms | 108.6 MB | 7/7 | 155553889038886 |
| elixir | 6.6ms | 1.8× | 2/7 | 195.6ms | 189.0ms | 70.5 MB | 6/7 | 155553889038886 |
| python | 3.6ms | 1.0× | 1/7 | 14.6ms | 11.0ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 7.5ms | 2.1× | 3/7 | 26.4ms | 18.9ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 8.3ms | 2.3× | 4/7 | 48.0ms | 39.7ms | 19.5 MB | 2/7 | 155553889038886 |
| dotnet | 8.5ms | 2.4× | 5/7 | 31.2ms | 22.7ms | 27.9 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 740.0ms | 46.0× | 6/7 | 774.1ms | 34.1ms | 122.7 MB | 5/7 | 6100000 |
| clojure | 196.3ms | 12.2× | 4/7 | 573.0ms | 376.7ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 16.1ms | 1.0× | 1/7 | 205.1ms | 189.0ms | 76.8 MB | 4/7 | 6100000 |
| python | 581.0ms | 36.1× | 5/7 | 592.0ms | 11.0ms | 28.0 MB | 1/7 | 6100000 |
| node | 54.4ms | 3.4× | 3/7 | 73.3ms | 18.9ms | 51.1 MB | 3/7 | 6100000 |
| ruby | 1.619s | 100.5× | 7/7 | 1.658s | 39.7ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 17.3ms | 1.1× | 2/7 | 40.0ms | 22.7ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 184.4ms | 1.5× | 2/7 | 218.5ms | 34.1ms | 31.0 MB | 4/7 | 134626900 |
| clojure | 406.3ms | 3.3× | 5/7 | 783.0ms | 376.7ms | 135.9 MB | 6/7 | 134626900 |
| elixir | 383.2ms | 3.1× | 4/7 | 572.2ms | 189.0ms | 71.9 MB | 5/7 | 134626900 |
| python | 2.838s | 23.1× | 7/7 | 2.849s | 11.0ms | 21.9 MB | 2/7 | 134626900 |
| node | 332.7ms | 2.7× | 3/7 | 351.6ms | 18.9ms | 182.5 MB | 7/7 | 134626900 |
| ruby | 2.087s | 17.0× | 6/7 | 2.127s | 39.7ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 122.8ms | 1.0× | 1/7 | 145.5ms | 22.7ms | 27.8 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 154.9ms | 1.2× | 3/7 | 189.0ms | 34.1ms | 125.4 MB | 5/7 | 500 |
| clojure | 854.3ms | 6.5× | 7/7 | 1.231s | 376.7ms | 274.3 MB | 6/7 | 500 |
| elixir | 644.2ms | 4.9× | 6/7 | 833.2ms | 189.0ms | 510.6 MB | 7/7 | 500 |
| python | 226.1ms | 1.7× | 5/7 | 237.1ms | 11.0ms | 42.4 MB | 1/7 | 500 |
| node | 131.1ms | 1.0× | 1/7 | 150.0ms | 18.9ms | 64.7 MB | 4/7 | 500 |
| ruby | 209.1ms | 1.6× | 4/7 | 248.8ms | 39.7ms | 45.8 MB | 2/7 | 500 |
| dotnet | 148.5ms | 1.1× | 2/7 | 171.2ms | 22.7ms | 47.8 MB | 3/7 | 500 |
