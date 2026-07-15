# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-15 18:22.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.5ms | 3.0× | 4/7 | 31.5ms | — | 19.7 MB | 3/7 | 0 |
| clojure | 336.3ms | 32.3× | 7/7 | 336.3ms | — | 103.5 MB | 7/7 | 0 |
| elixir | 183.9ms | 17.7× | 6/7 | 183.9ms | — | 72.7 MB | 6/7 | 0 |
| python | 10.4ms | 1.0× | 1/7 | 10.4ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.9ms | 1.7× | 2/7 | 17.9ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 40.2ms | 3.9× | 5/7 | 40.2ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 23.3ms | 2.2× | 3/7 | 23.3ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 59.1ms | 1.4× | 2/7 | 90.6ms | 31.5ms | 23.3 MB | 3/7 | 9227465 |
| clojure | 201.5ms | 4.7× | 5/7 | 537.8ms | 336.3ms | 108.5 MB | 7/7 | 9227465 |
| elixir | 77.8ms | 1.8× | 4/7 | 261.7ms | 183.9ms | 72.9 MB | 6/7 | 9227465 |
| python | 736.6ms | 17.2× | 7/7 | 747.0ms | 10.4ms | 9.8 MB | 1/7 | 9227465 |
| node | 74.0ms | 1.7× | 3/7 | 91.9ms | 17.9ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 602.1ms | 14.0× | 6/7 | 642.3ms | 40.2ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 42.9ms | 1.0× | 1/7 | 66.2ms | 23.3ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 282.4ms | 25.4× | 5/7 | 313.9ms | 31.5ms | 23.5 MB | 3/7 | 449999985000000 |
| clojure | 146.2ms | 13.2× | 4/7 | 482.5ms | 336.3ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 49.9ms | 4.5× | 3/7 | 233.8ms | 183.9ms | 70.2 MB | 6/7 | 449999985000000 |
| python | 2.255s | 203.2× | 7/7 | 2.266s | 10.4ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.0ms | 2.7× | 2/7 | 47.9ms | 17.9ms | 49.9 MB | 5/7 | 449999985000000 |
| ruby | 589.2ms | 53.1× | 6/7 | 629.4ms | 40.2ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 11.1ms | 1.0× | 1/7 | 34.4ms | 23.3ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.6ms | 1.0× | 1/7 | 35.1ms | 31.5ms | 19.9 MB | 3/7 | 12499997500000 |
| clojure | 175.2ms | 48.7× | 5/7 | 511.5ms | 336.3ms | 221.2 MB | 7/7 | 12499997500000 |
| elixir | 28.5ms | 7.9× | 3/7 | 212.4ms | 183.9ms | 72.4 MB | 5/7 | 12499997500000 |
| python | 105.0ms | 29.2× | 4/7 | 115.4ms | 10.4ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 218.6ms | 60.7× | 6/7 | 236.5ms | 17.9ms | 90.1 MB | 6/7 | 12499997500000 |
| ruby | 222.6ms | 61.8× | 7/7 | 262.8ms | 40.2ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 10.5ms | 2.9× | 2/7 | 33.8ms | 23.3ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 48.8ms | 7.3× | 4/7 | 80.3ms | 31.5ms | 23.8 MB | 3/7 | 13848 |
| clojure | 142.7ms | 21.3× | 7/7 | 479.0ms | 336.3ms | 108.5 MB | 7/7 | 13848 |
| elixir | 18.0ms | 2.7× | 3/7 | 201.9ms | 183.9ms | 70.4 MB | 6/7 | 13848 |
| python | 119.9ms | 17.9× | 6/7 | 130.3ms | 10.4ms | 9.9 MB | 1/7 | 13848 |
| node | 9.4ms | 1.4× | 2/7 | 27.3ms | 17.9ms | 48.5 MB | 5/7 | 13848 |
| ruby | 114.5ms | 17.1× | 5/7 | 154.7ms | 40.2ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 6.7ms | 1.0× | 1/7 | 30.0ms | 23.3ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 138.9ms | 3.0× | 3/7 | 170.4ms | 31.5ms | 23.5 MB | 3/7 | 442 |
| clojure | 428.1ms | 9.3× | 5/7 | 764.4ms | 336.3ms | 370.7 MB | 7/7 | 442 |
| elixir | 104.1ms | 2.3× | 2/7 | 288.0ms | 183.9ms | 71.4 MB | 6/7 | 442 |
| python | 2.482s | 53.8× | 7/7 | 2.492s | 10.4ms | 9.8 MB | 1/7 | 442 |
| node | 174.7ms | 3.8× | 4/7 | 192.6ms | 17.9ms | 48.5 MB | 5/7 | 442 |
| ruby | 874.8ms | 19.0× | 6/7 | 915.0ms | 40.2ms | 19.1 MB | 2/7 | 442 |
| dotnet | 46.1ms | 1.0× | 1/7 | 69.4ms | 23.3ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 252.3ms | 15.3× | 5/7 | 283.8ms | 31.5ms | 23.7 MB | 3/7 | 6129302 |
| clojure | 169.8ms | 10.3× | 3/7 | 506.1ms | 336.3ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 251.5ms | 15.2× | 4/7 | 435.4ms | 183.9ms | 72.8 MB | 6/7 | 6129302 |
| python | 1.378s | 83.5× | 7/7 | 1.388s | 10.4ms | 9.9 MB | 1/7 | 6129302 |
| node | 21.1ms | 1.3× | 2/7 | 39.0ms | 17.9ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 434.9ms | 26.4× | 6/7 | 475.1ms | 40.2ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 16.5ms | 1.0× | 1/7 | 39.8ms | 23.3ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 131.9ms | 34.7× | 4/7 | 163.4ms | 31.5ms | 37.2 MB | 4/7 | 654353666 |
| clojure | 201.2ms | 52.9× | 5/7 | 537.5ms | 336.3ms | 117.5 MB | 7/7 | 654353666 |
| elixir | 61.9ms | 16.3× | 3/7 | 245.8ms | 183.9ms | 77.4 MB | 6/7 | 654353666 |
| python | 454.6ms | 119.6× | 7/7 | 465.0ms | 10.4ms | 10.3 MB | 1/7 | 654353666 |
| node | 16.7ms | 4.4× | 2/7 | 34.6ms | 17.9ms | 52.3 MB | 5/7 | 654353666 |
| ruby | 277.1ms | 72.9× | 6/7 | 317.3ms | 40.2ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 3.8ms | 1.0× | 1/7 | 27.1ms | 23.3ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.4ms | 1.0× | 1/7 | 44.9ms | 31.5ms | 30.0 MB | 1/7 | 3388889 |
| clojure | 167.5ms | 12.5× | 7/7 | 503.8ms | 336.3ms | 168.1 MB | 6/7 | 3388889 |
| elixir | 116.8ms | 8.7× | 6/7 | 300.7ms | 183.9ms | 199.3 MB | 7/7 | 3388889 |
| python | 43.5ms | 3.2× | 3/7 | 53.9ms | 10.4ms | 39.9 MB | 2/7 | 3388889 |
| node | 65.8ms | 4.9× | 4/7 | 83.7ms | 17.9ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 82.7ms | 6.2× | 5/7 | 122.9ms | 40.2ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 29.2ms | 2.2× | 2/7 | 52.5ms | 23.3ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.9ms | 1.8× | 3/7 | 84.4ms | 31.5ms | 24.6 MB | 3/7 | 374854840 |
| clojure | 274.8ms | 9.1× | 7/7 | 611.1ms | 336.3ms | 302.4 MB | 7/7 | 374854840 |
| elixir | 171.3ms | 5.7× | 6/7 | 355.2ms | 183.9ms | 70.9 MB | 6/7 | 374854840 |
| python | 171.0ms | 5.7× | 5/7 | 181.4ms | 10.4ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.1ms | 1.0× | 1/7 | 48.0ms | 17.9ms | 50.1 MB | 5/7 | 374854840 |
| ruby | 68.3ms | 2.3× | 4/7 | 108.5ms | 40.2ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 35.6ms | 1.2× | 2/7 | 58.9ms | 23.3ms | 27.1 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.9ms | 8.4× | 6/7 | 133.4ms | 31.5ms | 47.5 MB | 4/7 | 1638200 |
| clojure | 167.2ms | 13.8× | 7/7 | 503.5ms | 336.3ms | 149.7 MB | 7/7 | 1638200 |
| elixir | 12.8ms | 1.1× | 2/7 | 196.7ms | 183.9ms | 71.3 MB | 6/7 | 1638200 |
| python | 95.7ms | 7.9× | 4/7 | 106.1ms | 10.4ms | 10.1 MB | 1/7 | 1638200 |
| node | 22.9ms | 1.9× | 3/7 | 40.8ms | 17.9ms | 56.0 MB | 5/7 | 1638200 |
| ruby | 97.5ms | 8.1× | 5/7 | 137.7ms | 40.2ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 12.1ms | 1.0× | 1/7 | 35.4ms | 23.3ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.1ms | 3.5× | 6/7 | 249.6ms | 31.5ms | 183.3 MB | 7/7 | 46468819 |
| clojure | 255.5ms | 4.0× | 7/7 | 591.8ms | 336.3ms | 123.2 MB | 5/7 | 46468819 |
| elixir | 112.4ms | 1.8× | 4/7 | 296.3ms | 183.9ms | 158.9 MB | 6/7 | 46468819 |
| python | 180.3ms | 2.9× | 5/7 | 190.7ms | 10.4ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.5ms | 1.7× | 3/7 | 122.4ms | 17.9ms | 64.9 MB | 4/7 | 46468819 |
| ruby | 69.6ms | 1.1× | 2/7 | 109.8ms | 40.2ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 63.2ms | 1.0× | 1/7 | 86.5ms | 23.3ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.1ms | 19.3× | 6/7 | 168.6ms | 31.5ms | 42.4 MB | 4/7 | 724 |
| clojure | 215.0ms | 30.3× | 7/7 | 551.3ms | 336.3ms | 132.5 MB | 7/7 | 724 |
| elixir | 7.9ms | 1.1× | 2/7 | 191.8ms | 183.9ms | 72.2 MB | 6/7 | 724 |
| python | 54.0ms | 7.6× | 4/7 | 64.4ms | 10.4ms | 9.8 MB | 1/7 | 724 |
| node | 7.1ms | 1.0× | 1/7 | 25.0ms | 17.9ms | 50.5 MB | 5/7 | 724 |
| ruby | 120.7ms | 17.0× | 5/7 | 160.9ms | 40.2ms | 19.4 MB | 2/7 | 724 |
| dotnet | 17.7ms | 2.5× | 3/7 | 41.0ms | 23.3ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 1.9× | 2/7 | 70.4ms | 31.5ms | 23.6 MB | 3/7 | 9900000 |
| clojure | 1.110s | 54.9× | 7/7 | 1.446s | 336.3ms | 370.7 MB | 7/7 | 9900000 |
| elixir | 20.2ms | 1.0× | 1/7 | 204.1ms | 183.9ms | 70.4 MB | 6/7 | 9900000 |
| python | 50.3ms | 2.5× | 3/7 | 60.7ms | 10.4ms | 9.8 MB | 1/7 | 9900000 |
| node | 584.5ms | 28.9× | 6/7 | 602.4ms | 17.9ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 112.3ms | 5.6× | 4/7 | 152.5ms | 40.2ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 289.7ms | 14.3× | 5/7 | 313.0ms | 23.3ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.3ms | 4.0× | 2/7 | 70.8ms | 31.5ms | 23.8 MB | 2/7 | 2475000 |
| clojure | 1.348s | 136.2× | 7/7 | 1.684s | 336.3ms | 374.6 MB | 7/7 | 2475000 |
| elixir | 9.9ms | 1.0× | 1/7 | 193.8ms | 183.9ms | 70.4 MB | 6/7 | 2475000 |
| python | 238.0ms | 24.0× | 5/7 | 248.4ms | 10.4ms | 9.8 MB | 1/7 | 2475000 |
| node | 212.9ms | 21.5× | 4/7 | 230.8ms | 17.9ms | 50.1 MB | 5/7 | 2475000 |
| ruby | 110.4ms | 11.2× | 3/7 | 150.6ms | 40.2ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 688.5ms | 69.5× | 6/7 | 711.8ms | 23.3ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.8ms | 9.7× | 6/7 | 69.3ms | 31.5ms | 23.5 MB | 3/7 | 155553889038886 |
| clojure | 136.7ms | 35.1× | 7/7 | 473.0ms | 336.3ms | 109.6 MB | 7/7 | 155553889038886 |
| elixir | 6.7ms | 1.7× | 4/7 | 190.6ms | 183.9ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 1.0× | 1/7 | 14.3ms | 10.4ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 2.0× | 5/7 | 25.6ms | 17.9ms | 52.0 MB | 5/7 | 155553889038886 |
| ruby | 6.5ms | 1.7× | 3/7 | 46.7ms | 40.2ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 5.9ms | 1.5× | 2/7 | 29.2ms | 23.3ms | 27.9 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 345.4ms | 1.3× | 3/7 | 376.9ms | 31.5ms | 23.9 MB | 3/7 | 24558 |
| clojure | 563.9ms | 2.1× | 5/7 | 900.2ms | 336.3ms | 374.4 MB | 7/7 | 24558 |
| elixir | 283.7ms | 1.0× | 2/7 | 467.6ms | 183.9ms | 71.7 MB | 6/7 | 24558 |
| python | 3.921s | 14.4× | 7/7 | 3.931s | 10.4ms | 11.0 MB | 1/7 | 24558 |
| node | 399.2ms | 1.5× | 4/7 | 417.1ms | 17.9ms | 48.3 MB | 5/7 | 24558 |
| ruby | 1.650s | 6.0× | 6/7 | 1.690s | 40.2ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 273.0ms | 1.0× | 1/7 | 296.3ms | 23.3ms | 26.3 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 125.2ms | 78.3× | 6/7 | 156.7ms | 31.5ms | 58.6 MB | 5/7 | 78498 |
| clojure | 148.2ms | 92.6× | 7/7 | 484.5ms | 336.3ms | 108.1 MB | 7/7 | 78498 |
| elixir | 54.2ms | 33.9× | 3/7 | 238.1ms | 183.9ms | 78.0 MB | 6/7 | 78498 |
| python | 115.1ms | 71.9× | 5/7 | 125.5ms | 10.4ms | 10.8 MB | 1/7 | 78498 |
| node | 6.0ms | 3.8× | 2/7 | 23.9ms | 17.9ms | 49.5 MB | 4/7 | 78498 |
| ruby | 83.6ms | 52.3× | 4/7 | 123.8ms | 40.2ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 1.6ms | 1.0× | 1/7 | 24.9ms | 23.3ms | 27.4 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.2ms | 5.0× | 5/7 | 138.7ms | 31.5ms | 75.2 MB | 5/7 | 30039386344 |
| clojure | 306.2ms | 14.4× | 7/7 | 642.5ms | 336.3ms | 291.3 MB | 7/7 | 30039386344 |
| elixir | 118.1ms | 5.5× | 6/7 | 302.0ms | 183.9ms | 99.4 MB | 6/7 | 30039386344 |
| python | 78.0ms | 3.7× | 4/7 | 88.4ms | 10.4ms | 14.8 MB | 1/7 | 30039386344 |
| node | 22.6ms | 1.1× | 2/7 | 40.5ms | 17.9ms | 53.9 MB | 4/7 | 30039386344 |
| ruby | 38.4ms | 1.8× | 3/7 | 78.6ms | 40.2ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 21.3ms | 1.0× | 1/7 | 44.6ms | 23.3ms | 30.2 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 504.1ms | 95.1× | 6/7 | 535.6ms | 31.5ms | 44.0 MB | 4/7 | -169078071 |
| clojure | 184.2ms | 34.8× | 4/7 | 520.5ms | 336.3ms | 109.2 MB | 7/7 | -169078071 |
| elixir | 137.0ms | 25.8× | 3/7 | 320.9ms | 183.9ms | 73.1 MB | 6/7 | -169078071 |
| python | 690.3ms | 130.2× | 7/7 | 700.7ms | 10.4ms | 10.3 MB | 1/7 | -169078071 |
| node | 12.5ms | 2.4× | 2/7 | 30.4ms | 17.9ms | 50.1 MB | 5/7 | -169078071 |
| ruby | 300.5ms | 56.7× | 5/7 | 340.7ms | 40.2ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 5.3ms | 1.0× | 1/7 | 28.6ms | 23.3ms | 26.9 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 269.1ms | 149.5× | 6/7 | 300.6ms | 31.5ms | 107.2 MB | 6/7 | 1489952542 |
| clojure | 389.0ms | 216.1× | 7/7 | 725.3ms | 336.3ms | 157.8 MB | 7/7 | 1489952542 |
| elixir | 5.9ms | 3.3× | 3/7 | 189.8ms | 183.9ms | 73.8 MB | 5/7 | 1489952542 |
| python | 9.0ms | 5.0× | 4/7 | 19.4ms | 10.4ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.8ms | 1.0× | 1/7 | 19.7ms | 17.9ms | 43.9 MB | 4/7 | 1489952542 |
| ruby | 3.1ms | 1.7× | 2/7 | 43.3ms | 40.2ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 42.6ms | 23.7× | 5/7 | 65.9ms | 23.3ms | 34.0 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 557.7ms | 146.8× | 7/7 | 589.2ms | 31.5ms | 178.1 MB | 7/7 | 10000 |
| clojure | 139.9ms | 36.8× | 6/7 | 476.2ms | 336.3ms | 108.7 MB | 6/7 | 10000 |
| elixir | 14.9ms | 3.9× | 5/7 | 198.8ms | 183.9ms | 70.5 MB | 5/7 | 10000 |
| python | 12.3ms | 3.2× | 4/7 | 22.7ms | 10.4ms | 11.0 MB | 1/7 | 10000 |
| node | 3.8ms | 1.0× | 1/7 | 21.7ms | 17.9ms | 50.3 MB | 4/7 | 10000 |
| ruby | 6.1ms | 1.6× | 2/7 | 46.3ms | 40.2ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.0ms | 3.2× | 3/7 | 35.3ms | 23.3ms | 31.8 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 135.7ms | 38.8× | 6/7 | 167.2ms | 31.5ms | 104.5 MB | 6/7 | 12081249 |
| clojure | 173.2ms | 49.5× | 7/7 | 509.5ms | 336.3ms | 109.6 MB | 7/7 | 12081249 |
| elixir | 9.2ms | 2.6× | 4/7 | 193.1ms | 183.9ms | 75.6 MB | 5/7 | 12081249 |
| python | 13.5ms | 3.9× | 5/7 | 23.9ms | 10.4ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.7ms | 1.6× | 2/7 | 23.6ms | 17.9ms | 50.8 MB | 4/7 | 12081249 |
| ruby | 7.2ms | 2.1× | 3/7 | 47.4ms | 40.2ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 3.5ms | 1.0× | 1/7 | 26.8ms | 23.3ms | 27.1 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.5ms | 3.1× | 3/7 | 83.0ms | 31.5ms | 51.9 MB | 4/7 | 6100000 |
| clojure | 198.5ms | 12.0× | 5/7 | 534.8ms | 336.3ms | 133.4 MB | 7/7 | 6100000 |
| elixir | 22.8ms | 1.4× | 2/7 | 206.7ms | 183.9ms | 76.4 MB | 5/7 | 6100000 |
| python | 542.9ms | 32.9× | 6/7 | 553.3ms | 10.4ms | 27.8 MB | 1/7 | 6100000 |
| node | 53.2ms | 3.2× | 4/7 | 71.1ms | 17.9ms | 51.5 MB | 3/7 | 6100000 |
| ruby | 1.592s | 96.5× | 7/7 | 1.632s | 40.2ms | 133.0 MB | 6/7 | 6100000 |
| dotnet | 16.5ms | 1.0× | 1/7 | 39.8ms | 23.3ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 214.0ms | 1.9× | 2/7 | 245.5ms | 31.5ms | 26.4 MB | 3/7 | 134626900 |
| clojure | 408.9ms | 3.6× | 5/7 | 745.2ms | 336.3ms | 137.2 MB | 6/7 | 134626900 |
| elixir | 316.6ms | 2.8× | 4/7 | 500.5ms | 183.9ms | 72.1 MB | 5/7 | 134626900 |
| python | 2.548s | 22.6× | 7/7 | 2.558s | 10.4ms | 21.8 MB | 2/7 | 134626900 |
| node | 303.7ms | 2.7× | 3/7 | 321.6ms | 17.9ms | 181.9 MB | 7/7 | 134626900 |
| ruby | 1.918s | 17.0× | 6/7 | 1.958s | 40.2ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 112.9ms | 1.0× | 1/7 | 136.2ms | 23.3ms | 28.2 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 158.9ms | 1.4× | 3/7 | 190.4ms | 31.5ms | 110.6 MB | 5/7 | 500 |
| clojure | 810.4ms | 6.9× | 7/7 | 1.147s | 336.3ms | 334.2 MB | 6/7 | 500 |
| elixir | 577.4ms | 4.9× | 6/7 | 761.3ms | 183.9ms | 493.7 MB | 7/7 | 500 |
| python | 175.8ms | 1.5× | 4/7 | 186.2ms | 10.4ms | 44.4 MB | 1/7 | 500 |
| node | 117.2ms | 1.0× | 1/7 | 135.1ms | 17.9ms | 64.5 MB | 4/7 | 500 |
| ruby | 210.8ms | 1.8× | 5/7 | 251.0ms | 40.2ms | 45.7 MB | 2/7 | 500 |
| dotnet | 151.2ms | 1.3× | 2/7 | 174.5ms | 23.3ms | 47.9 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 259.5ms | 5.0× | 3/7 | 291.0ms | 31.5ms | 101.0 MB | 6/7 | 100000 |
| clojure | 603.5ms | 11.7× | 4/7 | 939.8ms | 336.3ms | 132.8 MB | 7/7 | 100000 |
| elixir | 51.8ms | 1.0× | 1/7 | 235.7ms | 183.9ms | 70.0 MB | 5/7 | 100000 |
| python | 838.4ms | 16.2× | 7/7 | 848.8ms | 10.4ms | 10.8 MB | 1/7 | 100000 |
| node | 656.4ms | 12.7× | 6/7 | 674.3ms | 17.9ms | 67.2 MB | 4/7 | 100000 |
| ruby | 608.8ms | 11.8× | 5/7 | 649.0ms | 40.2ms | 19.1 MB | 2/7 | 100000 |
| dotnet | 163.2ms | 3.2× | 2/7 | 186.5ms | 23.3ms | 27.9 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.340s | 11.7× | 4/7 | 1.371s | 31.5ms | 285.9 MB | 6/7 | 1000000 |
| clojure | 4.560s | 39.7× | 6/7 | 4.896s | 336.3ms | 754.5 MB | 7/7 | 1000000 |
| elixir | 258.0ms | 2.2× | 2/7 | 441.9ms | 183.9ms | 70.6 MB | 5/7 | 1000000 |
| python | 4.806s | 41.8× | 7/7 | 4.816s | 10.4ms | 16.1 MB | 1/7 | 1000000 |
| node | 115.0ms | 1.0× | 1/7 | 132.9ms | 17.9ms | 65.3 MB | 4/7 | 1000000 |
| ruby | 3.565s | 31.0× | 5/7 | 3.606s | 40.2ms | 23.1 MB | 2/7 | 1000000 |
| dotnet | 828.2ms | 7.2× | 3/7 | 851.5ms | 23.3ms | 30.5 MB | 3/7 | 1000000 |
