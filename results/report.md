# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-27-generic-x86_64-with-glibc2.43 — 2026-07-11 06:44.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.9ms | 3.0× | 4/7 | 31.9ms | — | 24.1 MB | 3/7 | 0 |
| clojure | 352.6ms | 33.3× | 7/7 | 352.6ms | — | 101.5 MB | 7/7 | 0 |
| elixir | 188.6ms | 17.8× | 6/7 | 188.6ms | — | 70.1 MB | 6/7 | 0 |
| python | 10.6ms | 1.0× | 1/7 | 10.6ms | — | 9.6 MB | 1/7 | 0 |
| node | 18.8ms | 1.8× | 2/7 | 18.8ms | — | 42.2 MB | 5/7 | 0 |
| ruby | 40.4ms | 3.8× | 5/7 | 40.4ms | — | 19.0 MB | 2/7 | 0 |
| dotnet | 22.9ms | 2.2× | 3/7 | 22.9ms | — | 25.6 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.4ms | 1.3× | 2/7 | 86.3ms | 31.9ms | 27.8 MB | 4/7 | 9227465 |
| clojure | 206.6ms | 5.1× | 5/7 | 559.2ms | 352.6ms | 108.5 MB | 7/7 | 9227465 |
| elixir | 74.6ms | 1.8× | 4/7 | 263.2ms | 188.6ms | 70.9 MB | 6/7 | 9227465 |
| python | 754.2ms | 18.5× | 7/7 | 764.8ms | 10.6ms | 9.8 MB | 1/7 | 9227465 |
| node | 74.5ms | 1.8× | 3/7 | 93.3ms | 18.8ms | 47.6 MB | 5/7 | 9227465 |
| ruby | 616.4ms | 15.1× | 6/7 | 656.8ms | 40.4ms | 19.0 MB | 2/7 | 9227465 |
| dotnet | 40.7ms | 1.0× | 1/7 | 63.6ms | 22.9ms | 25.6 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.2ms | 3.4× | 3/7 | 70.1ms | 31.9ms | 27.8 MB | 4/7 | 449999985000000 |
| clojure | 148.5ms | 13.1× | 5/7 | 501.1ms | 352.6ms | 108.2 MB | 7/7 | 449999985000000 |
| elixir | 54.7ms | 4.8× | 4/7 | 243.3ms | 188.6ms | 71.8 MB | 6/7 | 449999985000000 |
| python | 2.413s | 213.6× | 7/7 | 2.424s | 10.6ms | 9.6 MB | 1/7 | 449999985000000 |
| node | 30.1ms | 2.7× | 2/7 | 48.9ms | 18.8ms | 49.5 MB | 5/7 | 449999985000000 |
| ruby | 628.5ms | 55.6× | 6/7 | 668.9ms | 40.4ms | 19.0 MB | 2/7 | 449999985000000 |
| dotnet | 11.3ms | 1.0× | 1/7 | 34.2ms | 22.9ms | 26.2 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 4.0ms | 1.0× | 1/7 | 35.9ms | 31.9ms | 24.0 MB | 3/7 | 12499997500000 |
| clojure | 176.4ms | 44.1× | 5/7 | 529.0ms | 352.6ms | 220.4 MB | 7/7 | 12499997500000 |
| elixir | 34.8ms | 8.7× | 3/7 | 223.4ms | 188.6ms | 70.0 MB | 5/7 | 12499997500000 |
| python | 108.9ms | 27.2× | 4/7 | 119.5ms | 10.6ms | 10.5 MB | 1/7 | 12499997500000 |
| node | 230.2ms | 57.5× | 6/7 | 249.0ms | 18.8ms | 89.7 MB | 6/7 | 12499997500000 |
| ruby | 231.5ms | 57.9× | 7/7 | 271.9ms | 40.4ms | 19.0 MB | 2/7 | 12499997500000 |
| dotnet | 11.0ms | 2.8× | 2/7 | 33.9ms | 22.9ms | 27.3 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.4ms | 5.0× | 4/7 | 73.3ms | 31.9ms | 28.2 MB | 4/7 | 13848 |
| clojure | 147.5ms | 18.0× | 7/7 | 500.1ms | 352.6ms | 108.4 MB | 7/7 | 13848 |
| elixir | 14.1ms | 1.7× | 3/7 | 202.7ms | 188.6ms | 72.7 MB | 6/7 | 13848 |
| python | 120.8ms | 14.7× | 5/7 | 131.4ms | 10.6ms | 9.9 MB | 1/7 | 13848 |
| node | 8.3ms | 1.0× | 2/7 | 27.1ms | 18.8ms | 48.2 MB | 5/7 | 13848 |
| ruby | 125.8ms | 15.3× | 6/7 | 166.2ms | 40.4ms | 19.0 MB | 2/7 | 13848 |
| dotnet | 8.2ms | 1.0× | 1/7 | 31.1ms | 22.9ms | 26.1 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 78.7ms | 1.7× | 2/7 | 110.6ms | 31.9ms | 28.1 MB | 4/7 | 442 |
| clojure | 418.8ms | 9.2× | 5/7 | 771.4ms | 352.6ms | 370.8 MB | 7/7 | 442 |
| elixir | 111.7ms | 2.4× | 3/7 | 300.3ms | 188.6ms | 70.7 MB | 6/7 | 442 |
| python | 2.679s | 58.6× | 7/7 | 2.689s | 10.6ms | 9.8 MB | 1/7 | 442 |
| node | 177.4ms | 3.9× | 4/7 | 196.2ms | 18.8ms | 47.8 MB | 5/7 | 442 |
| ruby | 889.3ms | 19.5× | 6/7 | 929.7ms | 40.4ms | 19.0 MB | 2/7 | 442 |
| dotnet | 45.7ms | 1.0× | 1/7 | 68.6ms | 22.9ms | 26.1 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 222.1ms | 12.3× | 4/7 | 254.0ms | 31.9ms | 28.2 MB | 4/7 | 6129302 |
| clojure | 156.0ms | 8.6× | 3/7 | 508.6ms | 352.6ms | 116.4 MB | 7/7 | 6129302 |
| elixir | 260.6ms | 14.4× | 5/7 | 449.2ms | 188.6ms | 70.1 MB | 6/7 | 6129302 |
| python | 1.406s | 77.7× | 7/7 | 1.417s | 10.6ms | 9.9 MB | 1/7 | 6129302 |
| node | 20.5ms | 1.1× | 2/7 | 39.3ms | 18.8ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 444.5ms | 24.6× | 6/7 | 484.9ms | 40.4ms | 19.2 MB | 2/7 | 6129302 |
| dotnet | 18.1ms | 1.0× | 1/7 | 41.0ms | 22.9ms | 26.1 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.4ms | 46.6× | 4/7 | 204.3ms | 31.9ms | 36.8 MB | 4/7 | 654353666 |
| clojure | 187.0ms | 50.5× | 5/7 | 539.6ms | 352.6ms | 117.4 MB | 7/7 | 654353666 |
| elixir | 58.4ms | 15.8× | 3/7 | 247.0ms | 188.6ms | 77.6 MB | 6/7 | 654353666 |
| python | 439.5ms | 118.8× | 7/7 | 450.1ms | 10.6ms | 10.3 MB | 1/7 | 654353666 |
| node | 15.9ms | 4.3× | 2/7 | 34.7ms | 18.8ms | 51.6 MB | 5/7 | 654353666 |
| ruby | 283.0ms | 76.5× | 6/7 | 323.4ms | 40.4ms | 19.3 MB | 2/7 | 654353666 |
| dotnet | 3.7ms | 1.0× | 1/7 | 26.6ms | 22.9ms | 26.5 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.1ms | 1.0× | 1/7 | 42.0ms | 31.9ms | 31.1 MB | 1/7 | 3388889 |
| clojure | 152.4ms | 15.1× | 7/7 | 505.0ms | 352.6ms | 168.1 MB | 6/7 | 3388889 |
| elixir | 110.0ms | 10.9× | 6/7 | 298.6ms | 188.6ms | 200.2 MB | 7/7 | 3388889 |
| python | 42.2ms | 4.2× | 3/7 | 52.8ms | 10.6ms | 39.9 MB | 2/7 | 3388889 |
| node | 64.9ms | 6.4× | 4/7 | 83.7ms | 18.8ms | 94.8 MB | 5/7 | 3388889 |
| ruby | 82.9ms | 8.2× | 5/7 | 123.3ms | 40.4ms | 47.7 MB | 3/7 | 3388889 |
| dotnet | 29.9ms | 3.0× | 2/7 | 52.8ms | 22.9ms | 56.6 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 116.6ms | 3.9× | 4/7 | 148.5ms | 31.9ms | 28.4 MB | 4/7 | 374854840 |
| clojure | 256.8ms | 8.6× | 7/7 | 609.4ms | 352.6ms | 302.1 MB | 7/7 | 374854840 |
| elixir | 164.8ms | 5.5× | 5/7 | 353.4ms | 188.6ms | 72.7 MB | 6/7 | 374854840 |
| python | 174.2ms | 5.8× | 6/7 | 184.8ms | 10.6ms | 9.9 MB | 1/7 | 374854840 |
| node | 29.8ms | 1.0× | 1/7 | 48.6ms | 18.8ms | 49.6 MB | 5/7 | 374854840 |
| ruby | 71.4ms | 2.4× | 3/7 | 111.8ms | 40.4ms | 19.0 MB | 2/7 | 374854840 |
| dotnet | 36.3ms | 1.2× | 2/7 | 59.2ms | 22.9ms | 27.1 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.2ms | 9.6× | 4/7 | 123.1ms | 31.9ms | 49.8 MB | 4/7 | 1638200 |
| clojure | 167.8ms | 17.7× | 7/7 | 520.4ms | 352.6ms | 150.0 MB | 7/7 | 1638200 |
| elixir | 9.5ms | 1.0× | 1/7 | 198.1ms | 188.6ms | 71.4 MB | 6/7 | 1638200 |
| python | 97.3ms | 10.2× | 5/7 | 107.9ms | 10.6ms | 10.1 MB | 1/7 | 1638200 |
| node | 20.5ms | 2.2× | 3/7 | 39.3ms | 18.8ms | 55.5 MB | 5/7 | 1638200 |
| ruby | 100.4ms | 10.6× | 6/7 | 140.8ms | 40.4ms | 19.3 MB | 2/7 | 1638200 |
| dotnet | 12.9ms | 1.4× | 2/7 | 35.8ms | 22.9ms | 32.1 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.4ms | 2.4× | 5/7 | 187.3ms | 31.9ms | 164.8 MB | 7/7 | 46468819 |
| clojure | 243.5ms | 3.8× | 7/7 | 596.1ms | 352.6ms | 123.8 MB | 5/7 | 46468819 |
| elixir | 100.5ms | 1.6× | 3/7 | 289.1ms | 188.6ms | 158.8 MB | 6/7 | 46468819 |
| python | 183.1ms | 2.8× | 6/7 | 193.7ms | 10.6ms | 25.8 MB | 2/7 | 46468819 |
| node | 104.0ms | 1.6× | 4/7 | 122.8ms | 18.8ms | 64.6 MB | 4/7 | 46468819 |
| ruby | 70.2ms | 1.1× | 2/7 | 110.6ms | 40.4ms | 24.8 MB | 1/7 | 46468819 |
| dotnet | 64.6ms | 1.0× | 1/7 | 87.5ms | 22.9ms | 29.5 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 88.3ms | 88.3× | 5/7 | 120.2ms | 31.9ms | 37.3 MB | 4/7 | 724 |
| clojure | 213.0ms | 213.0× | 7/7 | 565.6ms | 352.6ms | 132.4 MB | 7/7 | 724 |
| elixir | 0.1ms | < 1× | 1/7 | 188.7ms | 188.6ms | 71.7 MB | 6/7 | 724 |
| python | 53.9ms | 53.9× | 4/7 | 64.5ms | 10.6ms | 9.8 MB | 1/7 | 724 |
| node | 6.4ms | 6.4× | 2/7 | 25.2ms | 18.8ms | 50.1 MB | 5/7 | 724 |
| ruby | 120.6ms | 120.6× | 6/7 | 161.0ms | 40.4ms | 19.3 MB | 2/7 | 724 |
| dotnet | 18.5ms | 18.5× | 3/7 | 41.4ms | 22.9ms | 29.0 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.4ms | 2.5× | 2/7 | 69.3ms | 31.9ms | 28.2 MB | 3/7 | 9900000 |
| clojure | 1.086s | 71.9× | 7/7 | 1.439s | 352.6ms | 371.2 MB | 7/7 | 9900000 |
| elixir | 15.1ms | 1.0× | 1/7 | 203.7ms | 188.6ms | 71.8 MB | 6/7 | 9900000 |
| python | 48.8ms | 3.2× | 3/7 | 59.4ms | 10.6ms | 9.8 MB | 1/7 | 9900000 |
| node | 574.0ms | 38.0× | 6/7 | 592.8ms | 18.8ms | 50.0 MB | 5/7 | 9900000 |
| ruby | 106.4ms | 7.0× | 4/7 | 146.8ms | 40.4ms | 21.7 MB | 2/7 | 9900000 |
| dotnet | 299.4ms | 19.8× | 5/7 | 322.3ms | 22.9ms | 32.8 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.1ms | 53.1× | 2/7 | 85.0ms | 31.9ms | 28.2 MB | 3/7 | 2475000 |
| clojure | 1.317s | 1317.5× | 7/7 | 1.670s | 352.6ms | 374.7 MB | 7/7 | 2475000 |
| elixir | 0.5ms | < 1× | 1/7 | 189.1ms | 188.6ms | 71.6 MB | 6/7 | 2475000 |
| python | 231.3ms | 231.3× | 5/7 | 241.9ms | 10.6ms | 9.8 MB | 1/7 | 2475000 |
| node | 208.1ms | 208.1× | 4/7 | 226.9ms | 18.8ms | 49.7 MB | 5/7 | 2475000 |
| ruby | 111.4ms | 111.4× | 3/7 | 151.8ms | 40.4ms | 25.8 MB | 2/7 | 2475000 |
| dotnet | 684.8ms | 684.8× | 6/7 | 707.7ms | 22.9ms | 32.8 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 7.9× | 6/7 | 61.9ms | 31.9ms | 28.0 MB | 4/7 | 155553889038886 |
| clojure | 122.8ms | 32.3× | 7/7 | 475.4ms | 352.6ms | 108.5 MB | 7/7 | 155553889038886 |
| elixir | 8.5ms | 2.2× | 5/7 | 197.1ms | 188.6ms | 70.3 MB | 6/7 | 155553889038886 |
| python | 3.8ms | 1.0× | 1/7 | 14.4ms | 10.6ms | 9.8 MB | 1/7 | 155553889038886 |
| node | 7.3ms | 1.9× | 3/7 | 26.1ms | 18.8ms | 51.5 MB | 5/7 | 155553889038886 |
| ruby | 6.3ms | 1.7× | 2/7 | 46.7ms | 40.4ms | 19.7 MB | 2/7 | 155553889038886 |
| dotnet | 7.4ms | 1.9× | 4/7 | 30.3ms | 22.9ms | 27.8 MB | 3/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.667s | 108.9× | 7/7 | 1.699s | 31.9ms | 117.3 MB | 5/7 | 6100000 |
| clojure | 176.7ms | 11.5× | 4/7 | 529.3ms | 352.6ms | 133.5 MB | 7/7 | 6100000 |
| elixir | 15.3ms | 1.0× | 1/7 | 203.9ms | 188.6ms | 75.7 MB | 4/7 | 6100000 |
| python | 555.3ms | 36.3× | 5/7 | 565.9ms | 10.6ms | 28.0 MB | 1/7 | 6100000 |
| node | 53.1ms | 3.5× | 3/7 | 71.9ms | 18.8ms | 51.3 MB | 3/7 | 6100000 |
| ruby | 1.571s | 102.7× | 6/7 | 1.611s | 40.4ms | 133.5 MB | 6/7 | 6100000 |
| dotnet | 16.5ms | 1.1× | 2/7 | 39.4ms | 22.9ms | 31.0 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 162.4ms | 1.5× | 2/7 | 194.3ms | 31.9ms | 31.1 MB | 4/7 | 134626900 |
| clojure | 366.6ms | 3.3× | 5/7 | 719.2ms | 352.6ms | 135.3 MB | 6/7 | 134626900 |
| elixir | 297.4ms | 2.7× | 4/7 | 486.0ms | 188.6ms | 73.2 MB | 5/7 | 134626900 |
| python | 2.473s | 22.2× | 7/7 | 2.484s | 10.6ms | 21.9 MB | 2/7 | 134626900 |
| node | 290.0ms | 2.6× | 3/7 | 308.8ms | 18.8ms | 181.4 MB | 7/7 | 134626900 |
| ruby | 1.835s | 16.5× | 6/7 | 1.875s | 40.4ms | 19.0 MB | 1/7 | 134626900 |
| dotnet | 111.3ms | 1.0× | 1/7 | 134.2ms | 22.9ms | 28.1 MB | 3/7 | 134626900 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 141.4ms | 1.2× | 2/7 | 173.3ms | 31.9ms | 124.6 MB | 5/7 | 500 |
| clojure | 810.3ms | 6.8× | 7/7 | 1.163s | 352.6ms | 287.9 MB | 6/7 | 500 |
| elixir | 552.6ms | 4.6× | 6/7 | 741.2ms | 188.6ms | 488.9 MB | 7/7 | 500 |
| python | 175.7ms | 1.5× | 4/7 | 186.3ms | 10.6ms | 44.9 MB | 1/7 | 500 |
| node | 119.4ms | 1.0× | 1/7 | 138.2ms | 18.8ms | 64.6 MB | 4/7 | 500 |
| ruby | 205.6ms | 1.7× | 5/7 | 246.0ms | 40.4ms | 45.7 MB | 2/7 | 500 |
| dotnet | 142.8ms | 1.2× | 3/7 | 165.7ms | 22.9ms | 47.8 MB | 3/7 | 500 |
