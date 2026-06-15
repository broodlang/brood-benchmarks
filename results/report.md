# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-15 20:37.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.8ms | 3.1× | 4/6 | 35.8ms | — | 12.4 MB | 2/6 | 0 |
| elixir | 293.3ms | 25.3× | 6/6 | 293.3ms | — | 76.3 MB | 6/6 | 0 |
| python | 11.6ms | 1.0× | 1/6 | 11.6ms | — | 9.7 MB | 1/6 | 0 |
| node | 19.6ms | 1.7× | 2/6 | 19.6ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 47.9ms | 4.1× | 5/6 | 47.9ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 24.1ms | 2.1× | 3/6 | 24.1ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 691.5ms | 15.5× | 5/6 | 727.3ms | 35.8ms | 13.6 MB | 2/6 | 9227465 |
| elixir | 136.8ms | 3.1× | 3/6 | 430.1ms | 293.3ms | 80.7 MB | 6/6 | 9227465 |
| python | 819.7ms | 18.4× | 6/6 | 831.3ms | 11.6ms | 9.7 MB | 1/6 | 9227465 |
| node | 87.0ms | 2.0× | 2/6 | 106.6ms | 19.6ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 667.0ms | 15.0× | 4/6 | 714.9ms | 47.9ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 44.5ms | 1.0× | 1/6 | 68.6ms | 24.1ms | 25.9 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 170.3ms | 12.4× | 4/6 | 206.1ms | 35.8ms | 13.4 MB | 2/6 | 449999985000000 |
| elixir | 109.9ms | 8.0× | 3/6 | 403.2ms | 293.3ms | 81.0 MB | 6/6 | 449999985000000 |
| python | 2.560s | 186.9× | 6/6 | 2.572s | 11.6ms | 9.7 MB | 1/6 | 449999985000000 |
| node | 35.2ms | 2.6× | 2/6 | 54.8ms | 19.6ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 632.9ms | 46.2× | 5/6 | 680.8ms | 47.9ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 13.7ms | 1.0× | 1/6 | 37.8ms | 24.1ms | 26.4 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.8ms | 7.9× | 3/6 | 148.6ms | 35.8ms | 12.6 MB | 2/6 | 12499997500000 |
| elixir | 50.6ms | 3.5× | 2/6 | 343.9ms | 293.3ms | 77.3 MB | 5/6 | 12499997500000 |
| python | 120.4ms | 8.4× | 4/6 | 132.0ms | 11.6ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 248.6ms | 17.4× | 5/6 | 268.2ms | 19.6ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 253.0ms | 17.7× | 6/6 | 300.9ms | 47.9ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 14.3ms | 1.0× | 1/6 | 38.4ms | 24.1ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.4ms | 4.1× | 3/6 | 78.2ms | 35.8ms | 13.5 MB | 2/6 | 13848 |
| elixir | 67.0ms | 6.4× | 4/6 | 360.3ms | 293.3ms | 81.2 MB | 6/6 | 13848 |
| python | 138.1ms | 13.3× | 6/6 | 149.7ms | 11.6ms | 9.9 MB | 1/6 | 13848 |
| node | 12.3ms | 1.2× | 2/6 | 31.9ms | 19.6ms | 49.2 MB | 5/6 | 13848 |
| ruby | 132.4ms | 12.7× | 5/6 | 180.3ms | 47.9ms | 23.6 MB | 3/6 | 13848 |
| dotnet | 10.4ms | 1.0× | 1/6 | 34.5ms | 24.1ms | 26.4 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 553.4ms | 11.3× | 4/6 | 589.2ms | 35.8ms | 28.6 MB | 4/6 | 442 |
| elixir | 170.4ms | 3.5× | 2/6 | 463.7ms | 293.3ms | 81.7 MB | 6/6 | 442 |
| python | 2.680s | 54.6× | 6/6 | 2.691s | 11.6ms | 9.7 MB | 1/6 | 442 |
| node | 191.6ms | 3.9× | 3/6 | 211.2ms | 19.6ms | 49.1 MB | 5/6 | 442 |
| ruby | 961.5ms | 19.6× | 5/6 | 1.009s | 47.9ms | 23.5 MB | 2/6 | 442 |
| dotnet | 49.1ms | 1.0× | 1/6 | 73.2ms | 24.1ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 250.4ms | 12.0× | 3/6 | 286.2ms | 35.8ms | 13.6 MB | 2/6 | 6129302 |
| elixir | 309.9ms | 14.8× | 4/6 | 603.2ms | 293.3ms | 81.4 MB | 6/6 | 6129302 |
| python | 1.452s | 69.5× | 6/6 | 1.464s | 11.6ms | 10.0 MB | 1/6 | 6129302 |
| node | 23.3ms | 1.1× | 2/6 | 42.9ms | 19.6ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 469.0ms | 22.4× | 5/6 | 516.9ms | 47.9ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 20.9ms | 1.0× | 1/6 | 45.0ms | 24.1ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 197.3ms | 29.4× | 4/6 | 233.1ms | 35.8ms | 20.8 MB | 2/6 | 654353666 |
| elixir | 89.4ms | 13.3× | 3/6 | 382.7ms | 293.3ms | 82.4 MB | 6/6 | 654353666 |
| python | 478.0ms | 71.3× | 6/6 | 489.6ms | 11.6ms | 10.3 MB | 1/6 | 654353666 |
| node | 23.0ms | 3.4× | 2/6 | 42.6ms | 19.6ms | 52.8 MB | 5/6 | 654353666 |
| ruby | 328.4ms | 49.0× | 5/6 | 376.3ms | 47.9ms | 23.8 MB | 3/6 | 654353666 |
| dotnet | 6.7ms | 1.0× | 1/6 | 30.8ms | 24.1ms | 26.9 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 949.4ms | 27.2× | 6/6 | 985.2ms | 35.8ms | 175.3 MB | 5/6 | 3388889 |
| elixir | 138.2ms | 4.0× | 5/6 | 431.5ms | 293.3ms | 199.1 MB | 6/6 | 3388889 |
| python | 45.9ms | 1.3× | 2/6 | 57.5ms | 11.6ms | 39.8 MB | 1/6 | 3388889 |
| node | 66.8ms | 1.9× | 3/6 | 86.4ms | 19.6ms | 96.0 MB | 4/6 | 3388889 |
| ruby | 94.9ms | 2.7× | 4/6 | 142.8ms | 47.9ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 34.9ms | 1.0× | 1/6 | 59.0ms | 24.1ms | 56.8 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.123s | 32.2× | 6/6 | 1.159s | 35.8ms | 54.3 MB | 5/6 | 374854840 |
| elixir | 201.8ms | 5.8× | 5/6 | 495.1ms | 293.3ms | 78.5 MB | 6/6 | 374854840 |
| python | 187.4ms | 5.4× | 4/6 | 199.0ms | 11.6ms | 9.9 MB | 1/6 | 374854840 |
| node | 34.9ms | 1.0× | 1/6 | 54.5ms | 19.6ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 74.7ms | 2.1× | 3/6 | 122.6ms | 47.9ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 41.6ms | 1.2× | 2/6 | 65.7ms | 24.1ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 494.6ms | 30.0× | 6/6 | 530.4ms | 35.8ms | 25.2 MB | 3/6 | 1638200 |
| elixir | 64.6ms | 3.9× | 3/6 | 357.9ms | 293.3ms | 81.1 MB | 6/6 | 1638200 |
| python | 106.3ms | 6.4× | 4/6 | 117.9ms | 11.6ms | 10.0 MB | 1/6 | 1638200 |
| node | 25.2ms | 1.5× | 2/6 | 44.8ms | 19.6ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 109.2ms | 6.6× | 5/6 | 157.1ms | 47.9ms | 23.7 MB | 2/6 | 1638200 |
| dotnet | 16.5ms | 1.0× | 1/6 | 40.6ms | 24.1ms | 32.5 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 327.2ms | 4.5× | 6/6 | 363.0ms | 35.8ms | 84.5 MB | 5/6 | 46468819 |
| elixir | 143.5ms | 2.0× | 4/6 | 436.8ms | 293.3ms | 164.8 MB | 6/6 | 46468819 |
| python | 230.8ms | 3.2× | 5/6 | 242.4ms | 11.6ms | 25.9 MB | 1/6 | 46468819 |
| node | 120.7ms | 1.7× | 3/6 | 140.3ms | 19.6ms | 65.7 MB | 4/6 | 46468819 |
| ruby | 79.0ms | 1.1× | 2/6 | 126.9ms | 47.9ms | 29.2 MB | 2/6 | 46468819 |
| dotnet | 73.1ms | 1.0× | 1/6 | 97.2ms | 24.1ms | 29.7 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 610.3ms | 51.3× | 6/6 | 646.1ms | 35.8ms | 21.5 MB | 2/6 | 724 |
| elixir | 60.5ms | 5.1× | 4/6 | 353.8ms | 293.3ms | 80.6 MB | 6/6 | 724 |
| python | 57.3ms | 4.8× | 3/6 | 68.9ms | 11.6ms | 9.7 MB | 1/6 | 724 |
| node | 11.9ms | 1.0× | 1/6 | 31.5ms | 19.6ms | 51.3 MB | 5/6 | 724 |
| ruby | 137.2ms | 11.5× | 5/6 | 185.1ms | 47.9ms | 23.8 MB | 3/6 | 724 |
| dotnet | 22.4ms | 1.9× | 2/6 | 46.5ms | 24.1ms | 29.5 MB | 4/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 219.0ms | 4.1× | 4/6 | 254.8ms | 35.8ms | 32.8 MB | 4/6 | 9900000 |
| elixir | 94.2ms | 1.8× | 2/6 | 387.5ms | 293.3ms | 81.5 MB | 6/6 | 9900000 |
| python | 53.4ms | 1.0× | 1/6 | 65.0ms | 11.6ms | 9.7 MB | 1/6 | 9900000 |
| node | 638.6ms | 12.0× | 6/6 | 658.2ms | 19.6ms | 50.9 MB | 5/6 | 9900000 |
| ruby | 126.3ms | 2.4× | 3/6 | 174.2ms | 47.9ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 317.8ms | 6.0× | 5/6 | 341.9ms | 24.1ms | 32.6 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 289.3ms | 3.4× | 5/6 | 325.1ms | 35.8ms | 30.0 MB | 2/6 | 2475000 |
| elixir | 85.9ms | 1.0× | 1/6 | 379.2ms | 293.3ms | 81.6 MB | 6/6 | 2475000 |
| python | 237.5ms | 2.8× | 3/6 | 249.1ms | 11.6ms | 9.8 MB | 1/6 | 2475000 |
| node | 239.7ms | 2.8× | 4/6 | 259.3ms | 19.6ms | 50.8 MB | 5/6 | 2475000 |
| ruby | 129.0ms | 1.5× | 2/6 | 176.9ms | 47.9ms | 30.1 MB | 3/6 | 2475000 |
| dotnet | 786.2ms | 9.2× | 6/6 | 810.3ms | 24.1ms | 32.7 MB | 4/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 8.3× | 6/6 | 74.7ms | 35.8ms | 13.3 MB | 2/6 | 155553889038886 |
| elixir | 21.6ms | 4.6× | 5/6 | 314.9ms | 293.3ms | 78.7 MB | 6/6 | 155553889038886 |
| python | 4.7ms | 1.0× | 1/6 | 16.3ms | 11.6ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 10.9ms | 2.3× | 4/6 | 30.5ms | 19.6ms | 52.7 MB | 5/6 | 155553889038886 |
| ruby | 8.3ms | 1.8× | 2/6 | 56.2ms | 47.9ms | 24.0 MB | 3/6 | 155553889038886 |
| dotnet | 9.2ms | 2.0× | 3/6 | 33.3ms | 24.1ms | 28.2 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 610.1ms | 33.3× | 5/6 | 645.9ms | 35.8ms | 118.0 MB | 5/6 | 6100000 |
| elixir | 43.1ms | 2.4× | 2/6 | 336.4ms | 293.3ms | 87.7 MB | 4/6 | 6100000 |
| python | 601.8ms | 32.9× | 4/6 | 613.4ms | 11.6ms | 28.1 MB | 1/6 | 6100000 |
| node | 59.1ms | 3.2× | 3/6 | 78.7ms | 19.6ms | 52.0 MB | 3/6 | 6100000 |
| ruby | 1.785s | 97.6× | 6/6 | 1.833s | 47.9ms | 137.2 MB | 6/6 | 6100000 |
| dotnet | 18.3ms | 1.0× | 1/6 | 42.4ms | 24.1ms | 31.0 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 464.3ms | 12.3× | 4/6 | 500.1ms | 35.8ms | 15.2 MB | 1/6 | 31781100 |
| elixir | 124.9ms | 3.3× | 2/6 | 418.2ms | 293.3ms | 83.8 MB | 5/6 | 31781100 |
| python | 794.3ms | 21.0× | 6/6 | 805.9ms | 11.6ms | 22.2 MB | 2/6 | 31781100 |
| node | 134.1ms | 3.5× | 3/6 | 153.7ms | 19.6ms | 183.1 MB | 6/6 | 31781100 |
| ruby | 497.0ms | 13.1× | 5/6 | 544.9ms | 47.9ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 37.9ms | 1.0× | 1/6 | 62.0ms | 24.1ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 164.8ms | 1.2× | 2/6 | 200.6ms | 35.8ms | 101.6 MB | 5/6 | 500 |
| elixir | 767.8ms | 5.7× | 6/6 | 1.061s | 293.3ms | 551.1 MB | 6/6 | 500 |
| python | 201.5ms | 1.5× | 4/6 | 213.1ms | 11.6ms | 46.8 MB | 1/6 | 500 |
| node | 135.3ms | 1.0× | 1/6 | 154.9ms | 19.6ms | 65.1 MB | 4/6 | 500 |
| ruby | 228.5ms | 1.7× | 5/6 | 276.4ms | 47.9ms | 50.1 MB | 2/6 | 500 |
| dotnet | 169.7ms | 1.3× | 3/6 | 193.8ms | 24.1ms | 50.2 MB | 3/6 | 500 |
