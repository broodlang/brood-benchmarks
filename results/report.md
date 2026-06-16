# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-16 14:02.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.3ms | 2.0× | 5/6 | 50.3ms | — | 24.1 MB | 3/6 | 0 |
| elixir | 263.7ms | 10.7× | 6/6 | 263.7ms | — | 76.7 MB | 6/6 | 0 |
| python | 24.6ms | 1.0× | 1/6 | 24.6ms | — | 9.7 MB | 1/6 | 0 |
| node | 25.5ms | 1.0× | 2/6 | 25.5ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 48.2ms | 2.0× | 4/6 | 48.2ms | — | 23.5 MB | 2/6 | 0 |
| dotnet | 36.0ms | 1.5× | 3/6 | 36.0ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 478.9ms | 18.1× | 4/6 | 529.2ms | 50.3ms | 27.5 MB | 4/6 | 9227465 |
| elixir | 121.6ms | 4.6× | 3/6 | 385.3ms | 263.7ms | 80.7 MB | 6/6 | 9227465 |
| python | 728.8ms | 27.6× | 6/6 | 753.4ms | 24.6ms | 9.8 MB | 1/6 | 9227465 |
| node | 80.9ms | 3.1× | 2/6 | 106.4ms | 25.5ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 624.4ms | 23.7× | 5/6 | 672.6ms | 48.2ms | 23.5 MB | 2/6 | 9227465 |
| dotnet | 26.4ms | 1.0× | 1/6 | 62.4ms | 36.0ms | 26.1 MB | 3/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 98.8ms | 8.5× | 3/6 | 149.1ms | 50.3ms | 27.5 MB | 4/6 | 449999985000000 |
| elixir | 99.3ms | 8.6× | 4/6 | 363.0ms | 263.7ms | 80.7 MB | 6/6 | 449999985000000 |
| python | 2.402s | 207.1× | 6/6 | 2.427s | 24.6ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 37.3ms | 3.2× | 2/6 | 62.8ms | 25.5ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 550.0ms | 47.4× | 5/6 | 598.2ms | 48.2ms | 23.5 MB | 2/6 | 449999985000000 |
| dotnet | 11.6ms | 1.0× | 1/6 | 47.6ms | 36.0ms | 26.4 MB | 3/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 91.6ms | 10.2× | 3/6 | 141.9ms | 50.3ms | 24.0 MB | 3/6 | 12499997500000 |
| elixir | 46.3ms | 5.1× | 2/6 | 310.0ms | 263.7ms | 78.2 MB | 5/6 | 12499997500000 |
| python | 108.8ms | 12.1× | 4/6 | 133.4ms | 24.6ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 229.2ms | 25.5× | 5/6 | 254.7ms | 25.5ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 238.5ms | 26.5× | 6/6 | 286.7ms | 48.2ms | 23.5 MB | 2/6 | 12499997500000 |
| dotnet | 9.0ms | 1.0× | 1/6 | 45.0ms | 36.0ms | 27.6 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.0ms | 5.4× | 3/6 | 88.3ms | 50.3ms | 27.7 MB | 4/6 | 13848 |
| elixir | 63.5ms | 8.9× | 4/6 | 327.2ms | 263.7ms | 80.9 MB | 6/6 | 13848 |
| python | 123.2ms | 17.4× | 5/6 | 147.8ms | 24.6ms | 9.9 MB | 1/6 | 13848 |
| node | 17.9ms | 2.5× | 2/6 | 43.4ms | 25.5ms | 49.2 MB | 5/6 | 13848 |
| ruby | 125.0ms | 17.6× | 6/6 | 173.2ms | 48.2ms | 23.5 MB | 2/6 | 13848 |
| dotnet | 7.1ms | 1.0× | 1/6 | 43.1ms | 36.0ms | 26.3 MB | 3/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 490.5ms | 15.5× | 4/6 | 540.8ms | 50.3ms | 41.3 MB | 4/6 | 442 |
| elixir | 154.7ms | 4.9× | 2/6 | 418.4ms | 263.7ms | 80.7 MB | 6/6 | 442 |
| python | 2.566s | 81.2× | 6/6 | 2.590s | 24.6ms | 9.7 MB | 1/6 | 442 |
| node | 182.8ms | 5.8× | 3/6 | 208.3ms | 25.5ms | 49.1 MB | 5/6 | 442 |
| ruby | 881.1ms | 27.9× | 5/6 | 929.3ms | 48.2ms | 23.5 MB | 2/6 | 442 |
| dotnet | 31.6ms | 1.0× | 1/6 | 67.6ms | 36.0ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 223.9ms | 16.0× | 3/6 | 274.2ms | 50.3ms | 27.7 MB | 4/6 | 6129302 |
| elixir | 285.6ms | 20.4× | 4/6 | 549.3ms | 263.7ms | 82.2 MB | 6/6 | 6129302 |
| python | 1.466s | 104.7× | 6/6 | 1.491s | 24.6ms | 10.0 MB | 1/6 | 6129302 |
| node | 27.7ms | 2.0× | 2/6 | 53.2ms | 25.5ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 440.0ms | 31.4× | 5/6 | 488.2ms | 48.2ms | 23.6 MB | 2/6 | 6129302 |
| dotnet | 14.0ms | 1.0× | 1/6 | 50.0ms | 36.0ms | 26.4 MB | 3/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 162.5ms | 45.1× | 4/6 | 212.8ms | 50.3ms | 39.8 MB | 4/6 | 654353666 |
| elixir | 80.0ms | 22.2× | 3/6 | 343.7ms | 263.7ms | 82.5 MB | 6/6 | 654353666 |
| python | 456.7ms | 126.9× | 6/6 | 481.3ms | 24.6ms | 10.3 MB | 1/6 | 654353666 |
| node | 28.1ms | 7.8× | 2/6 | 53.6ms | 25.5ms | 52.8 MB | 5/6 | 654353666 |
| ruby | 294.9ms | 81.9× | 5/6 | 343.1ms | 48.2ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 3.6ms | 1.0× | 1/6 | 39.6ms | 36.0ms | 26.8 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 0.0ms | < 1× | 1/6 | 48.2ms | 50.3ms | 34.3 MB | 1/6 | 3388889 |
| elixir | 113.8ms | 113.8× | 6/6 | 377.5ms | 263.7ms | 198.6 MB | 6/6 | 3388889 |
| python | 31.8ms | 31.8× | 3/6 | 56.4ms | 24.6ms | 39.8 MB | 2/6 | 3388889 |
| node | 51.0ms | 51.0× | 4/6 | 76.5ms | 25.5ms | 96.0 MB | 5/6 | 3388889 |
| ruby | 87.6ms | 87.6× | 5/6 | 135.8ms | 48.2ms | 52.1 MB | 3/6 | 3388889 |
| dotnet | 29.4ms | 29.4× | 2/6 | 65.4ms | 36.0ms | 56.9 MB | 4/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 864.7ms | 22.8× | 6/6 | 915.0ms | 50.3ms | 93.4 MB | 6/6 | 374854840 |
| elixir | 184.1ms | 4.8× | 5/6 | 447.8ms | 263.7ms | 78.8 MB | 5/6 | 374854840 |
| python | 160.7ms | 4.2× | 4/6 | 185.3ms | 24.6ms | 9.9 MB | 1/6 | 374854840 |
| node | 38.9ms | 1.0× | 2/6 | 64.4ms | 25.5ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 78.8ms | 2.1× | 3/6 | 127.0ms | 48.2ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 38.0ms | 1.0× | 1/6 | 74.0ms | 36.0ms | 27.4 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 412.6ms | 27.9× | 6/6 | 462.9ms | 50.3ms | 38.5 MB | 4/6 | 1638200 |
| elixir | 57.9ms | 3.9× | 3/6 | 321.6ms | 263.7ms | 83.9 MB | 6/6 | 1638200 |
| python | 80.6ms | 5.4× | 4/6 | 105.2ms | 24.6ms | 10.0 MB | 1/6 | 1638200 |
| node | 29.5ms | 2.0× | 2/6 | 55.0ms | 25.5ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 105.2ms | 7.1× | 5/6 | 153.4ms | 48.2ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 14.8ms | 1.0× | 1/6 | 50.8ms | 36.0ms | 32.5 MB | 3/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 296.7ms | 5.8× | 6/6 | 347.0ms | 50.3ms | 123.3 MB | 5/6 | 46468819 |
| elixir | 124.7ms | 2.4× | 4/6 | 388.4ms | 263.7ms | 166.1 MB | 6/6 | 46468819 |
| python | 176.2ms | 3.5× | 5/6 | 200.8ms | 24.6ms | 26.0 MB | 1/6 | 46468819 |
| node | 102.2ms | 2.0× | 3/6 | 127.7ms | 25.5ms | 65.6 MB | 4/6 | 46468819 |
| ruby | 65.6ms | 1.3× | 2/6 | 113.8ms | 48.2ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 50.9ms | 1.0× | 1/6 | 86.9ms | 36.0ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 557.3ms | 32.8× | 6/6 | 607.6ms | 50.3ms | 35.6 MB | 4/6 | 724 |
| elixir | 57.4ms | 3.4× | 4/6 | 321.1ms | 263.7ms | 81.0 MB | 6/6 | 724 |
| python | 53.9ms | 3.2× | 3/6 | 78.5ms | 24.6ms | 9.8 MB | 1/6 | 724 |
| node | 17.0ms | 1.0× | 1/6 | 42.5ms | 25.5ms | 51.3 MB | 5/6 | 724 |
| ruby | 131.1ms | 7.7× | 5/6 | 179.3ms | 48.2ms | 23.8 MB | 2/6 | 724 |
| dotnet | 18.5ms | 1.1× | 2/6 | 54.5ms | 36.0ms | 29.4 MB | 3/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 188.5ms | 5.4× | 4/6 | 238.8ms | 50.3ms | 41.6 MB | 4/6 | 9900000 |
| elixir | 67.8ms | 1.9× | 2/6 | 331.5ms | 263.7ms | 81.5 MB | 6/6 | 9900000 |
| python | 35.2ms | 1.0× | 1/6 | 59.8ms | 24.6ms | 9.8 MB | 1/6 | 9900000 |
| node | 584.8ms | 16.6× | 6/6 | 610.3ms | 25.5ms | 51.0 MB | 5/6 | 9900000 |
| ruby | 116.9ms | 3.3× | 3/6 | 165.1ms | 48.2ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 293.2ms | 8.3× | 5/6 | 329.2ms | 36.0ms | 32.6 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 257.0ms | 3.4× | 5/6 | 307.3ms | 50.3ms | 42.5 MB | 4/6 | 2475000 |
| elixir | 76.7ms | 1.0× | 1/6 | 340.4ms | 263.7ms | 81.5 MB | 6/6 | 2475000 |
| python | 222.6ms | 2.9× | 4/6 | 247.2ms | 24.6ms | 9.9 MB | 1/6 | 2475000 |
| node | 219.1ms | 2.9× | 3/6 | 244.6ms | 25.5ms | 50.8 MB | 5/6 | 2475000 |
| ruby | 120.0ms | 1.6× | 2/6 | 168.2ms | 48.2ms | 30.1 MB | 2/6 | 2475000 |
| dotnet | 701.7ms | 9.1× | 6/6 | 737.7ms | 36.0ms | 32.7 MB | 3/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.9ms | 30.9× | 6/6 | 81.2ms | 50.3ms | 27.6 MB | 3/6 | 155553889038886 |
| elixir | 24.6ms | 24.6× | 5/6 | 288.3ms | 263.7ms | 77.9 MB | 6/6 | 155553889038886 |
| python | 0.0ms | < 1× | 1/6 | 20.4ms | 24.6ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 16.5ms | 16.5× | 4/6 | 42.0ms | 25.5ms | 52.5 MB | 5/6 | 155553889038886 |
| ruby | 14.7ms | 14.7× | 3/6 | 62.9ms | 48.2ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 6.7ms | 6.7× | 2/6 | 42.7ms | 36.0ms | 28.1 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 95.5ms | 7.3× | 4/6 | 145.8ms | 50.3ms | 71.1 MB | 4/6 | 6100000 |
| elixir | 64.8ms | 5.0× | 3/6 | 328.5ms | 263.7ms | 87.5 MB | 5/6 | 6100000 |
| python | 530.8ms | 40.8× | 5/6 | 555.4ms | 24.6ms | 28.1 MB | 1/6 | 6100000 |
| node | 54.3ms | 4.2× | 2/6 | 79.8ms | 25.5ms | 52.1 MB | 3/6 | 6100000 |
| ruby | 1.552s | 119.4× | 6/6 | 1.600s | 48.2ms | 137.8 MB | 6/6 | 6100000 |
| dotnet | 13.0ms | 1.0× | 1/6 | 49.0ms | 36.0ms | 30.8 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 330.7ms | 12.1× | 4/6 | 381.0ms | 50.3ms | 29.6 MB | 4/6 | 31781100 |
| elixir | 114.6ms | 4.2× | 3/6 | 378.3ms | 263.7ms | 85.7 MB | 5/6 | 31781100 |
| python | 682.9ms | 24.9× | 6/6 | 707.5ms | 24.6ms | 22.2 MB | 1/6 | 31781100 |
| node | 105.1ms | 3.8× | 2/6 | 130.6ms | 25.5ms | 183.1 MB | 6/6 | 31781100 |
| ruby | 416.3ms | 15.2× | 5/6 | 464.5ms | 48.2ms | 23.7 MB | 2/6 | 31781100 |
| dotnet | 27.4ms | 1.0× | 1/6 | 63.4ms | 36.0ms | 27.9 MB | 3/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 131.8ms | 1.2× | 2/6 | 182.1ms | 50.3ms | 125.6 MB | 5/6 | 500 |
| elixir | 671.7ms | 6.0× | 6/6 | 935.4ms | 263.7ms | 545.0 MB | 6/6 | 500 |
| python | 162.5ms | 1.4× | 4/6 | 187.1ms | 24.6ms | 48.0 MB | 1/6 | 500 |
| node | 112.5ms | 1.0× | 1/6 | 138.0ms | 25.5ms | 65.3 MB | 4/6 | 500 |
| ruby | 195.2ms | 1.7× | 5/6 | 243.4ms | 48.2ms | 50.3 MB | 3/6 | 500 |
| dotnet | 142.0ms | 1.3× | 3/6 | 178.0ms | 36.0ms | 48.2 MB | 2/6 | 500 |
