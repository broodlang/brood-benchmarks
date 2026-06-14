# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-14 13:06.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.0ms | 2.7× | 4/6 | 28.0ms | — | 14.4 MB | 2/6 | 0 |
| elixir | 259.3ms | 24.7× | 6/6 | 259.3ms | — | 76.2 MB | 6/6 | 0 |
| python | 10.5ms | 1.0× | 1/6 | 10.5ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.8ms | 1.8× | 2/6 | 18.8ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 42.1ms | 4.0× | 5/6 | 42.1ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.3ms | 2.0× | 3/6 | 21.3ms | — | 25.9 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 645.1ms | 16.1× | 5/6 | 673.1ms | 28.0ms | 15.5 MB | 2/6 | 9227465 |
| elixir | 122.9ms | 3.1× | 3/6 | 382.2ms | 259.3ms | 84.2 MB | 6/6 | 9227465 |
| python | 766.2ms | 19.1× | 6/6 | 776.7ms | 10.5ms | 9.7 MB | 1/6 | 9227465 |
| node | 74.5ms | 1.9× | 2/6 | 93.3ms | 18.8ms | 48.7 MB | 5/6 | 9227465 |
| ruby | 640.0ms | 16.0× | 4/6 | 682.1ms | 42.1ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 40.1ms | 1.0× | 1/6 | 61.4ms | 21.3ms | 26.0 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 182.6ms | 7.3× | 4/6 | 210.6ms | 28.0ms | 15.4 MB | 2/6 | 449999985000000 |
| elixir | 92.0ms | 3.7× | 3/6 | 351.3ms | 259.3ms | 81.6 MB | 6/6 | 449999985000000 |
| python | 2.358s | 94.7× | 6/6 | 2.368s | 10.5ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 31.1ms | 1.2× | 2/6 | 49.9ms | 18.8ms | 50.1 MB | 5/6 | 449999985000000 |
| ruby | 609.5ms | 24.5× | 5/6 | 651.6ms | 42.1ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 24.9ms | 1.0× | 1/6 | 46.2ms | 21.3ms | 26.3 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.5ms | 8.1× | 3/6 | 135.5ms | 28.0ms | 14.5 MB | 2/6 | 12499997500000 |
| elixir | 48.1ms | 3.6× | 2/6 | 307.4ms | 259.3ms | 77.4 MB | 5/6 | 12499997500000 |
| python | 109.7ms | 8.2× | 4/6 | 120.2ms | 10.5ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 232.4ms | 17.5× | 5/6 | 251.2ms | 18.8ms | 90.7 MB | 6/6 | 12499997500000 |
| ruby | 234.4ms | 17.6× | 6/6 | 276.5ms | 42.1ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 13.3ms | 1.0× | 1/6 | 34.6ms | 21.3ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.1ms | 4.7× | 3/6 | 71.1ms | 28.0ms | 15.7 MB | 2/6 | 13848 |
| elixir | 68.1ms | 7.5× | 4/6 | 327.4ms | 259.3ms | 81.7 MB | 6/6 | 13848 |
| python | 125.5ms | 13.8× | 6/6 | 136.0ms | 10.5ms | 9.9 MB | 1/6 | 13848 |
| node | 15.6ms | 1.7× | 2/6 | 34.4ms | 18.8ms | 49.2 MB | 5/6 | 13848 |
| ruby | 121.2ms | 13.3× | 5/6 | 163.3ms | 42.1ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 9.1ms | 1.0× | 1/6 | 30.4ms | 21.3ms | 26.3 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 491.4ms | 8.2× | 4/6 | 519.4ms | 28.0ms | 29.8 MB | 4/6 | 442 |
| elixir | 151.4ms | 2.5× | 2/6 | 410.7ms | 259.3ms | 80.8 MB | 6/6 | 442 |
| python | 2.469s | 41.1× | 6/6 | 2.480s | 10.5ms | 9.8 MB | 1/6 | 442 |
| node | 179.8ms | 3.0× | 3/6 | 198.6ms | 18.8ms | 49.0 MB | 5/6 | 442 |
| ruby | 893.1ms | 14.9× | 5/6 | 935.2ms | 42.1ms | 23.5 MB | 2/6 | 442 |
| dotnet | 60.1ms | 1.0× | 1/6 | 81.4ms | 21.3ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.332s | 69.7× | 5/6 | 1.360s | 28.0ms | 15.8 MB | 2/6 | 6129302 |
| elixir | 291.5ms | 15.3× | 3/6 | 550.8ms | 259.3ms | 81.3 MB | 6/6 | 6129302 |
| python | 1.386s | 72.5× | 6/6 | 1.396s | 10.5ms | 10.0 MB | 1/6 | 6129302 |
| node | 21.1ms | 1.1× | 2/6 | 39.9ms | 18.8ms | 49.8 MB | 5/6 | 6129302 |
| ruby | 434.8ms | 22.8× | 4/6 | 476.9ms | 42.1ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 19.1ms | 1.0× | 1/6 | 40.4ms | 21.3ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 542.2ms | 100.4× | 6/6 | 570.2ms | 28.0ms | 31.7 MB | 4/6 | 654353666 |
| elixir | 78.9ms | 14.6× | 3/6 | 338.2ms | 259.3ms | 81.3 MB | 6/6 | 654353666 |
| python | 469.5ms | 86.9× | 5/6 | 480.0ms | 10.5ms | 10.3 MB | 1/6 | 654353666 |
| node | 27.2ms | 5.0× | 2/6 | 46.0ms | 18.8ms | 53.0 MB | 5/6 | 654353666 |
| ruby | 294.4ms | 54.5× | 4/6 | 336.5ms | 42.1ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 5.4ms | 1.0× | 1/6 | 26.7ms | 21.3ms | 26.8 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 823.8ms | 22.9× | 6/6 | 851.8ms | 28.0ms | 175.0 MB | 5/6 | 3388889 |
| elixir | 128.3ms | 3.6× | 5/6 | 387.6ms | 259.3ms | 198.6 MB | 6/6 | 3388889 |
| python | 46.5ms | 1.3× | 2/6 | 57.0ms | 10.5ms | 39.8 MB | 1/6 | 3388889 |
| node | 58.3ms | 1.6× | 3/6 | 77.1ms | 18.8ms | 96.0 MB | 4/6 | 3388889 |
| ruby | 90.3ms | 2.5× | 4/6 | 132.4ms | 42.1ms | 52.2 MB | 2/6 | 3388889 |
| dotnet | 35.9ms | 1.0× | 1/6 | 57.2ms | 21.3ms | 56.9 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.014s | 27.3× | 6/6 | 1.042s | 28.0ms | 56.6 MB | 5/6 | 374854840 |
| elixir | 187.8ms | 5.1× | 5/6 | 447.1ms | 259.3ms | 78.9 MB | 6/6 | 374854840 |
| python | 182.8ms | 4.9× | 4/6 | 193.3ms | 10.5ms | 9.9 MB | 1/6 | 374854840 |
| node | 38.3ms | 1.0× | 2/6 | 57.1ms | 18.8ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 71.9ms | 1.9× | 3/6 | 114.0ms | 42.1ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 37.1ms | 1.0× | 1/6 | 58.4ms | 21.3ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 451.7ms | 26.9× | 6/6 | 479.7ms | 28.0ms | 25.9 MB | 3/6 | 1638200 |
| elixir | 57.6ms | 3.4× | 3/6 | 316.9ms | 259.3ms | 81.1 MB | 6/6 | 1638200 |
| python | 96.3ms | 5.7× | 4/6 | 106.8ms | 10.5ms | 10.0 MB | 1/6 | 1638200 |
| node | 21.5ms | 1.3× | 2/6 | 40.3ms | 18.8ms | 56.7 MB | 5/6 | 1638200 |
| ruby | 101.9ms | 6.1× | 5/6 | 144.0ms | 42.1ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 16.8ms | 1.0× | 1/6 | 38.1ms | 21.3ms | 32.4 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 289.1ms | 4.0× | 6/6 | 317.1ms | 28.0ms | 86.5 MB | 5/6 | 46468819 |
| elixir | 122.8ms | 1.7× | 4/6 | 382.1ms | 259.3ms | 164.8 MB | 6/6 | 46468819 |
| python | 189.7ms | 2.6× | 5/6 | 200.2ms | 10.5ms | 25.9 MB | 1/6 | 46468819 |
| node | 106.8ms | 1.5× | 3/6 | 125.6ms | 18.8ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 72.5ms | 1.0× | 1/6 | 114.6ms | 42.1ms | 29.2 MB | 2/6 | 46468819 |
| dotnet | 77.4ms | 1.1× | 2/6 | 98.7ms | 21.3ms | 29.7 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 512.1ms | 23.3× | 6/6 | 540.1ms | 28.0ms | 23.8 MB | 3/6 | 724 |
| elixir | 61.8ms | 2.8× | 3/6 | 321.1ms | 259.3ms | 81.4 MB | 6/6 | 724 |
| python | 66.9ms | 3.0× | 4/6 | 77.4ms | 10.5ms | 9.8 MB | 1/6 | 724 |
| node | 23.8ms | 1.1× | 2/6 | 42.6ms | 18.8ms | 51.2 MB | 5/6 | 724 |
| ruby | 127.7ms | 5.8× | 5/6 | 169.8ms | 42.1ms | 23.8 MB | 2/6 | 724 |
| dotnet | 22.0ms | 1.0× | 1/6 | 43.3ms | 21.3ms | 29.3 MB | 4/6 | 724 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 551.6ms | 65.7× | 6/6 | 579.6ms | 28.0ms | 36.4 MB | 4/6 | 155553889038886 |
| elixir | 22.9ms | 2.7× | 5/6 | 282.2ms | 259.3ms | 78.0 MB | 6/6 | 155553889038886 |
| python | 9.1ms | 1.1× | 2/6 | 19.6ms | 10.5ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 12.1ms | 1.4× | 3/6 | 30.9ms | 18.8ms | 52.6 MB | 5/6 | 155553889038886 |
| ruby | 19.1ms | 2.3× | 4/6 | 61.2ms | 42.1ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 8.4ms | 1.0× | 1/6 | 29.7ms | 21.3ms | 28.1 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 520.1ms | 20.0× | 4/6 | 548.1ms | 28.0ms | 118.2 MB | 5/6 | 6100000 |
| elixir | 55.9ms | 2.1× | 3/6 | 315.2ms | 259.3ms | 87.3 MB | 4/6 | 6100000 |
| python | 554.0ms | 21.3× | 5/6 | 564.5ms | 10.5ms | 28.1 MB | 1/6 | 6100000 |
| node | 53.9ms | 2.1× | 2/6 | 72.7ms | 18.8ms | 51.8 MB | 3/6 | 6100000 |
| ruby | 1.601s | 61.6× | 6/6 | 1.643s | 42.1ms | 137.4 MB | 6/6 | 6100000 |
| dotnet | 26.0ms | 1.0× | 1/6 | 47.3ms | 21.3ms | 30.9 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 406.7ms | 11.6× | 4/6 | 434.7ms | 28.0ms | 17.2 MB | 1/6 | 31781100 |
| elixir | 122.7ms | 3.5× | 3/6 | 382.0ms | 259.3ms | 81.8 MB | 5/6 | 31781100 |
| python | 683.7ms | 19.5× | 6/6 | 694.2ms | 10.5ms | 22.1 MB | 2/6 | 31781100 |
| node | 111.0ms | 3.2× | 2/6 | 129.8ms | 18.8ms | 183.1 MB | 6/6 | 31781100 |
| ruby | 442.1ms | 12.6× | 5/6 | 484.2ms | 42.1ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 35.1ms | 1.0× | 1/6 | 56.4ms | 21.3ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 139.2ms | 1.2× | 2/6 | 167.2ms | 28.0ms | 102.0 MB | 5/6 | 500 |
| elixir | 641.1ms | 5.3× | 6/6 | 900.4ms | 259.3ms | 530.6 MB | 6/6 | 500 |
| python | 176.2ms | 1.5× | 4/6 | 186.7ms | 10.5ms | 46.4 MB | 1/6 | 500 |
| node | 120.3ms | 1.0× | 1/6 | 139.1ms | 18.8ms | 65.2 MB | 4/6 | 500 |
| ruby | 208.2ms | 1.7× | 5/6 | 250.3ms | 42.1ms | 50.1 MB | 3/6 | 500 |
| dotnet | 157.6ms | 1.3× | 3/6 | 178.9ms | 21.3ms | 48.1 MB | 2/6 | 500 |
