# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-27 10:32.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.3ms | 1.2× | 2/7 | 12.3ms | — | 20.2 MB | 3/7 | 0 |
| clojure | 340.5ms | 33.1× | 7/7 | 340.5ms | — | 103.2 MB | 7/7 | 0 |
| elixir | 180.5ms | 17.5× | 6/7 | 180.5ms | — | 71.7 MB | 6/7 | 0 |
| python | 10.3ms | 1.0× | 1/7 | 10.3ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.9ms | 1.7× | 3/7 | 17.9ms | — | 42.8 MB | 5/7 | 0 |
| ruby | 39.0ms | 3.8× | 5/7 | 39.0ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 22.0ms | 2.1× | 4/7 | 22.0ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.3ms | 1.7× | 2/7 | 87.6ms | 12.3ms | 24.2 MB | 3/7 | 9227465 |
| clojure | 208.7ms | 4.8× | 5/7 | 549.2ms | 340.5ms | 108.2 MB | 7/7 | 9227465 |
| elixir | 77.5ms | 1.8× | 3/7 | 258.0ms | 180.5ms | 72.4 MB | 6/7 | 9227465 |
| python | 763.3ms | 17.7× | 7/7 | 773.6ms | 10.3ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.7ms | 1.8× | 4/7 | 96.6ms | 17.9ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 636.2ms | 14.8× | 6/7 | 675.2ms | 39.0ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 43.1ms | 1.0× | 1/7 | 65.1ms | 22.0ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.5ms | 3.7× | 3/7 | 53.8ms | 12.3ms | 24.7 MB | 3/7 | 449999985000000 |
| clojure | 149.5ms | 13.3× | 5/7 | 490.0ms | 340.5ms | 108.2 MB | 7/7 | 449999985000000 |
| elixir | 58.7ms | 5.2× | 4/7 | 239.2ms | 180.5ms | 71.9 MB | 6/7 | 449999985000000 |
| python | 2.543s | 227.1× | 7/7 | 2.554s | 10.3ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 30.9ms | 2.8× | 2/7 | 48.8ms | 17.9ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 583.2ms | 52.1× | 6/7 | 622.2ms | 39.0ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 11.2ms | 1.0× | 1/7 | 33.2ms | 22.0ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 15.6ms | 12.3ms | 20.3 MB | 3/7 | 12499997500000 |
| clojure | 165.5ms | 50.2× | 5/7 | 506.0ms | 340.5ms | 220.5 MB | 7/7 | 12499997500000 |
| elixir | 27.9ms | 8.5× | 3/7 | 208.4ms | 180.5ms | 70.5 MB | 5/7 | 12499997500000 |
| python | 105.0ms | 31.8× | 4/7 | 115.3ms | 10.3ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 221.3ms | 67.1× | 6/7 | 239.2ms | 17.9ms | 90.2 MB | 6/7 | 12499997500000 |
| ruby | 223.0ms | 67.6× | 7/7 | 262.0ms | 39.0ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.1ms | 3.4× | 2/7 | 33.1ms | 22.0ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.2ms | 6.1× | 4/7 | 58.5ms | 12.3ms | 24.9 MB | 3/7 | 13848 |
| clojure | 140.3ms | 18.5× | 7/7 | 480.8ms | 340.5ms | 108.4 MB | 7/7 | 13848 |
| elixir | 18.3ms | 2.4× | 3/7 | 198.8ms | 180.5ms | 71.2 MB | 6/7 | 13848 |
| python | 121.0ms | 15.9× | 6/7 | 131.3ms | 10.3ms | 9.9 MB | 1/7 | 13848 |
| node | 8.9ms | 1.2× | 2/7 | 26.8ms | 17.9ms | 48.6 MB | 5/7 | 13848 |
| ruby | 115.8ms | 15.2× | 5/7 | 154.8ms | 39.0ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 7.6ms | 1.0× | 1/7 | 29.6ms | 22.0ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 85.5ms | 1.9× | 2/7 | 97.8ms | 12.3ms | 25.0 MB | 3/7 | 442 |
| clojure | 431.2ms | 9.4× | 5/7 | 771.7ms | 340.5ms | 370.9 MB | 7/7 | 442 |
| elixir | 104.9ms | 2.3× | 3/7 | 285.4ms | 180.5ms | 70.9 MB | 6/7 | 442 |
| python | 2.420s | 52.8× | 7/7 | 2.431s | 10.3ms | 9.9 MB | 1/7 | 442 |
| node | 174.7ms | 3.8× | 4/7 | 192.6ms | 17.9ms | 48.5 MB | 5/7 | 442 |
| ruby | 837.8ms | 18.3× | 6/7 | 876.8ms | 39.0ms | 19.2 MB | 2/7 | 442 |
| dotnet | 45.8ms | 1.0× | 1/7 | 67.8ms | 22.0ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.9ms | 9.6× | 4/7 | 185.2ms | 12.3ms | 25.0 MB | 3/7 | 6129302 |
| clojure | 155.2ms | 8.6× | 3/7 | 495.7ms | 340.5ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 260.3ms | 14.5× | 5/7 | 440.8ms | 180.5ms | 71.9 MB | 6/7 | 6129302 |
| python | 1.384s | 76.9× | 7/7 | 1.395s | 10.3ms | 10.0 MB | 1/7 | 6129302 |
| node | 19.6ms | 1.1× | 2/7 | 37.5ms | 17.9ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 422.7ms | 23.5× | 6/7 | 461.7ms | 39.0ms | 19.3 MB | 2/7 | 6129302 |
| dotnet | 18.0ms | 1.0× | 1/7 | 40.0ms | 22.0ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.7ms | 32.6× | 4/7 | 146.0ms | 12.3ms | 44.3 MB | 4/7 | 654353666 |
| clojure | 185.0ms | 45.1× | 5/7 | 525.5ms | 340.5ms | 117.8 MB | 7/7 | 654353666 |
| elixir | 58.6ms | 14.3× | 3/7 | 239.1ms | 180.5ms | 77.2 MB | 6/7 | 654353666 |
| python | 460.3ms | 112.3× | 7/7 | 470.6ms | 10.3ms | 10.3 MB | 1/7 | 654353666 |
| node | 17.6ms | 4.3× | 2/7 | 35.5ms | 17.9ms | 52.1 MB | 5/7 | 654353666 |
| ruby | 278.5ms | 67.9× | 6/7 | 317.5ms | 39.0ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 4.1ms | 1.0× | 1/7 | 26.1ms | 22.0ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.4ms | 1.0× | 1/7 | 24.7ms | 12.3ms | 30.8 MB | 1/7 | 3388889 |
| clojure | 155.6ms | 12.5× | 7/7 | 496.1ms | 340.5ms | 168.0 MB | 6/7 | 3388889 |
| elixir | 120.0ms | 9.7× | 6/7 | 300.5ms | 180.5ms | 201.4 MB | 7/7 | 3388889 |
| python | 42.9ms | 3.5× | 3/7 | 53.2ms | 10.3ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.9ms | 5.2× | 4/7 | 82.8ms | 17.9ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 82.0ms | 6.6× | 5/7 | 121.0ms | 39.0ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.6ms | 2.5× | 2/7 | 52.6ms | 22.0ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.3ms | 1.2× | 2/7 | 47.6ms | 12.3ms | 25.9 MB | 3/7 | 374854840 |
| clojure | 262.5ms | 8.6× | 7/7 | 603.0ms | 340.5ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 172.3ms | 5.6× | 5/7 | 352.8ms | 180.5ms | 70.5 MB | 6/7 | 374854840 |
| python | 177.2ms | 5.8× | 6/7 | 187.5ms | 10.3ms | 10.0 MB | 1/7 | 374854840 |
| node | 30.6ms | 1.0× | 1/7 | 48.5ms | 17.9ms | 50.1 MB | 5/7 | 374854840 |
| ruby | 71.3ms | 2.3× | 4/7 | 110.3ms | 39.0ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 36.6ms | 1.2× | 3/7 | 58.6ms | 22.0ms | 27.3 MB | 4/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.0ms | 11.1× | 6/7 | 125.3ms | 12.3ms | 56.2 MB | 5/7 | 1638200 |
| clojure | 166.0ms | 16.3× | 7/7 | 506.5ms | 340.5ms | 150.5 MB | 7/7 | 1638200 |
| elixir | 10.2ms | 1.0× | 1/7 | 190.7ms | 180.5ms | 72.9 MB | 6/7 | 1638200 |
| python | 97.1ms | 9.5× | 5/7 | 107.4ms | 10.3ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.4ms | 2.1× | 3/7 | 39.3ms | 17.9ms | 56.1 MB | 4/7 | 1638200 |
| ruby | 97.1ms | 9.5× | 4/7 | 136.1ms | 39.0ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.1ms | 1.4× | 2/7 | 36.1ms | 22.0ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.6ms | 3.0× | 6/7 | 205.9ms | 12.3ms | 188.2 MB | 7/7 | 46468819 |
| clojure | 241.0ms | 3.7× | 7/7 | 581.5ms | 340.5ms | 123.4 MB | 5/7 | 46468819 |
| elixir | 114.8ms | 1.8× | 4/7 | 295.3ms | 180.5ms | 157.4 MB | 6/7 | 46468819 |
| python | 180.9ms | 2.8× | 5/7 | 191.2ms | 10.3ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.0ms | 1.6× | 3/7 | 121.9ms | 17.9ms | 64.9 MB | 4/7 | 46468819 |
| ruby | 73.0ms | 1.1× | 2/7 | 112.0ms | 39.0ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 64.9ms | 1.0× | 1/7 | 86.9ms | 22.0ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.2ms | 11.6× | 5/7 | 95.5ms | 12.3ms | 41.4 MB | 4/7 | 724 |
| clojure | 190.4ms | 26.4× | 7/7 | 530.9ms | 340.5ms | 136.1 MB | 7/7 | 724 |
| elixir | 7.5ms | 1.0× | 2/7 | 188.0ms | 180.5ms | 70.2 MB | 6/7 | 724 |
| python | 54.0ms | 7.5× | 4/7 | 64.3ms | 10.3ms | 9.8 MB | 1/7 | 724 |
| node | 7.2ms | 1.0× | 1/7 | 25.1ms | 17.9ms | 50.6 MB | 5/7 | 724 |
| ruby | 122.3ms | 17.0× | 6/7 | 161.3ms | 39.0ms | 19.4 MB | 2/7 | 724 |
| dotnet | 19.1ms | 2.7× | 3/7 | 41.1ms | 22.0ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.2ms | 2.2× | 2/7 | 59.5ms | 12.3ms | 24.9 MB | 3/7 | 9900000 |
| clojure | 1.100s | 51.6× | 7/7 | 1.440s | 340.5ms | 371.0 MB | 7/7 | 9900000 |
| elixir | 21.3ms | 1.0× | 1/7 | 201.8ms | 180.5ms | 70.9 MB | 6/7 | 9900000 |
| python | 48.7ms | 2.3× | 3/7 | 59.0ms | 10.3ms | 9.8 MB | 1/7 | 9900000 |
| node | 569.0ms | 26.7× | 6/7 | 586.9ms | 17.9ms | 50.1 MB | 5/7 | 9900000 |
| ruby | 109.2ms | 5.1× | 4/7 | 148.2ms | 39.0ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 290.4ms | 13.6× | 5/7 | 312.4ms | 22.0ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.3ms | 4.2× | 2/7 | 58.6ms | 12.3ms | 25.1 MB | 2/7 | 2475000 |
| clojure | 1.330s | 122.0× | 7/7 | 1.671s | 340.5ms | 374.6 MB | 7/7 | 2475000 |
| elixir | 10.9ms | 1.0× | 1/7 | 191.4ms | 180.5ms | 70.9 MB | 6/7 | 2475000 |
| python | 230.7ms | 21.2× | 5/7 | 241.0ms | 10.3ms | 9.8 MB | 1/7 | 2475000 |
| node | 209.1ms | 19.2× | 4/7 | 227.0ms | 17.9ms | 50.2 MB | 5/7 | 2475000 |
| ruby | 111.6ms | 10.2× | 3/7 | 150.6ms | 39.0ms | 25.9 MB | 3/7 | 2475000 |
| dotnet | 682.7ms | 62.6× | 6/7 | 704.7ms | 22.0ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.5ms | 8.1× | 6/7 | 44.8ms | 12.3ms | 25.0 MB | 3/7 | 155553889038886 |
| clojure | 133.6ms | 33.4× | 7/7 | 474.1ms | 340.5ms | 108.4 MB | 7/7 | 155553889038886 |
| elixir | 10.1ms | 2.5× | 5/7 | 190.6ms | 180.5ms | 70.9 MB | 6/7 | 155553889038886 |
| python | 4.0ms | 1.0× | 1/7 | 14.3ms | 10.3ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 9.4ms | 2.4× | 4/7 | 27.3ms | 17.9ms | 52.0 MB | 5/7 | 155553889038886 |
| ruby | 7.1ms | 1.8× | 3/7 | 46.1ms | 39.0ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 6.9ms | 1.7× | 2/7 | 28.9ms | 22.0ms | 28.1 MB | 4/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 359.8ms | 1.5× | 3/7 | 372.1ms | 12.3ms | 25.2 MB | 3/7 | 24558 |
| clojure | 539.0ms | 2.2× | 5/7 | 879.5ms | 340.5ms | 374.6 MB | 7/7 | 24558 |
| elixir | 282.9ms | 1.2× | 2/7 | 463.4ms | 180.5ms | 72.9 MB | 6/7 | 24558 |
| python | 3.825s | 15.8× | 7/7 | 3.835s | 10.3ms | 11.1 MB | 1/7 | 24558 |
| node | 393.9ms | 1.6× | 4/7 | 411.8ms | 17.9ms | 48.4 MB | 5/7 | 24558 |
| ruby | 1.663s | 6.9× | 6/7 | 1.702s | 39.0ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 242.7ms | 1.0× | 1/7 | 264.7ms | 22.0ms | 26.1 MB | 4/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 12.9× | 3/7 | 48.4ms | 12.3ms | 32.8 MB | 4/7 | 78498 |
| clojure | 134.5ms | 48.0× | 7/7 | 475.0ms | 340.5ms | 108.9 MB | 7/7 | 78498 |
| elixir | 58.2ms | 20.8× | 4/7 | 238.7ms | 180.5ms | 80.4 MB | 6/7 | 78498 |
| python | 120.7ms | 43.1× | 6/7 | 131.0ms | 10.3ms | 10.7 MB | 1/7 | 78498 |
| node | 6.1ms | 2.2× | 2/7 | 24.0ms | 17.9ms | 49.5 MB | 5/7 | 78498 |
| ruby | 84.0ms | 30.0× | 5/7 | 123.0ms | 39.0ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 2.8ms | 1.0× | 1/7 | 24.8ms | 22.0ms | 27.4 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.9ms | 2.8× | 4/7 | 75.2ms | 12.3ms | 71.3 MB | 5/7 | 30039386344 |
| clojure | 292.9ms | 13.3× | 7/7 | 633.4ms | 340.5ms | 291.0 MB | 7/7 | 30039386344 |
| elixir | 117.4ms | 5.3× | 6/7 | 297.9ms | 180.5ms | 99.6 MB | 6/7 | 30039386344 |
| python | 81.9ms | 3.7× | 5/7 | 92.2ms | 10.3ms | 14.8 MB | 1/7 | 30039386344 |
| node | 23.1ms | 1.0× | 2/7 | 41.0ms | 17.9ms | 54.1 MB | 4/7 | 30039386344 |
| ruby | 39.1ms | 1.8× | 3/7 | 78.1ms | 39.0ms | 21.6 MB | 2/7 | 30039386344 |
| dotnet | 22.1ms | 1.0× | 1/7 | 44.1ms | 22.0ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 327.1ms | 52.8× | 6/7 | 339.4ms | 12.3ms | 55.2 MB | 5/7 | -169078071 |
| clojure | 176.9ms | 28.5× | 4/7 | 517.4ms | 340.5ms | 109.1 MB | 7/7 | -169078071 |
| elixir | 138.7ms | 22.4× | 3/7 | 319.2ms | 180.5ms | 71.9 MB | 6/7 | -169078071 |
| python | 690.4ms | 111.4× | 7/7 | 700.7ms | 10.3ms | 10.4 MB | 1/7 | -169078071 |
| node | 12.9ms | 2.1× | 2/7 | 30.8ms | 17.9ms | 50.5 MB | 4/7 | -169078071 |
| ruby | 290.8ms | 46.9× | 5/7 | 329.8ms | 39.0ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 6.2ms | 1.0× | 1/7 | 28.2ms | 22.0ms | 27.0 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.4ms | 87.3× | 6/7 | 160.7ms | 12.3ms | 75.7 MB | 6/7 | 1489952542 |
| clojure | 382.9ms | 225.2× | 7/7 | 723.4ms | 340.5ms | 171.5 MB | 7/7 | 1489952542 |
| elixir | 3.4ms | 2.0× | 2/7 | 183.9ms | 180.5ms | 74.3 MB | 5/7 | 1489952542 |
| python | 8.1ms | 4.8× | 4/7 | 18.4ms | 10.3ms | 12.4 MB | 1/7 | 1489952542 |
| node | 1.7ms | 1.0× | 1/7 | 19.6ms | 17.9ms | 44.0 MB | 4/7 | 1489952542 |
| ruby | 4.2ms | 2.5× | 3/7 | 43.2ms | 39.0ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 42.5ms | 25.0× | 5/7 | 64.5ms | 22.0ms | 34.2 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.7ms | 21.9× | 6/7 | 100.0ms | 12.3ms | 42.9 MB | 4/7 | 10000 |
| clojure | 128.2ms | 32.0× | 7/7 | 468.7ms | 340.5ms | 108.5 MB | 7/7 | 10000 |
| elixir | 15.9ms | 4.0× | 5/7 | 196.4ms | 180.5ms | 72.4 MB | 6/7 | 10000 |
| python | 12.6ms | 3.1× | 3/7 | 22.9ms | 10.3ms | 11.1 MB | 1/7 | 10000 |
| node | 4.0ms | 1.0× | 1/7 | 21.9ms | 17.9ms | 50.4 MB | 5/7 | 10000 |
| ruby | 6.9ms | 1.7× | 2/7 | 45.9ms | 39.0ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.9ms | 3.2× | 4/7 | 34.9ms | 22.0ms | 31.9 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.1ms | 27.5× | 6/7 | 119.4ms | 12.3ms | 101.6 MB | 6/7 | 12081249 |
| clojure | 168.2ms | 43.1× | 7/7 | 508.7ms | 340.5ms | 109.2 MB | 7/7 | 12081249 |
| elixir | 8.0ms | 2.1× | 4/7 | 188.5ms | 180.5ms | 77.5 MB | 5/7 | 12081249 |
| python | 13.1ms | 3.4× | 5/7 | 23.4ms | 10.3ms | 10.2 MB | 1/7 | 12081249 |
| node | 5.6ms | 1.4× | 2/7 | 23.5ms | 17.9ms | 50.9 MB | 4/7 | 12081249 |
| ruby | 7.8ms | 2.0× | 3/7 | 46.8ms | 39.0ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 3.9ms | 1.0× | 1/7 | 25.9ms | 22.0ms | 27.2 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 46.9ms | 2.7× | 3/7 | 59.2ms | 12.3ms | 46.5 MB | 3/7 | 6100000 |
| clojure | 181.4ms | 10.4× | 5/7 | 521.9ms | 340.5ms | 133.4 MB | 6/7 | 6100000 |
| elixir | 20.9ms | 1.2× | 2/7 | 201.4ms | 180.5ms | 77.3 MB | 5/7 | 6100000 |
| python | 557.5ms | 31.9× | 6/7 | 567.8ms | 10.3ms | 28.0 MB | 1/7 | 6100000 |
| node | 52.7ms | 3.0× | 4/7 | 70.6ms | 17.9ms | 51.5 MB | 4/7 | 6100000 |
| ruby | 1.561s | 89.2× | 7/7 | 1.600s | 39.0ms | 133.7 MB | 7/7 | 6100000 |
| dotnet | 17.5ms | 1.0× | 1/7 | 39.5ms | 22.0ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 217.7ms | 2.0× | 2/7 | 230.0ms | 12.3ms | 27.1 MB | 3/7 | 134626900 |
| clojure | 366.6ms | 3.4× | 5/7 | 707.1ms | 340.5ms | 138.8 MB | 6/7 | 134626900 |
| elixir | 288.3ms | 2.6× | 4/7 | 468.8ms | 180.5ms | 70.9 MB | 5/7 | 134626900 |
| python | 2.423s | 22.2× | 7/7 | 2.434s | 10.3ms | 21.9 MB | 2/7 | 134626900 |
| node | 287.4ms | 2.6× | 3/7 | 305.3ms | 17.9ms | 182.1 MB | 7/7 | 134626900 |
| ruby | 1.776s | 16.2× | 6/7 | 1.815s | 39.0ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 109.3ms | 1.0× | 1/7 | 131.3ms | 22.0ms | 28.2 MB | 4/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 166.9ms | 1.4× | 3/7 | 179.2ms | 12.3ms | 85.1 MB | 5/7 | 500 |
| clojure | 795.1ms | 6.9× | 7/7 | 1.136s | 340.5ms | 303.2 MB | 6/7 | 500 |
| elixir | 559.7ms | 4.8× | 6/7 | 740.2ms | 180.5ms | 522.8 MB | 7/7 | 500 |
| python | 174.1ms | 1.5× | 4/7 | 184.4ms | 10.3ms | 45.4 MB | 1/7 | 500 |
| node | 115.8ms | 1.0× | 1/7 | 133.7ms | 17.9ms | 64.8 MB | 4/7 | 500 |
| ruby | 199.4ms | 1.7× | 5/7 | 238.4ms | 39.0ms | 45.8 MB | 2/7 | 500 |
| dotnet | 145.4ms | 1.3× | 2/7 | 167.4ms | 22.0ms | 47.8 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 188.3ms | 3.5× | 3/7 | 200.6ms | 12.3ms | 47.5 MB | 4/7 | 100000 |
| clojure | 567.4ms | 10.5× | 4/7 | 907.9ms | 340.5ms | 133.9 MB | 7/7 | 100000 |
| elixir | 54.0ms | 1.0× | 1/7 | 234.5ms | 180.5ms | 71.3 MB | 6/7 | 100000 |
| python | 791.4ms | 14.7× | 7/7 | 801.7ms | 10.3ms | 10.9 MB | 1/7 | 100000 |
| node | 636.4ms | 11.8× | 6/7 | 654.3ms | 17.9ms | 67.3 MB | 5/7 | 100000 |
| ruby | 588.4ms | 10.9× | 5/7 | 627.4ms | 39.0ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 159.5ms | 3.0× | 2/7 | 181.5ms | 22.0ms | 27.6 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 716.4ms | 6.3× | 3/7 | 728.7ms | 12.3ms | 98.0 MB | 6/7 | 1000000 |
| clojure | 4.309s | 37.9× | 6/7 | 4.649s | 340.5ms | 762.0 MB | 7/7 | 1000000 |
| elixir | 258.9ms | 2.3× | 2/7 | 439.4ms | 180.5ms | 72.1 MB | 5/7 | 1000000 |
| python | 4.575s | 40.2× | 7/7 | 4.585s | 10.3ms | 16.1 MB | 1/7 | 1000000 |
| node | 113.7ms | 1.0× | 1/7 | 131.6ms | 17.9ms | 65.3 MB | 4/7 | 1000000 |
| ruby | 3.377s | 29.7× | 5/7 | 3.416s | 39.0ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 721.3ms | 6.3× | 4/7 | 743.3ms | 22.0ms | 30.7 MB | 3/7 | 1000000 |
