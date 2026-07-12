# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-12 13:01.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.5ms | 3.3× | 4/7 | 34.5ms | — | 25.2 MB | 3/7 | 0 |
| clojure | 344.9ms | 32.8× | 7/7 | 344.9ms | — | 102.0 MB | 7/7 | 0 |
| elixir | 184.9ms | 17.6× | 6/7 | 184.9ms | — | 70.0 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.1ms | 1.7× | 2/7 | 18.1ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 39.2ms | 3.7× | 5/7 | 39.2ms | — | 19.1 MB | 2/7 | 0 |
| dotnet | 21.6ms | 2.1× | 3/7 | 21.6ms | — | 25.6 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.1ms | 1.1× | 2/7 | 85.6ms | 34.5ms | 28.7 MB | 4/7 | 9227465 |
| clojure | 192.7ms | 4.3× | 5/7 | 537.6ms | 344.9ms | 108.3 MB | 7/7 | 9227465 |
| elixir | 71.9ms | 1.6× | 3/7 | 256.8ms | 184.9ms | 70.9 MB | 6/7 | 9227465 |
| python | 734.9ms | 16.5× | 7/7 | 745.4ms | 10.5ms | 9.7 MB | 1/7 | 9227465 |
| node | 77.9ms | 1.7× | 4/7 | 96.0ms | 18.1ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 610.2ms | 13.7× | 6/7 | 649.4ms | 39.2ms | 19.1 MB | 2/7 | 9227465 |
| dotnet | 44.6ms | 1.0× | 1/7 | 66.2ms | 21.6ms | 25.7 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 291.8ms | 22.1× | 5/7 | 326.3ms | 34.5ms | 28.7 MB | 4/7 | 449999985000000 |
| clojure | 138.2ms | 10.5× | 4/7 | 483.1ms | 344.9ms | 108.9 MB | 7/7 | 449999985000000 |
| elixir | 47.7ms | 3.6× | 3/7 | 232.6ms | 184.9ms | 72.3 MB | 6/7 | 449999985000000 |
| python | 2.351s | 178.1× | 7/7 | 2.361s | 10.5ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 30.8ms | 2.3× | 2/7 | 48.9ms | 18.1ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 603.0ms | 45.7× | 6/7 | 642.2ms | 39.2ms | 19.1 MB | 2/7 | 449999985000000 |
| dotnet | 13.2ms | 1.0× | 1/7 | 34.8ms | 21.6ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.7ms | 1.0× | 1/7 | 36.2ms | 34.5ms | 25.0 MB | 3/7 | 12499997500000 |
| clojure | 185.4ms | 109.1× | 5/7 | 530.3ms | 344.9ms | 220.4 MB | 7/7 | 12499997500000 |
| elixir | 35.6ms | 20.9× | 3/7 | 220.5ms | 184.9ms | 71.6 MB | 5/7 | 12499997500000 |
| python | 105.2ms | 61.9× | 4/7 | 115.7ms | 10.5ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 224.4ms | 132.0× | 7/7 | 242.5ms | 18.1ms | 90.0 MB | 6/7 | 12499997500000 |
| ruby | 223.6ms | 131.5× | 6/7 | 262.8ms | 39.2ms | 19.1 MB | 2/7 | 12499997500000 |
| dotnet | 12.4ms | 7.3× | 2/7 | 34.0ms | 21.6ms | 27.4 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.2ms | 5.7× | 4/7 | 86.7ms | 34.5ms | 29.1 MB | 4/7 | 13848 |
| clojure | 137.2ms | 14.9× | 7/7 | 482.1ms | 344.9ms | 108.8 MB | 7/7 | 13848 |
| elixir | 19.0ms | 2.1× | 3/7 | 203.9ms | 184.9ms | 70.6 MB | 6/7 | 13848 |
| python | 122.7ms | 13.3× | 6/7 | 133.2ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 9.4ms | 1.0× | 2/7 | 27.5ms | 18.1ms | 48.6 MB | 5/7 | 13848 |
| ruby | 116.7ms | 12.7× | 5/7 | 155.9ms | 39.2ms | 19.1 MB | 2/7 | 13848 |
| dotnet | 9.2ms | 1.0× | 1/7 | 30.8ms | 21.6ms | 26.2 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 166.5ms | 3.5× | 3/7 | 201.0ms | 34.5ms | 28.9 MB | 4/7 | 442 |
| clojure | 426.9ms | 9.1× | 5/7 | 771.8ms | 344.9ms | 371.2 MB | 7/7 | 442 |
| elixir | 111.9ms | 2.4× | 2/7 | 296.8ms | 184.9ms | 70.1 MB | 6/7 | 442 |
| python | 2.678s | 56.8× | 7/7 | 2.688s | 10.5ms | 9.7 MB | 1/7 | 442 |
| node | 175.4ms | 3.7× | 4/7 | 193.5ms | 18.1ms | 48.3 MB | 5/7 | 442 |
| ruby | 847.7ms | 18.0× | 6/7 | 886.9ms | 39.2ms | 19.1 MB | 2/7 | 442 |
| dotnet | 47.1ms | 1.0× | 1/7 | 68.7ms | 21.6ms | 26.2 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 259.9ms | 13.4× | 5/7 | 294.4ms | 34.5ms | 28.9 MB | 4/7 | 6129302 |
| clojure | 150.3ms | 7.7× | 3/7 | 495.2ms | 344.9ms | 115.1 MB | 7/7 | 6129302 |
| elixir | 259.8ms | 13.4× | 4/7 | 444.7ms | 184.9ms | 72.6 MB | 6/7 | 6129302 |
| python | 1.303s | 67.1× | 7/7 | 1.313s | 10.5ms | 9.8 MB | 1/7 | 6129302 |
| node | 20.8ms | 1.1× | 2/7 | 38.9ms | 18.1ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 461.4ms | 23.8× | 6/7 | 500.6ms | 39.2ms | 19.4 MB | 2/7 | 6129302 |
| dotnet | 19.4ms | 1.0× | 1/7 | 41.0ms | 21.6ms | 26.2 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 141.0ms | 26.6× | 4/7 | 175.5ms | 34.5ms | 44.8 MB | 4/7 | 654353666 |
| clojure | 192.1ms | 36.2× | 5/7 | 537.0ms | 344.9ms | 117.8 MB | 7/7 | 654353666 |
| elixir | 62.2ms | 11.7× | 3/7 | 247.1ms | 184.9ms | 74.4 MB | 6/7 | 654353666 |
| python | 447.9ms | 84.5× | 7/7 | 458.4ms | 10.5ms | 10.2 MB | 1/7 | 654353666 |
| node | 16.1ms | 3.0× | 2/7 | 34.2ms | 18.1ms | 51.9 MB | 5/7 | 654353666 |
| ruby | 280.8ms | 53.0× | 6/7 | 320.0ms | 39.2ms | 19.4 MB | 2/7 | 654353666 |
| dotnet | 5.3ms | 1.0× | 1/7 | 26.9ms | 21.6ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.4ms | 1.0× | 1/7 | 44.9ms | 34.5ms | 34.9 MB | 1/7 | 3388889 |
| clojure | 161.7ms | 15.5× | 7/7 | 506.6ms | 344.9ms | 168.2 MB | 6/7 | 3388889 |
| elixir | 117.3ms | 11.3× | 6/7 | 302.2ms | 184.9ms | 202.9 MB | 7/7 | 3388889 |
| python | 42.3ms | 4.1× | 3/7 | 52.8ms | 10.5ms | 39.8 MB | 2/7 | 3388889 |
| node | 64.2ms | 6.2× | 4/7 | 82.3ms | 18.1ms | 95.3 MB | 5/7 | 3388889 |
| ruby | 88.5ms | 8.5× | 5/7 | 127.7ms | 39.2ms | 47.8 MB | 3/7 | 3388889 |
| dotnet | 30.6ms | 2.9× | 2/7 | 52.2ms | 21.6ms | 56.5 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 122.2ms | 4.0× | 4/7 | 156.7ms | 34.5ms | 30.3 MB | 4/7 | 374854840 |
| clojure | 270.7ms | 8.8× | 7/7 | 615.6ms | 344.9ms | 302.3 MB | 7/7 | 374854840 |
| elixir | 169.2ms | 5.5× | 5/7 | 354.1ms | 184.9ms | 70.2 MB | 6/7 | 374854840 |
| python | 172.5ms | 5.6× | 6/7 | 183.0ms | 10.5ms | 9.8 MB | 1/7 | 374854840 |
| node | 30.6ms | 1.0× | 1/7 | 48.7ms | 18.1ms | 50.2 MB | 5/7 | 374854840 |
| ruby | 69.7ms | 2.3× | 3/7 | 108.9ms | 39.2ms | 19.1 MB | 2/7 | 374854840 |
| dotnet | 38.0ms | 1.2× | 2/7 | 59.6ms | 21.6ms | 27.0 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 93.5ms | 7.5× | 4/7 | 128.0ms | 34.5ms | 55.9 MB | 4/7 | 1638200 |
| clojure | 178.1ms | 14.4× | 7/7 | 523.0ms | 344.9ms | 149.0 MB | 7/7 | 1638200 |
| elixir | 12.4ms | 1.0× | 1/7 | 197.3ms | 184.9ms | 70.2 MB | 6/7 | 1638200 |
| python | 94.7ms | 7.6× | 5/7 | 105.2ms | 10.5ms | 10.0 MB | 1/7 | 1638200 |
| node | 20.8ms | 1.7× | 3/7 | 38.9ms | 18.1ms | 56.0 MB | 5/7 | 1638200 |
| ruby | 95.9ms | 7.7× | 6/7 | 135.1ms | 39.2ms | 19.4 MB | 2/7 | 1638200 |
| dotnet | 14.6ms | 1.2× | 2/7 | 36.2ms | 21.6ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 216.3ms | 3.4× | 6/7 | 250.8ms | 34.5ms | 187.1 MB | 7/7 | 46468819 |
| clojure | 255.1ms | 4.0× | 7/7 | 600.0ms | 344.9ms | 123.6 MB | 5/7 | 46468819 |
| elixir | 118.4ms | 1.8× | 4/7 | 303.3ms | 184.9ms | 157.7 MB | 6/7 | 46468819 |
| python | 191.2ms | 3.0× | 5/7 | 201.7ms | 10.5ms | 25.9 MB | 2/7 | 46468819 |
| node | 102.3ms | 1.6× | 3/7 | 120.4ms | 18.1ms | 65.0 MB | 4/7 | 46468819 |
| ruby | 71.9ms | 1.1× | 2/7 | 111.1ms | 39.2ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 64.5ms | 1.0× | 1/7 | 86.1ms | 21.6ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 138.5ms | 18.2× | 6/7 | 173.0ms | 34.5ms | 47.6 MB | 4/7 | 724 |
| clojure | 209.1ms | 27.5× | 7/7 | 554.0ms | 344.9ms | 128.5 MB | 7/7 | 724 |
| elixir | 9.2ms | 1.2× | 2/7 | 194.1ms | 184.9ms | 70.8 MB | 6/7 | 724 |
| python | 54.8ms | 7.2× | 4/7 | 65.3ms | 10.5ms | 9.7 MB | 1/7 | 724 |
| node | 7.6ms | 1.0× | 1/7 | 25.7ms | 18.1ms | 50.7 MB | 5/7 | 724 |
| ruby | 123.4ms | 16.2× | 5/7 | 162.6ms | 39.2ms | 19.4 MB | 2/7 | 724 |
| dotnet | 20.0ms | 2.6× | 3/7 | 41.6ms | 21.6ms | 29.1 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.5ms | 2.1× | 2/7 | 72.0ms | 34.5ms | 28.9 MB | 3/7 | 9900000 |
| clojure | 1.124s | 62.1× | 7/7 | 1.469s | 344.9ms | 370.9 MB | 7/7 | 9900000 |
| elixir | 18.1ms | 1.0× | 1/7 | 203.0ms | 184.9ms | 72.2 MB | 6/7 | 9900000 |
| python | 46.6ms | 2.6× | 3/7 | 57.1ms | 10.5ms | 9.7 MB | 1/7 | 9900000 |
| node | 567.1ms | 31.3× | 6/7 | 585.2ms | 18.1ms | 50.3 MB | 5/7 | 9900000 |
| ruby | 114.2ms | 6.3× | 4/7 | 153.4ms | 39.2ms | 21.8 MB | 2/7 | 9900000 |
| dotnet | 292.8ms | 16.2× | 5/7 | 314.4ms | 21.6ms | 32.7 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 249.0ms | 26.5× | 5/7 | 283.5ms | 34.5ms | 29.2 MB | 3/7 | 2475000 |
| clojure | 1.335s | 142.1× | 7/7 | 1.680s | 344.9ms | 373.5 MB | 7/7 | 2475000 |
| elixir | 9.4ms | 1.0× | 1/7 | 194.3ms | 184.9ms | 72.5 MB | 6/7 | 2475000 |
| python | 234.1ms | 24.9× | 4/7 | 244.6ms | 10.5ms | 9.9 MB | 1/7 | 2475000 |
| node | 207.4ms | 22.1× | 3/7 | 225.5ms | 18.1ms | 50.2 MB | 5/7 | 2475000 |
| ruby | 109.9ms | 11.7× | 2/7 | 149.1ms | 39.2ms | 25.9 MB | 2/7 | 2475000 |
| dotnet | 670.7ms | 71.4× | 6/7 | 692.3ms | 21.6ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 9.3× | 6/7 | 70.6ms | 34.5ms | 28.9 MB | 4/7 | 155553889038886 |
| clojure | 130.3ms | 33.4× | 7/7 | 475.2ms | 344.9ms | 108.3 MB | 7/7 | 155553889038886 |
| elixir | 9.2ms | 2.4× | 5/7 | 194.1ms | 184.9ms | 70.7 MB | 6/7 | 155553889038886 |
| python | 3.9ms | 1.0× | 1/7 | 14.4ms | 10.5ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 2.0× | 3/7 | 25.8ms | 18.1ms | 52.1 MB | 5/7 | 155553889038886 |
| ruby | 7.7ms | 2.0× | 2/7 | 46.9ms | 39.2ms | 19.8 MB | 2/7 | 155553889038886 |
| dotnet | 8.0ms | 2.1× | 4/7 | 29.6ms | 21.6ms | 27.9 MB | 3/7 | 155553889038886 |

## ackermann — deep double-recursion (Ackermann ack(3,9))  (N=6)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.060s | 16.6× | 7/7 | 4.095s | 34.5ms | 30.5 MB | 4/7 | 24558 |
| clojure | 562.0ms | 2.3× | 4/7 | 906.9ms | 344.9ms | 377.4 MB | 7/7 | 24558 |
| elixir | 281.0ms | 1.2× | 2/7 | 465.9ms | 184.9ms | 70.6 MB | 6/7 | 24558 |
| python | 3.849s | 15.8× | 6/7 | 3.859s | 10.5ms | 10.9 MB | 1/7 | 24558 |
| node | 394.1ms | 1.6× | 3/7 | 412.2ms | 18.1ms | 48.6 MB | 5/7 | 24558 |
| ruby | 1.655s | 6.8× | 5/7 | 1.694s | 39.2ms | 19.6 MB | 2/7 | 24558 |
| dotnet | 244.1ms | 1.0× | 1/7 | 265.7ms | 21.6ms | 26.2 MB | 3/7 | 24558 |

## sieve — Sieve of Eratosthenes (mutable array vs Table)  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.219s | 304.8× | 7/7 | 1.254s | 34.5ms | 466.6 MB | 7/7 | 78498 |
| clojure | 142.0ms | 35.5× | 6/7 | 486.9ms | 344.9ms | 108.6 MB | 6/7 | 78498 |
| elixir | 55.5ms | 13.9× | 3/7 | 240.4ms | 184.9ms | 77.8 MB | 5/7 | 78498 |
| python | 125.5ms | 31.4× | 5/7 | 136.0ms | 10.5ms | 10.6 MB | 1/7 | 78498 |
| node | 6.3ms | 1.6× | 2/7 | 24.4ms | 18.1ms | 49.7 MB | 4/7 | 78498 |
| ruby | 90.0ms | 22.5× | 4/7 | 129.2ms | 39.2ms | 26.8 MB | 2/7 | 78498 |
| dotnet | 4.0ms | 1.0× | 1/7 | 25.6ms | 21.6ms | 27.2 MB | 3/7 | 78498 |

## persistent-map — read-modify-write churn on a map (deep CHAMP)  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 611.9ms | 26.6× | 7/7 | 646.4ms | 34.5ms | 237.9 MB | 6/7 | 30039386344 |
| clojure | 292.4ms | 12.7× | 6/7 | 637.3ms | 344.9ms | 288.0 MB | 7/7 | 30039386344 |
| elixir | 117.2ms | 5.1× | 5/7 | 302.1ms | 184.9ms | 97.5 MB | 5/7 | 30039386344 |
| python | 80.6ms | 3.5× | 4/7 | 91.1ms | 10.5ms | 14.9 MB | 1/7 | 30039386344 |
| node | 23.0ms | 1.0× | 1/7 | 41.1ms | 18.1ms | 54.2 MB | 4/7 | 30039386344 |
| ruby | 38.9ms | 1.7× | 3/7 | 78.1ms | 39.2ms | 21.5 MB | 2/7 | 30039386344 |
| dotnet | 23.8ms | 1.0× | 2/7 | 45.4ms | 21.6ms | 30.1 MB | 3/7 | 30039386344 |

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 6.124s | 887.6× | 7/7 | 6.159s | 34.5ms | 41.7 MB | 4/7 | -169078071 |
| clojure | 181.3ms | 26.3× | 4/7 | 526.2ms | 344.9ms | 108.3 MB | 7/7 | -169078071 |
| elixir | 143.0ms | 20.7× | 3/7 | 327.9ms | 184.9ms | 71.9 MB | 6/7 | -169078071 |
| python | 753.2ms | 109.2× | 6/7 | 763.7ms | 10.5ms | 10.4 MB | 1/7 | -169078071 |
| node | 13.1ms | 1.9× | 2/7 | 31.2ms | 18.1ms | 50.6 MB | 5/7 | -169078071 |
| ruby | 299.3ms | 43.4× | 5/7 | 338.5ms | 39.2ms | 19.1 MB | 2/7 | -169078071 |
| dotnet | 6.9ms | 1.0× | 1/7 | 28.5ms | 21.6ms | 26.8 MB | 3/7 | -169078071 |

## json — JSON encode+parse round-trip (pure-Brood vs native)  (N=2000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 361.6ms | 226.0× | 6/7 | 396.1ms | 34.5ms | 108.3 MB | 6/7 | 1489952542 |
| clojure | 390.6ms | 244.1× | 7/7 | 735.5ms | 344.9ms | 165.6 MB | 7/7 | 1489952542 |
| elixir | 6.9ms | 4.3× | 3/7 | 191.8ms | 184.9ms | 76.0 MB | 5/7 | 1489952542 |
| python | 7.8ms | 4.9× | 4/7 | 18.3ms | 10.5ms | 12.3 MB | 1/7 | 1489952542 |
| node | 1.6ms | 1.0× | 1/7 | 19.7ms | 18.1ms | 44.1 MB | 4/7 | 1489952542 |
| ruby | 3.8ms | 2.4× | 2/7 | 43.0ms | 39.2ms | 19.8 MB | 2/7 | 1489952542 |
| dotnet | 44.0ms | 27.5× | 5/7 | 65.6ms | 21.6ms | 33.9 MB | 3/7 | 1489952542 |

## regex — regex full-match count (pure-Brood vs native)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.000s | 263.3× | 7/7 | 1.035s | 34.5ms | 172.6 MB | 7/7 | 10000 |
| clojure | 136.9ms | 36.0× | 6/7 | 481.8ms | 344.9ms | 109.2 MB | 6/7 | 10000 |
| elixir | 15.3ms | 4.0× | 5/7 | 200.2ms | 184.9ms | 72.6 MB | 5/7 | 10000 |
| python | 13.7ms | 3.6× | 4/7 | 24.2ms | 10.5ms | 11.0 MB | 1/7 | 10000 |
| node | 3.8ms | 1.0× | 1/7 | 21.9ms | 18.1ms | 50.5 MB | 4/7 | 10000 |
| ruby | 8.8ms | 2.3× | 2/7 | 48.0ms | 39.2ms | 19.4 MB | 2/7 | 10000 |
| dotnet | 12.0ms | 3.2× | 3/7 | 33.6ms | 21.6ms | 31.7 MB | 3/7 | 10000 |

## base64 — base64 encode+decode (pure-Brood vs native)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 130.3ms | 29.0× | 6/7 | 164.8ms | 34.5ms | 109.5 MB | 7/7 | 12081249 |
| clojure | 165.1ms | 36.7× | 7/7 | 510.0ms | 344.9ms | 108.8 MB | 6/7 | 12081249 |
| elixir | 8.5ms | 1.9× | 4/7 | 193.4ms | 184.9ms | 75.7 MB | 5/7 | 12081249 |
| python | 13.0ms | 2.9× | 5/7 | 23.5ms | 10.5ms | 10.2 MB | 1/7 | 12081249 |
| node | 6.8ms | 1.5× | 2/7 | 24.9ms | 18.1ms | 51.1 MB | 4/7 | 12081249 |
| ruby | 8.4ms | 1.9× | 3/7 | 47.6ms | 39.2ms | 19.5 MB | 2/7 | 12081249 |
| dotnet | 4.5ms | 1.0× | 1/7 | 26.1ms | 21.6ms | 27.0 MB | 3/7 | 12081249 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 49.7ms | 2.6× | 3/7 | 84.2ms | 34.5ms | 58.1 MB | 4/7 | 6100000 |
| clojure | 194.1ms | 10.1× | 5/7 | 539.0ms | 344.9ms | 134.0 MB | 7/7 | 6100000 |
| elixir | 22.6ms | 1.2× | 2/7 | 207.5ms | 184.9ms | 77.9 MB | 5/7 | 6100000 |
| python | 545.8ms | 28.4× | 6/7 | 556.3ms | 10.5ms | 27.9 MB | 1/7 | 6100000 |
| node | 52.8ms | 2.8× | 4/7 | 70.9ms | 18.1ms | 51.6 MB | 3/7 | 6100000 |
| ruby | 1.605s | 83.6× | 7/7 | 1.645s | 39.2ms | 132.4 MB | 6/7 | 6100000 |
| dotnet | 19.2ms | 1.0× | 1/7 | 40.8ms | 21.6ms | 30.7 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 161.8ms | 1.4× | 2/7 | 196.3ms | 34.5ms | 31.1 MB | 4/7 | 134626900 |
| clojure | 396.5ms | 3.5× | 5/7 | 741.4ms | 344.9ms | 135.3 MB | 6/7 | 134626900 |
| elixir | 313.1ms | 2.8× | 4/7 | 498.0ms | 184.9ms | 71.0 MB | 5/7 | 134626900 |
| python | 2.522s | 22.5× | 7/7 | 2.532s | 10.5ms | 21.8 MB | 2/7 | 134626900 |
| node | 301.1ms | 2.7× | 3/7 | 319.2ms | 18.1ms | 182.7 MB | 7/7 | 134626900 |
| ruby | 1.916s | 17.1× | 6/7 | 1.955s | 39.2ms | 19.1 MB | 1/7 | 134626900 |
| dotnet | 112.1ms | 1.0× | 1/7 | 133.7ms | 21.6ms | 28.0 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.5ms | 1.2× | 3/7 | 190.0ms | 34.5ms | 108.6 MB | 5/7 | 500 |
| clojure | 819.3ms | 6.4× | 7/7 | 1.164s | 344.9ms | 284.0 MB | 6/7 | 500 |
| elixir | 562.0ms | 4.4× | 6/7 | 746.9ms | 184.9ms | 508.3 MB | 7/7 | 500 |
| python | 179.2ms | 1.4× | 4/7 | 189.7ms | 10.5ms | 44.2 MB | 1/7 | 500 |
| node | 128.6ms | 1.0× | 1/7 | 146.7ms | 18.1ms | 64.9 MB | 4/7 | 500 |
| ruby | 201.8ms | 1.6× | 5/7 | 241.0ms | 39.2ms | 45.7 MB | 2/7 | 500 |
| dotnet | 153.2ms | 1.2× | 2/7 | 174.8ms | 21.6ms | 48.0 MB | 3/7 | 500 |

## pingpong — message round-trip latency — two units bounce a token N times  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 306.6ms | 6.2× | 3/7 | 341.1ms | 34.5ms | 110.2 MB | 6/7 | 100000 |
| clojure | 619.6ms | 12.6× | 5/7 | 964.5ms | 344.9ms | 133.3 MB | 7/7 | 100000 |
| elixir | 49.1ms | 1.0× | 1/7 | 234.0ms | 184.9ms | 71.4 MB | 5/7 | 100000 |
| python | 834.3ms | 17.0× | 7/7 | 844.8ms | 10.5ms | 10.8 MB | 1/7 | 100000 |
| node | 662.0ms | 13.5× | 6/7 | 680.1ms | 18.1ms | 67.5 MB | 4/7 | 100000 |
| ruby | 603.1ms | 12.3× | 4/7 | 642.3ms | 39.2ms | 19.2 MB | 2/7 | 100000 |
| dotnet | 171.4ms | 3.5× | 2/7 | 193.0ms | 21.6ms | 27.7 MB | 3/7 | 100000 |

## ring — N-process ring — token travels N*5000 hops  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.040s | 17.5× | 4/7 | 2.075s | 34.5ms | 352.7 MB | 6/7 | 1000000 |
| clojure | 4.553s | 39.0× | 6/7 | 4.898s | 344.9ms | 771.0 MB | 7/7 | 1000000 |
| elixir | 250.2ms | 2.1× | 2/7 | 435.1ms | 184.9ms | 70.3 MB | 5/7 | 1000000 |
| python | 4.810s | 41.2× | 7/7 | 4.820s | 10.5ms | 16.1 MB | 1/7 | 1000000 |
| node | 116.7ms | 1.0× | 1/7 | 134.8ms | 18.1ms | 65.5 MB | 4/7 | 1000000 |
| ruby | 3.554s | 30.4× | 5/7 | 3.593s | 39.2ms | 23.2 MB | 2/7 | 1000000 |
| dotnet | 817.1ms | 7.0× | 3/7 | 838.7ms | 21.6ms | 30.2 MB | 3/7 | 1000000 |
