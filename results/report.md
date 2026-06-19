# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 21:43.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.4ms | 2.4× | 4/7 | 26.4ms | — | 18.3 MB | 2/7 | 0 |
| elixir | 202.8ms | 18.6× | 6/7 | 202.8ms | — | 69.6 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.9ms | 1.7× | 2/7 | 18.9ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 43.1ms | 4.0× | 5/7 | 43.1ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.5ms | 2.1× | 3/7 | 22.5ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 282.0ms | 6.9× | 4/7 | 308.4ms | 26.4ms | 21.8 MB | 2/7 | 9227465 |
| elixir | 82.6ms | 2.0× | 3/7 | 285.4ms | 202.8ms | 69.7 MB | 6/7 | 9227465 |
| python | 780.3ms | 19.1× | 7/7 | 791.2ms | 10.9ms | 9.8 MB | 1/7 | 9227465 |
| node | 78.4ms | 1.9× | 2/7 | 97.3ms | 18.9ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 643.0ms | 15.7× | 6/7 | 686.1ms | 43.1ms | 23.5 MB | 3/7 | 9227465 |
| dotnet | 40.9ms | 1.0× | 1/7 | 63.4ms | 22.5ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.6ms | 2.8× | 3/7 | 64.0ms | 26.4ms | 21.7 MB | 2/7 | 449999985000000 |
| elixir | 68.0ms | 5.2× | 4/7 | 270.8ms | 202.8ms | 69.6 MB | 6/7 | 449999985000000 |
| python | 2.369s | 179.5× | 7/7 | 2.380s | 10.9ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 34.4ms | 2.6× | 2/7 | 53.3ms | 18.9ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 614.8ms | 46.6× | 6/7 | 657.9ms | 43.1ms | 23.5 MB | 3/7 | 449999985000000 |
| dotnet | 13.2ms | 1.0× | 1/7 | 35.7ms | 22.5ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 111.0ms | 8.2× | 3/7 | 137.4ms | 26.4ms | 18.3 MB | 2/7 | 12499997500000 |
| elixir | 32.4ms | 2.4× | 2/7 | 235.2ms | 202.8ms | 72.9 MB | 5/7 | 12499997500000 |
| python | 112.8ms | 8.4× | 4/7 | 123.7ms | 10.9ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 237.9ms | 17.6× | 5/7 | 256.8ms | 18.9ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 238.0ms | 17.6× | 6/7 | 281.1ms | 43.1ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 13.5ms | 1.0× | 1/7 | 36.0ms | 22.5ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.3ms | 4.4× | 4/7 | 65.7ms | 26.4ms | 21.7 MB | 2/7 | 13848 |
| elixir | 17.8ms | 2.0× | 3/7 | 220.6ms | 202.8ms | 69.7 MB | 6/7 | 13848 |
| python | 127.4ms | 14.2× | 6/7 | 138.3ms | 10.9ms | 9.9 MB | 1/7 | 13848 |
| node | 11.6ms | 1.3× | 2/7 | 30.5ms | 18.9ms | 49.1 MB | 5/7 | 13848 |
| ruby | 122.1ms | 13.6× | 5/7 | 165.2ms | 43.1ms | 23.5 MB | 3/7 | 13848 |
| dotnet | 9.0ms | 1.0× | 1/7 | 31.5ms | 22.5ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 319.5ms | 6.7× | 4/7 | 345.9ms | 26.4ms | 35.8 MB | 4/7 | 442 |
| elixir | 104.6ms | 2.2× | 2/7 | 307.4ms | 202.8ms | 69.7 MB | 6/7 | 442 |
| python | 2.522s | 53.1× | 7/7 | 2.533s | 10.9ms | 9.8 MB | 1/7 | 442 |
| node | 185.8ms | 3.9× | 3/7 | 204.7ms | 18.9ms | 48.9 MB | 5/7 | 442 |
| ruby | 910.3ms | 19.2× | 6/7 | 953.4ms | 43.1ms | 23.5 MB | 2/7 | 442 |
| dotnet | 47.5ms | 1.0× | 1/7 | 70.0ms | 22.5ms | 26.4 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 226.0ms | 11.7× | 3/7 | 252.4ms | 26.4ms | 21.8 MB | 2/7 | 6129302 |
| elixir | 265.8ms | 13.8× | 4/7 | 468.6ms | 202.8ms | 69.8 MB | 6/7 | 6129302 |
| python | 1.416s | 73.4× | 7/7 | 1.427s | 10.9ms | 10.0 MB | 1/7 | 6129302 |
| node | 22.3ms | 1.2× | 2/7 | 41.2ms | 18.9ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 441.5ms | 22.9× | 5/7 | 484.6ms | 43.1ms | 23.6 MB | 3/7 | 6129302 |
| dotnet | 19.3ms | 1.0× | 1/7 | 41.8ms | 22.5ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.4ms | 16.3× | 4/7 | 122.8ms | 26.4ms | 34.3 MB | 4/7 | 654353666 |
| elixir | 65.5ms | 11.1× | 3/7 | 268.3ms | 202.8ms | 75.3 MB | 6/7 | 654353666 |
| python | 450.4ms | 76.3× | 6/7 | 461.3ms | 10.9ms | 10.3 MB | 1/7 | 654353666 |
| node | 25.5ms | 4.3× | 2/7 | 44.4ms | 18.9ms | 52.7 MB | 5/7 | 654353666 |
| ruby | 302.7ms | 51.3× | 5/7 | 345.8ms | 43.1ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 5.9ms | 1.0× | 1/7 | 28.4ms | 22.5ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.3ms | 1.0× | 1/7 | 38.7ms | 26.4ms | 28.4 MB | 1/7 | 3388889 |
| elixir | 125.4ms | 10.2× | 6/7 | 328.2ms | 202.8ms | 203.3 MB | 7/7 | 3388889 |
| python | 45.2ms | 3.7× | 3/7 | 56.1ms | 10.9ms | 39.9 MB | 2/7 | 3388889 |
| node | 61.8ms | 5.0× | 4/7 | 80.7ms | 18.9ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 88.8ms | 7.2× | 5/7 | 131.9ms | 43.1ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 32.3ms | 2.6× | 2/7 | 54.8ms | 22.5ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 423.4ms | 12.3× | 6/7 | 449.8ms | 26.4ms | 90.9 MB | 6/7 | 374854840 |
| elixir | 172.9ms | 5.0× | 4/7 | 375.7ms | 202.8ms | 70.6 MB | 5/7 | 374854840 |
| python | 183.0ms | 5.3× | 5/7 | 193.9ms | 10.9ms | 9.9 MB | 1/7 | 374854840 |
| node | 34.4ms | 1.0× | 1/7 | 53.3ms | 18.9ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 77.1ms | 2.2× | 3/7 | 120.2ms | 43.1ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 38.2ms | 1.1× | 2/7 | 60.7ms | 22.5ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.1ms | 17.5× | 6/7 | 131.5ms | 26.4ms | 36.9 MB | 4/7 | 1638200 |
| elixir | 6.0ms | 1.0× | 1/7 | 208.8ms | 202.8ms | 70.1 MB | 6/7 | 1638200 |
| python | 98.8ms | 16.5× | 4/7 | 109.7ms | 10.9ms | 10.0 MB | 1/7 | 1638200 |
| node | 22.7ms | 3.8× | 3/7 | 41.6ms | 18.9ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 100.5ms | 16.8× | 5/7 | 143.6ms | 43.1ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 15.3ms | 2.5× | 2/7 | 37.8ms | 22.5ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.5ms | 2.5× | 5/7 | 197.9ms | 26.4ms | 129.9 MB | 5/7 | 46468819 |
| elixir | 117.3ms | 1.7× | 4/7 | 320.1ms | 202.8ms | 157.2 MB | 7/7 | 46468819 |
| python | 192.6ms | 2.8× | 6/7 | 203.5ms | 10.9ms | 26.0 MB | 1/7 | 46468819 |
| node | 113.4ms | 1.7× | 3/7 | 132.3ms | 18.9ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 75.9ms | 1.1× | 2/7 | 119.0ms | 43.1ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 68.7ms | 1.0× | 1/7 | 91.2ms | 22.5ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 137.0ms | 13.4× | 6/7 | 163.4ms | 26.4ms | 32.1 MB | 4/7 | 724 |
| elixir | 10.2ms | 1.0× | 1/7 | 213.0ms | 202.8ms | 72.1 MB | 6/7 | 724 |
| python | 57.0ms | 5.6× | 4/7 | 67.9ms | 10.9ms | 9.8 MB | 1/7 | 724 |
| node | 11.1ms | 1.1× | 2/7 | 30.0ms | 18.9ms | 51.2 MB | 5/7 | 724 |
| ruby | 132.8ms | 13.0× | 5/7 | 175.9ms | 43.1ms | 23.8 MB | 2/7 | 724 |
| dotnet | 21.0ms | 2.1× | 3/7 | 43.5ms | 22.5ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 190.9ms | 8.2× | 4/7 | 217.3ms | 26.4ms | 33.8 MB | 4/7 | 9900000 |
| elixir | 23.4ms | 1.0× | 1/7 | 226.2ms | 202.8ms | 69.8 MB | 6/7 | 9900000 |
| python | 50.8ms | 2.2× | 2/7 | 61.7ms | 10.9ms | 9.8 MB | 1/7 | 9900000 |
| node | 603.3ms | 25.8× | 6/7 | 622.2ms | 18.9ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 114.7ms | 4.9× | 3/7 | 157.8ms | 43.1ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 304.4ms | 13.0× | 5/7 | 326.9ms | 22.5ms | 32.4 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 272.4ms | 55.6× | 5/7 | 298.8ms | 26.4ms | 34.1 MB | 4/7 | 2475000 |
| elixir | 4.9ms | 1.0× | 1/7 | 207.7ms | 202.8ms | 69.8 MB | 6/7 | 2475000 |
| python | 230.5ms | 47.0× | 4/7 | 241.4ms | 10.9ms | 9.9 MB | 1/7 | 2475000 |
| node | 228.3ms | 46.6× | 3/7 | 247.2ms | 18.9ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 125.4ms | 25.6× | 2/7 | 168.5ms | 43.1ms | 30.1 MB | 2/7 | 2475000 |
| dotnet | 730.5ms | 149.1× | 6/7 | 753.0ms | 22.5ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.8ms | 8.3× | 6/7 | 66.2ms | 26.4ms | 21.6 MB | 2/7 | 155553889038886 |
| elixir | 9.2ms | 1.9× | 4/7 | 212.0ms | 202.8ms | 70.4 MB | 6/7 | 155553889038886 |
| python | 4.8ms | 1.0× | 1/7 | 15.7ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.6ms | 2.2× | 5/7 | 29.5ms | 18.9ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 9.1ms | 1.9× | 3/7 | 52.2ms | 43.1ms | 24.0 MB | 3/7 | 155553889038886 |
| dotnet | 8.1ms | 1.7× | 2/7 | 30.6ms | 22.5ms | 28.0 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 127.9ms | 127.9× | 5/7 | 154.3ms | 26.4ms | 104.5 MB | 5/7 | 6100000 |
| elixir | 7.0ms | 7.0× | 2/7 | 209.8ms | 202.8ms | 75.8 MB | 4/7 | 6100000 |
| python | 578.2ms | 578.2× | 6/7 | 589.1ms | 10.9ms | 28.1 MB | 1/7 | 6100000 |
| node | 56.4ms | 56.4× | 4/7 | 75.3ms | 18.9ms | 52.0 MB | 3/7 | 6100000 |
| ruby | 1.618s | 1617.7× | 7/7 | 1.661s | 43.1ms | 137.1 MB | 7/7 | 6100000 |
| dotnet | 18.6ms | 18.6× | 3/7 | 41.1ms | 22.5ms | 31.1 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 402.3ms | 402.3× | 5/7 | 428.7ms | 26.4ms | 26.6 MB | 3/7 | 31781100 |
| elixir | 64.4ms | 64.4× | 3/7 | 267.2ms | 202.8ms | 71.7 MB | 5/7 | 31781100 |
| python | 748.8ms | 748.8× | 7/7 | 759.7ms | 10.9ms | 22.2 MB | 1/7 | 31781100 |
| node | 125.8ms | 125.8× | 4/7 | 144.7ms | 18.9ms | 182.9 MB | 7/7 | 31781100 |
| ruby | 510.8ms | 510.8× | 6/7 | 553.9ms | 43.1ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 37.4ms | 37.4× | 2/7 | 59.9ms | 22.5ms | 28.0 MB | 4/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.2ms | 1.1× | 2/7 | 174.6ms | 26.4ms | 117.8 MB | 5/7 | 500 |
| elixir | 574.0ms | 4.4× | 7/7 | 776.8ms | 202.8ms | 493.5 MB | 7/7 | 500 |
| python | 183.2ms | 1.4× | 4/7 | 194.1ms | 10.9ms | 45.3 MB | 1/7 | 500 |
| node | 129.4ms | 1.0× | 1/7 | 148.3ms | 18.9ms | 65.0 MB | 4/7 | 500 |
| ruby | 216.3ms | 1.7× | 5/7 | 259.4ms | 43.1ms | 50.1 MB | 3/7 | 500 |
| dotnet | 165.7ms | 1.3× | 3/7 | 188.2ms | 22.5ms | 48.2 MB | 2/7 | 500 |
