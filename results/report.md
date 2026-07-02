# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-02 12:53.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.5ms | 2.9× | 4/7 | 29.5ms | — | 23.4 MB | 3/7 | 0 |
| clojure | 335.6ms | 32.6× | 7/7 | 335.6ms | — | 102.2 MB | 7/7 | 0 |
| elixir | 183.0ms | 17.8× | 6/7 | 183.0ms | — | 70.4 MB | 6/7 | 0 |
| python | 10.3ms | 1.0× | 1/7 | 10.3ms | — | 9.6 MB | 1/7 | 0 |
| node | 17.4ms | 1.7× | 2/7 | 17.4ms | — | 42.4 MB | 5/7 | 0 |
| ruby | 38.9ms | 3.8× | 5/7 | 38.9ms | — | 19.3 MB | 2/7 | 0 |
| dotnet | 21.5ms | 2.1× | 3/7 | 21.5ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.1ms | 1.3× | 2/7 | 82.6ms | 29.5ms | 26.8 MB | 4/7 | 9227465 |
| clojure | 208.6ms | 5.2× | 5/7 | 544.2ms | 335.6ms | 108.6 MB | 7/7 | 9227465 |
| elixir | 75.3ms | 1.9× | 3/7 | 258.3ms | 183.0ms | 72.2 MB | 6/7 | 9227465 |
| python | 747.6ms | 18.7× | 7/7 | 757.9ms | 10.3ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.7ms | 2.0× | 4/7 | 96.1ms | 17.4ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 608.8ms | 15.2× | 6/7 | 647.7ms | 38.9ms | 19.3 MB | 2/7 | 9227465 |
| dotnet | 40.0ms | 1.0× | 1/7 | 61.5ms | 21.5ms | 25.8 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.6ms | 3.0× | 3/7 | 66.1ms | 29.5ms | 27.1 MB | 4/7 | 449999985000000 |
| clojure | 146.9ms | 12.1× | 5/7 | 482.5ms | 335.6ms | 108.0 MB | 7/7 | 449999985000000 |
| elixir | 54.2ms | 4.5× | 4/7 | 237.2ms | 183.0ms | 70.6 MB | 6/7 | 449999985000000 |
| python | 2.281s | 188.5× | 7/7 | 2.291s | 10.3ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.3ms | 2.5× | 2/7 | 47.7ms | 17.4ms | 49.6 MB | 5/7 | 449999985000000 |
| ruby | 572.3ms | 47.3× | 6/7 | 611.2ms | 38.9ms | 19.3 MB | 2/7 | 449999985000000 |
| dotnet | 12.1ms | 1.0× | 1/7 | 33.6ms | 21.5ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.0ms | 1.0× | 1/7 | 32.5ms | 29.5ms | 23.6 MB | 3/7 | 12499997500000 |
| clojure | 181.8ms | 60.6× | 5/7 | 517.4ms | 335.6ms | 219.7 MB | 7/7 | 12499997500000 |
| elixir | 30.8ms | 10.3× | 3/7 | 213.8ms | 183.0ms | 70.4 MB | 5/7 | 12499997500000 |
| python | 107.2ms | 35.7× | 4/7 | 117.5ms | 10.3ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 220.0ms | 73.3× | 6/7 | 237.4ms | 17.4ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 229.5ms | 76.5× | 7/7 | 268.4ms | 38.9ms | 19.3 MB | 2/7 | 12499997500000 |
| dotnet | 12.1ms | 4.0× | 2/7 | 33.6ms | 21.5ms | 27.5 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 34.3ms | 4.0× | 4/7 | 63.8ms | 29.5ms | 26.9 MB | 4/7 | 13848 |
| clojure | 143.9ms | 16.9× | 7/7 | 479.5ms | 335.6ms | 109.6 MB | 7/7 | 13848 |
| elixir | 20.8ms | 2.4× | 3/7 | 203.8ms | 183.0ms | 72.8 MB | 6/7 | 13848 |
| python | 121.0ms | 14.2× | 6/7 | 131.3ms | 10.3ms | 9.9 MB | 1/7 | 13848 |
| node | 8.5ms | 1.0× | 1/7 | 25.9ms | 17.4ms | 48.1 MB | 5/7 | 13848 |
| ruby | 117.0ms | 13.8× | 5/7 | 155.9ms | 38.9ms | 19.3 MB | 2/7 | 13848 |
| dotnet | 8.5ms | 1.0× | 2/7 | 30.0ms | 21.5ms | 26.3 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.2ms | 1.6× | 2/7 | 104.7ms | 29.5ms | 27.0 MB | 4/7 | 442 |
| clojure | 431.0ms | 9.2× | 5/7 | 766.6ms | 335.6ms | 370.6 MB | 7/7 | 442 |
| elixir | 106.5ms | 2.3× | 3/7 | 289.5ms | 183.0ms | 71.4 MB | 6/7 | 442 |
| python | 2.312s | 49.3× | 7/7 | 2.322s | 10.3ms | 9.8 MB | 1/7 | 442 |
| node | 173.8ms | 3.7× | 4/7 | 191.2ms | 17.4ms | 48.0 MB | 5/7 | 442 |
| ruby | 864.4ms | 18.4× | 6/7 | 903.3ms | 38.9ms | 19.3 MB | 2/7 | 442 |
| dotnet | 46.9ms | 1.0× | 1/7 | 68.4ms | 21.5ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.6ms | 11.2× | 4/7 | 248.1ms | 29.5ms | 27.0 MB | 4/7 | 6129302 |
| clojure | 167.3ms | 8.5× | 3/7 | 502.9ms | 335.6ms | 115.5 MB | 7/7 | 6129302 |
| elixir | 253.1ms | 12.9× | 5/7 | 436.1ms | 183.0ms | 69.9 MB | 6/7 | 6129302 |
| python | 1.343s | 68.5× | 7/7 | 1.354s | 10.3ms | 10.0 MB | 1/7 | 6129302 |
| node | 20.9ms | 1.1× | 2/7 | 38.3ms | 17.4ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 419.6ms | 21.4× | 6/7 | 458.5ms | 38.9ms | 19.5 MB | 2/7 | 6129302 |
| dotnet | 19.6ms | 1.0× | 1/7 | 41.1ms | 21.5ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 93.1ms | 20.7× | 4/7 | 122.6ms | 29.5ms | 40.5 MB | 4/7 | 654353666 |
| clojure | 199.9ms | 44.4× | 5/7 | 535.5ms | 335.6ms | 118.1 MB | 7/7 | 654353666 |
| elixir | 64.0ms | 14.2× | 3/7 | 247.0ms | 183.0ms | 76.5 MB | 6/7 | 654353666 |
| python | 438.9ms | 97.5× | 7/7 | 449.2ms | 10.3ms | 10.4 MB | 1/7 | 654353666 |
| node | 16.3ms | 3.6× | 2/7 | 33.7ms | 17.4ms | 51.8 MB | 5/7 | 654353666 |
| ruby | 298.0ms | 66.2× | 6/7 | 336.9ms | 38.9ms | 19.5 MB | 2/7 | 654353666 |
| dotnet | 4.5ms | 1.0× | 1/7 | 26.0ms | 21.5ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.1ms | 1.0× | 1/7 | 39.6ms | 29.5ms | 29.8 MB | 1/7 | 3388889 |
| clojure | 168.1ms | 16.6× | 7/7 | 503.7ms | 335.6ms | 168.0 MB | 6/7 | 3388889 |
| elixir | 121.4ms | 12.0× | 6/7 | 304.4ms | 183.0ms | 200.2 MB | 7/7 | 3388889 |
| python | 42.8ms | 4.2× | 3/7 | 53.1ms | 10.3ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.5ms | 6.4× | 4/7 | 81.9ms | 17.4ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 83.2ms | 8.2× | 5/7 | 122.1ms | 38.9ms | 47.9 MB | 3/7 | 3388889 |
| dotnet | 31.5ms | 3.1× | 2/7 | 53.0ms | 21.5ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.9ms | 3.4× | 4/7 | 136.4ms | 29.5ms | 28.0 MB | 4/7 | 374854840 |
| clojure | 274.6ms | 8.8× | 7/7 | 610.2ms | 335.6ms | 302.5 MB | 7/7 | 374854840 |
| elixir | 176.9ms | 5.7× | 6/7 | 359.9ms | 183.0ms | 72.5 MB | 6/7 | 374854840 |
| python | 172.8ms | 5.5× | 5/7 | 183.1ms | 10.3ms | 9.9 MB | 1/7 | 374854840 |
| node | 31.3ms | 1.0× | 1/7 | 48.7ms | 17.4ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 72.3ms | 2.3× | 3/7 | 111.2ms | 38.9ms | 19.3 MB | 2/7 | 374854840 |
| dotnet | 38.2ms | 1.2× | 2/7 | 59.7ms | 21.5ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 87.6ms | 8.0× | 4/7 | 117.1ms | 29.5ms | 43.3 MB | 4/7 | 1638200 |
| clojure | 182.1ms | 16.7× | 7/7 | 517.7ms | 335.6ms | 151.0 MB | 7/7 | 1638200 |
| elixir | 10.9ms | 1.0× | 1/7 | 193.9ms | 183.0ms | 71.6 MB | 6/7 | 1638200 |
| python | 93.9ms | 8.6× | 5/7 | 104.2ms | 10.3ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.1ms | 1.8× | 3/7 | 37.5ms | 17.4ms | 55.6 MB | 5/7 | 1638200 |
| ruby | 95.3ms | 8.7× | 6/7 | 134.2ms | 38.9ms | 19.6 MB | 2/7 | 1638200 |
| dotnet | 14.3ms | 1.3× | 2/7 | 35.8ms | 21.5ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.1ms | 2.3× | 5/7 | 179.6ms | 29.5ms | 154.2 MB | 6/7 | 46468819 |
| clojure | 253.8ms | 3.8× | 7/7 | 589.4ms | 335.6ms | 123.9 MB | 5/7 | 46468819 |
| elixir | 117.7ms | 1.8× | 4/7 | 300.7ms | 183.0ms | 158.7 MB | 7/7 | 46468819 |
| python | 194.2ms | 2.9× | 6/7 | 204.5ms | 10.3ms | 25.9 MB | 2/7 | 46468819 |
| node | 103.2ms | 1.6× | 3/7 | 120.6ms | 17.4ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 71.6ms | 1.1× | 2/7 | 110.5ms | 38.9ms | 24.9 MB | 1/7 | 46468819 |
| dotnet | 66.4ms | 1.0× | 1/7 | 87.9ms | 21.5ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 98.6ms | 12.8× | 5/7 | 128.1ms | 29.5ms | 41.9 MB | 4/7 | 724 |
| clojure | 240.7ms | 31.3× | 7/7 | 576.3ms | 335.6ms | 136.4 MB | 7/7 | 724 |
| elixir | 8.1ms | 1.1× | 2/7 | 191.1ms | 183.0ms | 71.8 MB | 6/7 | 724 |
| python | 55.1ms | 7.2× | 4/7 | 65.4ms | 10.3ms | 9.8 MB | 1/7 | 724 |
| node | 7.7ms | 1.0× | 1/7 | 25.1ms | 17.4ms | 50.1 MB | 5/7 | 724 |
| ruby | 126.0ms | 16.4× | 6/7 | 164.9ms | 38.9ms | 19.5 MB | 2/7 | 724 |
| dotnet | 20.4ms | 2.6× | 3/7 | 41.9ms | 21.5ms | 29.2 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.3ms | 1.9× | 2/7 | 68.8ms | 29.5ms | 24.4 MB | 3/7 | 9900000 |
| clojure | 1.110s | 54.7× | 7/7 | 1.445s | 335.6ms | 370.9 MB | 7/7 | 9900000 |
| elixir | 20.3ms | 1.0× | 1/7 | 203.3ms | 183.0ms | 72.7 MB | 6/7 | 9900000 |
| python | 49.3ms | 2.4× | 3/7 | 59.6ms | 10.3ms | 9.8 MB | 1/7 | 9900000 |
| node | 575.3ms | 28.3× | 6/7 | 592.7ms | 17.4ms | 49.7 MB | 5/7 | 9900000 |
| ruby | 111.9ms | 5.5× | 4/7 | 150.8ms | 38.9ms | 21.9 MB | 2/7 | 9900000 |
| dotnet | 286.3ms | 14.1× | 5/7 | 307.8ms | 21.5ms | 33.0 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 49.5ms | 7.9× | 2/7 | 79.0ms | 29.5ms | 27.3 MB | 3/7 | 2475000 |
| clojure | 1.325s | 210.4× | 7/7 | 1.661s | 335.6ms | 375.1 MB | 7/7 | 2475000 |
| elixir | 6.3ms | 1.0× | 1/7 | 189.3ms | 183.0ms | 71.1 MB | 6/7 | 2475000 |
| python | 217.7ms | 34.6× | 5/7 | 228.0ms | 10.3ms | 9.8 MB | 1/7 | 2475000 |
| node | 208.0ms | 33.0× | 4/7 | 225.4ms | 17.4ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 113.0ms | 17.9× | 3/7 | 151.9ms | 38.9ms | 26.0 MB | 2/7 | 2475000 |
| dotnet | 675.7ms | 107.3× | 6/7 | 697.2ms | 21.5ms | 33.0 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 6.4× | 6/7 | 60.4ms | 29.5ms | 27.4 MB | 3/7 | 155553889038886 |
| clojure | 145.2ms | 30.3× | 7/7 | 480.8ms | 335.6ms | 108.5 MB | 7/7 | 155553889038886 |
| elixir | 10.2ms | 2.1× | 5/7 | 193.2ms | 183.0ms | 73.8 MB | 6/7 | 155553889038886 |
| python | 4.8ms | 1.0× | 1/7 | 15.1ms | 10.3ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 8.1ms | 1.7× | 4/7 | 25.5ms | 17.4ms | 51.6 MB | 5/7 | 155553889038886 |
| ruby | 7.7ms | 1.6× | 2/7 | 46.6ms | 38.9ms | 19.9 MB | 2/7 | 155553889038886 |
| dotnet | 7.9ms | 1.6× | 3/7 | 29.4ms | 21.5ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 93.6ms | 5.5× | 4/7 | 123.1ms | 29.5ms | 82.1 MB | 5/7 | 6100000 |
| clojure | 191.5ms | 11.3× | 5/7 | 527.1ms | 335.6ms | 134.7 MB | 7/7 | 6100000 |
| elixir | 24.1ms | 1.4× | 2/7 | 207.1ms | 183.0ms | 75.5 MB | 4/7 | 6100000 |
| python | 543.7ms | 32.2× | 6/7 | 554.0ms | 10.3ms | 28.1 MB | 1/7 | 6100000 |
| node | 53.0ms | 3.1× | 3/7 | 70.4ms | 17.4ms | 50.9 MB | 3/7 | 6100000 |
| ruby | 1.614s | 95.5× | 7/7 | 1.653s | 38.9ms | 132.8 MB | 6/7 | 6100000 |
| dotnet | 16.9ms | 1.0× | 1/7 | 38.4ms | 21.5ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 152.1ms | 1.3× | 2/7 | 181.6ms | 29.5ms | 30.1 MB | 4/7 | 134626900 |
| clojure | 406.6ms | 3.5× | 5/7 | 742.2ms | 335.6ms | 136.7 MB | 6/7 | 134626900 |
| elixir | 311.9ms | 2.7× | 4/7 | 494.9ms | 183.0ms | 72.8 MB | 5/7 | 134626900 |
| python | 2.559s | 22.1× | 7/7 | 2.569s | 10.3ms | 22.2 MB | 2/7 | 134626900 |
| node | 299.4ms | 2.6× | 3/7 | 316.8ms | 17.4ms | 181.4 MB | 7/7 | 134626900 |
| ruby | 1.927s | 16.6× | 6/7 | 1.966s | 38.9ms | 19.4 MB | 1/7 | 134626900 |
| dotnet | 115.9ms | 1.0× | 1/7 | 137.4ms | 21.5ms | 28.2 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.5ms | 1.2× | 2/7 | 174.0ms | 29.5ms | 124.0 MB | 5/7 | 500 |
| clojure | 842.1ms | 7.0× | 7/7 | 1.178s | 335.6ms | 292.0 MB | 6/7 | 500 |
| elixir | 567.7ms | 4.7× | 6/7 | 750.7ms | 183.0ms | 458.8 MB | 7/7 | 500 |
| python | 173.5ms | 1.4× | 4/7 | 183.8ms | 10.3ms | 44.4 MB | 1/7 | 500 |
| node | 119.7ms | 1.0× | 1/7 | 137.1ms | 17.4ms | 64.3 MB | 4/7 | 500 |
| ruby | 209.5ms | 1.8× | 5/7 | 248.4ms | 38.9ms | 46.0 MB | 2/7 | 500 |
| dotnet | 145.7ms | 1.2× | 3/7 | 167.2ms | 21.5ms | 48.2 MB | 3/7 | 500 |
