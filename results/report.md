# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-11 20:23.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.1ms | 3.0× | 4/7 | 32.1ms | — | 24.4 MB | 3/7 | 0 |
| clojure | 345.9ms | 32.6× | 7/7 | 345.9ms | — | 102.9 MB | 7/7 | 0 |
| elixir | 193.9ms | 18.3× | 6/7 | 193.9ms | — | 71.5 MB | 6/7 | 0 |
| python | 10.6ms | 1.0× | 1/7 | 10.6ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.4ms | 1.7× | 2/7 | 18.4ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.6ms | 3.7× | 5/7 | 39.6ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 21.7ms | 2.0× | 3/7 | 21.7ms | — | 25.5 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 55.5ms | 1.3× | 2/7 | 87.6ms | 32.1ms | 28.3 MB | 4/7 | 9227465 |
| clojure | 212.2ms | 5.0× | 5/7 | 558.1ms | 345.9ms | 109.2 MB | 7/7 | 9227465 |
| elixir | 69.0ms | 1.6× | 3/7 | 262.9ms | 193.9ms | 70.1 MB | 6/7 | 9227465 |
| python | 786.7ms | 18.5× | 7/7 | 797.3ms | 10.6ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.9ms | 1.9× | 4/7 | 97.3ms | 18.4ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 627.7ms | 14.7× | 6/7 | 667.3ms | 39.6ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 42.6ms | 1.0× | 1/7 | 64.3ms | 21.7ms | 25.6 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.9ms | 2.9× | 3/7 | 68.0ms | 32.1ms | 28.6 MB | 4/7 | 449999985000000 |
| clojure | 157.4ms | 12.7× | 5/7 | 503.3ms | 345.9ms | 107.4 MB | 7/7 | 449999985000000 |
| elixir | 41.5ms | 3.3× | 4/7 | 235.4ms | 193.9ms | 70.8 MB | 6/7 | 449999985000000 |
| python | 2.364s | 190.6× | 7/7 | 2.374s | 10.6ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 29.9ms | 2.4× | 2/7 | 48.3ms | 18.4ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 552.8ms | 44.6× | 6/7 | 592.4ms | 39.6ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 12.4ms | 1.0× | 1/7 | 34.1ms | 21.7ms | 26.0 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.6ms | 1.0× | 1/7 | 35.7ms | 32.1ms | 24.8 MB | 3/7 | 12499997500000 |
| clojure | 185.0ms | 51.4× | 5/7 | 530.9ms | 345.9ms | 221.2 MB | 7/7 | 12499997500000 |
| elixir | 26.5ms | 7.4× | 3/7 | 220.4ms | 193.9ms | 70.3 MB | 5/7 | 12499997500000 |
| python | 108.2ms | 30.1× | 4/7 | 118.8ms | 10.6ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 228.1ms | 63.4× | 6/7 | 246.5ms | 18.4ms | 89.8 MB | 6/7 | 12499997500000 |
| ruby | 247.8ms | 68.8× | 7/7 | 287.4ms | 39.6ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 11.6ms | 3.2× | 2/7 | 33.3ms | 21.7ms | 27.2 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.2ms | 5.3× | 4/7 | 75.3ms | 32.1ms | 28.6 MB | 4/7 | 13848 |
| clojure | 170.3ms | 20.8× | 7/7 | 516.2ms | 345.9ms | 109.0 MB | 7/7 | 13848 |
| elixir | 11.6ms | 1.4× | 3/7 | 205.5ms | 193.9ms | 71.6 MB | 6/7 | 13848 |
| python | 123.5ms | 15.1× | 6/7 | 134.1ms | 10.6ms | 9.9 MB | 1/7 | 13848 |
| node | 10.6ms | 1.3× | 2/7 | 29.0ms | 18.4ms | 48.9 MB | 5/7 | 13848 |
| ruby | 117.0ms | 14.3× | 5/7 | 156.6ms | 39.6ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 8.2ms | 1.0× | 1/7 | 29.9ms | 21.7ms | 26.0 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.4ms | 1.8× | 2/7 | 116.5ms | 32.1ms | 28.9 MB | 4/7 | 442 |
| clojure | 454.6ms | 9.9× | 5/7 | 800.5ms | 345.9ms | 370.3 MB | 7/7 | 442 |
| elixir | 98.3ms | 2.1× | 3/7 | 292.2ms | 193.9ms | 73.4 MB | 6/7 | 442 |
| python | 2.756s | 60.0× | 7/7 | 2.766s | 10.6ms | 9.8 MB | 1/7 | 442 |
| node | 181.6ms | 4.0× | 4/7 | 200.0ms | 18.4ms | 47.9 MB | 5/7 | 442 |
| ruby | 871.5ms | 19.0× | 6/7 | 911.1ms | 39.6ms | 19.0 MB | 2/7 | 442 |
| dotnet | 45.9ms | 1.0× | 1/7 | 67.6ms | 21.7ms | 26.0 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.3ms | 11.5× | 4/7 | 250.4ms | 32.1ms | 28.9 MB | 4/7 | 6129302 |
| clojure | 169.0ms | 8.9× | 3/7 | 514.9ms | 345.9ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 254.5ms | 13.4× | 5/7 | 448.4ms | 193.9ms | 72.9 MB | 6/7 | 6129302 |
| python | 1.442s | 75.9× | 7/7 | 1.452s | 10.6ms | 9.9 MB | 1/7 | 6129302 |
| node | 21.4ms | 1.1× | 2/7 | 39.8ms | 18.4ms | 49.5 MB | 5/7 | 6129302 |
| ruby | 436.8ms | 23.0× | 6/7 | 476.4ms | 39.6ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 19.0ms | 1.0× | 1/7 | 40.7ms | 21.7ms | 26.0 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.5ms | 30.1× | 4/7 | 164.6ms | 32.1ms | 42.7 MB | 4/7 | 654353666 |
| clojure | 201.8ms | 45.9× | 5/7 | 547.7ms | 345.9ms | 118.8 MB | 7/7 | 654353666 |
| elixir | 53.0ms | 12.0× | 3/7 | 246.9ms | 193.9ms | 77.0 MB | 6/7 | 654353666 |
| python | 443.9ms | 100.9× | 7/7 | 454.5ms | 10.6ms | 10.2 MB | 1/7 | 654353666 |
| node | 16.6ms | 3.8× | 2/7 | 35.0ms | 18.4ms | 51.5 MB | 5/7 | 654353666 |
| ruby | 277.2ms | 63.0× | 6/7 | 316.8ms | 39.6ms | 19.3 MB | 2/7 | 654353666 |
| dotnet | 4.4ms | 1.0× | 1/7 | 26.1ms | 21.7ms | 26.4 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.3ms | 1.0× | 1/7 | 42.4ms | 32.1ms | 31.7 MB | 1/7 | 3388889 |
| clojure | 174.5ms | 16.9× | 7/7 | 520.4ms | 345.9ms | 168.6 MB | 6/7 | 3388889 |
| elixir | 120.0ms | 11.7× | 6/7 | 313.9ms | 193.9ms | 202.0 MB | 7/7 | 3388889 |
| python | 42.2ms | 4.1× | 3/7 | 52.8ms | 10.6ms | 39.8 MB | 2/7 | 3388889 |
| node | 65.1ms | 6.3× | 4/7 | 83.5ms | 18.4ms | 94.9 MB | 5/7 | 3388889 |
| ruby | 84.6ms | 8.2× | 5/7 | 124.2ms | 39.6ms | 47.6 MB | 3/7 | 3388889 |
| dotnet | 31.8ms | 3.1× | 2/7 | 53.5ms | 21.7ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 118.0ms | 3.7× | 4/7 | 150.1ms | 32.1ms | 29.2 MB | 4/7 | 374854840 |
| clojure | 278.0ms | 8.8× | 7/7 | 623.9ms | 345.9ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 166.8ms | 5.3× | 5/7 | 360.7ms | 193.9ms | 70.7 MB | 6/7 | 374854840 |
| python | 172.5ms | 5.5× | 6/7 | 183.1ms | 10.6ms | 9.9 MB | 1/7 | 374854840 |
| node | 31.6ms | 1.0× | 1/7 | 50.0ms | 18.4ms | 49.8 MB | 5/7 | 374854840 |
| ruby | 71.3ms | 2.3× | 3/7 | 110.9ms | 39.6ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 38.1ms | 1.2× | 2/7 | 59.8ms | 21.7ms | 27.0 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.9ms | 26.4× | 4/7 | 127.0ms | 32.1ms | 50.7 MB | 4/7 | 1638200 |
| clojure | 185.5ms | 51.5× | 7/7 | 531.4ms | 345.9ms | 149.6 MB | 7/7 | 1638200 |
| elixir | 3.6ms | 1.0× | 1/7 | 197.5ms | 193.9ms | 73.4 MB | 6/7 | 1638200 |
| python | 106.1ms | 29.5× | 6/7 | 116.7ms | 10.6ms | 10.0 MB | 1/7 | 1638200 |
| node | 21.8ms | 6.1× | 3/7 | 40.2ms | 18.4ms | 55.7 MB | 5/7 | 1638200 |
| ruby | 99.5ms | 27.6× | 5/7 | 139.1ms | 39.6ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.6ms | 4.1× | 2/7 | 36.3ms | 21.7ms | 32.0 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.9ms | 2.4× | 5/7 | 197.0ms | 32.1ms | 165.5 MB | 7/7 | 46468819 |
| clojure | 280.1ms | 4.0× | 7/7 | 626.0ms | 345.9ms | 123.0 MB | 5/7 | 46468819 |
| elixir | 111.6ms | 1.6× | 4/7 | 305.5ms | 193.9ms | 159.0 MB | 6/7 | 46468819 |
| python | 215.0ms | 3.1× | 6/7 | 225.6ms | 10.6ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.7ms | 1.5× | 3/7 | 122.1ms | 18.4ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 76.6ms | 1.1× | 2/7 | 116.2ms | 39.6ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 69.2ms | 1.0× | 1/7 | 90.9ms | 21.7ms | 29.4 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.7ms | 28.3× | 5/7 | 119.8ms | 32.1ms | 43.1 MB | 4/7 | 724 |
| clojure | 272.5ms | 87.9× | 7/7 | 618.4ms | 345.9ms | 132.7 MB | 7/7 | 724 |
| elixir | 3.1ms | 1.0× | 1/7 | 197.0ms | 193.9ms | 69.9 MB | 6/7 | 724 |
| python | 60.5ms | 19.5× | 4/7 | 71.1ms | 10.6ms | 9.7 MB | 1/7 | 724 |
| node | 6.5ms | 2.1× | 2/7 | 24.9ms | 18.4ms | 50.5 MB | 5/7 | 724 |
| ruby | 124.4ms | 40.1× | 6/7 | 164.0ms | 39.6ms | 19.3 MB | 2/7 | 724 |
| dotnet | 20.0ms | 6.5× | 3/7 | 41.7ms | 21.7ms | 29.0 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.4ms | 1.0× | 1/7 | 69.5ms | 32.1ms | 28.9 MB | 3/7 | 9900000 |
| clojure | 1.149s | 30.7× | 7/7 | 1.495s | 345.9ms | 370.5 MB | 7/7 | 9900000 |
| elixir | 92.1ms | 2.5× | 3/7 | 286.0ms | 193.9ms | 72.2 MB | 6/7 | 9900000 |
| python | 54.0ms | 1.4× | 2/7 | 64.6ms | 10.6ms | 9.7 MB | 1/7 | 9900000 |
| node | 643.5ms | 17.2× | 6/7 | 661.9ms | 18.4ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 126.2ms | 3.4× | 4/7 | 165.8ms | 39.6ms | 21.6 MB | 2/7 | 9900000 |
| dotnet | 294.6ms | 7.9× | 5/7 | 316.3ms | 21.7ms | 32.7 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.8ms | 16.7× | 2/7 | 88.9ms | 32.1ms | 28.8 MB | 3/7 | 2475000 |
| clojure | 1.372s | 403.6× | 7/7 | 1.718s | 345.9ms | 374.3 MB | 7/7 | 2475000 |
| elixir | 3.4ms | 1.0× | 1/7 | 197.3ms | 193.9ms | 70.1 MB | 6/7 | 2475000 |
| python | 242.7ms | 71.4× | 5/7 | 253.3ms | 10.6ms | 9.9 MB | 1/7 | 2475000 |
| node | 211.7ms | 62.3× | 4/7 | 230.1ms | 18.4ms | 49.8 MB | 5/7 | 2475000 |
| ruby | 115.3ms | 33.9× | 3/7 | 154.9ms | 39.6ms | 25.8 MB | 2/7 | 2475000 |
| dotnet | 693.5ms | 204.0× | 6/7 | 715.2ms | 21.7ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.1ms | 29.1× | 6/7 | 61.2ms | 32.1ms | 28.7 MB | 4/7 | 155553889038886 |
| clojure | 149.6ms | 149.6× | 7/7 | 495.5ms | 345.9ms | 108.8 MB | 7/7 | 155553889038886 |
| elixir | 0.0ms | < 1× | 1/7 | 193.5ms | 193.9ms | 71.3 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 4.3× | 2/7 | 14.9ms | 10.6ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 8.7ms | 8.7× | 5/7 | 27.1ms | 18.4ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 7.8ms | 7.8× | 4/7 | 47.4ms | 39.6ms | 19.6 MB | 2/7 | 155553889038886 |
| dotnet | 7.0ms | 7.0× | 3/7 | 28.7ms | 21.7ms | 27.7 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 63.9ms | 5.2× | 4/7 | 96.0ms | 32.1ms | 60.9 MB | 4/7 | 6100000 |
| clojure | 203.8ms | 16.6× | 5/7 | 549.7ms | 345.9ms | 134.2 MB | 7/7 | 6100000 |
| elixir | 12.3ms | 1.0× | 1/7 | 206.2ms | 193.9ms | 76.3 MB | 5/7 | 6100000 |
| python | 562.4ms | 45.7× | 6/7 | 573.0ms | 10.6ms | 27.9 MB | 1/7 | 6100000 |
| node | 53.5ms | 4.3× | 3/7 | 71.9ms | 18.4ms | 51.4 MB | 3/7 | 6100000 |
| ruby | 1.612s | 131.0× | 7/7 | 1.651s | 39.6ms | 132.3 MB | 6/7 | 6100000 |
| dotnet | 18.6ms | 1.5× | 2/7 | 40.3ms | 21.7ms | 30.6 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 169.6ms | 1.4× | 2/7 | 201.7ms | 32.1ms | 31.6 MB | 4/7 | 134626900 |
| clojure | 423.3ms | 3.4× | 5/7 | 769.2ms | 345.9ms | 135.7 MB | 6/7 | 134626900 |
| elixir | 305.6ms | 2.5× | 3/7 | 499.5ms | 193.9ms | 71.7 MB | 5/7 | 134626900 |
| python | 2.689s | 21.8× | 7/7 | 2.700s | 10.6ms | 22.1 MB | 2/7 | 134626900 |
| node | 319.3ms | 2.6× | 4/7 | 337.7ms | 18.4ms | 182.7 MB | 7/7 | 134626900 |
| ruby | 2.022s | 16.4× | 6/7 | 2.062s | 39.6ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 123.3ms | 1.0× | 1/7 | 145.0ms | 21.7ms | 27.7 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.6ms | 1.4× | 3/7 | 196.7ms | 32.1ms | 122.3 MB | 5/7 | 500 |
| clojure | 852.8ms | 7.0× | 7/7 | 1.199s | 345.9ms | 282.1 MB | 6/7 | 500 |
| elixir | 627.9ms | 5.2× | 6/7 | 821.8ms | 193.9ms | 543.0 MB | 7/7 | 500 |
| python | 175.2ms | 1.4× | 4/7 | 185.8ms | 10.6ms | 44.8 MB | 1/7 | 500 |
| node | 121.6ms | 1.0× | 1/7 | 140.0ms | 18.4ms | 65.0 MB | 4/7 | 500 |
| ruby | 211.4ms | 1.7× | 5/7 | 251.0ms | 39.6ms | 45.7 MB | 2/7 | 500 |
| dotnet | 157.6ms | 1.3× | 2/7 | 179.3ms | 21.7ms | 47.7 MB | 3/7 | 500 |
