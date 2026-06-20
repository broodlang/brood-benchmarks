# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-20 08:25.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.3ms | 2.4× | 4/7 | 26.3ms | — | 18.3 MB | 2/7 | 0 |
| elixir | 203.7ms | 18.7× | 6/7 | 203.7ms | — | 70.2 MB | 6/7 | 0 |
| python | 10.9ms | 1.0× | 1/7 | 10.9ms | — | 9.7 MB | 1/7 | 0 |
| node | 19.3ms | 1.8× | 2/7 | 19.3ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 43.8ms | 4.0× | 5/7 | 43.8ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.7ms | 2.1× | 3/7 | 22.7ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 277.5ms | 5.9× | 4/7 | 303.8ms | 26.3ms | 21.7 MB | 2/7 | 9227465 |
| elixir | 80.7ms | 1.7× | 2/7 | 284.4ms | 203.7ms | 69.6 MB | 6/7 | 9227465 |
| python | 798.7ms | 16.9× | 7/7 | 809.6ms | 10.9ms | 9.8 MB | 1/7 | 9227465 |
| node | 86.3ms | 1.8× | 3/7 | 105.6ms | 19.3ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 722.8ms | 15.3× | 6/7 | 766.6ms | 43.8ms | 23.5 MB | 3/7 | 9227465 |
| dotnet | 47.2ms | 1.0× | 1/7 | 69.9ms | 22.7ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.2ms | 3.6× | 3/7 | 70.5ms | 26.3ms | 21.7 MB | 2/7 | 449999985000000 |
| elixir | 96.2ms | 7.9× | 4/7 | 299.9ms | 203.7ms | 70.4 MB | 6/7 | 449999985000000 |
| python | 2.556s | 209.5× | 7/7 | 2.567s | 10.9ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 33.0ms | 2.7× | 2/7 | 52.3ms | 19.3ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 608.8ms | 49.9× | 6/7 | 652.6ms | 43.8ms | 23.6 MB | 3/7 | 449999985000000 |
| dotnet | 12.2ms | 1.0× | 1/7 | 34.9ms | 22.7ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 109.3ms | 9.3× | 3/7 | 135.6ms | 26.3ms | 18.2 MB | 2/7 | 12499997500000 |
| elixir | 29.2ms | 2.5× | 2/7 | 232.9ms | 203.7ms | 69.8 MB | 5/7 | 12499997500000 |
| python | 117.7ms | 10.1× | 4/7 | 128.6ms | 10.9ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 231.7ms | 19.8× | 5/7 | 251.0ms | 19.3ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 244.5ms | 20.9× | 6/7 | 288.3ms | 43.8ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 11.7ms | 1.0× | 1/7 | 34.4ms | 22.7ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.1ms | 3.9× | 4/7 | 64.4ms | 26.3ms | 21.8 MB | 2/7 | 13848 |
| elixir | 16.6ms | 1.7× | 3/7 | 220.3ms | 203.7ms | 69.7 MB | 6/7 | 13848 |
| python | 127.0ms | 13.1× | 6/7 | 137.9ms | 10.9ms | 9.9 MB | 1/7 | 13848 |
| node | 10.3ms | 1.1× | 2/7 | 29.6ms | 19.3ms | 49.1 MB | 5/7 | 13848 |
| ruby | 125.0ms | 12.9× | 5/7 | 168.8ms | 43.8ms | 23.5 MB | 3/7 | 13848 |
| dotnet | 9.7ms | 1.0× | 1/7 | 32.4ms | 22.7ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 322.7ms | 6.8× | 4/7 | 349.0ms | 26.3ms | 35.7 MB | 4/7 | 442 |
| elixir | 112.0ms | 2.4× | 2/7 | 315.7ms | 203.7ms | 69.7 MB | 6/7 | 442 |
| python | 2.514s | 53.3× | 7/7 | 2.525s | 10.9ms | 9.8 MB | 1/7 | 442 |
| node | 181.9ms | 3.9× | 3/7 | 201.2ms | 19.3ms | 48.9 MB | 5/7 | 442 |
| ruby | 896.9ms | 19.0× | 6/7 | 940.7ms | 43.8ms | 23.5 MB | 2/7 | 442 |
| dotnet | 47.2ms | 1.0× | 1/7 | 69.9ms | 22.7ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 204.2ms | 10.2× | 3/7 | 230.5ms | 26.3ms | 21.6 MB | 2/7 | 6129302 |
| elixir | 261.7ms | 13.1× | 4/7 | 465.4ms | 203.7ms | 70.1 MB | 6/7 | 6129302 |
| python | 1.492s | 74.6× | 7/7 | 1.502s | 10.9ms | 10.1 MB | 1/7 | 6129302 |
| node | 22.3ms | 1.1× | 2/7 | 41.6ms | 19.3ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 445.6ms | 22.3× | 6/7 | 489.4ms | 43.8ms | 23.6 MB | 3/7 | 6129302 |
| dotnet | 20.0ms | 1.0× | 1/7 | 42.7ms | 22.7ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.7ms | 20.1× | 4/7 | 123.0ms | 26.3ms | 34.4 MB | 4/7 | 654353666 |
| elixir | 62.8ms | 13.1× | 3/7 | 266.5ms | 203.7ms | 79.4 MB | 6/7 | 654353666 |
| python | 487.0ms | 101.5× | 6/7 | 497.9ms | 10.9ms | 10.4 MB | 1/7 | 654353666 |
| node | 20.8ms | 4.3× | 2/7 | 40.1ms | 19.3ms | 52.7 MB | 5/7 | 654353666 |
| ruby | 303.4ms | 63.2× | 5/7 | 347.2ms | 43.8ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.8ms | 1.0× | 1/7 | 27.5ms | 22.7ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 12.9ms | 1.0× | 1/7 | 39.2ms | 26.3ms | 28.5 MB | 1/7 | 3388889 |
| elixir | 123.3ms | 9.6× | 6/7 | 327.0ms | 203.7ms | 199.2 MB | 7/7 | 3388889 |
| python | 44.7ms | 3.5× | 3/7 | 55.6ms | 10.9ms | 39.8 MB | 2/7 | 3388889 |
| node | 61.3ms | 4.8× | 4/7 | 80.6ms | 19.3ms | 95.9 MB | 5/7 | 3388889 |
| ruby | 90.5ms | 7.0× | 5/7 | 134.3ms | 43.8ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 33.2ms | 2.6× | 2/7 | 55.9ms | 22.7ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 437.0ms | 13.0× | 6/7 | 463.3ms | 26.3ms | 91.0 MB | 6/7 | 374854840 |
| elixir | 175.7ms | 5.2× | 4/7 | 379.4ms | 203.7ms | 70.5 MB | 5/7 | 374854840 |
| python | 179.6ms | 5.4× | 5/7 | 190.5ms | 10.9ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.5ms | 1.0× | 1/7 | 52.8ms | 19.3ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 81.0ms | 2.4× | 3/7 | 124.8ms | 43.8ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 40.0ms | 1.2× | 2/7 | 62.7ms | 22.7ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 102.6ms | 9.2× | 5/7 | 128.9ms | 26.3ms | 36.2 MB | 4/7 | 1638200 |
| elixir | 11.2ms | 1.0× | 1/7 | 214.9ms | 203.7ms | 70.4 MB | 6/7 | 1638200 |
| python | 100.3ms | 9.0× | 4/7 | 111.2ms | 10.9ms | 10.0 MB | 1/7 | 1638200 |
| node | 23.2ms | 2.1× | 3/7 | 42.5ms | 19.3ms | 56.6 MB | 5/7 | 1638200 |
| ruby | 105.4ms | 9.4× | 6/7 | 149.2ms | 43.8ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 15.1ms | 1.3× | 2/7 | 37.8ms | 22.7ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.2ms | 2.6× | 5/7 | 198.5ms | 26.3ms | 130.0 MB | 5/7 | 46468819 |
| elixir | 117.3ms | 1.7× | 4/7 | 321.0ms | 203.7ms | 156.8 MB | 7/7 | 46468819 |
| python | 204.3ms | 3.0× | 6/7 | 215.2ms | 10.9ms | 26.0 MB | 1/7 | 46468819 |
| node | 115.0ms | 1.7× | 3/7 | 134.3ms | 19.3ms | 65.5 MB | 4/7 | 46468819 |
| ruby | 76.7ms | 1.1× | 2/7 | 120.5ms | 43.8ms | 29.2 MB | 2/7 | 46468819 |
| dotnet | 67.2ms | 1.0× | 1/7 | 89.9ms | 22.7ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 138.3ms | 12.6× | 6/7 | 164.6ms | 26.3ms | 32.0 MB | 4/7 | 724 |
| elixir | 15.4ms | 1.4× | 2/7 | 219.1ms | 203.7ms | 69.7 MB | 6/7 | 724 |
| python | 56.7ms | 5.2× | 4/7 | 67.6ms | 10.9ms | 9.8 MB | 1/7 | 724 |
| node | 11.0ms | 1.0× | 1/7 | 30.3ms | 19.3ms | 51.2 MB | 5/7 | 724 |
| ruby | 134.1ms | 12.2× | 5/7 | 177.9ms | 43.8ms | 23.8 MB | 2/7 | 724 |
| dotnet | 22.6ms | 2.1× | 3/7 | 45.3ms | 22.7ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 199.0ms | 8.0× | 4/7 | 225.3ms | 26.3ms | 33.8 MB | 4/7 | 9900000 |
| elixir | 24.8ms | 1.0× | 1/7 | 228.5ms | 203.7ms | 69.8 MB | 6/7 | 9900000 |
| python | 52.1ms | 2.1× | 2/7 | 63.0ms | 10.9ms | 9.8 MB | 1/7 | 9900000 |
| node | 621.6ms | 25.1× | 6/7 | 640.9ms | 19.3ms | 50.8 MB | 5/7 | 9900000 |
| ruby | 121.2ms | 4.9× | 3/7 | 165.0ms | 43.8ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 318.9ms | 12.9× | 5/7 | 341.6ms | 22.7ms | 32.4 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 271.4ms | 26.1× | 5/7 | 297.7ms | 26.3ms | 34.1 MB | 4/7 | 2475000 |
| elixir | 10.4ms | 1.0× | 1/7 | 214.1ms | 203.7ms | 69.8 MB | 6/7 | 2475000 |
| python | 237.7ms | 22.9× | 4/7 | 248.6ms | 10.9ms | 9.9 MB | 1/7 | 2475000 |
| node | 226.3ms | 21.8× | 3/7 | 245.6ms | 19.3ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 119.4ms | 11.5× | 2/7 | 163.2ms | 43.8ms | 30.1 MB | 2/7 | 2475000 |
| dotnet | 732.1ms | 70.4× | 6/7 | 754.8ms | 22.7ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.5ms | 8.6× | 6/7 | 64.8ms | 26.3ms | 21.7 MB | 2/7 | 155553889038886 |
| elixir | 9.1ms | 2.0× | 4/7 | 212.8ms | 203.7ms | 70.2 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 1.0× | 1/7 | 15.4ms | 10.9ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.1ms | 2.2× | 5/7 | 29.4ms | 19.3ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 8.2ms | 1.8× | 2/7 | 52.0ms | 43.8ms | 24.0 MB | 3/7 | 155553889038886 |
| dotnet | 8.5ms | 1.9× | 3/7 | 31.2ms | 22.7ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 124.3ms | 124.3× | 5/7 | 150.6ms | 26.3ms | 72.5 MB | 4/7 | 6100000 |
| elixir | 5.4ms | 5.4× | 2/7 | 209.1ms | 203.7ms | 76.7 MB | 5/7 | 6100000 |
| python | 669.2ms | 669.2× | 6/7 | 680.1ms | 10.9ms | 28.1 MB | 1/7 | 6100000 |
| node | 67.7ms | 67.7× | 4/7 | 87.0ms | 19.3ms | 51.9 MB | 3/7 | 6100000 |
| ruby | 1.616s | 1615.9× | 7/7 | 1.660s | 43.8ms | 137.3 MB | 7/7 | 6100000 |
| dotnet | 17.1ms | 17.1× | 3/7 | 39.8ms | 22.7ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 383.3ms | 383.3× | 5/7 | 409.6ms | 26.3ms | 26.8 MB | 3/7 | 31781100 |
| elixir | 68.6ms | 68.6× | 3/7 | 272.3ms | 203.7ms | 72.6 MB | 5/7 | 31781100 |
| python | 750.5ms | 750.5× | 7/7 | 761.4ms | 10.9ms | 22.2 MB | 1/7 | 31781100 |
| node | 129.4ms | 129.4× | 4/7 | 148.7ms | 19.3ms | 182.7 MB | 7/7 | 31781100 |
| ruby | 503.3ms | 503.3× | 6/7 | 547.1ms | 43.8ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 37.5ms | 37.5× | 2/7 | 60.2ms | 22.7ms | 28.3 MB | 4/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.0ms | 1.2× | 2/7 | 176.3ms | 26.3ms | 115.9 MB | 5/7 | 500 |
| elixir | 606.3ms | 4.7× | 7/7 | 810.0ms | 203.7ms | 468.6 MB | 7/7 | 500 |
| python | 182.4ms | 1.4× | 4/7 | 193.3ms | 10.9ms | 43.4 MB | 1/7 | 500 |
| node | 130.1ms | 1.0× | 1/7 | 149.4ms | 19.3ms | 65.4 MB | 4/7 | 500 |
| ruby | 221.7ms | 1.7× | 5/7 | 265.5ms | 43.8ms | 50.3 MB | 3/7 | 500 |
| dotnet | 157.5ms | 1.2× | 3/7 | 180.2ms | 22.7ms | 49.9 MB | 2/7 | 500 |
