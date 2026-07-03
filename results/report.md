# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-03 13:25.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.5ms | 2.8× | 4/7 | 29.5ms | — | 23.6 MB | 3/7 | 0 |
| clojure | 344.1ms | 32.8× | 7/7 | 344.1ms | — | 103.2 MB | 7/7 | 0 |
| elixir | 183.4ms | 17.5× | 6/7 | 183.4ms | — | 70.3 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.6ms | 1.7× | 2/7 | 17.6ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.7ms | 3.8× | 5/7 | 39.7ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.9ms | 2.1× | 3/7 | 21.9ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.5ms | 1.3× | 2/7 | 82.0ms | 29.5ms | 26.9 MB | 4/7 | 9227465 |
| clojure | 189.2ms | 4.8× | 5/7 | 533.3ms | 344.1ms | 108.5 MB | 7/7 | 9227465 |
| elixir | 73.7ms | 1.9× | 4/7 | 257.1ms | 183.4ms | 70.4 MB | 6/7 | 9227465 |
| python | 745.0ms | 18.9× | 7/7 | 755.5ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 72.3ms | 1.8× | 3/7 | 89.9ms | 17.6ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 604.3ms | 15.3× | 6/7 | 644.0ms | 39.7ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.4ms | 1.0× | 1/7 | 61.3ms | 21.9ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.4ms | 2.9× | 3/7 | 64.9ms | 29.5ms | 27.6 MB | 4/7 | 449999985000000 |
| clojure | 132.4ms | 10.9× | 5/7 | 476.5ms | 344.1ms | 109.2 MB | 7/7 | 449999985000000 |
| elixir | 60.4ms | 5.0× | 4/7 | 243.8ms | 183.4ms | 70.3 MB | 6/7 | 449999985000000 |
| python | 2.312s | 191.1× | 7/7 | 2.322s | 10.5ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.4ms | 2.4× | 2/7 | 47.0ms | 17.6ms | 49.4 MB | 5/7 | 449999985000000 |
| ruby | 550.6ms | 45.5× | 6/7 | 590.3ms | 39.7ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 34.0ms | 21.9ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.2ms | 1.0× | 1/7 | 31.7ms | 29.5ms | 23.9 MB | 3/7 | 12499997500000 |
| clojure | 163.9ms | 74.5× | 5/7 | 508.0ms | 344.1ms | 219.9 MB | 7/7 | 12499997500000 |
| elixir | 28.5ms | 13.0× | 3/7 | 211.9ms | 183.4ms | 70.3 MB | 5/7 | 12499997500000 |
| python | 106.3ms | 48.3× | 4/7 | 116.8ms | 10.5ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 220.9ms | 100.4× | 6/7 | 238.5ms | 17.6ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 223.0ms | 101.4× | 7/7 | 262.7ms | 39.7ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 10.9ms | 5.0× | 2/7 | 32.8ms | 21.9ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.0ms | 4.3× | 4/7 | 62.5ms | 29.5ms | 27.7 MB | 4/7 | 13848 |
| clojure | 128.2ms | 16.6× | 7/7 | 472.3ms | 344.1ms | 108.3 MB | 7/7 | 13848 |
| elixir | 14.7ms | 1.9× | 3/7 | 198.1ms | 183.4ms | 72.3 MB | 6/7 | 13848 |
| python | 120.0ms | 15.6× | 6/7 | 130.5ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 9.8ms | 1.3× | 2/7 | 27.4ms | 17.6ms | 48.8 MB | 5/7 | 13848 |
| ruby | 115.6ms | 15.0× | 5/7 | 155.3ms | 39.7ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 7.7ms | 1.0× | 1/7 | 29.6ms | 21.9ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.8ms | 1.6× | 2/7 | 103.3ms | 29.5ms | 27.7 MB | 4/7 | 442 |
| clojure | 411.2ms | 9.2× | 5/7 | 755.3ms | 344.1ms | 370.9 MB | 7/7 | 442 |
| elixir | 101.4ms | 2.3× | 3/7 | 284.8ms | 183.4ms | 72.9 MB | 6/7 | 442 |
| python | 2.360s | 52.7× | 7/7 | 2.370s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 171.8ms | 3.8× | 4/7 | 189.4ms | 17.6ms | 48.0 MB | 5/7 | 442 |
| ruby | 852.3ms | 19.0× | 6/7 | 892.0ms | 39.7ms | 19.3 MB | 2/7 | 442 |
| dotnet | 44.8ms | 1.0× | 1/7 | 66.7ms | 21.9ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 212.2ms | 12.0× | 4/7 | 241.7ms | 29.5ms | 27.3 MB | 4/7 | 6129302 |
| clojure | 147.6ms | 8.3× | 3/7 | 491.7ms | 344.1ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 254.6ms | 14.4× | 5/7 | 438.0ms | 183.4ms | 71.3 MB | 6/7 | 6129302 |
| python | 1.296s | 73.2× | 7/7 | 1.306s | 10.5ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.3ms | 1.1× | 2/7 | 37.9ms | 17.6ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 417.4ms | 23.6× | 6/7 | 457.1ms | 39.7ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 17.7ms | 1.0× | 1/7 | 39.6ms | 21.9ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.8ms | 20.4× | 4/7 | 121.3ms | 29.5ms | 40.9 MB | 4/7 | 654353666 |
| clojure | 180.2ms | 40.0× | 5/7 | 524.3ms | 344.1ms | 118.3 MB | 7/7 | 654353666 |
| elixir | 58.7ms | 13.0× | 3/7 | 242.1ms | 183.4ms | 76.6 MB | 6/7 | 654353666 |
| python | 433.5ms | 96.3× | 7/7 | 444.0ms | 10.5ms | 10.5 MB | 1/7 | 654353666 |
| node | 16.2ms | 3.6× | 2/7 | 33.8ms | 17.6ms | 51.7 MB | 5/7 | 654353666 |
| ruby | 278.7ms | 61.9× | 6/7 | 318.4ms | 39.7ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 26.4ms | 21.9ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.2ms | 1.0× | 1/7 | 39.7ms | 29.5ms | 30.3 MB | 1/7 | 3388889 |
| clojure | 148.8ms | 14.6× | 7/7 | 492.9ms | 344.1ms | 168.1 MB | 6/7 | 3388889 |
| elixir | 117.7ms | 11.5× | 6/7 | 301.1ms | 183.4ms | 200.5 MB | 7/7 | 3388889 |
| python | 42.9ms | 4.2× | 3/7 | 53.4ms | 10.5ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.2ms | 6.3× | 4/7 | 81.8ms | 17.6ms | 94.7 MB | 5/7 | 3388889 |
| ruby | 81.3ms | 8.0× | 5/7 | 121.0ms | 39.7ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.5ms | 3.0× | 2/7 | 52.4ms | 21.9ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.1ms | 3.7× | 4/7 | 138.6ms | 29.5ms | 28.3 MB | 4/7 | 374854840 |
| clojure | 265.1ms | 9.0× | 7/7 | 609.2ms | 344.1ms | 302.6 MB | 7/7 | 374854840 |
| elixir | 151.5ms | 5.2× | 5/7 | 334.9ms | 183.4ms | 73.1 MB | 6/7 | 374854840 |
| python | 170.1ms | 5.8× | 6/7 | 180.6ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.4ms | 1.0× | 1/7 | 47.0ms | 17.6ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 69.0ms | 2.3× | 3/7 | 108.7ms | 39.7ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.1ms | 1.2× | 2/7 | 58.0ms | 21.9ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.3ms | 9.6× | 4/7 | 113.8ms | 29.5ms | 43.3 MB | 4/7 | 1638200 |
| clojure | 159.9ms | 18.2× | 7/7 | 504.0ms | 344.1ms | 150.5 MB | 7/7 | 1638200 |
| elixir | 8.8ms | 1.0× | 1/7 | 192.2ms | 183.4ms | 72.1 MB | 6/7 | 1638200 |
| python | 91.6ms | 10.4× | 5/7 | 102.1ms | 10.5ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.6ms | 2.3× | 3/7 | 38.2ms | 17.6ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 96.6ms | 11.0× | 6/7 | 136.3ms | 39.7ms | 19.7 MB | 2/7 | 1638200 |
| dotnet | 13.0ms | 1.5× | 2/7 | 34.9ms | 21.9ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.5ms | 2.2× | 5/7 | 174.0ms | 29.5ms | 154.6 MB | 6/7 | 46468819 |
| clojure | 237.4ms | 3.7× | 7/7 | 581.5ms | 344.1ms | 123.1 MB | 5/7 | 46468819 |
| elixir | 110.1ms | 1.7× | 4/7 | 293.5ms | 183.4ms | 159.8 MB | 7/7 | 46468819 |
| python | 178.6ms | 2.8× | 6/7 | 189.1ms | 10.5ms | 25.9 MB | 2/7 | 46468819 |
| node | 102.6ms | 1.6× | 3/7 | 120.2ms | 17.6ms | 64.4 MB | 4/7 | 46468819 |
| ruby | 70.5ms | 1.1× | 2/7 | 110.2ms | 39.7ms | 25.0 MB | 1/7 | 46468819 |
| dotnet | 64.3ms | 1.0× | 1/7 | 86.2ms | 21.9ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 80.2ms | 11.6× | 5/7 | 109.7ms | 29.5ms | 41.9 MB | 4/7 | 724 |
| clojure | 192.2ms | 27.9× | 7/7 | 536.3ms | 344.1ms | 132.6 MB | 7/7 | 724 |
| elixir | 7.7ms | 1.1× | 2/7 | 191.1ms | 183.4ms | 70.0 MB | 6/7 | 724 |
| python | 52.8ms | 7.7× | 4/7 | 63.3ms | 10.5ms | 9.8 MB | 1/7 | 724 |
| node | 6.9ms | 1.0× | 1/7 | 24.5ms | 17.6ms | 50.1 MB | 5/7 | 724 |
| ruby | 120.5ms | 17.5× | 6/7 | 160.2ms | 39.7ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.3ms | 2.8× | 3/7 | 41.2ms | 21.9ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.9ms | 1.8× | 2/7 | 67.4ms | 29.5ms | 24.7 MB | 3/7 | 9900000 |
| clojure | 1.072s | 50.8× | 7/7 | 1.416s | 344.1ms | 371.4 MB | 7/7 | 9900000 |
| elixir | 21.1ms | 1.0× | 1/7 | 204.5ms | 183.4ms | 70.3 MB | 6/7 | 9900000 |
| python | 47.1ms | 2.2× | 3/7 | 57.6ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 561.0ms | 26.6× | 6/7 | 578.6ms | 17.6ms | 49.7 MB | 5/7 | 9900000 |
| ruby | 105.7ms | 5.0× | 4/7 | 145.4ms | 39.7ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 283.8ms | 13.5× | 5/7 | 305.7ms | 21.9ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 49.7ms | 6.7× | 2/7 | 79.2ms | 29.5ms | 27.8 MB | 3/7 | 2475000 |
| clojure | 1.303s | 176.1× | 7/7 | 1.647s | 344.1ms | 373.9 MB | 7/7 | 2475000 |
| elixir | 7.4ms | 1.0× | 1/7 | 190.8ms | 183.4ms | 70.1 MB | 6/7 | 2475000 |
| python | 214.0ms | 28.9× | 5/7 | 224.5ms | 10.5ms | 9.8 MB | 1/7 | 2475000 |
| node | 208.9ms | 28.2× | 4/7 | 226.5ms | 17.6ms | 49.6 MB | 5/7 | 2475000 |
| ruby | 110.1ms | 14.9× | 3/7 | 149.8ms | 39.7ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 681.1ms | 92.0× | 6/7 | 703.0ms | 21.9ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.9ms | 6.4× | 6/7 | 54.4ms | 29.5ms | 27.7 MB | 3/7 | 155553889038886 |
| clojure | 117.8ms | 30.2× | 7/7 | 461.9ms | 344.1ms | 108.4 MB | 7/7 | 155553889038886 |
| elixir | 5.9ms | 1.5× | 2/7 | 189.3ms | 183.4ms | 72.3 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 1.0× | 1/7 | 14.4ms | 10.5ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.8ms | 2.0× | 5/7 | 25.4ms | 17.6ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.2ms | 1.8× | 3/7 | 46.9ms | 39.7ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.3ms | 1.9× | 4/7 | 29.2ms | 21.9ms | 28.2 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.5ms | 5.2× | 4/7 | 120.0ms | 29.5ms | 75.9 MB | 4/7 | 6100000 |
| clojure | 178.0ms | 10.3× | 5/7 | 522.1ms | 344.1ms | 133.6 MB | 7/7 | 6100000 |
| elixir | 17.9ms | 1.0× | 2/7 | 201.3ms | 183.4ms | 76.8 MB | 5/7 | 6100000 |
| python | 546.1ms | 31.6× | 6/7 | 556.6ms | 10.5ms | 28.1 MB | 1/7 | 6100000 |
| node | 51.6ms | 3.0× | 3/7 | 69.2ms | 17.6ms | 51.1 MB | 3/7 | 6100000 |
| ruby | 1.579s | 91.3× | 7/7 | 1.619s | 39.7ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 17.3ms | 1.0× | 1/7 | 39.2ms | 21.9ms | 31.1 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.4ms | 1.4× | 2/7 | 177.9ms | 29.5ms | 30.6 MB | 4/7 | 134626900 |
| clojure | 367.9ms | 3.4× | 5/7 | 712.0ms | 344.1ms | 135.2 MB | 6/7 | 134626900 |
| elixir | 287.7ms | 2.6× | 3/7 | 471.1ms | 183.4ms | 71.4 MB | 5/7 | 134626900 |
| python | 2.444s | 22.3× | 7/7 | 2.454s | 10.5ms | 22.2 MB | 2/7 | 134626900 |
| node | 290.3ms | 2.7× | 4/7 | 307.9ms | 17.6ms | 181.3 MB | 7/7 | 134626900 |
| ruby | 1.885s | 17.2× | 6/7 | 1.925s | 39.7ms | 19.4 MB | 1/7 | 134626900 |
| dotnet | 109.4ms | 1.0× | 1/7 | 131.3ms | 21.9ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.3ms | 1.2× | 3/7 | 173.8ms | 29.5ms | 126.0 MB | 5/7 | 500 |
| clojure | 798.0ms | 6.8× | 7/7 | 1.142s | 344.1ms | 347.4 MB | 6/7 | 500 |
| elixir | 548.6ms | 4.6× | 6/7 | 732.0ms | 183.4ms | 473.3 MB | 7/7 | 500 |
| python | 172.3ms | 1.5× | 4/7 | 182.8ms | 10.5ms | 44.2 MB | 1/7 | 500 |
| node | 118.2ms | 1.0× | 1/7 | 135.8ms | 17.6ms | 64.4 MB | 4/7 | 500 |
| ruby | 207.5ms | 1.8× | 5/7 | 247.2ms | 39.7ms | 45.8 MB | 2/7 | 500 |
| dotnet | 143.8ms | 1.2× | 2/7 | 165.7ms | 21.9ms | 50.6 MB | 3/7 | 500 |
