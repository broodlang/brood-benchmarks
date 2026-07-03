# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-03 09:52.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.6ms | 2.6× | 4/7 | 29.6ms | — | 24.1 MB | 3/7 | 0 |
| clojure | 336.5ms | 30.0× | 7/7 | 336.5ms | — | 103.3 MB | 7/7 | 0 |
| elixir | 184.6ms | 16.5× | 6/7 | 184.6ms | — | 73.0 MB | 6/7 | 0 |
| python | 11.2ms | 1.0× | 1/7 | 11.2ms | — | 9.7 MB | 1/7 | 0 |
| node | 17.4ms | 1.6× | 2/7 | 17.4ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 40.2ms | 3.6× | 5/7 | 40.2ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.7ms | 1.9× | 3/7 | 21.7ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 52.8ms | 1.3× | 2/7 | 82.4ms | 29.6ms | 27.3 MB | 4/7 | 9227465 |
| clojure | 214.1ms | 5.2× | 5/7 | 550.6ms | 336.5ms | 108.9 MB | 7/7 | 9227465 |
| elixir | 84.3ms | 2.1× | 4/7 | 268.9ms | 184.6ms | 70.1 MB | 6/7 | 9227465 |
| python | 730.5ms | 17.9× | 7/7 | 741.7ms | 11.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 73.0ms | 1.8× | 3/7 | 90.4ms | 17.4ms | 47.9 MB | 5/7 | 9227465 |
| ruby | 614.0ms | 15.0× | 6/7 | 654.2ms | 40.2ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 40.8ms | 1.0× | 1/7 | 62.5ms | 21.7ms | 25.9 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.2ms | 3.1× | 3/7 | 66.8ms | 29.6ms | 27.3 MB | 4/7 | 449999985000000 |
| clojure | 148.1ms | 12.2× | 5/7 | 484.6ms | 336.5ms | 108.4 MB | 7/7 | 449999985000000 |
| elixir | 67.9ms | 5.6× | 4/7 | 252.5ms | 184.6ms | 70.6 MB | 6/7 | 449999985000000 |
| python | 2.444s | 202.0× | 7/7 | 2.455s | 11.2ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 31.0ms | 2.6× | 2/7 | 48.4ms | 17.4ms | 49.9 MB | 5/7 | 449999985000000 |
| ruby | 600.0ms | 49.6× | 6/7 | 640.2ms | 40.2ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 33.8ms | 21.7ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.8ms | 1.0× | 1/7 | 33.4ms | 29.6ms | 23.8 MB | 3/7 | 12499997500000 |
| clojure | 188.4ms | 49.6× | 5/7 | 524.9ms | 336.5ms | 220.2 MB | 7/7 | 12499997500000 |
| elixir | 35.0ms | 9.2× | 3/7 | 219.6ms | 184.6ms | 72.0 MB | 5/7 | 12499997500000 |
| python | 106.1ms | 27.9× | 4/7 | 117.3ms | 11.2ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 235.5ms | 62.0× | 6/7 | 252.9ms | 17.4ms | 89.9 MB | 6/7 | 12499997500000 |
| ruby | 243.8ms | 64.2× | 7/7 | 284.0ms | 40.2ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 13.2ms | 3.5× | 2/7 | 34.9ms | 21.7ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.0ms | 3.8× | 4/7 | 63.6ms | 29.6ms | 27.4 MB | 4/7 | 13848 |
| clojure | 150.9ms | 17.0× | 7/7 | 487.4ms | 336.5ms | 108.4 MB | 7/7 | 13848 |
| elixir | 19.0ms | 2.1× | 3/7 | 203.6ms | 184.6ms | 70.6 MB | 6/7 | 13848 |
| python | 121.1ms | 13.6× | 6/7 | 132.3ms | 11.2ms | 9.9 MB | 1/7 | 13848 |
| node | 8.9ms | 1.0× | 1/7 | 26.3ms | 17.4ms | 48.4 MB | 5/7 | 13848 |
| ruby | 114.4ms | 12.9× | 5/7 | 154.6ms | 40.2ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.9ms | 1.0× | 2/7 | 30.6ms | 21.7ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 74.1ms | 1.7× | 2/7 | 103.7ms | 29.6ms | 27.5 MB | 4/7 | 442 |
| clojure | 412.3ms | 9.2× | 5/7 | 748.8ms | 336.5ms | 370.8 MB | 7/7 | 442 |
| elixir | 100.2ms | 2.2× | 3/7 | 284.8ms | 184.6ms | 70.2 MB | 6/7 | 442 |
| python | 2.432s | 54.5× | 7/7 | 2.444s | 11.2ms | 9.8 MB | 1/7 | 442 |
| node | 172.1ms | 3.9× | 4/7 | 189.5ms | 17.4ms | 48.3 MB | 5/7 | 442 |
| ruby | 844.2ms | 18.9× | 6/7 | 884.4ms | 40.2ms | 19.3 MB | 2/7 | 442 |
| dotnet | 44.6ms | 1.0× | 1/7 | 66.3ms | 21.7ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.1ms | 11.5× | 4/7 | 240.7ms | 29.6ms | 27.7 MB | 4/7 | 6129302 |
| clojure | 161.7ms | 8.8× | 3/7 | 498.2ms | 336.5ms | 115.9 MB | 7/7 | 6129302 |
| elixir | 251.0ms | 13.7× | 5/7 | 435.6ms | 184.6ms | 72.0 MB | 6/7 | 6129302 |
| python | 1.465s | 80.1× | 7/7 | 1.476s | 11.2ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.4ms | 1.1× | 2/7 | 37.8ms | 17.4ms | 49.7 MB | 5/7 | 6129302 |
| ruby | 414.9ms | 22.7× | 6/7 | 455.1ms | 40.2ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 18.3ms | 1.0× | 1/7 | 40.0ms | 21.7ms | 26.2 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.5ms | 21.3× | 4/7 | 121.1ms | 29.6ms | 40.6 MB | 4/7 | 654353666 |
| clojure | 193.1ms | 44.9× | 5/7 | 529.6ms | 336.5ms | 118.4 MB | 7/7 | 654353666 |
| elixir | 54.0ms | 12.6× | 3/7 | 238.6ms | 184.6ms | 75.1 MB | 6/7 | 654353666 |
| python | 452.1ms | 105.1× | 7/7 | 463.3ms | 11.2ms | 10.4 MB | 1/7 | 654353666 |
| node | 15.0ms | 3.5× | 2/7 | 32.4ms | 17.4ms | 52.0 MB | 5/7 | 654353666 |
| ruby | 278.7ms | 64.8× | 6/7 | 318.9ms | 40.2ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.3ms | 1.0× | 1/7 | 26.0ms | 21.7ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.7ms | 1.0× | 1/7 | 40.3ms | 29.6ms | 30.4 MB | 1/7 | 3388889 |
| clojure | 159.5ms | 14.9× | 7/7 | 496.0ms | 336.5ms | 168.5 MB | 6/7 | 3388889 |
| elixir | 114.3ms | 10.7× | 6/7 | 298.9ms | 184.6ms | 199.1 MB | 7/7 | 3388889 |
| python | 40.8ms | 3.8× | 3/7 | 52.0ms | 11.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 63.5ms | 5.9× | 4/7 | 80.9ms | 17.4ms | 95.0 MB | 5/7 | 3388889 |
| ruby | 80.8ms | 7.6× | 5/7 | 121.0ms | 40.2ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 30.4ms | 2.8× | 2/7 | 52.1ms | 21.7ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.8ms | 3.7× | 4/7 | 137.4ms | 29.6ms | 28.0 MB | 4/7 | 374854840 |
| clojure | 261.5ms | 9.0× | 7/7 | 598.0ms | 336.5ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 158.6ms | 5.4× | 5/7 | 343.2ms | 184.6ms | 72.1 MB | 6/7 | 374854840 |
| python | 166.3ms | 5.7× | 6/7 | 177.5ms | 11.2ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.2ms | 1.0× | 1/7 | 46.6ms | 17.4ms | 49.9 MB | 5/7 | 374854840 |
| ruby | 67.0ms | 2.3× | 3/7 | 107.2ms | 40.2ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 36.0ms | 1.2× | 2/7 | 57.7ms | 21.7ms | 27.2 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.8ms | 11.5× | 4/7 | 114.4ms | 29.6ms | 43.3 MB | 4/7 | 1638200 |
| clojure | 163.7ms | 22.1× | 7/7 | 500.2ms | 336.5ms | 150.0 MB | 7/7 | 1638200 |
| elixir | 7.4ms | 1.0× | 1/7 | 192.0ms | 184.6ms | 72.1 MB | 6/7 | 1638200 |
| python | 92.1ms | 12.4× | 5/7 | 103.3ms | 11.2ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.2ms | 2.7× | 3/7 | 37.6ms | 17.4ms | 55.9 MB | 5/7 | 1638200 |
| ruby | 95.2ms | 12.9× | 6/7 | 135.4ms | 40.2ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 13.8ms | 1.9× | 2/7 | 35.5ms | 21.7ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.1ms | 2.3× | 5/7 | 176.7ms | 29.6ms | 154.4 MB | 6/7 | 46468819 |
| clojure | 239.8ms | 3.7× | 7/7 | 576.3ms | 336.5ms | 124.2 MB | 5/7 | 46468819 |
| elixir | 104.8ms | 1.6× | 4/7 | 289.4ms | 184.6ms | 157.0 MB | 7/7 | 46468819 |
| python | 191.0ms | 2.9× | 6/7 | 202.2ms | 11.2ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.4ms | 1.6× | 3/7 | 120.8ms | 17.4ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 69.9ms | 1.1× | 2/7 | 110.1ms | 40.2ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 64.8ms | 1.0× | 1/7 | 86.5ms | 21.7ms | 29.8 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 79.8ms | 11.6× | 5/7 | 109.4ms | 29.6ms | 41.7 MB | 4/7 | 724 |
| clojure | 222.8ms | 32.3× | 7/7 | 559.3ms | 336.5ms | 132.7 MB | 7/7 | 724 |
| elixir | 6.9ms | 1.0× | 1/7 | 191.5ms | 184.6ms | 73.2 MB | 6/7 | 724 |
| python | 51.7ms | 7.5× | 4/7 | 62.9ms | 11.2ms | 9.8 MB | 1/7 | 724 |
| node | 7.0ms | 1.0× | 2/7 | 24.4ms | 17.4ms | 50.4 MB | 5/7 | 724 |
| ruby | 119.6ms | 17.3× | 6/7 | 159.8ms | 40.2ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.6ms | 2.8× | 3/7 | 41.3ms | 21.7ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.8ms | 2.3× | 2/7 | 67.4ms | 29.6ms | 24.8 MB | 3/7 | 9900000 |
| clojure | 1.079s | 66.2× | 7/7 | 1.415s | 336.5ms | 371.0 MB | 7/7 | 9900000 |
| elixir | 16.3ms | 1.0× | 1/7 | 200.9ms | 184.6ms | 70.0 MB | 6/7 | 9900000 |
| python | 46.2ms | 2.8× | 3/7 | 57.4ms | 11.2ms | 9.9 MB | 1/7 | 9900000 |
| node | 563.3ms | 34.6× | 6/7 | 580.7ms | 17.4ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 105.8ms | 6.5× | 4/7 | 146.0ms | 40.2ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 284.7ms | 17.5× | 5/7 | 306.4ms | 21.7ms | 32.9 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 51.0ms | 6.6× | 2/7 | 80.6ms | 29.6ms | 27.5 MB | 3/7 | 2475000 |
| clojure | 1.311s | 170.2× | 7/7 | 1.647s | 336.5ms | 375.2 MB | 7/7 | 2475000 |
| elixir | 7.7ms | 1.0× | 1/7 | 192.3ms | 184.6ms | 70.2 MB | 6/7 | 2475000 |
| python | 215.3ms | 28.0× | 5/7 | 226.5ms | 11.2ms | 9.9 MB | 1/7 | 2475000 |
| node | 205.6ms | 26.7× | 4/7 | 223.0ms | 17.4ms | 50.0 MB | 5/7 | 2475000 |
| ruby | 109.2ms | 14.2× | 3/7 | 149.4ms | 40.2ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 681.9ms | 88.6× | 6/7 | 703.6ms | 21.7ms | 33.3 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.0ms | 7.8× | 6/7 | 54.6ms | 29.6ms | 27.2 MB | 3/7 | 155553889038886 |
| clojure | 127.9ms | 40.0× | 7/7 | 464.4ms | 336.5ms | 108.8 MB | 7/7 | 155553889038886 |
| elixir | 3.3ms | 1.0× | 2/7 | 187.9ms | 184.6ms | 71.1 MB | 6/7 | 155553889038886 |
| python | 3.2ms | 1.0× | 1/7 | 14.4ms | 11.2ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.7ms | 2.4× | 4/7 | 25.1ms | 17.4ms | 51.8 MB | 5/7 | 155553889038886 |
| ruby | 6.5ms | 2.0× | 3/7 | 46.7ms | 40.2ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.8ms | 2.4× | 5/7 | 29.5ms | 21.7ms | 28.0 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.6ms | 5.3× | 4/7 | 118.2ms | 29.6ms | 73.5 MB | 4/7 | 6100000 |
| clojure | 180.3ms | 10.7× | 5/7 | 516.8ms | 336.5ms | 133.5 MB | 7/7 | 6100000 |
| elixir | 16.9ms | 1.0× | 2/7 | 201.5ms | 184.6ms | 77.7 MB | 5/7 | 6100000 |
| python | 545.8ms | 32.5× | 6/7 | 557.0ms | 11.2ms | 28.1 MB | 1/7 | 6100000 |
| node | 51.9ms | 3.1× | 3/7 | 69.3ms | 17.4ms | 51.4 MB | 3/7 | 6100000 |
| ruby | 1.572s | 93.6× | 7/7 | 1.612s | 40.2ms | 132.6 MB | 6/7 | 6100000 |
| dotnet | 16.8ms | 1.0× | 1/7 | 38.5ms | 21.7ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.4ms | 1.4× | 2/7 | 180.0ms | 29.6ms | 30.7 MB | 4/7 | 134626900 |
| clojure | 384.7ms | 3.6× | 5/7 | 721.2ms | 336.5ms | 137.0 MB | 6/7 | 134626900 |
| elixir | 302.7ms | 2.8× | 4/7 | 487.3ms | 184.6ms | 73.2 MB | 5/7 | 134626900 |
| python | 2.574s | 23.8× | 7/7 | 2.585s | 11.2ms | 22.3 MB | 2/7 | 134626900 |
| node | 291.2ms | 2.7× | 3/7 | 308.6ms | 17.4ms | 182.0 MB | 7/7 | 134626900 |
| ruby | 1.865s | 17.3× | 6/7 | 1.905s | 40.2ms | 19.4 MB | 1/7 | 134626900 |
| dotnet | 108.1ms | 1.0× | 1/7 | 129.8ms | 21.7ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 141.9ms | 1.2× | 2/7 | 171.5ms | 29.6ms | 128.3 MB | 5/7 | 500 |
| clojure | 785.6ms | 6.8× | 7/7 | 1.122s | 336.5ms | 274.8 MB | 6/7 | 500 |
| elixir | 538.9ms | 4.7× | 6/7 | 723.5ms | 184.6ms | 474.2 MB | 7/7 | 500 |
| python | 170.0ms | 1.5× | 4/7 | 181.2ms | 11.2ms | 44.5 MB | 1/7 | 500 |
| node | 115.0ms | 1.0× | 1/7 | 132.4ms | 17.4ms | 64.6 MB | 4/7 | 500 |
| ruby | 200.2ms | 1.7× | 5/7 | 240.4ms | 40.2ms | 46.0 MB | 2/7 | 500 |
| dotnet | 146.4ms | 1.3× | 3/7 | 168.1ms | 21.7ms | 50.3 MB | 3/7 | 500 |
