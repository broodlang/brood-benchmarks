# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-16 10:40.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.8ms | 3.4× | 4/6 | 39.8ms | — | 24.0 MB | 3/6 | 0 |
| elixir | 295.1ms | 25.2× | 6/6 | 295.1ms | — | 79.9 MB | 6/6 | 0 |
| python | 11.7ms | 1.0× | 1/6 | 11.7ms | — | 9.8 MB | 1/6 | 0 |
| node | 19.6ms | 1.7× | 2/6 | 19.6ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 47.2ms | 4.0× | 5/6 | 47.2ms | — | 23.5 MB | 2/6 | 0 |
| dotnet | 25.2ms | 2.2× | 3/6 | 25.2ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 557.6ms | 12.6× | 4/6 | 597.4ms | 39.8ms | 27.5 MB | 4/6 | 9227465 |
| elixir | 126.6ms | 2.9× | 3/6 | 421.7ms | 295.1ms | 80.7 MB | 6/6 | 9227465 |
| python | 818.7ms | 18.5× | 6/6 | 830.4ms | 11.7ms | 9.8 MB | 1/6 | 9227465 |
| node | 81.4ms | 1.8× | 2/6 | 101.0ms | 19.6ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 668.9ms | 15.1× | 5/6 | 716.1ms | 47.2ms | 23.5 MB | 2/6 | 9227465 |
| dotnet | 44.3ms | 1.0× | 1/6 | 69.5ms | 25.2ms | 25.9 MB | 3/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.1ms | 9.7× | 4/6 | 151.9ms | 39.8ms | 27.4 MB | 4/6 | 449999985000000 |
| elixir | 106.3ms | 9.2× | 3/6 | 401.4ms | 295.1ms | 80.9 MB | 6/6 | 449999985000000 |
| python | 2.610s | 225.0× | 6/6 | 2.622s | 11.7ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 34.3ms | 3.0× | 2/6 | 53.9ms | 19.6ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 612.2ms | 52.8× | 5/6 | 659.4ms | 47.2ms | 23.5 MB | 2/6 | 449999985000000 |
| dotnet | 11.6ms | 1.0× | 1/6 | 36.8ms | 25.2ms | 26.3 MB | 3/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.9ms | 9.2× | 3/6 | 150.7ms | 39.8ms | 24.1 MB | 3/6 | 12499997500000 |
| elixir | 36.9ms | 3.1× | 2/6 | 332.0ms | 295.1ms | 77.1 MB | 5/6 | 12499997500000 |
| python | 118.0ms | 9.8× | 4/6 | 129.7ms | 11.7ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 247.9ms | 20.7× | 6/6 | 267.5ms | 19.6ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 244.4ms | 20.4× | 5/6 | 291.6ms | 47.2ms | 23.5 MB | 2/6 | 12499997500000 |
| dotnet | 12.0ms | 1.0× | 1/6 | 37.2ms | 25.2ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 5.5× | 3/6 | 82.9ms | 39.8ms | 27.7 MB | 4/6 | 13848 |
| elixir | 62.8ms | 8.1× | 4/6 | 357.9ms | 295.1ms | 81.0 MB | 6/6 | 13848 |
| python | 137.1ms | 17.6× | 6/6 | 148.8ms | 11.7ms | 9.9 MB | 1/6 | 13848 |
| node | 10.6ms | 1.4× | 2/6 | 30.2ms | 19.6ms | 49.2 MB | 5/6 | 13848 |
| ruby | 129.0ms | 16.5× | 5/6 | 176.2ms | 47.2ms | 23.5 MB | 2/6 | 13848 |
| dotnet | 7.8ms | 1.0× | 1/6 | 33.0ms | 25.2ms | 26.4 MB | 3/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 535.7ms | 11.2× | 4/6 | 575.5ms | 39.8ms | 41.4 MB | 4/6 | 442 |
| elixir | 167.1ms | 3.5× | 2/6 | 462.2ms | 295.1ms | 80.9 MB | 6/6 | 442 |
| python | 2.803s | 58.8× | 6/6 | 2.815s | 11.7ms | 9.7 MB | 1/6 | 442 |
| node | 188.7ms | 4.0× | 3/6 | 208.3ms | 19.6ms | 49.1 MB | 5/6 | 442 |
| ruby | 928.8ms | 19.5× | 5/6 | 976.0ms | 47.2ms | 23.5 MB | 2/6 | 442 |
| dotnet | 47.7ms | 1.0× | 1/6 | 72.9ms | 25.2ms | 26.3 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 239.3ms | 12.3× | 3/6 | 279.1ms | 39.8ms | 27.7 MB | 4/6 | 6129302 |
| elixir | 301.2ms | 15.4× | 4/6 | 596.3ms | 295.1ms | 81.5 MB | 6/6 | 6129302 |
| python | 1.542s | 79.1× | 6/6 | 1.553s | 11.7ms | 10.0 MB | 1/6 | 6129302 |
| node | 22.9ms | 1.2× | 2/6 | 42.5ms | 19.6ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 458.3ms | 23.5× | 5/6 | 505.5ms | 47.2ms | 23.6 MB | 2/6 | 6129302 |
| dotnet | 19.5ms | 1.0× | 1/6 | 44.7ms | 25.2ms | 26.3 MB | 3/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 175.9ms | 55.0× | 4/6 | 215.7ms | 39.8ms | 40.0 MB | 4/6 | 654353666 |
| elixir | 83.1ms | 26.0× | 3/6 | 378.2ms | 295.1ms | 83.1 MB | 6/6 | 654353666 |
| python | 502.1ms | 156.9× | 6/6 | 513.8ms | 11.7ms | 10.4 MB | 1/6 | 654353666 |
| node | 24.3ms | 7.6× | 2/6 | 43.9ms | 19.6ms | 52.9 MB | 5/6 | 654353666 |
| ruby | 324.2ms | 101.3× | 5/6 | 371.4ms | 47.2ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 3.2ms | 1.0× | 1/6 | 28.4ms | 25.2ms | 26.8 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.0ms | 1.0× | 1/6 | 51.8ms | 39.8ms | 34.3 MB | 1/6 | 3388889 |
| elixir | 130.2ms | 10.8× | 6/6 | 425.3ms | 295.1ms | 198.5 MB | 6/6 | 3388889 |
| python | 46.4ms | 3.9× | 3/6 | 58.1ms | 11.7ms | 39.8 MB | 2/6 | 3388889 |
| node | 64.9ms | 5.4× | 4/6 | 84.5ms | 19.6ms | 96.1 MB | 5/6 | 3388889 |
| ruby | 96.0ms | 8.0× | 5/6 | 143.2ms | 47.2ms | 52.1 MB | 3/6 | 3388889 |
| dotnet | 33.3ms | 2.8× | 2/6 | 58.5ms | 25.2ms | 56.8 MB | 4/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 954.0ms | 27.4× | 6/6 | 993.8ms | 39.8ms | 93.5 MB | 6/6 | 374854840 |
| elixir | 190.9ms | 5.5× | 5/6 | 486.0ms | 295.1ms | 79.0 MB | 5/6 | 374854840 |
| python | 190.3ms | 5.5× | 4/6 | 202.0ms | 11.7ms | 9.9 MB | 1/6 | 374854840 |
| node | 34.8ms | 1.0× | 1/6 | 54.4ms | 19.6ms | 50.8 MB | 4/6 | 374854840 |
| ruby | 77.1ms | 2.2× | 3/6 | 124.3ms | 47.2ms | 23.6 MB | 2/6 | 374854840 |
| dotnet | 39.1ms | 1.1× | 2/6 | 64.3ms | 25.2ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 450.9ms | 31.8× | 6/6 | 490.7ms | 39.8ms | 38.8 MB | 4/6 | 1638200 |
| elixir | 56.3ms | 4.0× | 3/6 | 351.4ms | 295.1ms | 81.3 MB | 6/6 | 1638200 |
| python | 105.0ms | 7.4× | 5/6 | 116.7ms | 11.7ms | 10.0 MB | 1/6 | 1638200 |
| node | 25.8ms | 1.8× | 2/6 | 45.4ms | 19.6ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 104.1ms | 7.3× | 4/6 | 151.3ms | 47.2ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 14.2ms | 1.0× | 1/6 | 39.4ms | 25.2ms | 32.4 MB | 3/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 320.5ms | 4.6× | 6/6 | 360.3ms | 39.8ms | 123.4 MB | 5/6 | 46468819 |
| elixir | 129.3ms | 1.8× | 4/6 | 424.4ms | 295.1ms | 167.9 MB | 6/6 | 46468819 |
| python | 233.1ms | 3.3× | 5/6 | 244.8ms | 11.7ms | 26.0 MB | 1/6 | 46468819 |
| node | 117.2ms | 1.7× | 3/6 | 136.8ms | 19.6ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 76.2ms | 1.1× | 2/6 | 123.4ms | 47.2ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 70.3ms | 1.0× | 1/6 | 95.5ms | 25.2ms | 29.7 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 610.1ms | 54.0× | 6/6 | 649.9ms | 39.8ms | 35.6 MB | 4/6 | 724 |
| elixir | 51.8ms | 4.6× | 3/6 | 346.9ms | 295.1ms | 81.2 MB | 6/6 | 724 |
| python | 58.9ms | 5.2× | 4/6 | 70.6ms | 11.7ms | 9.7 MB | 1/6 | 724 |
| node | 11.3ms | 1.0× | 1/6 | 30.9ms | 19.6ms | 51.3 MB | 5/6 | 724 |
| ruby | 136.6ms | 12.1× | 5/6 | 183.8ms | 47.2ms | 23.8 MB | 2/6 | 724 |
| dotnet | 20.0ms | 1.8× | 2/6 | 45.2ms | 25.2ms | 29.4 MB | 3/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 210.3ms | 4.1× | 4/6 | 250.1ms | 39.8ms | 41.6 MB | 4/6 | 9900000 |
| elixir | 87.5ms | 1.7× | 2/6 | 382.6ms | 295.1ms | 81.6 MB | 6/6 | 9900000 |
| python | 50.9ms | 1.0× | 1/6 | 62.6ms | 11.7ms | 9.8 MB | 1/6 | 9900000 |
| node | 636.0ms | 12.5× | 6/6 | 655.6ms | 19.6ms | 50.9 MB | 5/6 | 9900000 |
| ruby | 123.1ms | 2.4× | 3/6 | 170.3ms | 47.2ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 317.9ms | 6.2× | 5/6 | 343.1ms | 25.2ms | 32.5 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 277.0ms | 3.5× | 5/6 | 316.8ms | 39.8ms | 42.8 MB | 4/6 | 2475000 |
| elixir | 79.0ms | 1.0× | 1/6 | 374.1ms | 295.1ms | 82.8 MB | 6/6 | 2475000 |
| python | 237.7ms | 3.0× | 4/6 | 249.4ms | 11.7ms | 9.9 MB | 1/6 | 2475000 |
| node | 234.4ms | 3.0× | 3/6 | 254.0ms | 19.6ms | 50.8 MB | 5/6 | 2475000 |
| ruby | 127.2ms | 1.6× | 2/6 | 174.4ms | 47.2ms | 30.1 MB | 2/6 | 2475000 |
| dotnet | 770.4ms | 9.8× | 6/6 | 795.6ms | 25.2ms | 32.6 MB | 3/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.4ms | 9.6× | 6/6 | 82.2ms | 39.8ms | 27.7 MB | 3/6 | 155553889038886 |
| elixir | 14.3ms | 3.2× | 5/6 | 309.4ms | 295.1ms | 77.9 MB | 6/6 | 155553889038886 |
| python | 4.4ms | 1.0× | 1/6 | 16.1ms | 11.7ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 11.6ms | 2.6× | 4/6 | 31.2ms | 19.6ms | 52.6 MB | 5/6 | 155553889038886 |
| ruby | 7.7ms | 1.7× | 3/6 | 54.9ms | 47.2ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 6.6ms | 1.5× | 2/6 | 31.8ms | 25.2ms | 28.1 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 121.9ms | 6.9× | 4/6 | 161.7ms | 39.8ms | 72.3 MB | 4/6 | 6100000 |
| elixir | 48.0ms | 2.7× | 2/6 | 343.1ms | 295.1ms | 87.3 MB | 5/6 | 6100000 |
| python | 600.9ms | 34.1× | 5/6 | 612.6ms | 11.7ms | 28.1 MB | 1/6 | 6100000 |
| node | 56.9ms | 3.2× | 3/6 | 76.5ms | 19.6ms | 52.0 MB | 3/6 | 6100000 |
| ruby | 1.732s | 98.4× | 6/6 | 1.779s | 47.2ms | 136.6 MB | 6/6 | 6100000 |
| dotnet | 17.6ms | 1.0× | 1/6 | 42.8ms | 25.2ms | 30.8 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 399.3ms | 11.2× | 4/6 | 439.1ms | 39.8ms | 30.0 MB | 4/6 | 31781100 |
| elixir | 116.9ms | 3.3× | 2/6 | 412.0ms | 295.1ms | 82.7 MB | 5/6 | 31781100 |
| python | 774.6ms | 21.7× | 6/6 | 786.3ms | 11.7ms | 22.3 MB | 1/6 | 31781100 |
| node | 131.3ms | 3.7× | 3/6 | 150.9ms | 19.6ms | 183.5 MB | 6/6 | 31781100 |
| ruby | 483.5ms | 13.5× | 5/6 | 530.7ms | 47.2ms | 23.7 MB | 2/6 | 31781100 |
| dotnet | 35.7ms | 1.0× | 1/6 | 60.9ms | 25.2ms | 28.1 MB | 3/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.2ms | 1.2× | 2/6 | 195.0ms | 39.8ms | 122.5 MB | 5/6 | 500 |
| elixir | 758.1ms | 5.7× | 6/6 | 1.053s | 295.1ms | 517.3 MB | 6/6 | 500 |
| python | 192.9ms | 1.5× | 4/6 | 204.6ms | 11.7ms | 45.6 MB | 1/6 | 500 |
| node | 133.0ms | 1.0× | 1/6 | 152.6ms | 19.6ms | 65.3 MB | 4/6 | 500 |
| ruby | 225.6ms | 1.7× | 5/6 | 272.8ms | 47.2ms | 49.6 MB | 3/6 | 500 |
| dotnet | 162.0ms | 1.2× | 3/6 | 187.2ms | 25.2ms | 48.3 MB | 2/6 | 500 |
