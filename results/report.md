# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-13 18:05.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.7ms | 3.2× | 4/7 | 32.7ms | — | 25.1 MB | 3/7 | 0 |
| clojure | 341.3ms | 33.8× | 7/7 | 341.3ms | — | 102.3 MB | 7/7 | 0 |
| elixir | 183.3ms | 18.1× | 6/7 | 183.3ms | — | 69.7 MB | 6/7 | 0 |
| python | 10.1ms | 1.0× | 1/7 | 10.1ms | — | 9.4 MB | 1/7 | 0 |
| node | 18.0ms | 1.8× | 2/7 | 18.0ms | — | 42.2 MB | 5/7 | 0 |
| ruby | 38.8ms | 3.8× | 5/7 | 38.8ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 23.0ms | 2.3× | 3/7 | 23.0ms | — | 25.5 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.4ms | 1.2× | 2/7 | 86.1ms | 32.7ms | 28.7 MB | 4/7 | 9227465 |
| clojure | 198.5ms | 4.5× | 5/7 | 539.8ms | 341.3ms | 108.4 MB | 7/7 | 9227465 |
| elixir | 75.8ms | 1.7× | 3/7 | 259.1ms | 183.3ms | 72.8 MB | 6/7 | 9227465 |
| python | 752.7ms | 17.0× | 7/7 | 762.8ms | 10.1ms | 9.6 MB | 1/7 | 9227465 |
| node | 76.6ms | 1.7× | 4/7 | 94.6ms | 18.0ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 596.7ms | 13.4× | 6/7 | 635.5ms | 38.8ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 44.4ms | 1.0× | 1/7 | 67.4ms | 23.0ms | 25.5 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 304.3ms | 27.9× | 5/7 | 337.0ms | 32.7ms | 28.9 MB | 4/7 | 449999985000000 |
| clojure | 156.9ms | 14.4× | 4/7 | 498.2ms | 341.3ms | 108.6 MB | 7/7 | 449999985000000 |
| elixir | 62.0ms | 5.7× | 3/7 | 245.3ms | 183.3ms | 70.8 MB | 6/7 | 449999985000000 |
| python | 2.469s | 226.5× | 7/7 | 2.479s | 10.1ms | 9.4 MB | 1/7 | 449999985000000 |
| node | 30.3ms | 2.8× | 2/7 | 48.3ms | 18.0ms | 49.4 MB | 5/7 | 449999985000000 |
| ruby | 589.5ms | 54.1× | 6/7 | 628.3ms | 38.8ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 10.9ms | 1.0× | 1/7 | 33.9ms | 23.0ms | 26.1 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.1ms | 1.0× | 1/7 | 36.8ms | 32.7ms | 24.9 MB | 3/7 | 12499997500000 |
| clojure | 172.2ms | 42.0× | 5/7 | 513.5ms | 341.3ms | 220.3 MB | 7/7 | 12499997500000 |
| elixir | 34.6ms | 8.4× | 3/7 | 217.9ms | 183.3ms | 69.9 MB | 5/7 | 12499997500000 |
| python | 105.5ms | 25.7× | 4/7 | 115.6ms | 10.1ms | 10.3 MB | 1/7 | 12499997500000 |
| node | 226.1ms | 55.1× | 7/7 | 244.1ms | 18.0ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 225.6ms | 55.0× | 6/7 | 264.4ms | 38.8ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 10.3ms | 2.5× | 2/7 | 33.3ms | 23.0ms | 27.3 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 48.9ms | 6.6× | 4/7 | 81.6ms | 32.7ms | 28.8 MB | 4/7 | 13848 |
| clojure | 143.2ms | 19.4× | 7/7 | 484.5ms | 341.3ms | 108.4 MB | 7/7 | 13848 |
| elixir | 19.0ms | 2.6× | 3/7 | 202.3ms | 183.3ms | 71.8 MB | 6/7 | 13848 |
| python | 121.6ms | 16.4× | 6/7 | 131.7ms | 10.1ms | 9.7 MB | 1/7 | 13848 |
| node | 9.2ms | 1.2× | 2/7 | 27.2ms | 18.0ms | 48.2 MB | 5/7 | 13848 |
| ruby | 115.4ms | 15.6× | 5/7 | 154.2ms | 38.8ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 7.4ms | 1.0× | 1/7 | 30.4ms | 23.0ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 159.9ms | 3.5× | 3/7 | 192.6ms | 32.7ms | 28.9 MB | 4/7 | 442 |
| clojure | 418.4ms | 9.2× | 5/7 | 759.7ms | 341.3ms | 370.7 MB | 7/7 | 442 |
| elixir | 99.3ms | 2.2× | 2/7 | 282.6ms | 183.3ms | 72.2 MB | 6/7 | 442 |
| python | 2.399s | 52.6× | 7/7 | 2.409s | 10.1ms | 9.6 MB | 1/7 | 442 |
| node | 172.2ms | 3.8× | 4/7 | 190.2ms | 18.0ms | 47.8 MB | 5/7 | 442 |
| ruby | 873.0ms | 19.1× | 6/7 | 911.8ms | 38.8ms | 19.0 MB | 2/7 | 442 |
| dotnet | 45.6ms | 1.0× | 1/7 | 68.6ms | 23.0ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 263.1ms | 15.0× | 5/7 | 295.8ms | 32.7ms | 29.1 MB | 4/7 | 6129302 |
| clojure | 166.2ms | 9.5× | 3/7 | 507.5ms | 341.3ms | 114.5 MB | 7/7 | 6129302 |
| elixir | 246.9ms | 14.1× | 4/7 | 430.2ms | 183.3ms | 71.9 MB | 6/7 | 6129302 |
| python | 1.307s | 74.7× | 7/7 | 1.317s | 10.1ms | 9.7 MB | 1/7 | 6129302 |
| node | 19.5ms | 1.1× | 2/7 | 37.5ms | 18.0ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 418.6ms | 23.9× | 6/7 | 457.4ms | 38.8ms | 19.1 MB | 2/7 | 6129302 |
| dotnet | 17.5ms | 1.0× | 1/7 | 40.5ms | 23.0ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 138.7ms | 36.5× | 4/7 | 171.4ms | 32.7ms | 42.8 MB | 4/7 | 654353666 |
| clojure | 199.8ms | 52.6× | 5/7 | 541.1ms | 341.3ms | 118.1 MB | 7/7 | 654353666 |
| elixir | 57.5ms | 15.1× | 3/7 | 240.8ms | 183.3ms | 74.4 MB | 6/7 | 654353666 |
| python | 467.1ms | 122.9× | 7/7 | 477.2ms | 10.1ms | 10.1 MB | 1/7 | 654353666 |
| node | 16.4ms | 4.3× | 2/7 | 34.4ms | 18.0ms | 51.6 MB | 5/7 | 654353666 |
| ruby | 278.0ms | 73.2× | 6/7 | 316.8ms | 38.8ms | 19.2 MB | 2/7 | 654353666 |
| dotnet | 3.8ms | 1.0× | 1/7 | 26.8ms | 23.0ms | 26.4 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.3ms | 1.0× | 1/7 | 45.0ms | 32.7ms | 35.2 MB | 1/7 | 3388889 |
| clojure | 154.4ms | 12.6× | 7/7 | 495.7ms | 341.3ms | 167.1 MB | 6/7 | 3388889 |
| elixir | 113.7ms | 9.2× | 6/7 | 297.0ms | 183.3ms | 199.8 MB | 7/7 | 3388889 |
| python | 42.8ms | 3.5× | 3/7 | 52.9ms | 10.1ms | 39.7 MB | 2/7 | 3388889 |
| node | 64.8ms | 5.3× | 4/7 | 82.8ms | 18.0ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 82.3ms | 6.7× | 5/7 | 121.1ms | 38.8ms | 47.6 MB | 3/7 | 3388889 |
| dotnet | 30.0ms | 2.4× | 2/7 | 53.0ms | 23.0ms | 56.3 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.7ms | 4.0× | 4/7 | 152.4ms | 32.7ms | 30.3 MB | 4/7 | 374854840 |
| clojure | 268.7ms | 8.9× | 7/7 | 610.0ms | 341.3ms | 302.6 MB | 7/7 | 374854840 |
| elixir | 164.5ms | 5.4× | 5/7 | 347.8ms | 183.3ms | 70.1 MB | 6/7 | 374854840 |
| python | 175.2ms | 5.8× | 6/7 | 185.3ms | 10.1ms | 9.7 MB | 1/7 | 374854840 |
| node | 30.2ms | 1.0× | 1/7 | 48.2ms | 18.0ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 70.1ms | 2.3× | 3/7 | 108.9ms | 38.8ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 37.4ms | 1.2× | 2/7 | 60.4ms | 23.0ms | 26.9 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.8ms | 9.0× | 4/7 | 123.5ms | 32.7ms | 52.8 MB | 4/7 | 1638200 |
| clojure | 168.6ms | 16.7× | 7/7 | 509.9ms | 341.3ms | 148.8 MB | 7/7 | 1638200 |
| elixir | 10.1ms | 1.0× | 1/7 | 193.4ms | 183.3ms | 69.8 MB | 6/7 | 1638200 |
| python | 95.3ms | 9.4× | 5/7 | 105.4ms | 10.1ms | 9.9 MB | 1/7 | 1638200 |
| node | 21.0ms | 2.1× | 3/7 | 39.0ms | 18.0ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 95.7ms | 9.5× | 6/7 | 134.5ms | 38.8ms | 19.2 MB | 2/7 | 1638200 |
| dotnet | 13.2ms | 1.3× | 2/7 | 36.2ms | 23.0ms | 32.0 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 217.2ms | 3.4× | 6/7 | 249.9ms | 32.7ms | 187.0 MB | 7/7 | 46468819 |
| clojure | 247.8ms | 3.9× | 7/7 | 589.1ms | 341.3ms | 124.0 MB | 5/7 | 46468819 |
| elixir | 107.9ms | 1.7× | 4/7 | 291.2ms | 183.3ms | 158.0 MB | 6/7 | 46468819 |
| python | 178.7ms | 2.8× | 5/7 | 188.8ms | 10.1ms | 25.6 MB | 2/7 | 46468819 |
| node | 103.6ms | 1.6× | 3/7 | 121.6ms | 18.0ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 71.1ms | 1.1× | 2/7 | 109.9ms | 38.8ms | 24.7 MB | 1/7 | 46468819 |
| dotnet | 63.5ms | 1.0× | 1/7 | 86.5ms | 23.0ms | 29.4 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 134.2ms | 18.6× | 6/7 | 166.9ms | 32.7ms | 49.0 MB | 4/7 | 724 |
| clojure | 248.9ms | 34.6× | 7/7 | 590.2ms | 341.3ms | 134.9 MB | 7/7 | 724 |
| elixir | 8.1ms | 1.1× | 2/7 | 191.4ms | 183.3ms | 72.5 MB | 6/7 | 724 |
| python | 53.2ms | 7.4× | 4/7 | 63.3ms | 10.1ms | 9.6 MB | 1/7 | 724 |
| node | 7.2ms | 1.0× | 1/7 | 25.2ms | 18.0ms | 50.2 MB | 5/7 | 724 |
| ruby | 120.5ms | 16.7× | 5/7 | 159.3ms | 38.8ms | 19.2 MB | 2/7 | 724 |
| dotnet | 18.4ms | 2.6× | 3/7 | 41.4ms | 23.0ms | 29.0 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.7ms | 2.6× | 2/7 | 71.4ms | 32.7ms | 28.9 MB | 3/7 | 9900000 |
| clojure | 1.079s | 71.9× | 7/7 | 1.420s | 341.3ms | 371.1 MB | 7/7 | 9900000 |
| elixir | 15.0ms | 1.0× | 1/7 | 198.3ms | 183.3ms | 70.2 MB | 6/7 | 9900000 |
| python | 47.5ms | 3.2× | 3/7 | 57.6ms | 10.1ms | 9.6 MB | 1/7 | 9900000 |
| node | 612.3ms | 40.8× | 6/7 | 630.3ms | 18.0ms | 49.8 MB | 5/7 | 9900000 |
| ruby | 109.4ms | 7.3× | 4/7 | 148.2ms | 38.8ms | 21.6 MB | 2/7 | 9900000 |
| dotnet | 283.0ms | 18.9× | 5/7 | 306.0ms | 23.0ms | 32.6 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 247.1ms | 56.2× | 5/7 | 279.8ms | 32.7ms | 28.8 MB | 3/7 | 2475000 |
| clojure | 1.306s | 296.9× | 7/7 | 1.647s | 341.3ms | 374.1 MB | 7/7 | 2475000 |
| elixir | 4.4ms | 1.0× | 1/7 | 187.7ms | 183.3ms | 72.4 MB | 6/7 | 2475000 |
| python | 232.2ms | 52.8× | 4/7 | 242.3ms | 10.1ms | 9.6 MB | 1/7 | 2475000 |
| node | 207.0ms | 47.0× | 3/7 | 225.0ms | 18.0ms | 49.8 MB | 5/7 | 2475000 |
| ruby | 113.6ms | 25.8× | 2/7 | 152.4ms | 38.8ms | 25.7 MB | 2/7 | 2475000 |
| dotnet | 704.7ms | 160.2× | 6/7 | 727.7ms | 23.0ms | 32.7 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.3ms | 8.6× | 6/7 | 69.0ms | 32.7ms | 29.0 MB | 4/7 | 155553889038886 |
| clojure | 130.7ms | 31.1× | 7/7 | 472.0ms | 341.3ms | 108.4 MB | 7/7 | 155553889038886 |
| elixir | 5.7ms | 1.4× | 2/7 | 189.0ms | 183.3ms | 70.6 MB | 6/7 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/7 | 14.3ms | 10.1ms | 9.6 MB | 1/7 | 155553889038886 |
| node | 8.7ms | 2.1× | 5/7 | 26.7ms | 18.0ms | 51.7 MB | 5/7 | 155553889038886 |
| ruby | 8.2ms | 2.0× | 4/7 | 47.0ms | 38.8ms | 19.6 MB | 2/7 | 155553889038886 |
| dotnet | 6.0ms | 1.4× | 3/7 | 29.0ms | 23.0ms | 27.6 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 328.1ms | 1.4× | 3/7 | 360.8ms | 32.7ms | 29.1 MB | 4/7 | 24558 |
| clojure | 533.1ms | 2.2× | 5/7 | 874.4ms | 341.3ms | 374.5 MB | 7/7 | 24558 |
| elixir | 278.2ms | 1.2× | 2/7 | 461.5ms | 183.3ms | 70.3 MB | 6/7 | 24558 |
| python | 3.821s | 15.8× | 7/7 | 3.831s | 10.1ms | 10.8 MB | 1/7 | 24558 |
| node | 392.0ms | 1.6× | 4/7 | 410.0ms | 18.0ms | 48.1 MB | 5/7 | 24558 |
| ruby | 1.648s | 6.8× | 6/7 | 1.686s | 38.8ms | 19.5 MB | 2/7 | 24558 |
| dotnet | 241.9ms | 1.0× | 1/7 | 264.9ms | 23.0ms | 26.0 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.006s | 503.0× | 7/7 | 1.039s | 32.7ms | 416.9 MB | 7/7 | 78498 |
| clojure | 138.0ms | 69.0× | 6/7 | 479.3ms | 341.3ms | 108.5 MB | 6/7 | 78498 |
| elixir | 52.3ms | 26.1× | 3/7 | 235.6ms | 183.3ms | 78.6 MB | 5/7 | 78498 |
| python | 116.8ms | 58.4× | 5/7 | 126.9ms | 10.1ms | 10.6 MB | 1/7 | 78498 |
| node | 6.0ms | 3.0× | 2/7 | 24.0ms | 18.0ms | 49.2 MB | 4/7 | 78498 |
| ruby | 84.7ms | 42.4× | 4/7 | 123.5ms | 38.8ms | 26.6 MB | 2/7 | 78498 |
| dotnet | 2.0ms | 1.0× | 1/7 | 25.0ms | 23.0ms | 27.0 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 612.1ms | 29.0× | 7/7 | 644.8ms | 32.7ms | 237.3 MB | 6/7 | 30039386344 |
| clojure | 285.4ms | 13.5× | 6/7 | 626.7ms | 341.3ms | 290.5 MB | 7/7 | 30039386344 |
| elixir | 118.1ms | 5.6× | 5/7 | 301.4ms | 183.3ms | 98.8 MB | 5/7 | 30039386344 |
| python | 77.8ms | 3.7× | 4/7 | 87.9ms | 10.1ms | 14.7 MB | 1/7 | 30039386344 |
| node | 23.1ms | 1.1× | 2/7 | 41.1ms | 18.0ms | 53.8 MB | 4/7 | 30039386344 |
| ruby | 38.9ms | 1.8× | 3/7 | 77.7ms | 38.8ms | 21.4 MB | 2/7 | 30039386344 |
| dotnet | 21.1ms | 1.0× | 1/7 | 44.1ms | 23.0ms | 30.1 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 5.915s | 1019.7× | 7/7 | 5.947s | 32.7ms | 41.9 MB | 4/7 | -169078071 |
| clojure | 178.9ms | 30.8× | 4/7 | 520.2ms | 341.3ms | 108.3 MB | 7/7 | -169078071 |
| elixir | 149.6ms | 25.8× | 3/7 | 332.9ms | 183.3ms | 73.0 MB | 6/7 | -169078071 |
| python | 729.4ms | 125.8× | 6/7 | 739.5ms | 10.1ms | 10.1 MB | 1/7 | -169078071 |
| node | 14.3ms | 2.5× | 2/7 | 32.3ms | 18.0ms | 49.8 MB | 5/7 | -169078071 |
| ruby | 289.0ms | 49.8× | 5/7 | 327.8ms | 38.8ms | 19.0 MB | 2/7 | -169078071 |
| dotnet | 5.8ms | 1.0× | 1/7 | 28.8ms | 23.0ms | 26.6 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 360.7ms | 225.4× | 6/7 | 393.4ms | 32.7ms | 95.4 MB | 6/7 | 1489952542 |
| clojure | 390.3ms | 243.9× | 7/7 | 731.6ms | 341.3ms | 158.9 MB | 7/7 | 1489952542 |
| elixir | 9.2ms | 5.7× | 4/7 | 192.5ms | 183.3ms | 73.4 MB | 5/7 | 1489952542 |
| python | 8.6ms | 5.4× | 3/7 | 18.7ms | 10.1ms | 12.2 MB | 1/7 | 1489952542 |
| node | 1.6ms | 1.0× | 1/7 | 19.6ms | 18.0ms | 43.8 MB | 4/7 | 1489952542 |
| ruby | 3.8ms | 2.4× | 2/7 | 42.6ms | 38.8ms | 19.6 MB | 2/7 | 1489952542 |
| dotnet | 40.9ms | 25.6× | 5/7 | 63.9ms | 23.0ms | 33.8 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 980.9ms | 245.2× | 7/7 | 1.014s | 32.7ms | 160.7 MB | 7/7 | 10000 |
| clojure | 122.4ms | 30.6× | 6/7 | 463.7ms | 341.3ms | 108.5 MB | 6/7 | 10000 |
| elixir | 15.7ms | 3.9× | 5/7 | 199.0ms | 183.3ms | 69.9 MB | 5/7 | 10000 |
| python | 13.1ms | 3.3× | 4/7 | 23.2ms | 10.1ms | 10.9 MB | 1/7 | 10000 |
| node | 4.0ms | 1.0× | 1/7 | 22.0ms | 18.0ms | 50.0 MB | 4/7 | 10000 |
| ruby | 6.8ms | 1.7× | 2/7 | 45.6ms | 38.8ms | 19.2 MB | 2/7 | 10000 |
| dotnet | 10.4ms | 2.6× | 3/7 | 33.4ms | 23.0ms | 31.5 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.8ms | 49.2× | 6/7 | 165.5ms | 32.7ms | 105.6 MB | 6/7 | 12081249 |
| clojure | 154.6ms | 57.3× | 7/7 | 495.9ms | 341.3ms | 109.1 MB | 7/7 | 12081249 |
| elixir | 6.8ms | 2.5× | 3/7 | 190.1ms | 183.3ms | 78.6 MB | 5/7 | 12081249 |
| python | 12.7ms | 4.7× | 5/7 | 22.8ms | 10.1ms | 10.0 MB | 1/7 | 12081249 |
| node | 5.8ms | 2.1× | 2/7 | 23.8ms | 18.0ms | 50.6 MB | 4/7 | 12081249 |
| ruby | 8.0ms | 3.0× | 4/7 | 46.8ms | 38.8ms | 19.3 MB | 2/7 | 12081249 |
| dotnet | 2.7ms | 1.0× | 1/7 | 25.7ms | 23.0ms | 26.9 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.8ms | 2.9× | 3/7 | 80.5ms | 32.7ms | 57.0 MB | 4/7 | 6100000 |
| clojure | 177.9ms | 10.7× | 5/7 | 519.2ms | 341.3ms | 133.2 MB | 7/7 | 6100000 |
| elixir | 18.4ms | 1.1× | 2/7 | 201.7ms | 183.3ms | 78.0 MB | 5/7 | 6100000 |
| python | 548.6ms | 33.0× | 6/7 | 558.7ms | 10.1ms | 27.7 MB | 1/7 | 6100000 |
| node | 52.5ms | 3.2× | 4/7 | 70.5ms | 18.0ms | 51.2 MB | 3/7 | 6100000 |
| ruby | 1.569s | 94.5× | 7/7 | 1.608s | 38.8ms | 132.0 MB | 6/7 | 6100000 |
| dotnet | 16.6ms | 1.0× | 1/7 | 39.6ms | 23.0ms | 30.4 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 186.6ms | 1.7× | 2/7 | 219.3ms | 32.7ms | 31.2 MB | 4/7 | 134626900 |
| clojure | 372.8ms | 3.3× | 5/7 | 714.1ms | 341.3ms | 136.4 MB | 6/7 | 134626900 |
| elixir | 301.9ms | 2.7× | 4/7 | 485.2ms | 183.3ms | 71.7 MB | 5/7 | 134626900 |
| python | 2.519s | 22.6× | 7/7 | 2.530s | 10.1ms | 21.7 MB | 2/7 | 134626900 |
| node | 295.3ms | 2.7× | 3/7 | 313.3ms | 18.0ms | 181.6 MB | 7/7 | 134626900 |
| ruby | 1.891s | 17.0× | 6/7 | 1.930s | 38.8ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 111.3ms | 1.0× | 1/7 | 134.3ms | 23.0ms | 27.9 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.8ms | 1.3× | 3/7 | 184.5ms | 32.7ms | 112.4 MB | 5/7 | 500 |
| clojure | 772.9ms | 6.6× | 7/7 | 1.114s | 341.3ms | 337.6 MB | 6/7 | 500 |
| elixir | 551.3ms | 4.7× | 6/7 | 734.6ms | 183.3ms | 494.6 MB | 7/7 | 500 |
| python | 173.3ms | 1.5× | 4/7 | 183.4ms | 10.1ms | 44.0 MB | 1/7 | 500 |
| node | 116.6ms | 1.0× | 1/7 | 134.6ms | 18.0ms | 64.6 MB | 4/7 | 500 |
| ruby | 205.1ms | 1.8× | 5/7 | 243.9ms | 38.8ms | 45.7 MB | 2/7 | 500 |
| dotnet | 145.4ms | 1.2× | 2/7 | 168.4ms | 23.0ms | 47.7 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 257.7ms | 5.0× | 3/7 | 290.4ms | 32.7ms | 105.2 MB | 6/7 | 100000 |
| clojure | 596.3ms | 11.7× | 4/7 | 937.6ms | 341.3ms | 132.3 MB | 7/7 | 100000 |
| elixir | 51.1ms | 1.0× | 1/7 | 234.4ms | 183.3ms | 71.4 MB | 5/7 | 100000 |
| python | 817.2ms | 16.0× | 7/7 | 827.3ms | 10.1ms | 10.6 MB | 1/7 | 100000 |
| node | 641.4ms | 12.6× | 6/7 | 659.4ms | 18.0ms | 66.9 MB | 4/7 | 100000 |
| ruby | 603.0ms | 11.8× | 5/7 | 641.8ms | 38.8ms | 19.0 MB | 2/7 | 100000 |
| dotnet | 162.1ms | 3.2× | 2/7 | 185.1ms | 23.0ms | 27.4 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.457s | 13.0× | 4/7 | 1.490s | 32.7ms | 280.7 MB | 6/7 | 1000000 |
| clojure | 4.463s | 40.0× | 6/7 | 4.804s | 341.3ms | 745.8 MB | 7/7 | 1000000 |
| elixir | 262.8ms | 2.4× | 2/7 | 446.1ms | 183.3ms | 70.4 MB | 5/7 | 1000000 |
| python | 4.708s | 42.1× | 7/7 | 4.718s | 10.1ms | 16.0 MB | 1/7 | 1000000 |
| node | 111.7ms | 1.0× | 1/7 | 129.7ms | 18.0ms | 65.3 MB | 4/7 | 1000000 |
| ruby | 3.542s | 31.7× | 5/7 | 3.581s | 38.8ms | 23.0 MB | 2/7 | 1000000 |
| dotnet | 879.7ms | 7.9× | 3/7 | 902.7ms | 23.0ms | 30.3 MB | 3/7 | 1000000 |
