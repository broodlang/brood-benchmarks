# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-22 14:01.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.9ms | 2.4× | 4/7 | 26.9ms | — | 20.8 MB | 2/7 | 0 |
| elixir | 208.9ms | 18.7× | 6/7 | 208.9ms | — | 70.1 MB | 6/7 | 0 |
| python | 11.2ms | 1.0× | 1/7 | 11.2ms | — | 9.8 MB | 1/7 | 0 |
| node | 19.0ms | 1.7× | 2/7 | 19.0ms | — | 43.2 MB | 5/7 | 0 |
| ruby | 43.2ms | 3.9× | 5/7 | 43.2ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.8ms | 2.0× | 3/7 | 22.8ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 228.7ms | 5.3× | 4/7 | 255.6ms | 26.9ms | 24.7 MB | 3/7 | 9227465 |
| elixir | 83.4ms | 1.9× | 2/7 | 292.3ms | 208.9ms | 69.8 MB | 6/7 | 9227465 |
| python | 838.5ms | 19.3× | 7/7 | 849.7ms | 11.2ms | 9.8 MB | 1/7 | 9227465 |
| node | 85.0ms | 2.0× | 3/7 | 104.0ms | 19.0ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 702.8ms | 16.2× | 6/7 | 746.0ms | 43.2ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 43.4ms | 1.0× | 1/7 | 66.2ms | 22.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.9ms | 3.0× | 3/7 | 66.8ms | 26.9ms | 24.3 MB | 3/7 | 449999985000000 |
| elixir | 62.0ms | 4.7× | 4/7 | 270.9ms | 208.9ms | 69.8 MB | 6/7 | 449999985000000 |
| python | 2.396s | 182.9× | 7/7 | 2.407s | 11.2ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 33.3ms | 2.5× | 2/7 | 52.3ms | 19.0ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 622.6ms | 47.5× | 6/7 | 665.8ms | 43.2ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 13.1ms | 1.0× | 1/7 | 35.9ms | 22.8ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.3ms | 1.0× | 1/7 | 30.2ms | 26.9ms | 20.7 MB | 2/7 | 12499997500000 |
| elixir | 64.4ms | 19.5× | 3/7 | 273.3ms | 208.9ms | 70.1 MB | 5/7 | 12499997500000 |
| python | 127.5ms | 38.6× | 4/7 | 138.7ms | 11.2ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 242.3ms | 73.4× | 5/7 | 261.3ms | 19.0ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 251.9ms | 76.3× | 6/7 | 295.1ms | 43.2ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 13.8ms | 4.2× | 2/7 | 36.6ms | 22.8ms | 27.7 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.8ms | 3.2× | 4/7 | 62.7ms | 26.9ms | 24.6 MB | 3/7 | 13848 |
| elixir | 30.4ms | 2.7× | 3/7 | 239.3ms | 208.9ms | 69.9 MB | 6/7 | 13848 |
| python | 141.3ms | 12.7× | 6/7 | 152.5ms | 11.2ms | 9.9 MB | 1/7 | 13848 |
| node | 11.3ms | 1.0× | 2/7 | 30.3ms | 19.0ms | 49.1 MB | 5/7 | 13848 |
| ruby | 132.2ms | 11.9× | 5/7 | 175.4ms | 43.2ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 11.1ms | 1.0× | 1/7 | 33.9ms | 22.8ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 90.3ms | 1.8× | 2/7 | 117.2ms | 26.9ms | 24.6 MB | 3/7 | 442 |
| elixir | 134.8ms | 2.7× | 3/7 | 343.7ms | 208.9ms | 70.0 MB | 6/7 | 442 |
| python | 2.714s | 55.1× | 7/7 | 2.725s | 11.2ms | 9.8 MB | 1/7 | 442 |
| node | 188.4ms | 3.8× | 4/7 | 207.4ms | 19.0ms | 48.9 MB | 5/7 | 442 |
| ruby | 911.2ms | 18.5× | 6/7 | 954.4ms | 43.2ms | 23.5 MB | 2/7 | 442 |
| dotnet | 49.3ms | 1.0× | 1/7 | 72.1ms | 22.8ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 224.6ms | 9.9× | 3/7 | 251.5ms | 26.9ms | 25.8 MB | 3/7 | 6129302 |
| elixir | 258.5ms | 11.4× | 4/7 | 467.4ms | 208.9ms | 70.1 MB | 6/7 | 6129302 |
| python | 1.526s | 67.5× | 7/7 | 1.537s | 11.2ms | 10.1 MB | 1/7 | 6129302 |
| node | 23.8ms | 1.1× | 2/7 | 42.8ms | 19.0ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 492.6ms | 21.8× | 6/7 | 535.8ms | 43.2ms | 23.7 MB | 2/7 | 6129302 |
| dotnet | 22.6ms | 1.0× | 1/7 | 45.4ms | 22.8ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | — | — | — | — | — | — | — | ERROR |
| elixir | 80.6ms | 14.7× | 3/6 | 289.5ms | 208.9ms | 75.3 MB | 5/6 | 654353666 |
| python | 523.2ms | 95.1× | 5/6 | 534.4ms | 11.2ms | 10.4 MB | 1/6 | 654353666 |
| node | 24.3ms | 4.4× | 2/6 | 43.3ms | 19.0ms | 52.8 MB | 4/6 | 654353666 |
| ruby | 329.5ms | 59.9× | 4/6 | 372.7ms | 43.2ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 5.5ms | 1.0× | 1/6 | 28.3ms | 22.8ms | 26.8 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 14.0ms | 1.0× | 1/7 | 40.9ms | 26.9ms | 32.1 MB | 1/7 | 3388889 |
| elixir | 137.3ms | 9.8× | 6/7 | 346.2ms | 208.9ms | 199.2 MB | 7/7 | 3388889 |
| python | 47.2ms | 3.4× | 3/7 | 58.4ms | 11.2ms | 39.9 MB | 2/7 | 3388889 |
| node | 59.9ms | 4.3× | 4/7 | 78.9ms | 19.0ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 87.3ms | 6.2× | 5/7 | 130.5ms | 43.2ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 31.7ms | 2.3× | 2/7 | 54.5ms | 22.8ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 403.2ms | 12.0× | 6/7 | 430.1ms | 26.9ms | 94.8 MB | 6/7 | 374854840 |
| elixir | 171.0ms | 5.1× | 4/7 | 379.9ms | 208.9ms | 70.7 MB | 5/7 | 374854840 |
| python | 178.6ms | 5.3× | 5/7 | 189.8ms | 11.2ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.6ms | 1.0× | 1/7 | 52.6ms | 19.0ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 73.3ms | 2.2× | 3/7 | 116.5ms | 43.2ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 38.0ms | 1.1× | 2/7 | 60.8ms | 22.8ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 98.8ms | 10.1× | 4/7 | 125.7ms | 26.9ms | 40.5 MB | 4/7 | 1638200 |
| elixir | 9.8ms | 1.0× | 1/7 | 218.7ms | 208.9ms | 70.6 MB | 6/7 | 1638200 |
| python | 100.2ms | 10.2× | 5/7 | 111.4ms | 11.2ms | 10.1 MB | 1/7 | 1638200 |
| node | 24.0ms | 2.4× | 3/7 | 43.0ms | 19.0ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 102.3ms | 10.4× | 6/7 | 145.5ms | 43.2ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 14.3ms | 1.5× | 2/7 | 37.1ms | 22.8ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 174.2ms | 2.3× | 5/7 | 201.1ms | 26.9ms | 134.8 MB | 5/7 | 46468819 |
| elixir | 108.3ms | 1.4× | 3/7 | 317.2ms | 208.9ms | 156.9 MB | 7/7 | 46468819 |
| python | 195.9ms | 2.6× | 6/7 | 207.1ms | 11.2ms | 26.0 MB | 1/7 | 46468819 |
| node | 112.4ms | 1.5× | 4/7 | 131.4ms | 19.0ms | 65.5 MB | 4/7 | 46468819 |
| ruby | 76.0ms | 1.0× | 1/7 | 119.2ms | 43.2ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 81.6ms | 1.1× | 2/7 | 104.4ms | 22.8ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.3ms | 43.2× | 5/7 | 139.2ms | 26.9ms | 41.1 MB | 4/7 | 724 |
| elixir | 2.6ms | 1.0× | 1/7 | 211.5ms | 208.9ms | 69.7 MB | 6/7 | 724 |
| python | 57.3ms | 22.0× | 4/7 | 68.5ms | 11.2ms | 9.8 MB | 1/7 | 724 |
| node | 10.0ms | 3.8× | 2/7 | 29.0ms | 19.0ms | 51.2 MB | 5/7 | 724 |
| ruby | 129.5ms | 49.8× | 6/7 | 172.7ms | 43.2ms | 23.8 MB | 2/7 | 724 |
| dotnet | 21.0ms | 8.1× | 3/7 | 43.8ms | 22.8ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.8ms | 2.9× | 2/7 | 63.7ms | 26.9ms | 22.3 MB | 2/7 | 9900000 |
| elixir | 12.9ms | 1.0× | 1/7 | 221.8ms | 208.9ms | 69.9 MB | 6/7 | 9900000 |
| python | 50.0ms | 3.9× | 3/7 | 61.2ms | 11.2ms | 9.8 MB | 1/7 | 9900000 |
| node | 594.5ms | 46.1× | 6/7 | 613.5ms | 19.0ms | 50.8 MB | 5/7 | 9900000 |
| ruby | 114.7ms | 8.9× | 4/7 | 157.9ms | 43.2ms | 26.1 MB | 3/7 | 9900000 |
| dotnet | 301.3ms | 23.4× | 5/7 | 324.1ms | 22.8ms | 32.5 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.2ms | 36.3× | 2/7 | 74.1ms | 26.9ms | 25.5 MB | 2/7 | 2475000 |
| elixir | 1.3ms | 1.0× | 1/7 | 210.2ms | 208.9ms | 69.9 MB | 6/7 | 2475000 |
| python | 233.3ms | 179.5× | 5/7 | 244.5ms | 11.2ms | 9.9 MB | 1/7 | 2475000 |
| node | 221.2ms | 170.2× | 4/7 | 240.2ms | 19.0ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 119.9ms | 92.2× | 3/7 | 163.1ms | 43.2ms | 30.2 MB | 3/7 | 2475000 |
| dotnet | 721.0ms | 554.6× | 6/7 | 743.8ms | 22.8ms | 32.5 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.2ms | 11.1× | 6/7 | 59.1ms | 26.9ms | 25.6 MB | 3/7 | 155553889038886 |
| elixir | 2.9ms | 1.0× | 1/7 | 211.8ms | 208.9ms | 70.7 MB | 6/7 | 155553889038886 |
| python | 4.3ms | 1.5× | 2/7 | 15.5ms | 11.2ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.1ms | 3.5× | 5/7 | 29.1ms | 19.0ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 8.3ms | 2.9× | 4/7 | 51.5ms | 43.2ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 7.8ms | 2.7× | 3/7 | 30.6ms | 22.8ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 114.7ms | 114.7× | 5/7 | 141.6ms | 26.9ms | 83.3 MB | 5/7 | 6100000 |
| elixir | 4.0ms | 4.0× | 2/7 | 212.9ms | 208.9ms | 75.8 MB | 4/7 | 6100000 |
| python | 579.5ms | 579.5× | 6/7 | 590.7ms | 11.2ms | 28.1 MB | 1/7 | 6100000 |
| node | 56.1ms | 56.1× | 4/7 | 75.1ms | 19.0ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.625s | 1624.8× | 7/7 | 1.668s | 43.2ms | 137.5 MB | 7/7 | 6100000 |
| dotnet | 19.4ms | 19.4× | 3/7 | 42.2ms | 22.8ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 400.1ms | 400.1× | 5/7 | 427.0ms | 26.9ms | 30.9 MB | 4/7 | 31781100 |
| elixir | 70.1ms | 70.1× | 3/7 | 279.0ms | 208.9ms | 72.1 MB | 5/7 | 31781100 |
| python | 748.1ms | 748.1× | 7/7 | 759.3ms | 11.2ms | 22.2 MB | 1/7 | 31781100 |
| node | 126.6ms | 126.6× | 4/7 | 145.6ms | 19.0ms | 182.7 MB | 7/7 | 31781100 |
| ruby | 519.9ms | 519.9× | 6/7 | 563.1ms | 43.2ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 36.6ms | 36.6× | 2/7 | 59.4ms | 22.8ms | 28.0 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 146.4ms | 1.0× | 2/7 | 173.3ms | 26.9ms | 120.1 MB | 5/7 | 500 |
| elixir | 590.4ms | 4.1× | 7/7 | 799.3ms | 208.9ms | 479.8 MB | 7/7 | 500 |
| python | 206.4ms | 1.4× | 4/7 | 217.6ms | 11.2ms | 46.5 MB | 1/7 | 500 |
| node | 144.3ms | 1.0× | 1/7 | 163.3ms | 19.0ms | 64.9 MB | 4/7 | 500 |
| ruby | 240.1ms | 1.7× | 5/7 | 283.3ms | 43.2ms | 50.1 MB | 2/7 | 500 |
| dotnet | 179.0ms | 1.2× | 3/7 | 201.8ms | 22.8ms | 50.2 MB | 3/7 | 500 |
