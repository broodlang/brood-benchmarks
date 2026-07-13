# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-13 09:51.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.9ms | 3.2× | 4/7 | 31.9ms | — | 25.3 MB | 3/7 | 0 |
| clojure | 336.6ms | 33.3× | 7/7 | 336.6ms | — | 103.5 MB | 7/7 | 0 |
| elixir | 184.6ms | 18.3× | 6/7 | 184.6ms | — | 71.3 MB | 6/7 | 0 |
| python | 10.1ms | 1.0× | 1/7 | 10.1ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.5ms | 1.8× | 2/7 | 18.5ms | — | 42.3 MB | 5/7 | 0 |
| ruby | 40.0ms | 4.0× | 5/7 | 40.0ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 22.2ms | 2.2× | 3/7 | 22.2ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 55.4ms | 1.2× | 2/7 | 87.3ms | 31.9ms | 28.7 MB | 4/7 | 9227465 |
| clojure | 205.4ms | 4.5× | 5/7 | 542.0ms | 336.6ms | 107.7 MB | 7/7 | 9227465 |
| elixir | 68.7ms | 1.5× | 3/7 | 253.3ms | 184.6ms | 70.1 MB | 6/7 | 9227465 |
| python | 809.4ms | 17.9× | 7/7 | 819.5ms | 10.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 74.5ms | 1.6× | 4/7 | 93.0ms | 18.5ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 598.3ms | 13.2× | 6/7 | 638.3ms | 40.0ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 45.2ms | 1.0× | 1/7 | 67.4ms | 22.2ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 305.4ms | 21.8× | 5/7 | 337.3ms | 31.9ms | 28.8 MB | 4/7 | 449999985000000 |
| clojure | 154.4ms | 11.0× | 4/7 | 491.0ms | 336.6ms | 108.1 MB | 7/7 | 449999985000000 |
| elixir | 50.2ms | 3.6× | 3/7 | 234.8ms | 184.6ms | 70.3 MB | 6/7 | 449999985000000 |
| python | 2.390s | 170.7× | 7/7 | 2.400s | 10.1ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.9ms | 2.1× | 2/7 | 48.4ms | 18.5ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 606.7ms | 43.3× | 6/7 | 646.7ms | 40.0ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 14.0ms | 1.0× | 1/7 | 36.2ms | 22.2ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.9ms | 1.0× | 1/7 | 35.8ms | 31.9ms | 24.9 MB | 3/7 | 12499997500000 |
| clojure | 181.6ms | 46.6× | 5/7 | 518.2ms | 336.6ms | 218.6 MB | 7/7 | 12499997500000 |
| elixir | 31.5ms | 8.1× | 3/7 | 216.1ms | 184.6ms | 72.8 MB | 5/7 | 12499997500000 |
| python | 104.7ms | 26.8× | 4/7 | 114.8ms | 10.1ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 236.7ms | 60.7× | 7/7 | 255.2ms | 18.5ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 222.9ms | 57.2× | 6/7 | 262.9ms | 40.0ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 12.3ms | 3.2× | 2/7 | 34.5ms | 22.2ms | 27.4 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.0ms | 6.7× | 4/7 | 84.9ms | 31.9ms | 28.9 MB | 4/7 | 13848 |
| clojure | 149.0ms | 18.9× | 7/7 | 485.6ms | 336.6ms | 109.0 MB | 7/7 | 13848 |
| elixir | 14.2ms | 1.8× | 3/7 | 198.8ms | 184.6ms | 70.2 MB | 6/7 | 13848 |
| python | 122.4ms | 15.5× | 5/7 | 132.5ms | 10.1ms | 9.9 MB | 1/7 | 13848 |
| node | 9.7ms | 1.2× | 2/7 | 28.2ms | 18.5ms | 48.7 MB | 5/7 | 13848 |
| ruby | 123.5ms | 15.6× | 6/7 | 163.5ms | 40.0ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 7.9ms | 1.0× | 1/7 | 30.1ms | 22.2ms | 26.2 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 169.4ms | 3.7× | 3/7 | 201.3ms | 31.9ms | 29.2 MB | 4/7 | 442 |
| clojure | 418.5ms | 9.1× | 5/7 | 755.1ms | 336.6ms | 371.4 MB | 7/7 | 442 |
| elixir | 102.8ms | 2.2× | 2/7 | 287.4ms | 184.6ms | 70.3 MB | 6/7 | 442 |
| python | 2.692s | 58.6× | 7/7 | 2.702s | 10.1ms | 9.8 MB | 1/7 | 442 |
| node | 178.3ms | 3.9× | 4/7 | 196.8ms | 18.5ms | 47.8 MB | 5/7 | 442 |
| ruby | 881.3ms | 19.2× | 6/7 | 921.3ms | 40.0ms | 19.1 MB | 2/7 | 442 |
| dotnet | 45.9ms | 1.0× | 1/7 | 68.1ms | 22.2ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 262.4ms | 14.7× | 5/7 | 294.3ms | 31.9ms | 29.1 MB | 4/7 | 6129302 |
| clojure | 161.8ms | 9.1× | 3/7 | 498.4ms | 336.6ms | 114.1 MB | 7/7 | 6129302 |
| elixir | 254.6ms | 14.3× | 4/7 | 439.2ms | 184.6ms | 71.8 MB | 6/7 | 6129302 |
| python | 1.367s | 76.8× | 7/7 | 1.377s | 10.1ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.3ms | 1.1× | 2/7 | 38.8ms | 18.5ms | 49.5 MB | 5/7 | 6129302 |
| ruby | 412.9ms | 23.2× | 6/7 | 452.9ms | 40.0ms | 19.2 MB | 2/7 | 6129302 |
| dotnet | 17.8ms | 1.0× | 1/7 | 40.0ms | 22.2ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 139.3ms | 37.6× | 4/7 | 171.2ms | 31.9ms | 42.6 MB | 4/7 | 654353666 |
| clojure | 195.5ms | 52.8× | 5/7 | 532.1ms | 336.6ms | 117.5 MB | 7/7 | 654353666 |
| elixir | 55.8ms | 15.1× | 3/7 | 240.4ms | 184.6ms | 76.4 MB | 6/7 | 654353666 |
| python | 443.4ms | 119.8× | 7/7 | 453.5ms | 10.1ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.1ms | 4.4× | 2/7 | 34.6ms | 18.5ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 279.1ms | 75.4× | 6/7 | 319.1ms | 40.0ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 3.7ms | 1.0× | 1/7 | 25.9ms | 22.2ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.9ms | 1.0× | 1/7 | 44.8ms | 31.9ms | 35.5 MB | 1/7 | 3388889 |
| clojure | 166.0ms | 12.9× | 7/7 | 502.6ms | 336.6ms | 168.6 MB | 6/7 | 3388889 |
| elixir | 112.2ms | 8.7× | 6/7 | 296.8ms | 184.6ms | 201.7 MB | 7/7 | 3388889 |
| python | 42.6ms | 3.3× | 3/7 | 52.7ms | 10.1ms | 39.8 MB | 2/7 | 3388889 |
| node | 64.3ms | 5.0× | 4/7 | 82.8ms | 18.5ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 81.0ms | 6.3× | 5/7 | 121.0ms | 40.0ms | 47.7 MB | 3/7 | 3388889 |
| dotnet | 31.1ms | 2.4× | 2/7 | 53.3ms | 22.2ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 120.3ms | 4.0× | 4/7 | 152.2ms | 31.9ms | 30.2 MB | 4/7 | 374854840 |
| clojure | 269.4ms | 8.9× | 7/7 | 606.0ms | 336.6ms | 301.9 MB | 7/7 | 374854840 |
| elixir | 159.3ms | 5.3× | 5/7 | 343.9ms | 184.6ms | 73.3 MB | 6/7 | 374854840 |
| python | 174.2ms | 5.7× | 6/7 | 184.3ms | 10.1ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.3ms | 1.0× | 1/7 | 48.8ms | 18.5ms | 49.7 MB | 5/7 | 374854840 |
| ruby | 67.3ms | 2.2× | 3/7 | 107.3ms | 40.0ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 36.5ms | 1.2× | 2/7 | 58.7ms | 22.2ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.2ms | 12.8× | 4/7 | 123.1ms | 31.9ms | 53.0 MB | 4/7 | 1638200 |
| clojure | 170.6ms | 24.0× | 7/7 | 507.2ms | 336.6ms | 149.4 MB | 7/7 | 1638200 |
| elixir | 7.1ms | 1.0× | 1/7 | 191.7ms | 184.6ms | 70.5 MB | 6/7 | 1638200 |
| python | 95.2ms | 13.4× | 5/7 | 105.3ms | 10.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 19.3ms | 2.7× | 3/7 | 37.8ms | 18.5ms | 55.7 MB | 5/7 | 1638200 |
| ruby | 96.9ms | 13.6× | 6/7 | 136.9ms | 40.0ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.3ms | 2.0× | 2/7 | 36.5ms | 22.2ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 217.7ms | 3.5× | 6/7 | 249.6ms | 31.9ms | 187.2 MB | 7/7 | 46468819 |
| clojure | 256.5ms | 4.1× | 7/7 | 593.1ms | 336.6ms | 123.3 MB | 5/7 | 46468819 |
| elixir | 108.2ms | 1.7× | 4/7 | 292.8ms | 184.6ms | 158.4 MB | 6/7 | 46468819 |
| python | 185.6ms | 2.9× | 5/7 | 195.7ms | 10.1ms | 25.8 MB | 2/7 | 46468819 |
| node | 107.4ms | 1.7× | 3/7 | 125.9ms | 18.5ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 70.1ms | 1.1× | 2/7 | 110.1ms | 40.0ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 63.0ms | 1.0× | 1/7 | 85.2ms | 22.2ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.4ms | 20.2× | 6/7 | 165.3ms | 31.9ms | 49.3 MB | 4/7 | 724 |
| clojure | 212.0ms | 32.1× | 7/7 | 548.6ms | 336.6ms | 136.1 MB | 7/7 | 724 |
| elixir | 7.7ms | 1.2× | 2/7 | 192.3ms | 184.6ms | 72.1 MB | 6/7 | 724 |
| python | 54.5ms | 8.3× | 4/7 | 64.6ms | 10.1ms | 9.8 MB | 1/7 | 724 |
| node | 6.6ms | 1.0× | 1/7 | 25.1ms | 18.5ms | 50.3 MB | 5/7 | 724 |
| ruby | 121.8ms | 18.5× | 5/7 | 161.8ms | 40.0ms | 19.4 MB | 2/7 | 724 |
| dotnet | 18.9ms | 2.9× | 3/7 | 41.1ms | 22.2ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.7ms | 2.1× | 2/7 | 71.6ms | 31.9ms | 29.2 MB | 3/7 | 9900000 |
| clojure | 1.078s | 56.4× | 7/7 | 1.415s | 336.6ms | 370.1 MB | 7/7 | 9900000 |
| elixir | 19.1ms | 1.0× | 1/7 | 203.7ms | 184.6ms | 72.5 MB | 6/7 | 9900000 |
| python | 48.2ms | 2.5× | 3/7 | 58.3ms | 10.1ms | 9.8 MB | 1/7 | 9900000 |
| node | 584.0ms | 30.6× | 6/7 | 602.5ms | 18.5ms | 49.8 MB | 5/7 | 9900000 |
| ruby | 106.4ms | 5.6× | 4/7 | 146.4ms | 40.0ms | 21.7 MB | 2/7 | 9900000 |
| dotnet | 282.5ms | 14.8× | 5/7 | 304.7ms | 22.2ms | 32.7 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 244.0ms | 62.6× | 5/7 | 275.9ms | 31.9ms | 29.0 MB | 3/7 | 2475000 |
| clojure | 1.332s | 341.5× | 7/7 | 1.669s | 336.6ms | 373.9 MB | 7/7 | 2475000 |
| elixir | 3.9ms | 1.0× | 1/7 | 188.5ms | 184.6ms | 72.3 MB | 6/7 | 2475000 |
| python | 233.6ms | 59.9× | 4/7 | 243.7ms | 10.1ms | 9.8 MB | 1/7 | 2475000 |
| node | 213.0ms | 54.6× | 3/7 | 231.5ms | 18.5ms | 49.9 MB | 5/7 | 2475000 |
| ruby | 108.7ms | 27.9× | 2/7 | 148.7ms | 40.0ms | 25.9 MB | 2/7 | 2475000 |
| dotnet | 706.0ms | 181.0× | 6/7 | 728.2ms | 22.2ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.6ms | 8.5× | 6/7 | 69.5ms | 31.9ms | 29.2 MB | 4/7 | 155553889038886 |
| clojure | 135.9ms | 30.9× | 7/7 | 472.5ms | 336.6ms | 107.5 MB | 7/7 | 155553889038886 |
| elixir | 7.4ms | 1.7× | 4/7 | 192.0ms | 184.6ms | 73.8 MB | 6/7 | 155553889038886 |
| python | 4.4ms | 1.0× | 1/7 | 14.5ms | 10.1ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.4ms | 1.7× | 3/7 | 25.9ms | 18.5ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 7.0ms | 1.6× | 2/7 | 47.0ms | 40.0ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 8.0ms | 1.8× | 5/7 | 30.2ms | 22.2ms | 27.8 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.016s | 16.5× | 7/7 | 4.047s | 31.9ms | 30.9 MB | 4/7 | 24558 |
| clojure | 536.9ms | 2.2× | 4/7 | 873.5ms | 336.6ms | 375.4 MB | 7/7 | 24558 |
| elixir | 275.2ms | 1.1× | 2/7 | 459.8ms | 184.6ms | 70.1 MB | 6/7 | 24558 |
| python | 3.857s | 15.9× | 6/7 | 3.867s | 10.1ms | 11.0 MB | 1/7 | 24558 |
| node | 391.6ms | 1.6× | 3/7 | 410.1ms | 18.5ms | 48.1 MB | 5/7 | 24558 |
| ruby | 1.657s | 6.8× | 5/7 | 1.697s | 40.0ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 242.8ms | 1.0× | 1/7 | 265.0ms | 22.2ms | 26.1 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.034s | 413.6× | 7/7 | 1.066s | 31.9ms | 416.5 MB | 7/7 | 78498 |
| clojure | 139.4ms | 55.8× | 6/7 | 476.0ms | 336.6ms | 108.9 MB | 6/7 | 78498 |
| elixir | 51.5ms | 20.6× | 3/7 | 236.1ms | 184.6ms | 78.1 MB | 5/7 | 78498 |
| python | 118.0ms | 47.2× | 5/7 | 128.1ms | 10.1ms | 10.8 MB | 1/7 | 78498 |
| node | 6.2ms | 2.5× | 2/7 | 24.7ms | 18.5ms | 49.2 MB | 4/7 | 78498 |
| ruby | 85.4ms | 34.2× | 4/7 | 125.4ms | 40.0ms | 26.7 MB | 2/7 | 78498 |
| dotnet | 2.5ms | 1.0× | 1/7 | 24.7ms | 22.2ms | 27.2 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 606.2ms | 27.8× | 7/7 | 638.1ms | 31.9ms | 237.5 MB | 6/7 | 30039386344 |
| clojure | 296.4ms | 13.6× | 6/7 | 633.0ms | 336.6ms | 292.1 MB | 7/7 | 30039386344 |
| elixir | 115.6ms | 5.3× | 5/7 | 300.2ms | 184.6ms | 96.2 MB | 5/7 | 30039386344 |
| python | 84.9ms | 3.9× | 4/7 | 95.0ms | 10.1ms | 14.9 MB | 1/7 | 30039386344 |
| node | 22.6ms | 1.0× | 2/7 | 41.1ms | 18.5ms | 53.7 MB | 4/7 | 30039386344 |
| ruby | 37.6ms | 1.7× | 3/7 | 77.6ms | 40.0ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 21.8ms | 1.0× | 1/7 | 44.0ms | 22.2ms | 30.2 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 5.850s | 975.0× | 7/7 | 5.882s | 31.9ms | 41.9 MB | 4/7 | -169078071 |
| clojure | 176.4ms | 29.4× | 4/7 | 513.0ms | 336.6ms | 108.8 MB | 7/7 | -169078071 |
| elixir | 141.0ms | 23.5× | 3/7 | 325.6ms | 184.6ms | 70.5 MB | 6/7 | -169078071 |
| python | 729.1ms | 121.5× | 6/7 | 739.2ms | 10.1ms | 10.3 MB | 1/7 | -169078071 |
| node | 12.8ms | 2.1× | 2/7 | 31.3ms | 18.5ms | 50.2 MB | 5/7 | -169078071 |
| ruby | 289.3ms | 48.2× | 5/7 | 329.3ms | 40.0ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 6.0ms | 1.0× | 1/7 | 28.2ms | 22.2ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 353.8ms | 353.8× | 6/7 | 385.7ms | 31.9ms | 95.7 MB | 6/7 | 1489952542 |
| clojure | 400.3ms | 400.3× | 7/7 | 736.9ms | 336.6ms | 167.9 MB | 7/7 | 1489952542 |
| elixir | 3.5ms | 3.5× | 2/7 | 188.1ms | 184.6ms | 74.1 MB | 5/7 | 1489952542 |
| python | 8.4ms | 8.4× | 4/7 | 18.5ms | 10.1ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.0ms | 1.0× | 1/7 | 19.5ms | 18.5ms | 43.8 MB | 4/7 | 1489952542 |
| ruby | 4.3ms | 4.3× | 3/7 | 44.3ms | 40.0ms | 19.7 MB | 2/7 | 1489952542 |
| dotnet | 41.8ms | 41.8× | 5/7 | 64.0ms | 22.2ms | 33.9 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 945.9ms | 305.1× | 7/7 | 977.8ms | 31.9ms | 165.6 MB | 7/7 | 10000 |
| clojure | 136.0ms | 43.9× | 6/7 | 472.6ms | 336.6ms | 109.4 MB | 6/7 | 10000 |
| elixir | 13.0ms | 4.2× | 5/7 | 197.6ms | 184.6ms | 70.6 MB | 5/7 | 10000 |
| python | 12.9ms | 4.2× | 4/7 | 23.0ms | 10.1ms | 11.1 MB | 1/7 | 10000 |
| node | 3.1ms | 1.0× | 1/7 | 21.6ms | 18.5ms | 50.1 MB | 4/7 | 10000 |
| ruby | 6.2ms | 2.0× | 2/7 | 46.2ms | 40.0ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.2ms | 3.9× | 3/7 | 34.4ms | 22.2ms | 31.8 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.4ms | 35.8× | 6/7 | 164.3ms | 31.9ms | 105.6 MB | 6/7 | 12081249 |
| clojure | 159.5ms | 43.1× | 7/7 | 496.1ms | 336.6ms | 108.6 MB | 7/7 | 12081249 |
| elixir | 7.6ms | 2.1× | 4/7 | 192.2ms | 184.6ms | 76.8 MB | 5/7 | 12081249 |
| python | 13.5ms | 3.6× | 5/7 | 23.6ms | 10.1ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.2ms | 1.4× | 2/7 | 23.7ms | 18.5ms | 50.6 MB | 4/7 | 12081249 |
| ruby | 6.6ms | 1.8× | 3/7 | 46.6ms | 40.0ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 3.7ms | 1.0× | 1/7 | 25.9ms | 22.2ms | 27.1 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.9ms | 2.9× | 3/7 | 82.8ms | 31.9ms | 56.3 MB | 4/7 | 6100000 |
| clojure | 186.5ms | 10.5× | 5/7 | 523.1ms | 336.6ms | 134.4 MB | 7/7 | 6100000 |
| elixir | 20.5ms | 1.2× | 2/7 | 205.1ms | 184.6ms | 77.4 MB | 5/7 | 6100000 |
| python | 552.0ms | 31.0× | 6/7 | 562.1ms | 10.1ms | 27.9 MB | 1/7 | 6100000 |
| node | 52.1ms | 2.9× | 4/7 | 70.6ms | 18.5ms | 51.4 MB | 3/7 | 6100000 |
| ruby | 1.578s | 88.6× | 7/7 | 1.618s | 40.0ms | 133.3 MB | 6/7 | 6100000 |
| dotnet | 17.8ms | 1.0× | 1/7 | 40.0ms | 22.2ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 184.6ms | 1.6× | 2/7 | 216.5ms | 31.9ms | 31.4 MB | 4/7 | 134626900 |
| clojure | 379.7ms | 3.3× | 5/7 | 716.3ms | 336.6ms | 135.6 MB | 6/7 | 134626900 |
| elixir | 291.0ms | 2.6× | 3/7 | 475.6ms | 184.6ms | 72.3 MB | 5/7 | 134626900 |
| python | 2.489s | 21.9× | 7/7 | 2.499s | 10.1ms | 22.0 MB | 2/7 | 134626900 |
| node | 295.3ms | 2.6× | 4/7 | 313.8ms | 18.5ms | 181.2 MB | 7/7 | 134626900 |
| ruby | 1.894s | 16.7× | 6/7 | 1.934s | 40.0ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 113.5ms | 1.0× | 1/7 | 135.7ms | 22.2ms | 27.9 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 159.4ms | 1.3× | 3/7 | 191.3ms | 31.9ms | 110.2 MB | 5/7 | 500 |
| clojure | 801.6ms | 6.3× | 7/7 | 1.138s | 336.6ms | 341.0 MB | 6/7 | 500 |
| elixir | 565.5ms | 4.4× | 6/7 | 750.1ms | 184.6ms | 491.8 MB | 7/7 | 500 |
| python | 174.1ms | 1.4× | 4/7 | 184.2ms | 10.1ms | 46.9 MB | 2/7 | 500 |
| node | 127.1ms | 1.0× | 1/7 | 145.6ms | 18.5ms | 64.6 MB | 4/7 | 500 |
| ruby | 209.2ms | 1.6× | 5/7 | 249.2ms | 40.0ms | 45.8 MB | 1/7 | 500 |
| dotnet | 142.0ms | 1.1× | 2/7 | 164.2ms | 22.2ms | 48.0 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 257.6ms | 5.6× | 3/7 | 289.5ms | 31.9ms | 116.1 MB | 6/7 | 100000 |
| clojure | 596.6ms | 12.9× | 5/7 | 933.2ms | 336.6ms | 132.6 MB | 7/7 | 100000 |
| elixir | 46.1ms | 1.0× | 1/7 | 230.7ms | 184.6ms | 72.0 MB | 5/7 | 100000 |
| python | 819.5ms | 17.8× | 7/7 | 829.6ms | 10.1ms | 10.8 MB | 1/7 | 100000 |
| node | 639.8ms | 13.9× | 6/7 | 658.3ms | 18.5ms | 67.5 MB | 4/7 | 100000 |
| ruby | 591.8ms | 12.8× | 4/7 | 631.8ms | 40.0ms | 19.1 MB | 2/7 | 100000 |
| dotnet | 166.3ms | 3.6× | 2/7 | 188.5ms | 22.2ms | 27.7 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.426s | 12.5× | 4/7 | 1.458s | 31.9ms | 288.7 MB | 6/7 | 1000000 |
| clojure | 4.433s | 39.0× | 6/7 | 4.769s | 336.6ms | 746.2 MB | 7/7 | 1000000 |
| elixir | 256.2ms | 2.3× | 2/7 | 440.8ms | 184.6ms | 70.3 MB | 5/7 | 1000000 |
| python | 4.668s | 41.1× | 7/7 | 4.678s | 10.1ms | 16.2 MB | 1/7 | 1000000 |
| node | 113.7ms | 1.0× | 1/7 | 132.2ms | 18.5ms | 65.3 MB | 4/7 | 1000000 |
| ruby | 3.522s | 31.0× | 5/7 | 3.562s | 40.0ms | 23.1 MB | 2/7 | 1000000 |
| dotnet | 886.8ms | 7.8× | 3/7 | 909.0ms | 22.2ms | 30.3 MB | 3/7 | 1000000 |
