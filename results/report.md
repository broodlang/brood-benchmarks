# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 09:05.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.9ms | 3.5× | 4/6 | 36.9ms | — | 24.1 MB | 3/6 | 0 |
| elixir | 201.8ms | 19.4× | 6/6 | 201.8ms | — | 70.1 MB | 6/6 | 0 |
| python | 10.4ms | 1.0× | 1/6 | 10.4ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.7ms | 1.7× | 2/6 | 17.7ms | — | 46.4 MB | 5/6 | 0 |
| ruby | 40.9ms | 3.9× | 5/6 | 40.9ms | — | 23.5 MB | 2/6 | 0 |
| dotnet | 21.5ms | 2.1× | 3/6 | 21.5ms | — | 25.9 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 274.1ms | 6.6× | 4/6 | 311.0ms | 36.9ms | 27.9 MB | 4/6 | 9227465 |
| elixir | 77.2ms | 1.9× | 2/6 | 279.0ms | 201.8ms | 69.8 MB | 6/6 | 9227465 |
| python | 761.0ms | 18.3× | 6/6 | 771.4ms | 10.4ms | 9.7 MB | 1/6 | 9227465 |
| node | 78.9ms | 1.9× | 3/6 | 96.6ms | 17.7ms | 52.3 MB | 5/6 | 9227465 |
| ruby | 629.3ms | 15.1× | 5/6 | 670.2ms | 40.9ms | 23.5 MB | 2/6 | 9227465 |
| dotnet | 41.6ms | 1.0× | 1/6 | 63.1ms | 21.5ms | 25.9 MB | 3/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.8ms | 7.7× | 4/6 | 139.7ms | 36.9ms | 27.6 MB | 4/6 | 449999985000000 |
| elixir | 64.8ms | 4.9× | 3/6 | 266.6ms | 201.8ms | 69.8 MB | 6/6 | 449999985000000 |
| python | 2.409s | 181.1× | 6/6 | 2.419s | 10.4ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 33.1ms | 2.5× | 2/6 | 50.8ms | 17.7ms | 54.2 MB | 5/6 | 449999985000000 |
| ruby | 601.4ms | 45.2× | 5/6 | 642.3ms | 40.9ms | 23.5 MB | 2/6 | 449999985000000 |
| dotnet | 13.3ms | 1.0× | 1/6 | 34.8ms | 21.5ms | 26.3 MB | 3/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.1ms | 8.8× | 3/6 | 143.0ms | 36.9ms | 24.2 MB | 3/6 | 12499997500000 |
| elixir | 27.4ms | 2.3× | 2/6 | 229.2ms | 201.8ms | 69.7 MB | 5/6 | 12499997500000 |
| python | 109.2ms | 9.1× | 4/6 | 119.6ms | 10.4ms | 10.6 MB | 1/6 | 12499997500000 |
| node | 240.6ms | 20.1× | 6/6 | 258.3ms | 17.7ms | 94.4 MB | 6/6 | 12499997500000 |
| ruby | 238.3ms | 19.9× | 5/6 | 279.2ms | 40.9ms | 23.5 MB | 2/6 | 12499997500000 |
| dotnet | 12.0ms | 1.0× | 1/6 | 33.5ms | 21.5ms | 27.6 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.9ms | 4.8× | 4/6 | 77.8ms | 36.9ms | 27.8 MB | 4/6 | 13848 |
| elixir | 16.8ms | 2.0× | 3/6 | 218.6ms | 201.8ms | 70.5 MB | 6/6 | 13848 |
| python | 123.9ms | 14.6× | 6/6 | 134.3ms | 10.4ms | 9.9 MB | 1/6 | 13848 |
| node | 11.2ms | 1.3× | 2/6 | 28.9ms | 17.7ms | 52.8 MB | 5/6 | 13848 |
| ruby | 118.8ms | 14.0× | 5/6 | 159.7ms | 40.9ms | 23.5 MB | 2/6 | 13848 |
| dotnet | 8.5ms | 1.0× | 1/6 | 30.0ms | 21.5ms | 26.3 MB | 3/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 468.6ms | 10.2× | 4/6 | 505.5ms | 36.9ms | 41.4 MB | 4/6 | 442 |
| elixir | 112.0ms | 2.4× | 2/6 | 313.8ms | 201.8ms | 70.3 MB | 6/6 | 442 |
| python | 2.396s | 52.1× | 6/6 | 2.407s | 10.4ms | 9.8 MB | 1/6 | 442 |
| node | 179.2ms | 3.9× | 3/6 | 196.9ms | 17.7ms | 52.6 MB | 5/6 | 442 |
| ruby | 878.1ms | 19.1× | 5/6 | 919.0ms | 40.9ms | 23.5 MB | 2/6 | 442 |
| dotnet | 46.0ms | 1.0× | 1/6 | 67.5ms | 21.5ms | 26.3 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 222.6ms | 11.4× | 3/6 | 259.5ms | 36.9ms | 27.9 MB | 4/6 | 6129302 |
| elixir | 255.6ms | 13.1× | 4/6 | 457.4ms | 201.8ms | 70.0 MB | 6/6 | 6129302 |
| python | 1.379s | 70.7× | 6/6 | 1.389s | 10.4ms | 10.0 MB | 1/6 | 6129302 |
| node | 21.9ms | 1.1× | 2/6 | 39.6ms | 17.7ms | 54.0 MB | 5/6 | 6129302 |
| ruby | 430.6ms | 22.1× | 5/6 | 471.5ms | 40.9ms | 23.6 MB | 2/6 | 6129302 |
| dotnet | 19.5ms | 1.0× | 1/6 | 41.0ms | 21.5ms | 26.4 MB | 3/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 151.7ms | 8.0× | 4/6 | 188.6ms | 36.9ms | 38.2 MB | 4/6 | 654353666 |
| elixir | 54.8ms | 2.9× | 3/6 | 256.6ms | 201.8ms | 75.7 MB | 6/6 | 654353666 |
| python | 453.2ms | 23.9× | 6/6 | 463.6ms | 10.4ms | 10.4 MB | 1/6 | 654353666 |
| node | 35.1ms | 1.8× | 2/6 | 52.8ms | 17.7ms | 56.7 MB | 5/6 | 654353666 |
| ruby | 294.8ms | 15.5× | 5/6 | 335.7ms | 40.9ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 19.0ms | 1.0× | 1/6 | 40.5ms | 21.5ms | 26.7 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.9ms | 1.0× | 1/6 | 61.8ms | 36.9ms | 34.3 MB | 1/6 | 3388889 |
| elixir | 120.4ms | 4.8× | 6/6 | 322.2ms | 201.8ms | 199.1 MB | 6/6 | 3388889 |
| python | 56.3ms | 2.3× | 3/6 | 66.7ms | 10.4ms | 39.8 MB | 2/6 | 3388889 |
| node | 58.4ms | 2.3× | 4/6 | 76.1ms | 17.7ms | 99.6 MB | 5/6 | 3388889 |
| ruby | 98.9ms | 4.0× | 5/6 | 139.8ms | 40.9ms | 52.1 MB | 3/6 | 3388889 |
| dotnet | 45.0ms | 1.8× | 2/6 | 66.5ms | 21.5ms | 56.8 MB | 4/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 820.8ms | 26.1× | 6/6 | 857.7ms | 36.9ms | 93.9 MB | 6/6 | 374854840 |
| elixir | 170.7ms | 5.4× | 4/6 | 372.5ms | 201.8ms | 71.2 MB | 5/6 | 374854840 |
| python | 185.6ms | 5.9× | 5/6 | 196.0ms | 10.4ms | 9.9 MB | 1/6 | 374854840 |
| node | 31.5ms | 1.0× | 1/6 | 49.2ms | 17.7ms | 54.5 MB | 4/6 | 374854840 |
| ruby | 85.7ms | 2.7× | 3/6 | 126.6ms | 40.9ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 51.0ms | 1.6× | 2/6 | 72.5ms | 21.5ms | 27.4 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 383.7ms | 34.3× | 6/6 | 420.6ms | 36.9ms | 37.9 MB | 4/6 | 1638200 |
| elixir | 11.2ms | 1.0× | 1/6 | 213.0ms | 201.8ms | 70.8 MB | 6/6 | 1638200 |
| python | 106.6ms | 9.5× | 5/6 | 117.0ms | 10.4ms | 10.0 MB | 1/6 | 1638200 |
| node | 35.5ms | 3.2× | 3/6 | 53.2ms | 17.7ms | 60.5 MB | 5/6 | 1638200 |
| ruby | 99.6ms | 8.9× | 4/6 | 140.5ms | 40.9ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 19.4ms | 1.7× | 2/6 | 40.9ms | 21.5ms | 32.3 MB | 3/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 281.4ms | 3.5× | 6/6 | 318.3ms | 36.9ms | 123.6 MB | 5/6 | 46468819 |
| elixir | 99.0ms | 1.2× | 3/6 | 300.8ms | 201.8ms | 156.9 MB | 6/6 | 46468819 |
| python | 199.0ms | 2.5× | 5/6 | 209.4ms | 10.4ms | 26.0 MB | 1/6 | 46468819 |
| node | 108.4ms | 1.4× | 4/6 | 126.1ms | 17.7ms | 69.5 MB | 4/6 | 46468819 |
| ruby | 86.5ms | 1.1× | 2/6 | 127.4ms | 40.9ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 79.8ms | 1.0× | 1/6 | 101.3ms | 21.5ms | 29.7 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 485.3ms | 41.1× | 6/6 | 522.2ms | 36.9ms | 37.7 MB | 4/6 | 724 |
| elixir | 11.8ms | 1.0× | 1/6 | 213.6ms | 201.8ms | 70.4 MB | 6/6 | 724 |
| python | 54.8ms | 4.6× | 4/6 | 65.2ms | 10.4ms | 9.8 MB | 1/6 | 724 |
| node | 13.4ms | 1.1× | 2/6 | 31.1ms | 17.7ms | 55.1 MB | 5/6 | 724 |
| ruby | 136.0ms | 11.5× | 5/6 | 176.9ms | 40.9ms | 23.8 MB | 2/6 | 724 |
| dotnet | 19.4ms | 1.6× | 3/6 | 40.9ms | 21.5ms | 29.3 MB | 3/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.7ms | 8.7× | 4/6 | 230.6ms | 36.9ms | 41.4 MB | 4/6 | 9900000 |
| elixir | 22.2ms | 1.0× | 1/6 | 224.0ms | 201.8ms | 70.5 MB | 6/6 | 9900000 |
| python | 62.5ms | 2.8× | 2/6 | 72.9ms | 10.4ms | 9.8 MB | 1/6 | 9900000 |
| node | 570.5ms | 25.7× | 6/6 | 588.2ms | 17.7ms | 54.7 MB | 5/6 | 9900000 |
| ruby | 123.4ms | 5.6× | 3/6 | 164.3ms | 40.9ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 297.7ms | 13.4× | 5/6 | 319.2ms | 21.5ms | 32.5 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 259.1ms | 34.1× | 5/6 | 296.0ms | 36.9ms | 42.7 MB | 4/6 | 2475000 |
| elixir | 7.6ms | 1.0× | 1/6 | 209.4ms | 201.8ms | 70.4 MB | 6/6 | 2475000 |
| python | 224.9ms | 29.6× | 4/6 | 235.3ms | 10.4ms | 9.9 MB | 1/6 | 2475000 |
| node | 224.2ms | 29.5× | 3/6 | 241.9ms | 17.7ms | 54.6 MB | 5/6 | 2475000 |
| ruby | 123.6ms | 16.3× | 2/6 | 164.5ms | 40.9ms | 30.1 MB | 2/6 | 2475000 |
| dotnet | 708.9ms | 93.3× | 6/6 | 730.4ms | 21.5ms | 32.6 MB | 3/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 47.2ms | 47.2× | 6/6 | 84.1ms | 36.9ms | 27.7 MB | 3/6 | 155553889038886 |
| elixir | 0.0ms | < 1× | 1/6 | 199.9ms | 201.8ms | 70.3 MB | 6/6 | 155553889038886 |
| python | 4.2ms | 4.2× | 2/6 | 14.6ms | 10.4ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 13.4ms | 13.4× | 3/6 | 31.1ms | 17.7ms | 56.3 MB | 5/6 | 155553889038886 |
| ruby | 18.4ms | 18.4× | 4/6 | 59.3ms | 40.9ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 21.5ms | 21.5× | 5/6 | 43.0ms | 21.5ms | 28.0 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 100.7ms | 62.9× | 4/6 | 137.6ms | 36.9ms | 73.4 MB | 4/6 | 6100000 |
| elixir | 1.6ms | 1.0× | 1/6 | 203.4ms | 201.8ms | 76.4 MB | 5/6 | 6100000 |
| python | 554.0ms | 346.3× | 5/6 | 564.4ms | 10.4ms | 28.1 MB | 1/6 | 6100000 |
| node | 53.1ms | 33.2× | 3/6 | 70.8ms | 17.7ms | 55.6 MB | 3/6 | 6100000 |
| ruby | 1.574s | 983.6× | 6/6 | 1.615s | 40.9ms | 137.5 MB | 6/6 | 6100000 |
| dotnet | 18.8ms | 11.8× | 2/6 | 40.3ms | 21.5ms | 31.0 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 394.4ms | 11.4× | 4/6 | 431.3ms | 36.9ms | 31.4 MB | 4/6 | 31781100 |
| elixir | 60.7ms | 1.8× | 2/6 | 262.5ms | 201.8ms | 72.3 MB | 5/6 | 31781100 |
| python | 687.7ms | 19.9× | 6/6 | 698.1ms | 10.4ms | 22.3 MB | 1/6 | 31781100 |
| node | 110.5ms | 3.2× | 3/6 | 128.2ms | 17.7ms | 186.8 MB | 6/6 | 31781100 |
| ruby | 423.1ms | 12.3× | 5/6 | 464.0ms | 40.9ms | 23.7 MB | 2/6 | 31781100 |
| dotnet | 34.5ms | 1.0× | 1/6 | 56.0ms | 21.5ms | 28.1 MB | 3/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.3ms | 1.1× | 2/6 | 181.2ms | 36.9ms | 129.9 MB | 5/6 | 500 |
| elixir | 567.4ms | 4.3× | 6/6 | 769.2ms | 201.8ms | 484.2 MB | 6/6 | 500 |
| python | 180.7ms | 1.4× | 3/6 | 191.1ms | 10.4ms | 44.3 MB | 1/6 | 500 |
| node | 130.8ms | 1.0× | 1/6 | 148.5ms | 17.7ms | 69.3 MB | 4/6 | 500 |
| ruby | 236.9ms | 1.8× | 5/6 | 277.8ms | 40.9ms | 49.9 MB | 3/6 | 500 |
| dotnet | 181.1ms | 1.4× | 4/6 | 202.6ms | 21.5ms | 48.0 MB | 2/6 | 500 |
