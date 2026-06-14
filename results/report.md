# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-15 00:28.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.2ms | 2.8× | 4/6 | 29.2ms | — | 14.9 MB | 2/6 | 0 |
| elixir | 262.7ms | 25.0× | 6/6 | 262.7ms | — | 76.5 MB | 6/6 | 0 |
| python | 10.5ms | 1.0× | 1/6 | 10.5ms | — | 9.7 MB | 1/6 | 0 |
| node | 17.6ms | 1.7× | 2/6 | 17.6ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 41.7ms | 4.0× | 5/6 | 41.7ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 22.0ms | 2.1× | 3/6 | 22.0ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 661.3ms | 16.1× | 5/6 | 690.5ms | 29.2ms | 16.1 MB | 2/6 | 9227465 |
| elixir | 117.2ms | 2.9× | 3/6 | 379.9ms | 262.7ms | 81.6 MB | 6/6 | 9227465 |
| python | 760.1ms | 18.5× | 6/6 | 770.6ms | 10.5ms | 9.7 MB | 1/6 | 9227465 |
| node | 77.0ms | 1.9× | 2/6 | 94.6ms | 17.6ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 626.7ms | 15.3× | 4/6 | 668.4ms | 41.7ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 41.0ms | 1.0× | 1/6 | 63.0ms | 22.0ms | 26.0 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.3ms | 14.6× | 4/6 | 202.5ms | 29.2ms | 16.1 MB | 2/6 | 449999985000000 |
| elixir | 103.4ms | 8.7× | 3/6 | 366.1ms | 262.7ms | 80.7 MB | 6/6 | 449999985000000 |
| python | 2.357s | 198.1× | 6/6 | 2.368s | 10.5ms | 9.7 MB | 1/6 | 449999985000000 |
| node | 32.3ms | 2.7× | 2/6 | 49.9ms | 17.6ms | 50.4 MB | 5/6 | 449999985000000 |
| ruby | 601.3ms | 50.5× | 5/6 | 643.0ms | 41.7ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 11.9ms | 1.0× | 1/6 | 33.9ms | 22.0ms | 26.4 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 104.6ms | 8.4× | 3/6 | 133.8ms | 29.2ms | 14.9 MB | 2/6 | 12499997500000 |
| elixir | 44.7ms | 3.6× | 2/6 | 307.4ms | 262.7ms | 77.5 MB | 5/6 | 12499997500000 |
| python | 109.9ms | 8.9× | 4/6 | 120.4ms | 10.5ms | 10.6 MB | 1/6 | 12499997500000 |
| node | 239.7ms | 19.3× | 6/6 | 257.3ms | 17.6ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 238.3ms | 19.2× | 5/6 | 280.0ms | 41.7ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 12.4ms | 1.0× | 1/6 | 34.4ms | 22.0ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.9ms | 4.4× | 3/6 | 74.1ms | 29.2ms | 16.3 MB | 2/6 | 13848 |
| elixir | 57.9ms | 5.6× | 4/6 | 320.6ms | 262.7ms | 81.0 MB | 6/6 | 13848 |
| python | 123.9ms | 12.0× | 6/6 | 134.4ms | 10.5ms | 9.9 MB | 1/6 | 13848 |
| node | 11.2ms | 1.1× | 2/6 | 28.8ms | 17.6ms | 49.2 MB | 5/6 | 13848 |
| ruby | 118.9ms | 11.5× | 5/6 | 160.6ms | 41.7ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 10.3ms | 1.0× | 1/6 | 32.3ms | 22.0ms | 26.4 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 476.2ms | 10.4× | 4/6 | 505.4ms | 29.2ms | 30.6 MB | 4/6 | 442 |
| elixir | 153.8ms | 3.4× | 2/6 | 416.5ms | 262.7ms | 80.8 MB | 6/6 | 442 |
| python | 2.656s | 57.9× | 6/6 | 2.667s | 10.5ms | 9.7 MB | 1/6 | 442 |
| node | 178.8ms | 3.9× | 3/6 | 196.4ms | 17.6ms | 49.1 MB | 5/6 | 442 |
| ruby | 885.9ms | 19.3× | 5/6 | 927.6ms | 41.7ms | 23.5 MB | 2/6 | 442 |
| dotnet | 45.9ms | 1.0× | 1/6 | 67.9ms | 22.0ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 239.4ms | 12.8× | 3/6 | 268.6ms | 29.2ms | 16.5 MB | 2/6 | 6129302 |
| elixir | 295.5ms | 15.8× | 4/6 | 558.2ms | 262.7ms | 81.5 MB | 6/6 | 6129302 |
| python | 1.336s | 71.4× | 6/6 | 1.347s | 10.5ms | 10.0 MB | 1/6 | 6129302 |
| node | 21.9ms | 1.2× | 2/6 | 39.5ms | 17.6ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 439.4ms | 23.5× | 5/6 | 481.1ms | 41.7ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 18.7ms | 1.0× | 1/6 | 40.7ms | 22.0ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 212.4ms | 45.2× | 4/6 | 241.6ms | 29.2ms | 23.4 MB | 2/6 | 654353666 |
| elixir | 84.8ms | 18.0× | 3/6 | 347.5ms | 262.7ms | 82.5 MB | 6/6 | 654353666 |
| python | 492.6ms | 104.8× | 6/6 | 503.1ms | 10.5ms | 10.4 MB | 1/6 | 654353666 |
| node | 21.1ms | 4.5× | 2/6 | 38.7ms | 17.6ms | 52.9 MB | 5/6 | 654353666 |
| ruby | 296.9ms | 63.2× | 5/6 | 338.6ms | 41.7ms | 23.8 MB | 3/6 | 654353666 |
| dotnet | 4.7ms | 1.0× | 1/6 | 26.7ms | 22.0ms | 26.9 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 831.9ms | 25.8× | 6/6 | 861.1ms | 29.2ms | 177.6 MB | 5/6 | 3388889 |
| elixir | 134.1ms | 4.2× | 5/6 | 396.8ms | 262.7ms | 198.6 MB | 6/6 | 3388889 |
| python | 43.8ms | 1.4× | 2/6 | 54.3ms | 10.5ms | 39.8 MB | 1/6 | 3388889 |
| node | 59.2ms | 1.8× | 3/6 | 76.8ms | 17.6ms | 96.1 MB | 4/6 | 3388889 |
| ruby | 87.1ms | 2.7× | 4/6 | 128.8ms | 41.7ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 32.2ms | 1.0× | 1/6 | 54.2ms | 22.0ms | 56.8 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 992.9ms | 29.8× | 6/6 | 1.022s | 29.2ms | 57.5 MB | 5/6 | 374854840 |
| elixir | 177.9ms | 5.3× | 5/6 | 440.6ms | 262.7ms | 79.2 MB | 6/6 | 374854840 |
| python | 174.4ms | 5.2× | 4/6 | 184.9ms | 10.5ms | 9.9 MB | 1/6 | 374854840 |
| node | 33.3ms | 1.0× | 1/6 | 50.9ms | 17.6ms | 50.8 MB | 4/6 | 374854840 |
| ruby | 73.3ms | 2.2× | 3/6 | 115.0ms | 41.7ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 37.0ms | 1.1× | 2/6 | 59.0ms | 22.0ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 447.0ms | 26.1× | 6/6 | 476.2ms | 29.2ms | 26.4 MB | 3/6 | 1638200 |
| elixir | 50.3ms | 2.9× | 3/6 | 313.0ms | 262.7ms | 81.2 MB | 6/6 | 1638200 |
| python | 110.5ms | 6.5× | 5/6 | 121.0ms | 10.5ms | 10.0 MB | 1/6 | 1638200 |
| node | 23.3ms | 1.4× | 2/6 | 40.9ms | 17.6ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 98.4ms | 5.8× | 4/6 | 140.1ms | 41.7ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 17.1ms | 1.0× | 1/6 | 39.1ms | 22.0ms | 32.5 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 287.9ms | 4.2× | 6/6 | 317.1ms | 29.2ms | 87.1 MB | 5/6 | 46468819 |
| elixir | 124.2ms | 1.8× | 4/6 | 386.9ms | 262.7ms | 165.1 MB | 6/6 | 46468819 |
| python | 195.9ms | 2.9× | 5/6 | 206.4ms | 10.5ms | 25.9 MB | 1/6 | 46468819 |
| node | 113.0ms | 1.6× | 3/6 | 130.6ms | 17.6ms | 65.7 MB | 4/6 | 46468819 |
| ruby | 73.7ms | 1.1× | 2/6 | 115.4ms | 41.7ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 68.7ms | 1.0× | 1/6 | 90.7ms | 22.0ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 514.4ms | 32.8× | 6/6 | 543.6ms | 29.2ms | 24.5 MB | 3/6 | 724 |
| elixir | 54.9ms | 3.5× | 3/6 | 317.6ms | 262.7ms | 81.5 MB | 6/6 | 724 |
| python | 56.5ms | 3.6× | 4/6 | 67.0ms | 10.5ms | 9.7 MB | 1/6 | 724 |
| node | 15.7ms | 1.0× | 1/6 | 33.3ms | 17.6ms | 51.3 MB | 5/6 | 724 |
| ruby | 131.4ms | 8.4× | 5/6 | 173.1ms | 41.7ms | 23.8 MB | 2/6 | 724 |
| dotnet | 34.1ms | 2.2× | 2/6 | 56.1ms | 22.0ms | 29.3 MB | 4/6 | 724 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 133.2ms | 30.3× | 6/6 | 162.4ms | 29.2ms | 34.1 MB | 4/6 | 155553889038886 |
| elixir | 14.3ms | 3.3× | 5/6 | 277.0ms | 262.7ms | 78.3 MB | 6/6 | 155553889038886 |
| python | 4.4ms | 1.0× | 1/6 | 14.9ms | 10.5ms | 9.8 MB | 1/6 | 155553889038886 |
| node | 10.2ms | 2.3× | 4/6 | 27.8ms | 17.6ms | 52.7 MB | 5/6 | 155553889038886 |
| ruby | 7.5ms | 1.7× | 3/6 | 49.2ms | 41.7ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 7.1ms | 1.6× | 2/6 | 29.1ms | 22.0ms | 28.1 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 561.0ms | 30.7× | 5/6 | 590.2ms | 29.2ms | 119.4 MB | 5/6 | 6100000 |
| elixir | 58.9ms | 3.2× | 3/6 | 321.6ms | 262.7ms | 88.1 MB | 4/6 | 6100000 |
| python | 549.6ms | 30.0× | 4/6 | 560.1ms | 10.5ms | 27.9 MB | 1/6 | 6100000 |
| node | 54.0ms | 3.0× | 2/6 | 71.6ms | 17.6ms | 51.9 MB | 3/6 | 6100000 |
| ruby | 1.620s | 88.5× | 6/6 | 1.661s | 41.7ms | 137.4 MB | 6/6 | 6100000 |
| dotnet | 18.3ms | 1.0× | 1/6 | 40.3ms | 22.0ms | 30.6 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 408.0ms | 11.2× | 4/6 | 437.2ms | 29.2ms | 18.0 MB | 1/6 | 31781100 |
| elixir | 128.6ms | 3.5× | 3/6 | 391.3ms | 262.7ms | 81.9 MB | 5/6 | 31781100 |
| python | 696.6ms | 19.1× | 6/6 | 707.1ms | 10.5ms | 22.2 MB | 2/6 | 31781100 |
| node | 112.5ms | 3.1× | 2/6 | 130.1ms | 17.6ms | 183.1 MB | 6/6 | 31781100 |
| ruby | 467.1ms | 12.8× | 5/6 | 508.8ms | 41.7ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 36.4ms | 1.0× | 1/6 | 58.4ms | 22.0ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.8ms | 1.2× | 2/6 | 178.0ms | 29.2ms | 102.9 MB | 5/6 | 500 |
| elixir | 677.8ms | 5.4× | 6/6 | 940.5ms | 262.7ms | 566.0 MB | 6/6 | 500 |
| python | 184.0ms | 1.5× | 4/6 | 194.5ms | 10.5ms | 47.1 MB | 1/6 | 500 |
| node | 124.9ms | 1.0× | 1/6 | 142.5ms | 17.6ms | 65.3 MB | 4/6 | 500 |
| ruby | 210.3ms | 1.7× | 5/6 | 252.0ms | 41.7ms | 49.9 MB | 2/6 | 500 |
| dotnet | 160.2ms | 1.3× | 3/6 | 182.2ms | 22.0ms | 50.3 MB | 3/6 | 500 |
