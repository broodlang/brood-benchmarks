# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-15 15:34.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 30.0ms | 2.8× | 4/6 | 30.0ms | — | 15.1 MB | 2/6 | 0 |
| elixir | 260.8ms | 24.6× | 6/6 | 260.8ms | — | 76.1 MB | 6/6 | 0 |
| python | 10.6ms | 1.0× | 1/6 | 10.6ms | — | 9.7 MB | 1/6 | 0 |
| node | 17.9ms | 1.7× | 2/6 | 17.9ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 41.1ms | 3.9× | 5/6 | 41.1ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.4ms | 2.0× | 3/6 | 21.4ms | — | 25.9 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 671.1ms | 16.3× | 5/6 | 701.1ms | 30.0ms | 16.3 MB | 2/6 | 9227465 |
| elixir | 128.2ms | 3.1× | 3/6 | 389.0ms | 260.8ms | 80.6 MB | 6/6 | 9227465 |
| python | 756.0ms | 18.4× | 6/6 | 766.6ms | 10.6ms | 9.7 MB | 1/6 | 9227465 |
| node | 77.5ms | 1.9× | 2/6 | 95.4ms | 17.9ms | 48.7 MB | 5/6 | 9227465 |
| ruby | 631.9ms | 15.4× | 4/6 | 673.0ms | 41.1ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 41.1ms | 1.0× | 1/6 | 62.5ms | 21.4ms | 26.0 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 261.3ms | 14.0× | 4/6 | 291.3ms | 30.0ms | 16.3 MB | 2/6 | 449999985000000 |
| elixir | 98.1ms | 5.2× | 3/6 | 358.9ms | 260.8ms | 80.7 MB | 6/6 | 449999985000000 |
| python | 2.351s | 125.7× | 6/6 | 2.361s | 10.6ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 31.4ms | 1.7× | 2/6 | 49.3ms | 17.9ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 603.1ms | 32.3× | 5/6 | 644.2ms | 41.1ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 18.7ms | 1.0× | 1/6 | 40.1ms | 21.4ms | 26.3 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.9ms | 4.8× | 3/6 | 137.9ms | 30.0ms | 15.0 MB | 2/6 | 12499997500000 |
| elixir | 51.9ms | 2.3× | 2/6 | 312.7ms | 260.8ms | 76.9 MB | 5/6 | 12499997500000 |
| python | 109.7ms | 4.9× | 4/6 | 120.3ms | 10.6ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 229.9ms | 10.2× | 5/6 | 247.8ms | 17.9ms | 90.7 MB | 6/6 | 12499997500000 |
| ruby | 235.1ms | 10.4× | 6/6 | 276.2ms | 41.1ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 22.5ms | 1.0× | 1/6 | 43.9ms | 21.4ms | 27.5 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 42.8ms | 3.8× | 3/6 | 72.8ms | 30.0ms | 16.4 MB | 2/6 | 13848 |
| elixir | 69.9ms | 6.2× | 4/6 | 330.7ms | 260.8ms | 81.0 MB | 6/6 | 13848 |
| python | 128.0ms | 11.3× | 6/6 | 138.6ms | 10.6ms | 9.9 MB | 1/6 | 13848 |
| node | 11.3ms | 1.0× | 1/6 | 29.2ms | 17.9ms | 49.1 MB | 5/6 | 13848 |
| ruby | 121.9ms | 10.8× | 5/6 | 163.0ms | 41.1ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 16.9ms | 1.5× | 2/6 | 38.3ms | 21.4ms | 26.3 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 490.7ms | 10.2× | 4/6 | 520.7ms | 30.0ms | 30.5 MB | 4/6 | 442 |
| elixir | 153.0ms | 3.2× | 2/6 | 413.8ms | 260.8ms | 81.7 MB | 6/6 | 442 |
| python | 2.513s | 52.3× | 6/6 | 2.523s | 10.6ms | 9.7 MB | 1/6 | 442 |
| node | 180.0ms | 3.7× | 3/6 | 197.9ms | 17.9ms | 49.0 MB | 5/6 | 442 |
| ruby | 892.1ms | 18.6× | 5/6 | 933.2ms | 41.1ms | 23.5 MB | 2/6 | 442 |
| dotnet | 48.0ms | 1.0× | 1/6 | 69.4ms | 21.4ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 238.1ms | 12.4× | 3/6 | 268.1ms | 30.0ms | 16.5 MB | 2/6 | 6129302 |
| elixir | 293.4ms | 15.3× | 4/6 | 554.2ms | 260.8ms | 82.2 MB | 6/6 | 6129302 |
| python | 1.345s | 70.1× | 6/6 | 1.356s | 10.6ms | 10.0 MB | 1/6 | 6129302 |
| node | 21.3ms | 1.1× | 2/6 | 39.2ms | 17.9ms | 49.8 MB | 5/6 | 6129302 |
| ruby | 436.4ms | 22.7× | 5/6 | 477.5ms | 41.1ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 19.2ms | 1.0× | 1/6 | 40.6ms | 21.4ms | 26.3 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.0ms | 30.0× | 4/6 | 201.0ms | 30.0ms | 23.7 MB | 2/6 | 654353666 |
| elixir | 82.1ms | 14.4× | 3/6 | 342.9ms | 260.8ms | 81.3 MB | 6/6 | 654353666 |
| python | 464.9ms | 81.6× | 6/6 | 475.5ms | 10.6ms | 10.4 MB | 1/6 | 654353666 |
| node | 21.7ms | 3.8× | 2/6 | 39.6ms | 17.9ms | 52.7 MB | 5/6 | 654353666 |
| ruby | 305.5ms | 53.6× | 5/6 | 346.6ms | 41.1ms | 23.7 MB | 3/6 | 654353666 |
| dotnet | 5.7ms | 1.0× | 1/6 | 27.1ms | 21.4ms | 26.7 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 828.3ms | 26.5× | 6/6 | 858.3ms | 30.0ms | 182.2 MB | 5/6 | 3388889 |
| elixir | 128.1ms | 4.1× | 5/6 | 388.9ms | 260.8ms | 200.1 MB | 6/6 | 3388889 |
| python | 43.5ms | 1.4× | 2/6 | 54.1ms | 10.6ms | 39.8 MB | 1/6 | 3388889 |
| node | 59.5ms | 1.9× | 3/6 | 77.4ms | 17.9ms | 96.0 MB | 4/6 | 3388889 |
| ruby | 87.6ms | 2.8× | 4/6 | 128.7ms | 41.1ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 31.2ms | 1.0× | 1/6 | 52.6ms | 21.4ms | 56.9 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.012s | 30.9× | 6/6 | 1.042s | 30.0ms | 57.2 MB | 5/6 | 374854840 |
| elixir | 196.0ms | 6.0× | 5/6 | 456.8ms | 260.8ms | 79.8 MB | 6/6 | 374854840 |
| python | 172.5ms | 5.3× | 4/6 | 183.1ms | 10.6ms | 9.9 MB | 1/6 | 374854840 |
| node | 32.8ms | 1.0× | 1/6 | 50.7ms | 17.9ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 80.0ms | 2.4× | 3/6 | 121.1ms | 41.1ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 46.1ms | 1.4× | 2/6 | 67.5ms | 21.4ms | 27.4 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 452.6ms | 16.0× | 6/6 | 482.6ms | 30.0ms | 26.2 MB | 3/6 | 1638200 |
| elixir | 48.7ms | 1.7× | 3/6 | 309.5ms | 260.8ms | 82.1 MB | 6/6 | 1638200 |
| python | 95.7ms | 3.4× | 4/6 | 106.3ms | 10.6ms | 10.0 MB | 1/6 | 1638200 |
| node | 35.5ms | 1.3× | 2/6 | 53.4ms | 17.9ms | 56.7 MB | 5/6 | 1638200 |
| ruby | 111.4ms | 4.0× | 5/6 | 152.5ms | 41.1ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 28.2ms | 1.0× | 1/6 | 49.6ms | 21.4ms | 32.4 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 285.7ms | 3.9× | 6/6 | 315.7ms | 30.0ms | 87.1 MB | 5/6 | 46468819 |
| elixir | 126.8ms | 1.7× | 4/6 | 387.6ms | 260.8ms | 164.8 MB | 6/6 | 46468819 |
| python | 201.2ms | 2.7× | 5/6 | 211.8ms | 10.6ms | 25.9 MB | 1/6 | 46468819 |
| node | 114.3ms | 1.6× | 3/6 | 132.2ms | 17.9ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 73.2ms | 1.0× | 1/6 | 114.3ms | 41.1ms | 29.2 MB | 2/6 | 46468819 |
| dotnet | 78.9ms | 1.1× | 2/6 | 100.3ms | 21.4ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 528.1ms | 36.9× | 6/6 | 558.1ms | 30.0ms | 24.2 MB | 3/6 | 724 |
| elixir | 49.1ms | 3.4× | 3/6 | 309.9ms | 260.8ms | 80.6 MB | 6/6 | 724 |
| python | 53.3ms | 3.7× | 4/6 | 63.9ms | 10.6ms | 9.7 MB | 1/6 | 724 |
| node | 14.3ms | 1.0× | 1/6 | 32.2ms | 17.9ms | 51.4 MB | 5/6 | 724 |
| ruby | 137.7ms | 9.6× | 5/6 | 178.8ms | 41.1ms | 23.7 MB | 2/6 | 724 |
| dotnet | 34.0ms | 2.4× | 2/6 | 55.4ms | 21.4ms | 29.5 MB | 4/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 207.7ms | 4.0× | 4/6 | 237.7ms | 30.0ms | 33.5 MB | 4/6 | 9900000 |
| elixir | 86.7ms | 1.7× | 2/6 | 347.5ms | 260.8ms | 86.3 MB | 6/6 | 9900000 |
| python | 52.4ms | 1.0× | 1/6 | 63.0ms | 10.6ms | 9.7 MB | 1/6 | 9900000 |
| node | 590.4ms | 11.3× | 6/6 | 608.3ms | 17.9ms | 50.9 MB | 5/6 | 9900000 |
| ruby | 111.4ms | 2.1× | 3/6 | 152.5ms | 41.1ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 301.1ms | 5.7× | 5/6 | 322.5ms | 21.4ms | 32.5 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 270.1ms | 4.0× | 5/6 | 300.1ms | 30.0ms | 32.6 MB | 4/6 | 2475000 |
| elixir | 68.3ms | 1.0× | 1/6 | 329.1ms | 260.8ms | 81.5 MB | 6/6 | 2475000 |
| python | 225.6ms | 3.3× | 3/6 | 236.2ms | 10.6ms | 9.9 MB | 1/6 | 2475000 |
| node | 226.0ms | 3.3× | 4/6 | 243.9ms | 17.9ms | 50.7 MB | 5/6 | 2475000 |
| ruby | 118.1ms | 1.7× | 2/6 | 159.2ms | 41.1ms | 30.1 MB | 2/6 | 2475000 |
| dotnet | 708.2ms | 10.4× | 6/6 | 729.6ms | 21.4ms | 32.5 MB | 3/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 131.1ms | 31.2× | 6/6 | 161.1ms | 30.0ms | 34.1 MB | 4/6 | 155553889038886 |
| elixir | 16.8ms | 4.0× | 5/6 | 277.6ms | 260.8ms | 78.0 MB | 6/6 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/6 | 14.8ms | 10.6ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 10.8ms | 2.6× | 3/6 | 28.7ms | 17.9ms | 52.6 MB | 5/6 | 155553889038886 |
| ruby | 7.8ms | 1.9× | 2/6 | 48.9ms | 41.1ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 14.1ms | 3.4× | 4/6 | 35.5ms | 21.4ms | 28.1 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 534.7ms | 20.0× | 4/6 | 564.7ms | 30.0ms | 120.4 MB | 5/6 | 6100000 |
| elixir | 56.7ms | 2.1× | 2/6 | 317.5ms | 260.8ms | 87.5 MB | 4/6 | 6100000 |
| python | 547.7ms | 20.5× | 5/6 | 558.3ms | 10.6ms | 28.0 MB | 1/6 | 6100000 |
| node | 63.5ms | 2.4× | 3/6 | 81.4ms | 17.9ms | 52.0 MB | 3/6 | 6100000 |
| ruby | 1.589s | 59.5× | 6/6 | 1.630s | 41.1ms | 136.9 MB | 6/6 | 6100000 |
| dotnet | 26.7ms | 1.0× | 1/6 | 48.1ms | 21.4ms | 30.7 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 409.9ms | 11.9× | 4/6 | 439.9ms | 30.0ms | 17.8 MB | 1/6 | 31781100 |
| elixir | 126.2ms | 3.7× | 3/6 | 387.0ms | 260.8ms | 81.7 MB | 5/6 | 31781100 |
| python | 688.7ms | 20.0× | 6/6 | 699.3ms | 10.6ms | 22.1 MB | 2/6 | 31781100 |
| node | 108.8ms | 3.2× | 2/6 | 126.7ms | 17.9ms | 183.2 MB | 6/6 | 31781100 |
| ruby | 450.4ms | 13.1× | 5/6 | 491.5ms | 41.1ms | 23.6 MB | 3/6 | 31781100 |
| dotnet | 34.5ms | 1.0× | 1/6 | 55.9ms | 21.4ms | 28.2 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 155.8ms | 1.2× | 2/6 | 185.8ms | 30.0ms | 101.3 MB | 5/6 | 500 |
| elixir | 691.3ms | 5.5× | 6/6 | 952.1ms | 260.8ms | 565.9 MB | 6/6 | 500 |
| python | 178.8ms | 1.4× | 4/6 | 189.4ms | 10.6ms | 46.8 MB | 1/6 | 500 |
| node | 124.7ms | 1.0× | 1/6 | 142.6ms | 17.9ms | 65.2 MB | 4/6 | 500 |
| ruby | 208.3ms | 1.7× | 5/6 | 249.4ms | 41.1ms | 50.0 MB | 2/6 | 500 |
| dotnet | 170.6ms | 1.4× | 3/6 | 192.0ms | 21.4ms | 50.6 MB | 3/6 | 500 |
