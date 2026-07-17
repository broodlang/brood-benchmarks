# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-17 08:19.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.6ms | 3.2× | 4/7 | 34.6ms | — | 25.5 MB | 3/7 | 0 |
| clojure | 366.9ms | 34.3× | 7/7 | 366.9ms | — | 103.8 MB | 7/7 | 0 |
| elixir | 186.3ms | 17.4× | 6/7 | 186.3ms | — | 72.8 MB | 6/7 | 0 |
| python | 10.7ms | 1.0× | 1/7 | 10.7ms | — | 9.7 MB | 1/7 | 0 |
| node | 19.5ms | 1.8× | 2/7 | 19.5ms | — | 42.6 MB | 5/7 | 0 |
| ruby | 41.3ms | 3.9× | 5/7 | 41.3ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 23.2ms | 2.2× | 3/7 | 23.2ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 59.2ms | 1.2× | 2/7 | 93.8ms | 34.6ms | 29.1 MB | 4/7 | 9227465 |
| clojure | 214.4ms | 4.5× | 5/7 | 581.3ms | 366.9ms | 107.1 MB | 7/7 | 9227465 |
| elixir | 86.2ms | 1.8× | 4/7 | 272.5ms | 186.3ms | 70.4 MB | 6/7 | 9227465 |
| python | 771.7ms | 16.2× | 7/7 | 782.4ms | 10.7ms | 9.9 MB | 1/7 | 9227465 |
| node | 81.4ms | 1.7× | 3/7 | 100.9ms | 19.5ms | 48.0 MB | 5/7 | 9227465 |
| ruby | 619.9ms | 13.0× | 6/7 | 661.2ms | 41.3ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 47.6ms | 1.0× | 1/7 | 70.8ms | 23.2ms | 26.0 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.3ms | 3.6× | 3/7 | 72.9ms | 34.6ms | 29.4 MB | 4/7 | 449999985000000 |
| clojure | 137.9ms | 13.0× | 5/7 | 504.8ms | 366.9ms | 107.8 MB | 7/7 | 449999985000000 |
| elixir | 53.6ms | 5.1× | 4/7 | 239.9ms | 186.3ms | 72.5 MB | 6/7 | 449999985000000 |
| python | 2.552s | 240.8× | 7/7 | 2.563s | 10.7ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 31.0ms | 2.9× | 2/7 | 50.5ms | 19.5ms | 50.0 MB | 5/7 | 449999985000000 |
| ruby | 587.5ms | 55.4× | 6/7 | 628.8ms | 41.3ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 10.6ms | 1.0× | 1/7 | 33.8ms | 23.2ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 37.9ms | 34.6ms | 25.5 MB | 3/7 | 12499997500000 |
| clojure | 188.2ms | 57.0× | 5/7 | 555.1ms | 366.9ms | 222.2 MB | 7/7 | 12499997500000 |
| elixir | 33.6ms | 10.2× | 3/7 | 219.9ms | 186.3ms | 70.2 MB | 5/7 | 12499997500000 |
| python | 110.1ms | 33.4× | 4/7 | 120.8ms | 10.7ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 233.7ms | 70.8× | 7/7 | 253.2ms | 19.5ms | 90.1 MB | 6/7 | 12499997500000 |
| ruby | 231.8ms | 70.2× | 6/7 | 273.1ms | 41.3ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 10.6ms | 3.2× | 2/7 | 33.8ms | 23.2ms | 27.8 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.7ms | 5.1× | 4/7 | 79.3ms | 34.6ms | 29.5 MB | 4/7 | 13848 |
| clojure | 154.7ms | 17.6× | 7/7 | 521.6ms | 366.9ms | 108.5 MB | 7/7 | 13848 |
| elixir | 19.9ms | 2.3× | 3/7 | 206.2ms | 186.3ms | 72.2 MB | 6/7 | 13848 |
| python | 122.9ms | 14.0× | 6/7 | 133.6ms | 10.7ms | 10.0 MB | 1/7 | 13848 |
| node | 8.9ms | 1.0× | 2/7 | 28.4ms | 19.5ms | 48.6 MB | 5/7 | 13848 |
| ruby | 118.4ms | 13.5× | 5/7 | 159.7ms | 41.3ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 8.8ms | 1.0× | 1/7 | 32.0ms | 23.2ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.7ms | 1.8× | 2/7 | 123.3ms | 34.6ms | 29.6 MB | 4/7 | 442 |
| clojure | 433.2ms | 8.9× | 5/7 | 800.1ms | 366.9ms | 370.9 MB | 7/7 | 442 |
| elixir | 115.3ms | 2.4× | 3/7 | 301.6ms | 186.3ms | 70.2 MB | 6/7 | 442 |
| python | 2.619s | 53.9× | 7/7 | 2.630s | 10.7ms | 9.8 MB | 1/7 | 442 |
| node | 177.7ms | 3.7× | 4/7 | 197.2ms | 19.5ms | 48.3 MB | 5/7 | 442 |
| ruby | 844.0ms | 17.4× | 6/7 | 885.3ms | 41.3ms | 19.2 MB | 2/7 | 442 |
| dotnet | 48.6ms | 1.0× | 1/7 | 71.8ms | 23.2ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.8ms | 9.5× | 4/7 | 208.4ms | 34.6ms | 29.5 MB | 4/7 | 6129302 |
| clojure | 165.7ms | 9.1× | 3/7 | 532.6ms | 366.9ms | 115.3 MB | 7/7 | 6129302 |
| elixir | 268.6ms | 14.8× | 5/7 | 454.9ms | 186.3ms | 73.1 MB | 6/7 | 6129302 |
| python | 1.352s | 74.3× | 7/7 | 1.363s | 10.7ms | 10.0 MB | 1/7 | 6129302 |
| node | 21.0ms | 1.2× | 2/7 | 40.5ms | 19.5ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 425.7ms | 23.4× | 6/7 | 467.0ms | 41.3ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 18.2ms | 1.0× | 1/7 | 41.4ms | 23.2ms | 26.4 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 135.3ms | 25.5× | 4/7 | 169.9ms | 34.6ms | 46.8 MB | 4/7 | 654353666 |
| clojure | 191.9ms | 36.2× | 5/7 | 558.8ms | 366.9ms | 121.5 MB | 7/7 | 654353666 |
| elixir | 68.3ms | 12.9× | 3/7 | 254.6ms | 186.3ms | 78.0 MB | 6/7 | 654353666 |
| python | 508.4ms | 95.9× | 7/7 | 519.1ms | 10.7ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.6ms | 3.1× | 2/7 | 36.1ms | 19.5ms | 52.2 MB | 5/7 | 654353666 |
| ruby | 290.1ms | 54.7× | 6/7 | 331.4ms | 41.3ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 5.3ms | 1.0× | 1/7 | 28.5ms | 23.2ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 16.7ms | 1.0× | 1/7 | 51.3ms | 34.6ms | 35.7 MB | 1/7 | 3388889 |
| clojure | 177.5ms | 10.6× | 7/7 | 544.4ms | 366.9ms | 167.8 MB | 6/7 | 3388889 |
| elixir | 123.3ms | 7.4× | 6/7 | 309.6ms | 186.3ms | 200.4 MB | 7/7 | 3388889 |
| python | 41.2ms | 2.5× | 3/7 | 51.9ms | 10.7ms | 40.0 MB | 2/7 | 3388889 |
| node | 65.0ms | 3.9× | 4/7 | 84.5ms | 19.5ms | 95.1 MB | 5/7 | 3388889 |
| ruby | 85.1ms | 5.1× | 5/7 | 126.4ms | 41.3ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 31.8ms | 1.9× | 2/7 | 55.0ms | 23.2ms | 56.9 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.8ms | 1.1× | 2/7 | 69.4ms | 34.6ms | 29.9 MB | 4/7 | 374854840 |
| clojure | 277.6ms | 8.8× | 7/7 | 644.5ms | 366.9ms | 302.5 MB | 7/7 | 374854840 |
| elixir | 194.7ms | 6.2× | 6/7 | 381.0ms | 186.3ms | 72.6 MB | 6/7 | 374854840 |
| python | 188.4ms | 6.0× | 5/7 | 199.1ms | 10.7ms | 10.0 MB | 1/7 | 374854840 |
| node | 31.4ms | 1.0× | 1/7 | 50.9ms | 19.5ms | 52.2 MB | 5/7 | 374854840 |
| ruby | 72.4ms | 2.3× | 4/7 | 113.7ms | 41.3ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 39.0ms | 1.2× | 3/7 | 62.2ms | 23.2ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 115.3ms | 8.8× | 6/7 | 149.9ms | 34.6ms | 55.8 MB | 4/7 | 1638200 |
| clojure | 168.1ms | 12.8× | 7/7 | 535.0ms | 366.9ms | 149.1 MB | 7/7 | 1638200 |
| elixir | 14.2ms | 1.1× | 2/7 | 200.5ms | 186.3ms | 73.2 MB | 6/7 | 1638200 |
| python | 104.6ms | 8.0× | 5/7 | 115.3ms | 10.7ms | 10.1 MB | 1/7 | 1638200 |
| node | 21.9ms | 1.7× | 3/7 | 41.4ms | 19.5ms | 58.1 MB | 5/7 | 1638200 |
| ruby | 93.6ms | 7.1× | 4/7 | 134.9ms | 41.3ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 13.1ms | 1.0× | 1/7 | 36.3ms | 23.2ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 205.3ms | 3.3× | 6/7 | 239.9ms | 34.6ms | 179.2 MB | 7/7 | 46468819 |
| clojure | 214.9ms | 3.4× | 7/7 | 581.8ms | 366.9ms | 123.8 MB | 5/7 | 46468819 |
| elixir | 109.7ms | 1.7× | 4/7 | 296.0ms | 186.3ms | 157.4 MB | 6/7 | 46468819 |
| python | 185.2ms | 2.9× | 5/7 | 195.9ms | 10.7ms | 25.9 MB | 2/7 | 46468819 |
| node | 107.7ms | 1.7× | 3/7 | 127.2ms | 19.5ms | 67.1 MB | 4/7 | 46468819 |
| ruby | 69.9ms | 1.1× | 2/7 | 111.2ms | 41.3ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 62.9ms | 1.0× | 1/7 | 86.1ms | 23.2ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.6ms | 13.3× | 5/7 | 114.2ms | 34.6ms | 48.3 MB | 4/7 | 724 |
| clojure | 210.4ms | 35.1× | 7/7 | 577.3ms | 366.9ms | 132.5 MB | 7/7 | 724 |
| elixir | 10.4ms | 1.7× | 2/7 | 196.7ms | 186.3ms | 72.6 MB | 6/7 | 724 |
| python | 52.8ms | 8.8× | 4/7 | 63.5ms | 10.7ms | 9.9 MB | 1/7 | 724 |
| node | 6.0ms | 1.0× | 1/7 | 25.5ms | 19.5ms | 52.8 MB | 5/7 | 724 |
| ruby | 118.3ms | 19.7× | 6/7 | 159.6ms | 41.3ms | 19.4 MB | 2/7 | 724 |
| dotnet | 18.0ms | 3.0× | 3/7 | 41.2ms | 23.2ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.7ms | 2.2× | 2/7 | 77.3ms | 34.6ms | 29.8 MB | 3/7 | 9900000 |
| clojure | 1.038s | 54.1× | 7/7 | 1.405s | 366.9ms | 370.8 MB | 7/7 | 9900000 |
| elixir | 19.2ms | 1.0× | 1/7 | 205.5ms | 186.3ms | 70.4 MB | 6/7 | 9900000 |
| python | 47.0ms | 2.4× | 3/7 | 57.7ms | 10.7ms | 9.9 MB | 1/7 | 9900000 |
| node | 554.7ms | 28.9× | 6/7 | 574.2ms | 19.5ms | 52.4 MB | 5/7 | 9900000 |
| ruby | 105.5ms | 5.5× | 4/7 | 146.8ms | 41.3ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 289.1ms | 15.1× | 5/7 | 312.3ms | 23.2ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.7ms | 6.1× | 2/7 | 73.3ms | 34.6ms | 29.4 MB | 3/7 | 2475000 |
| clojure | 1.261s | 200.1× | 7/7 | 1.627s | 366.9ms | 374.2 MB | 7/7 | 2475000 |
| elixir | 6.3ms | 1.0× | 1/7 | 192.6ms | 186.3ms | 70.6 MB | 6/7 | 2475000 |
| python | 233.7ms | 37.1× | 5/7 | 244.4ms | 10.7ms | 9.9 MB | 1/7 | 2475000 |
| node | 204.2ms | 32.4× | 4/7 | 223.7ms | 19.5ms | 52.4 MB | 5/7 | 2475000 |
| ruby | 106.6ms | 16.9× | 3/7 | 147.9ms | 41.3ms | 25.9 MB | 2/7 | 2475000 |
| dotnet | 675.4ms | 107.2× | 6/7 | 698.6ms | 23.2ms | 33.1 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 8.3× | 6/7 | 64.6ms | 34.6ms | 29.4 MB | 4/7 | 155553889038886 |
| clojure | 98.4ms | 27.3× | 7/7 | 465.3ms | 366.9ms | 108.2 MB | 7/7 | 155553889038886 |
| elixir | 7.9ms | 2.2× | 5/7 | 194.2ms | 186.3ms | 72.1 MB | 6/7 | 155553889038886 |
| python | 3.6ms | 1.0× | 1/7 | 14.3ms | 10.7ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 6.5ms | 1.8× | 3/7 | 26.0ms | 19.5ms | 54.0 MB | 5/7 | 155553889038886 |
| ruby | 4.9ms | 1.4× | 2/7 | 46.2ms | 41.3ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 7.1ms | 2.0× | 4/7 | 30.3ms | 23.2ms | 28.1 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 340.0ms | 1.4× | 3/7 | 374.6ms | 34.6ms | 30.3 MB | 4/7 | 24558 |
| clojure | 520.8ms | 2.2× | 5/7 | 887.7ms | 366.9ms | 374.7 MB | 7/7 | 24558 |
| elixir | 278.2ms | 1.2× | 2/7 | 464.5ms | 186.3ms | 71.6 MB | 6/7 | 24558 |
| python | 3.797s | 15.7× | 7/7 | 3.808s | 10.7ms | 11.0 MB | 1/7 | 24558 |
| node | 390.1ms | 1.6× | 4/7 | 409.6ms | 19.5ms | 50.5 MB | 5/7 | 24558 |
| ruby | 1.627s | 6.7× | 6/7 | 1.669s | 41.3ms | 19.7 MB | 2/7 | 24558 |
| dotnet | 241.6ms | 1.0× | 1/7 | 264.8ms | 23.2ms | 26.4 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.5ms | 19.7× | 3/7 | 68.1ms | 34.6ms | 37.3 MB | 4/7 | 78498 |
| clojure | 102.4ms | 60.2× | 6/7 | 469.3ms | 366.9ms | 109.1 MB | 7/7 | 78498 |
| elixir | 55.5ms | 32.6× | 4/7 | 241.8ms | 186.3ms | 78.1 MB | 6/7 | 78498 |
| python | 115.9ms | 68.2× | 7/7 | 126.6ms | 10.7ms | 10.9 MB | 1/7 | 78498 |
| node | 4.5ms | 2.6× | 2/7 | 24.0ms | 19.5ms | 51.6 MB | 5/7 | 78498 |
| ruby | 86.9ms | 51.1× | 5/7 | 128.2ms | 41.3ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 1.7ms | 1.0× | 1/7 | 24.9ms | 23.2ms | 27.5 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.6ms | 3.6× | 4/7 | 109.2ms | 34.6ms | 78.7 MB | 5/7 | 30039386344 |
| clojure | 260.3ms | 12.4× | 7/7 | 627.2ms | 366.9ms | 291.8 MB | 7/7 | 30039386344 |
| elixir | 117.1ms | 5.6× | 6/7 | 303.4ms | 186.3ms | 98.3 MB | 6/7 | 30039386344 |
| python | 79.7ms | 3.8× | 5/7 | 90.4ms | 10.7ms | 14.9 MB | 1/7 | 30039386344 |
| node | 21.6ms | 1.0× | 2/7 | 41.1ms | 19.5ms | 56.1 MB | 4/7 | 30039386344 |
| ruby | 37.0ms | 1.8× | 3/7 | 78.3ms | 41.3ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 21.0ms | 1.0× | 1/7 | 44.2ms | 23.2ms | 30.4 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 316.7ms | 66.0× | 6/7 | 351.3ms | 34.6ms | 49.8 MB | 4/7 | -169078071 |
| clojure | 152.2ms | 31.7× | 4/7 | 519.1ms | 366.9ms | 108.3 MB | 7/7 | -169078071 |
| elixir | 148.1ms | 30.9× | 3/7 | 334.4ms | 186.3ms | 72.6 MB | 6/7 | -169078071 |
| python | 708.6ms | 147.6× | 7/7 | 719.3ms | 10.7ms | 10.4 MB | 1/7 | -169078071 |
| node | 11.2ms | 2.3× | 2/7 | 30.7ms | 19.5ms | 52.5 MB | 5/7 | -169078071 |
| ruby | 288.6ms | 60.1× | 5/7 | 329.9ms | 41.3ms | 19.2 MB | 2/7 | -169078071 |
| dotnet | 4.8ms | 1.0× | 1/7 | 28.0ms | 23.2ms | 27.2 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 267.9ms | 267.9× | 6/7 | 302.5ms | 34.6ms | 120.0 MB | 6/7 | 1489952542 |
| clojure | 376.0ms | 376.0× | 7/7 | 742.9ms | 366.9ms | 166.7 MB | 7/7 | 1489952542 |
| elixir | 6.7ms | 6.7× | 3/7 | 193.0ms | 186.3ms | 73.7 MB | 5/7 | 1489952542 |
| python | 7.7ms | 7.7× | 4/7 | 18.4ms | 10.7ms | 12.4 MB | 1/7 | 1489952542 |
| node | 0.1ms | < 1× | 1/7 | 19.6ms | 19.5ms | 45.8 MB | 4/7 | 1489952542 |
| ruby | 1.9ms | 1.9× | 2/7 | 43.2ms | 41.3ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 41.9ms | 41.9× | 5/7 | 65.1ms | 23.2ms | 34.3 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 278.9ms | 107.3× | 7/7 | 313.5ms | 34.6ms | 66.6 MB | 5/7 | 10000 |
| clojure | 103.2ms | 39.7× | 6/7 | 470.1ms | 366.9ms | 109.1 MB | 7/7 | 10000 |
| elixir | 14.2ms | 5.5× | 5/7 | 200.5ms | 186.3ms | 72.2 MB | 6/7 | 10000 |
| python | 12.6ms | 4.8× | 4/7 | 23.3ms | 10.7ms | 11.1 MB | 1/7 | 10000 |
| node | 2.6ms | 1.0× | 1/7 | 22.1ms | 19.5ms | 52.5 MB | 4/7 | 10000 |
| ruby | 4.9ms | 1.9× | 2/7 | 46.2ms | 41.3ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 11.2ms | 4.3× | 3/7 | 34.4ms | 23.2ms | 32.1 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.0ms | 44.0× | 7/7 | 166.6ms | 34.6ms | 111.6 MB | 7/7 | 12081249 |
| clojure | 127.5ms | 42.5× | 6/7 | 494.4ms | 366.9ms | 111.2 MB | 6/7 | 12081249 |
| elixir | 12.2ms | 4.1× | 4/7 | 198.5ms | 186.3ms | 76.3 MB | 5/7 | 12081249 |
| python | 12.6ms | 4.2× | 5/7 | 23.3ms | 10.7ms | 10.2 MB | 1/7 | 12081249 |
| node | 4.0ms | 1.3× | 2/7 | 23.5ms | 19.5ms | 53.1 MB | 4/7 | 12081249 |
| ruby | 5.5ms | 1.8× | 3/7 | 46.8ms | 41.3ms | 19.6 MB | 2/7 | 12081249 |
| dotnet | 3.0ms | 1.0× | 1/7 | 26.2ms | 23.2ms | 27.4 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 68.3ms | 4.4× | 4/7 | 102.9ms | 34.6ms | 58.7 MB | 4/7 | 6100000 |
| clojure | 159.9ms | 10.4× | 5/7 | 526.8ms | 366.9ms | 133.7 MB | 7/7 | 6100000 |
| elixir | 19.7ms | 1.3× | 2/7 | 206.0ms | 186.3ms | 77.7 MB | 5/7 | 6100000 |
| python | 547.9ms | 35.6× | 6/7 | 558.6ms | 10.7ms | 28.0 MB | 1/7 | 6100000 |
| node | 51.0ms | 3.3× | 3/7 | 70.5ms | 19.5ms | 53.7 MB | 3/7 | 6100000 |
| ruby | 1.587s | 103.1× | 7/7 | 1.629s | 41.3ms | 133.6 MB | 6/7 | 6100000 |
| dotnet | 15.4ms | 1.0× | 1/7 | 38.6ms | 23.2ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 213.3ms | 1.9× | 2/7 | 247.9ms | 34.6ms | 31.9 MB | 4/7 | 134626900 |
| clojure | 357.4ms | 3.2× | 5/7 | 724.3ms | 366.9ms | 135.4 MB | 6/7 | 134626900 |
| elixir | 285.7ms | 2.6× | 3/7 | 472.0ms | 186.3ms | 72.3 MB | 5/7 | 134626900 |
| python | 2.524s | 22.6× | 7/7 | 2.535s | 10.7ms | 22.2 MB | 2/7 | 134626900 |
| node | 299.3ms | 2.7× | 4/7 | 318.8ms | 19.5ms | 185.5 MB | 7/7 | 134626900 |
| ruby | 1.888s | 16.9× | 6/7 | 1.930s | 41.3ms | 19.2 MB | 1/7 | 134626900 |
| dotnet | 111.5ms | 1.0× | 1/7 | 134.7ms | 23.2ms | 28.4 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 158.0ms | 1.4× | 3/7 | 192.6ms | 34.6ms | 107.5 MB | 5/7 | 500 |
| clojure | 779.9ms | 6.8× | 7/7 | 1.147s | 366.9ms | 289.5 MB | 6/7 | 500 |
| elixir | 579.1ms | 5.0× | 6/7 | 765.4ms | 186.3ms | 537.3 MB | 7/7 | 500 |
| python | 173.3ms | 1.5× | 4/7 | 184.0ms | 10.7ms | 43.2 MB | 1/7 | 500 |
| node | 115.4ms | 1.0× | 1/7 | 134.9ms | 19.5ms | 67.5 MB | 4/7 | 500 |
| ruby | 201.4ms | 1.7× | 5/7 | 242.7ms | 41.3ms | 45.8 MB | 2/7 | 500 |
| dotnet | 149.8ms | 1.3× | 2/7 | 173.0ms | 23.2ms | 47.9 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 263.0ms | 5.2× | 3/7 | 297.6ms | 34.6ms | 104.6 MB | 6/7 | 100000 |
| clojure | 585.7ms | 11.7× | 4/7 | 952.6ms | 366.9ms | 132.5 MB | 7/7 | 100000 |
| elixir | 50.1ms | 1.0× | 1/7 | 236.4ms | 186.3ms | 71.6 MB | 5/7 | 100000 |
| python | 813.3ms | 16.2× | 7/7 | 824.0ms | 10.7ms | 10.9 MB | 1/7 | 100000 |
| node | 644.7ms | 12.9× | 6/7 | 664.2ms | 19.5ms | 70.0 MB | 4/7 | 100000 |
| ruby | 610.7ms | 12.2× | 5/7 | 652.0ms | 41.3ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 163.6ms | 3.3× | 2/7 | 186.8ms | 23.2ms | 27.9 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.395s | 12.2× | 4/7 | 1.430s | 34.6ms | 280.0 MB | 6/7 | 1000000 |
| clojure | 4.450s | 39.0× | 6/7 | 4.816s | 366.9ms | 751.3 MB | 7/7 | 1000000 |
| elixir | 259.6ms | 2.3× | 2/7 | 445.9ms | 186.3ms | 72.7 MB | 5/7 | 1000000 |
| python | 4.728s | 41.5× | 7/7 | 4.739s | 10.7ms | 16.1 MB | 1/7 | 1000000 |
| node | 114.0ms | 1.0× | 1/7 | 133.5ms | 19.5ms | 67.6 MB | 4/7 | 1000000 |
| ruby | 3.516s | 30.8× | 5/7 | 3.557s | 41.3ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 885.0ms | 7.8× | 3/7 | 908.2ms | 23.2ms | 30.7 MB | 3/7 | 1000000 |
