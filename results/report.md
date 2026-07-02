# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 10:50.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.5ms | 3.0× | 4/7 | 30.5ms | — | 23.4 MB | 3/7 | 0 |
| clojure | 341.7ms | 33.8× | 7/7 | 341.7ms | — | 102.7 MB | 7/7 | 0 |
| elixir | 185.4ms | 18.4× | 6/7 | 185.4ms | — | 71.8 MB | 6/7 | 0 |
| python | 10.1ms | 1.0× | 1/7 | 10.1ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.5ms | 1.7× | 2/7 | 17.5ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 39.3ms | 3.9× | 5/7 | 39.3ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.1ms | 2.1× | 3/7 | 21.1ms | — | 25.7 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 220.5ms | 5.6× | 5/7 | 251.0ms | 30.5ms | 27.6 MB | 4/7 | 9227465 |
| clojure | 193.9ms | 4.9× | 4/7 | 535.6ms | 341.7ms | 108.7 MB | 7/7 | 9227465 |
| elixir | 71.3ms | 1.8× | 2/7 | 256.7ms | 185.4ms | 72.0 MB | 6/7 | 9227465 |
| python | 780.2ms | 19.7× | 7/7 | 790.3ms | 10.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 76.5ms | 1.9× | 3/7 | 94.0ms | 17.5ms | 47.7 MB | 5/7 | 9227465 |
| ruby | 610.3ms | 15.4× | 6/7 | 649.6ms | 39.3ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 39.6ms | 1.0× | 1/7 | 60.7ms | 21.1ms | 25.7 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.4ms | 2.6× | 3/7 | 65.9ms | 30.5ms | 26.5 MB | 4/7 | 449999985000000 |
| clojure | 142.2ms | 10.5× | 5/7 | 483.9ms | 341.7ms | 108.5 MB | 7/7 | 449999985000000 |
| elixir | 57.0ms | 4.2× | 4/7 | 242.4ms | 185.4ms | 72.1 MB | 6/7 | 449999985000000 |
| python | 2.274s | 168.4× | 7/7 | 2.284s | 10.1ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 29.9ms | 2.2× | 2/7 | 47.4ms | 17.5ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 574.7ms | 42.6× | 6/7 | 614.0ms | 39.3ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 13.5ms | 1.0× | 1/7 | 34.6ms | 21.1ms | 26.4 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.4ms | 1.0× | 1/7 | 32.9ms | 30.5ms | 23.3 MB | 3/7 | 12499997500000 |
| clojure | 177.6ms | 74.0× | 5/7 | 519.3ms | 341.7ms | 221.5 MB | 7/7 | 12499997500000 |
| elixir | 28.6ms | 11.9× | 3/7 | 214.0ms | 185.4ms | 72.0 MB | 5/7 | 12499997500000 |
| python | 107.4ms | 44.8× | 4/7 | 117.5ms | 10.1ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 219.6ms | 91.5× | 6/7 | 237.1ms | 17.5ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 224.5ms | 93.5× | 7/7 | 263.8ms | 39.3ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 12.8ms | 5.3× | 2/7 | 33.9ms | 21.1ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.0ms | 3.8× | 4/7 | 63.5ms | 30.5ms | 27.2 MB | 4/7 | 13848 |
| clojure | 144.2ms | 16.8× | 7/7 | 485.9ms | 341.7ms | 108.9 MB | 7/7 | 13848 |
| elixir | 16.3ms | 1.9× | 3/7 | 201.7ms | 185.4ms | 70.9 MB | 6/7 | 13848 |
| python | 122.1ms | 14.2× | 6/7 | 132.2ms | 10.1ms | 9.9 MB | 1/7 | 13848 |
| node | 8.6ms | 1.0× | 1/7 | 26.1ms | 17.5ms | 48.2 MB | 5/7 | 13848 |
| ruby | 115.8ms | 13.5× | 5/7 | 155.1ms | 39.3ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 9.8ms | 1.1× | 2/7 | 30.9ms | 21.1ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 73.2ms | 1.6× | 2/7 | 103.7ms | 30.5ms | 27.3 MB | 4/7 | 442 |
| clojure | 428.7ms | 9.4× | 5/7 | 770.4ms | 341.7ms | 370.6 MB | 7/7 | 442 |
| elixir | 103.2ms | 2.3× | 3/7 | 288.6ms | 185.4ms | 70.0 MB | 6/7 | 442 |
| python | 2.477s | 54.4× | 7/7 | 2.487s | 10.1ms | 9.8 MB | 1/7 | 442 |
| node | 180.4ms | 4.0× | 4/7 | 197.9ms | 17.5ms | 48.0 MB | 5/7 | 442 |
| ruby | 862.0ms | 18.9× | 6/7 | 901.3ms | 39.3ms | 19.3 MB | 2/7 | 442 |
| dotnet | 45.5ms | 1.0× | 1/7 | 66.6ms | 21.1ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 211.8ms | 11.0× | 4/7 | 242.3ms | 30.5ms | 27.5 MB | 4/7 | 6129302 |
| clojure | 169.2ms | 8.8× | 3/7 | 510.9ms | 341.7ms | 115.6 MB | 7/7 | 6129302 |
| elixir | 261.5ms | 13.5× | 5/7 | 446.9ms | 185.4ms | 70.5 MB | 6/7 | 6129302 |
| python | 1.449s | 75.1× | 7/7 | 1.459s | 10.1ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.1ms | 1.0× | 2/7 | 37.6ms | 17.5ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 417.8ms | 21.6× | 6/7 | 457.1ms | 39.3ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 19.3ms | 1.0× | 1/7 | 40.4ms | 21.1ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 92.8ms | 15.7× | 4/7 | 123.3ms | 30.5ms | 40.2 MB | 4/7 | 654353666 |
| clojure | 200.1ms | 33.9× | 5/7 | 541.8ms | 341.7ms | 118.7 MB | 7/7 | 654353666 |
| elixir | 54.4ms | 9.2× | 3/7 | 239.8ms | 185.4ms | 78.3 MB | 6/7 | 654353666 |
| python | 463.9ms | 78.6× | 7/7 | 474.0ms | 10.1ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.4ms | 2.8× | 2/7 | 33.9ms | 17.5ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 290.3ms | 49.2× | 6/7 | 329.6ms | 39.3ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 5.9ms | 1.0× | 1/7 | 27.0ms | 21.1ms | 26.6 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.0ms | 1.0× | 1/7 | 40.5ms | 30.5ms | 29.9 MB | 1/7 | 3388889 |
| clojure | 154.0ms | 15.4× | 7/7 | 495.7ms | 341.7ms | 168.4 MB | 6/7 | 3388889 |
| elixir | 118.0ms | 11.8× | 6/7 | 303.4ms | 185.4ms | 201.9 MB | 7/7 | 3388889 |
| python | 43.2ms | 4.3× | 3/7 | 53.3ms | 10.1ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.3ms | 6.4× | 4/7 | 81.8ms | 17.5ms | 94.7 MB | 5/7 | 3388889 |
| ruby | 82.6ms | 8.3× | 5/7 | 121.9ms | 39.3ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.6ms | 3.2× | 2/7 | 52.7ms | 21.1ms | 56.9 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 104.9ms | 3.5× | 4/7 | 135.4ms | 30.5ms | 28.0 MB | 4/7 | 374854840 |
| clojure | 270.3ms | 9.0× | 7/7 | 612.0ms | 341.7ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 159.3ms | 5.3× | 5/7 | 344.7ms | 185.4ms | 70.9 MB | 6/7 | 374854840 |
| python | 176.3ms | 5.9× | 6/7 | 186.4ms | 10.1ms | 9.9 MB | 1/7 | 374854840 |
| node | 30.0ms | 1.0× | 1/7 | 47.5ms | 17.5ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 70.5ms | 2.4× | 3/7 | 109.8ms | 39.3ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 39.0ms | 1.3× | 2/7 | 60.1ms | 21.1ms | 27.5 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 86.7ms | 8.2× | 4/7 | 117.2ms | 30.5ms | 43.3 MB | 4/7 | 1638200 |
| clojure | 173.0ms | 16.3× | 7/7 | 514.7ms | 341.7ms | 150.9 MB | 7/7 | 1638200 |
| elixir | 10.6ms | 1.0× | 1/7 | 196.0ms | 185.4ms | 72.7 MB | 6/7 | 1638200 |
| python | 93.7ms | 8.8× | 5/7 | 103.8ms | 10.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.2ms | 1.9× | 3/7 | 37.7ms | 17.5ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 97.0ms | 9.2× | 6/7 | 136.3ms | 39.3ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.8ms | 1.4× | 2/7 | 35.9ms | 21.1ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 153.2ms | 2.3× | 5/7 | 183.7ms | 30.5ms | 153.9 MB | 6/7 | 46468819 |
| clojure | 254.0ms | 3.8× | 7/7 | 595.7ms | 341.7ms | 123.9 MB | 5/7 | 46468819 |
| elixir | 108.3ms | 1.6× | 4/7 | 293.7ms | 185.4ms | 159.0 MB | 7/7 | 46468819 |
| python | 203.3ms | 3.0× | 6/7 | 213.4ms | 10.1ms | 25.8 MB | 2/7 | 46468819 |
| node | 103.9ms | 1.5× | 3/7 | 121.4ms | 17.5ms | 64.7 MB | 4/7 | 46468819 |
| ruby | 71.7ms | 1.1× | 2/7 | 111.0ms | 39.3ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 67.1ms | 1.0× | 1/7 | 88.2ms | 21.1ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.2ms | 14.4× | 5/7 | 132.7ms | 30.5ms | 41.7 MB | 4/7 | 724 |
| clojure | 256.0ms | 36.1× | 7/7 | 597.7ms | 341.7ms | 136.0 MB | 7/7 | 724 |
| elixir | 7.3ms | 1.0× | 2/7 | 192.7ms | 185.4ms | 72.7 MB | 6/7 | 724 |
| python | 53.2ms | 7.5× | 4/7 | 63.3ms | 10.1ms | 9.8 MB | 1/7 | 724 |
| node | 7.1ms | 1.0× | 1/7 | 24.6ms | 17.5ms | 50.1 MB | 5/7 | 724 |
| ruby | 123.9ms | 17.5× | 6/7 | 163.2ms | 39.3ms | 19.5 MB | 2/7 | 724 |
| dotnet | 19.7ms | 2.8× | 3/7 | 40.8ms | 21.1ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 1.9× | 2/7 | 69.4ms | 30.5ms | 24.3 MB | 3/7 | 9900000 |
| clojure | 1.092s | 53.8× | 7/7 | 1.433s | 341.7ms | 371.1 MB | 7/7 | 9900000 |
| elixir | 20.3ms | 1.0× | 1/7 | 205.7ms | 185.4ms | 72.5 MB | 6/7 | 9900000 |
| python | 47.7ms | 2.3× | 3/7 | 57.8ms | 10.1ms | 9.8 MB | 1/7 | 9900000 |
| node | 564.1ms | 27.8× | 6/7 | 581.6ms | 17.5ms | 49.9 MB | 5/7 | 9900000 |
| ruby | 108.9ms | 5.4× | 4/7 | 148.2ms | 39.3ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 299.9ms | 14.8× | 5/7 | 321.0ms | 21.1ms | 33.1 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 48.4ms | 6.8× | 2/7 | 78.9ms | 30.5ms | 27.2 MB | 3/7 | 2475000 |
| clojure | 1.341s | 188.9× | 7/7 | 1.683s | 341.7ms | 374.6 MB | 7/7 | 2475000 |
| elixir | 7.1ms | 1.0× | 1/7 | 192.5ms | 185.4ms | 70.0 MB | 6/7 | 2475000 |
| python | 230.6ms | 32.5× | 5/7 | 240.7ms | 10.1ms | 9.8 MB | 1/7 | 2475000 |
| node | 217.0ms | 30.6× | 4/7 | 234.5ms | 17.5ms | 49.5 MB | 5/7 | 2475000 |
| ruby | 123.5ms | 17.4× | 3/7 | 162.8ms | 39.3ms | 26.1 MB | 2/7 | 2475000 |
| dotnet | 703.7ms | 99.1× | 6/7 | 724.8ms | 21.1ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.8ms | 7.3× | 6/7 | 61.3ms | 30.5ms | 27.1 MB | 3/7 | 155553889038886 |
| clojure | 130.7ms | 31.1× | 7/7 | 472.4ms | 341.7ms | 108.6 MB | 7/7 | 155553889038886 |
| elixir | 6.0ms | 1.4× | 2/7 | 191.4ms | 185.4ms | 71.7 MB | 6/7 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/7 | 14.3ms | 10.1ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.5ms | 2.0× | 4/7 | 26.0ms | 17.5ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.1ms | 1.7× | 3/7 | 46.4ms | 39.3ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 9.4ms | 2.2× | 5/7 | 30.5ms | 21.1ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.2ms | 6.9× | 4/7 | 158.7ms | 30.5ms | 79.7 MB | 5/7 | 6100000 |
| clojure | 189.1ms | 10.1× | 5/7 | 530.8ms | 341.7ms | 135.3 MB | 7/7 | 6100000 |
| elixir | 20.3ms | 1.1× | 2/7 | 205.7ms | 185.4ms | 77.0 MB | 4/7 | 6100000 |
| python | 549.7ms | 29.4× | 6/7 | 559.8ms | 10.1ms | 28.1 MB | 1/7 | 6100000 |
| node | 52.7ms | 2.8× | 3/7 | 70.2ms | 17.5ms | 51.3 MB | 3/7 | 6100000 |
| ruby | 1.588s | 84.9× | 7/7 | 1.628s | 39.3ms | 132.7 MB | 6/7 | 6100000 |
| dotnet | 18.7ms | 1.0× | 1/7 | 39.8ms | 21.1ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 847.0ms | 7.3× | 5/7 | 877.5ms | 30.5ms | 32.9 MB | 4/7 | 134626900 |
| clojure | 393.2ms | 3.4× | 4/7 | 734.9ms | 341.7ms | 135.5 MB | 6/7 | 134626900 |
| elixir | 331.9ms | 2.8× | 3/7 | 517.3ms | 185.4ms | 71.2 MB | 5/7 | 134626900 |
| python | 2.566s | 22.0× | 7/7 | 2.576s | 10.1ms | 22.2 MB | 2/7 | 134626900 |
| node | 300.4ms | 2.6× | 2/7 | 317.9ms | 17.5ms | 180.9 MB | 7/7 | 134626900 |
| ruby | 1.912s | 16.4× | 6/7 | 1.952s | 39.3ms | 19.4 MB | 1/7 | 134626900 |
| dotnet | 116.5ms | 1.0× | 1/7 | 137.6ms | 21.1ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 149.4ms | 1.2× | 2/7 | 179.9ms | 30.5ms | 126.4 MB | 5/7 | 500 |
| clojure | 810.7ms | 6.6× | 7/7 | 1.152s | 341.7ms | 266.9 MB | 6/7 | 500 |
| elixir | 540.7ms | 4.4× | 6/7 | 726.1ms | 185.4ms | 513.7 MB | 7/7 | 500 |
| python | 176.5ms | 1.4× | 4/7 | 186.6ms | 10.1ms | 45.0 MB | 1/7 | 500 |
| node | 122.0ms | 1.0× | 1/7 | 139.5ms | 17.5ms | 64.4 MB | 4/7 | 500 |
| ruby | 211.5ms | 1.7× | 5/7 | 250.8ms | 39.3ms | 45.9 MB | 2/7 | 500 |
| dotnet | 153.6ms | 1.3× | 3/7 | 174.7ms | 21.1ms | 48.2 MB | 3/7 | 500 |
