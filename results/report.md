# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-05 22:55.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 2.7× | 4/7 | 32.0ms | — | 25.2 MB | 3/7 | 0 |
| clojure | 350.3ms | 29.7× | 7/7 | 350.3ms | — | 103.3 MB | 7/7 | 0 |
| elixir | 192.0ms | 16.3× | 6/7 | 192.0ms | — | 69.8 MB | 6/7 | 0 |
| python | 11.8ms | 1.0× | 1/7 | 11.8ms | — | 9.7 MB | 1/7 | 0 |
| node | 18.2ms | 1.5× | 2/7 | 18.2ms | — | 42.3 MB | 5/7 | 0 |
| ruby | 42.5ms | 3.6× | 5/7 | 42.5ms | — | 19.2 MB | 2/7 | 0 |
| dotnet | 22.3ms | 1.9× | 3/7 | 22.3ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 55.6ms | 1.4× | 2/7 | 87.6ms | 32.0ms | 29.1 MB | 4/7 | 9227465 |
| clojure | 214.4ms | 5.3× | 5/7 | 564.7ms | 350.3ms | 108.8 MB | 7/7 | 9227465 |
| elixir | 77.4ms | 1.9× | 3/7 | 269.4ms | 192.0ms | 72.6 MB | 6/7 | 9227465 |
| python | 756.1ms | 18.5× | 7/7 | 767.9ms | 11.8ms | 9.7 MB | 1/7 | 9227465 |
| node | 83.2ms | 2.0× | 4/7 | 101.4ms | 18.2ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 660.9ms | 16.2× | 6/7 | 703.4ms | 42.5ms | 19.2 MB | 2/7 | 9227465 |
| dotnet | 40.8ms | 1.0× | 1/7 | 63.1ms | 22.3ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.1ms | 2.9× | 3/7 | 70.1ms | 32.0ms | 29.0 MB | 4/7 | 449999985000000 |
| clojure | 174.5ms | 13.4× | 5/7 | 524.8ms | 350.3ms | 108.0 MB | 7/7 | 449999985000000 |
| elixir | 53.9ms | 4.1× | 4/7 | 245.9ms | 192.0ms | 71.6 MB | 6/7 | 449999985000000 |
| python | 2.457s | 189.0× | 7/7 | 2.469s | 11.8ms | 9.7 MB | 1/7 | 449999985000000 |
| node | 34.2ms | 2.6× | 2/7 | 52.4ms | 18.2ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 646.2ms | 49.7× | 6/7 | 688.7ms | 42.5ms | 19.2 MB | 2/7 | 449999985000000 |
| dotnet | 13.0ms | 1.0× | 1/7 | 35.3ms | 22.3ms | 26.1 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.7ms | 1.0× | 1/7 | 35.7ms | 32.0ms | 25.1 MB | 3/7 | 12499997500000 |
| clojure | 206.7ms | 55.9× | 5/7 | 557.0ms | 350.3ms | 220.5 MB | 7/7 | 12499997500000 |
| elixir | 27.6ms | 7.5× | 3/7 | 219.6ms | 192.0ms | 70.2 MB | 5/7 | 12499997500000 |
| python | 109.0ms | 29.5× | 4/7 | 120.8ms | 11.8ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 232.2ms | 62.8× | 7/7 | 250.4ms | 18.2ms | 89.5 MB | 6/7 | 12499997500000 |
| ruby | 231.8ms | 62.6× | 6/7 | 274.3ms | 42.5ms | 19.2 MB | 2/7 | 12499997500000 |
| dotnet | 11.4ms | 3.1× | 2/7 | 33.7ms | 22.3ms | 27.4 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.4ms | 4.5× | 4/7 | 76.4ms | 32.0ms | 29.5 MB | 4/7 | 13848 |
| clojure | 160.2ms | 16.2× | 7/7 | 510.5ms | 350.3ms | 108.8 MB | 7/7 | 13848 |
| elixir | 24.1ms | 2.4× | 3/7 | 216.1ms | 192.0ms | 70.6 MB | 6/7 | 13848 |
| python | 128.6ms | 13.0× | 6/7 | 140.4ms | 11.8ms | 9.9 MB | 1/7 | 13848 |
| node | 11.0ms | 1.1× | 2/7 | 29.2ms | 18.2ms | 48.4 MB | 5/7 | 13848 |
| ruby | 118.5ms | 12.0× | 5/7 | 161.0ms | 42.5ms | 19.2 MB | 2/7 | 13848 |
| dotnet | 9.9ms | 1.0× | 1/7 | 32.2ms | 22.3ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.0ms | 1.7× | 2/7 | 115.0ms | 32.0ms | 29.1 MB | 4/7 | 442 |
| clojure | 491.0ms | 10.2× | 5/7 | 841.3ms | 350.3ms | 370.7 MB | 7/7 | 442 |
| elixir | 103.7ms | 2.2× | 3/7 | 295.7ms | 192.0ms | 72.7 MB | 6/7 | 442 |
| python | 2.695s | 56.0× | 7/7 | 2.707s | 11.8ms | 9.7 MB | 1/7 | 442 |
| node | 184.4ms | 3.8× | 4/7 | 202.6ms | 18.2ms | 47.9 MB | 5/7 | 442 |
| ruby | 916.0ms | 19.0× | 6/7 | 958.5ms | 42.5ms | 19.2 MB | 2/7 | 442 |
| dotnet | 48.1ms | 1.0× | 1/7 | 70.4ms | 22.3ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 236.0ms | 11.9× | 4/7 | 268.0ms | 32.0ms | 28.9 MB | 4/7 | 6129302 |
| clojure | 186.9ms | 9.4× | 3/7 | 537.2ms | 350.3ms | 115.7 MB | 7/7 | 6129302 |
| elixir | 268.7ms | 13.6× | 5/7 | 460.7ms | 192.0ms | 72.9 MB | 6/7 | 6129302 |
| python | 1.449s | 73.2× | 7/7 | 1.461s | 11.8ms | 9.9 MB | 1/7 | 6129302 |
| node | 22.4ms | 1.1× | 2/7 | 40.6ms | 18.2ms | 49.5 MB | 5/7 | 6129302 |
| ruby | 450.3ms | 22.7× | 6/7 | 492.8ms | 42.5ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 19.8ms | 1.0× | 1/7 | 42.1ms | 22.3ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.8ms | 20.3× | 4/7 | 139.8ms | 32.0ms | 43.5 MB | 4/7 | 654353666 |
| clojure | 235.3ms | 44.4× | 5/7 | 585.6ms | 350.3ms | 118.7 MB | 7/7 | 654353666 |
| elixir | 63.5ms | 12.0× | 3/7 | 255.5ms | 192.0ms | 76.1 MB | 6/7 | 654353666 |
| python | 466.3ms | 88.0× | 7/7 | 478.1ms | 11.8ms | 10.4 MB | 1/7 | 654353666 |
| node | 19.6ms | 3.7× | 2/7 | 37.8ms | 18.2ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 301.4ms | 56.9× | 6/7 | 343.9ms | 42.5ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.3ms | 1.0× | 1/7 | 27.6ms | 22.3ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.0ms | 1.0× | 1/7 | 44.0ms | 32.0ms | 33.2 MB | 1/7 | 3388889 |
| clojure | 186.6ms | 15.5× | 7/7 | 536.9ms | 350.3ms | 168.5 MB | 6/7 | 3388889 |
| elixir | 128.7ms | 10.7× | 6/7 | 320.7ms | 192.0ms | 201.8 MB | 7/7 | 3388889 |
| python | 45.9ms | 3.8× | 3/7 | 57.7ms | 11.8ms | 39.8 MB | 2/7 | 3388889 |
| node | 68.0ms | 5.7× | 4/7 | 86.2ms | 18.2ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 95.2ms | 7.9× | 5/7 | 137.7ms | 42.5ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 34.1ms | 2.8× | 2/7 | 56.4ms | 22.3ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.8ms | 3.7× | 4/7 | 151.8ms | 32.0ms | 29.9 MB | 4/7 | 374854840 |
| clojure | 312.7ms | 9.8× | 7/7 | 663.0ms | 350.3ms | 302.3 MB | 7/7 | 374854840 |
| elixir | 169.1ms | 5.3× | 5/7 | 361.1ms | 192.0ms | 73.6 MB | 6/7 | 374854840 |
| python | 175.4ms | 5.5× | 6/7 | 187.2ms | 11.8ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.0ms | 1.0× | 1/7 | 50.2ms | 18.2ms | 49.8 MB | 5/7 | 374854840 |
| ruby | 76.1ms | 2.4× | 3/7 | 118.6ms | 42.5ms | 19.2 MB | 2/7 | 374854840 |
| dotnet | 38.0ms | 1.2× | 2/7 | 60.3ms | 22.3ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 92.2ms | 9.6× | 4/7 | 124.2ms | 32.0ms | 50.7 MB | 4/7 | 1638200 |
| clojure | 210.5ms | 21.9× | 7/7 | 560.8ms | 350.3ms | 149.9 MB | 7/7 | 1638200 |
| elixir | 9.6ms | 1.0× | 1/7 | 201.6ms | 192.0ms | 69.9 MB | 6/7 | 1638200 |
| python | 99.1ms | 10.3× | 5/7 | 110.9ms | 11.8ms | 10.0 MB | 1/7 | 1638200 |
| node | 22.9ms | 2.4× | 3/7 | 41.1ms | 18.2ms | 55.7 MB | 5/7 | 1638200 |
| ruby | 102.7ms | 10.7× | 6/7 | 145.2ms | 42.5ms | 19.5 MB | 2/7 | 1638200 |
| dotnet | 15.4ms | 1.6× | 2/7 | 37.7ms | 22.3ms | 32.2 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 157.6ms | 2.4× | 5/7 | 189.6ms | 32.0ms | 165.8 MB | 7/7 | 46468819 |
| clojure | 293.8ms | 4.4× | 7/7 | 644.1ms | 350.3ms | 123.2 MB | 5/7 | 46468819 |
| elixir | 127.6ms | 1.9× | 4/7 | 319.6ms | 192.0ms | 160.3 MB | 6/7 | 46468819 |
| python | 196.0ms | 3.0× | 6/7 | 207.8ms | 11.8ms | 25.9 MB | 2/7 | 46468819 |
| node | 109.6ms | 1.7× | 3/7 | 127.8ms | 18.2ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 84.7ms | 1.3× | 2/7 | 127.2ms | 42.5ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 66.2ms | 1.0× | 1/7 | 88.5ms | 22.3ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 86.3ms | 10.8× | 5/7 | 118.3ms | 32.0ms | 39.9 MB | 4/7 | 724 |
| clojure | 240.1ms | 30.0× | 7/7 | 590.4ms | 350.3ms | 132.6 MB | 7/7 | 724 |
| elixir | 19.5ms | 2.4× | 2/7 | 211.5ms | 192.0ms | 71.9 MB | 6/7 | 724 |
| python | 53.9ms | 6.7× | 4/7 | 65.7ms | 11.8ms | 9.7 MB | 1/7 | 724 |
| node | 8.0ms | 1.0× | 1/7 | 26.2ms | 18.2ms | 50.3 MB | 5/7 | 724 |
| ruby | 128.6ms | 16.1× | 6/7 | 171.1ms | 42.5ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.8ms | 2.6× | 3/7 | 43.1ms | 22.3ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.0ms | 1.9× | 2/7 | 76.0ms | 32.0ms | 29.3 MB | 3/7 | 9900000 |
| clojure | 1.180s | 50.9× | 7/7 | 1.531s | 350.3ms | 370.9 MB | 7/7 | 9900000 |
| elixir | 23.2ms | 1.0× | 1/7 | 215.2ms | 192.0ms | 70.1 MB | 6/7 | 9900000 |
| python | 48.8ms | 2.1× | 3/7 | 60.6ms | 11.8ms | 9.7 MB | 1/7 | 9900000 |
| node | 613.0ms | 26.4× | 6/7 | 631.2ms | 18.2ms | 50.0 MB | 5/7 | 9900000 |
| ruby | 123.1ms | 5.3× | 4/7 | 165.6ms | 42.5ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 301.7ms | 13.0× | 5/7 | 324.0ms | 22.3ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.9ms | 5.5× | 2/7 | 86.9ms | 32.0ms | 29.3 MB | 3/7 | 2475000 |
| clojure | 1.430s | 144.5× | 7/7 | 1.780s | 350.3ms | 374.4 MB | 7/7 | 2475000 |
| elixir | 9.9ms | 1.0× | 1/7 | 201.9ms | 192.0ms | 70.9 MB | 6/7 | 2475000 |
| python | 227.2ms | 22.9× | 5/7 | 239.0ms | 11.8ms | 9.8 MB | 1/7 | 2475000 |
| node | 222.4ms | 22.5× | 4/7 | 240.6ms | 18.2ms | 49.9 MB | 5/7 | 2475000 |
| ruby | 129.0ms | 13.0× | 3/7 | 171.5ms | 42.5ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 713.7ms | 72.1× | 6/7 | 736.0ms | 22.3ms | 32.9 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.8ms | 7.8× | 6/7 | 60.8ms | 32.0ms | 29.2 MB | 4/7 | 155553889038886 |
| clojure | 169.1ms | 45.7× | 7/7 | 519.4ms | 350.3ms | 107.8 MB | 7/7 | 155553889038886 |
| elixir | 12.9ms | 3.5× | 5/7 | 204.9ms | 192.0ms | 71.0 MB | 6/7 | 155553889038886 |
| python | 3.7ms | 1.0× | 1/7 | 15.5ms | 11.8ms | 9.7 MB | 1/7 | 155553889038886 |
| node | 10.5ms | 2.8× | 3/7 | 28.7ms | 18.2ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 11.4ms | 3.1× | 4/7 | 53.9ms | 42.5ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 8.8ms | 2.4× | 2/7 | 31.1ms | 22.3ms | 27.9 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 125.5ms | 6.4× | 4/7 | 157.5ms | 32.0ms | 92.1 MB | 5/7 | 6100000 |
| clojure | 208.5ms | 10.6× | 5/7 | 558.8ms | 350.3ms | 133.7 MB | 6/7 | 6100000 |
| elixir | 19.6ms | 1.0× | 1/7 | 211.6ms | 192.0ms | 77.1 MB | 4/7 | 6100000 |
| python | 568.0ms | 29.0× | 6/7 | 579.8ms | 11.8ms | 28.0 MB | 1/7 | 6100000 |
| node | 56.1ms | 2.9× | 3/7 | 74.3ms | 18.2ms | 51.3 MB | 3/7 | 6100000 |
| ruby | 1.683s | 85.8× | 7/7 | 1.725s | 42.5ms | 134.2 MB | 7/7 | 6100000 |
| dotnet | 20.4ms | 1.0× | 2/7 | 42.7ms | 22.3ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.1ms | 1.5× | 2/7 | 205.1ms | 32.0ms | 32.1 MB | 4/7 | 134626900 |
| clojure | 443.0ms | 3.7× | 5/7 | 793.3ms | 350.3ms | 137.5 MB | 6/7 | 134626900 |
| elixir | 349.0ms | 2.9× | 4/7 | 541.0ms | 192.0ms | 72.4 MB | 5/7 | 134626900 |
| python | 2.749s | 23.1× | 7/7 | 2.761s | 11.8ms | 21.9 MB | 2/7 | 134626900 |
| node | 320.0ms | 2.7× | 3/7 | 338.2ms | 18.2ms | 181.4 MB | 7/7 | 134626900 |
| ruby | 2.069s | 17.4× | 6/7 | 2.112s | 42.5ms | 19.3 MB | 1/7 | 134626900 |
| dotnet | 119.0ms | 1.0× | 1/7 | 141.3ms | 22.3ms | 28.0 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 153.6ms | 1.2× | 2/7 | 185.6ms | 32.0ms | 122.9 MB | 5/7 | 500 |
| clojure | 868.6ms | 6.9× | 7/7 | 1.219s | 350.3ms | 283.8 MB | 6/7 | 500 |
| elixir | 553.7ms | 4.4× | 6/7 | 745.7ms | 192.0ms | 482.9 MB | 7/7 | 500 |
| python | 181.4ms | 1.4× | 4/7 | 193.2ms | 11.8ms | 44.3 MB | 1/7 | 500 |
| node | 126.1ms | 1.0× | 1/7 | 144.3ms | 18.2ms | 64.9 MB | 4/7 | 500 |
| ruby | 214.3ms | 1.7× | 5/7 | 256.8ms | 42.5ms | 45.9 MB | 2/7 | 500 |
| dotnet | 153.8ms | 1.2× | 3/7 | 176.1ms | 22.3ms | 49.8 MB | 3/7 | 500 |
