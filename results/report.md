# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-21 16:20.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28).
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.7ms | 2.4× | 4/7 | 26.7ms | — | 18.4 MB | 2/7 | 0 |
| elixir | 214.3ms | 19.3× | 6/7 | 214.3ms | — | 69.7 MB | 6/7 | 0 |
| python | 11.1ms | 1.0× | 1/7 | 11.1ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.5ms | 1.7× | 2/7 | 18.5ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 43.3ms | 3.9× | 5/7 | 43.3ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.8ms | 2.1× | 3/7 | 22.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 238.6ms | 5.4× | 4/7 | 265.3ms | 26.7ms | 22.0 MB | 2/7 | 9227465 |
| elixir | 83.8ms | 1.9× | 3/7 | 298.1ms | 214.3ms | 69.7 MB | 6/7 | 9227465 |
| python | 776.2ms | 17.6× | 7/7 | 787.3ms | 11.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 80.4ms | 1.8× | 2/7 | 98.9ms | 18.5ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 654.4ms | 14.9× | 6/7 | 697.7ms | 43.3ms | 23.5 MB | 3/7 | 9227465 |
| dotnet | 44.0ms | 1.0× | 1/7 | 66.8ms | 22.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.5ms | 2.9× | 3/7 | 66.2ms | 26.7ms | 21.6 MB | 2/7 | 449999985000000 |
| elixir | 68.2ms | 5.0× | 4/7 | 282.5ms | 214.3ms | 69.8 MB | 6/7 | 449999985000000 |
| python | 2.637s | 193.9× | 7/7 | 2.648s | 11.1ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 32.8ms | 2.4× | 2/7 | 51.3ms | 18.5ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 626.6ms | 46.1× | 6/7 | 669.9ms | 43.3ms | 23.5 MB | 3/7 | 449999985000000 |
| dotnet | 13.6ms | 1.0× | 1/7 | 36.4ms | 22.8ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 3.5ms | 1.0× | 1/7 | 30.2ms | 26.7ms | 18.4 MB | 2/7 | 12499997500000 |
| elixir | 29.6ms | 8.5× | 3/7 | 243.9ms | 214.3ms | 69.6 MB | 5/7 | 12499997500000 |
| python | 113.0ms | 32.3× | 4/7 | 124.1ms | 11.1ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 236.9ms | 67.7× | 5/7 | 255.4ms | 18.5ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 237.7ms | 67.9× | 6/7 | 281.0ms | 43.3ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 12.8ms | 3.7× | 2/7 | 35.6ms | 22.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.6ms | 4.8× | 4/7 | 68.3ms | 26.7ms | 21.7 MB | 2/7 | 13848 |
| elixir | 17.1ms | 2.0× | 3/7 | 231.4ms | 214.3ms | 69.8 MB | 6/7 | 13848 |
| python | 127.8ms | 14.9× | 6/7 | 138.9ms | 11.1ms | 9.9 MB | 1/7 | 13848 |
| node | 11.9ms | 1.4× | 2/7 | 30.4ms | 18.5ms | 49.1 MB | 5/7 | 13848 |
| ruby | 121.9ms | 14.2× | 5/7 | 165.2ms | 43.3ms | 23.5 MB | 3/7 | 13848 |
| dotnet | 8.6ms | 1.0× | 1/7 | 31.4ms | 22.8ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 84.3ms | 1.7× | 2/7 | 111.0ms | 26.7ms | 21.6 MB | 2/7 | 442 |
| elixir | 108.3ms | 2.2× | 3/7 | 322.6ms | 214.3ms | 69.7 MB | 6/7 | 442 |
| python | 2.486s | 51.5× | 7/7 | 2.497s | 11.1ms | 9.8 MB | 1/7 | 442 |
| node | 187.7ms | 3.9× | 4/7 | 206.2ms | 18.5ms | 48.9 MB | 5/7 | 442 |
| ruby | 925.8ms | 19.2× | 6/7 | 969.1ms | 43.3ms | 23.5 MB | 3/7 | 442 |
| dotnet | 48.3ms | 1.0× | 1/7 | 71.1ms | 22.8ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 268.1ms | 13.0× | 3/7 | 294.8ms | 26.7ms | 21.8 MB | 2/7 | 6129302 |
| elixir | 344.3ms | 16.7× | 4/7 | 558.6ms | 214.3ms | 70.0 MB | 6/7 | 6129302 |
| python | 1.412s | 68.5× | 7/7 | 1.423s | 11.1ms | 10.1 MB | 1/7 | 6129302 |
| node | 23.0ms | 1.1× | 2/7 | 41.5ms | 18.5ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 464.1ms | 22.5× | 6/7 | 507.4ms | 43.3ms | 23.6 MB | 3/7 | 6129302 |
| dotnet | 20.6ms | 1.0× | 1/7 | 43.4ms | 22.8ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 124.1ms | 30.3× | 4/7 | 150.8ms | 26.7ms | 37.5 MB | 4/7 | 654353666 |
| elixir | 107.4ms | 26.2× | 3/7 | 321.7ms | 214.3ms | 75.6 MB | 6/7 | 654353666 |
| python | 492.2ms | 120.0× | 6/7 | 503.3ms | 11.1ms | 10.4 MB | 1/7 | 654353666 |
| node | 27.0ms | 6.6× | 2/7 | 45.5ms | 18.5ms | 52.8 MB | 5/7 | 654353666 |
| ruby | 304.4ms | 74.2× | 5/7 | 347.7ms | 43.3ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.1ms | 1.0× | 1/7 | 26.9ms | 22.8ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 18.1ms | 1.0× | 1/7 | 44.8ms | 26.7ms | 28.5 MB | 1/7 | 3388889 |
| elixir | 169.0ms | 9.3× | 6/7 | 383.3ms | 214.3ms | 199.8 MB | 7/7 | 3388889 |
| python | 45.9ms | 2.5× | 3/7 | 57.0ms | 11.1ms | 39.8 MB | 2/7 | 3388889 |
| node | 64.6ms | 3.6× | 4/7 | 83.1ms | 18.5ms | 95.8 MB | 5/7 | 3388889 |
| ruby | 91.1ms | 5.0× | 5/7 | 134.4ms | 43.3ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 32.7ms | 1.8× | 2/7 | 55.5ms | 22.8ms | 56.9 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 466.8ms | 13.8× | 6/7 | 493.5ms | 26.7ms | 90.6 MB | 6/7 | 374854840 |
| elixir | 229.7ms | 6.8× | 5/7 | 444.0ms | 214.3ms | 70.6 MB | 5/7 | 374854840 |
| python | 178.3ms | 5.3× | 4/7 | 189.4ms | 11.1ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.9ms | 1.0× | 1/7 | 52.4ms | 18.5ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 74.1ms | 2.2× | 3/7 | 117.4ms | 43.3ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 38.7ms | 1.1× | 2/7 | 61.5ms | 22.8ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 126.4ms | 8.3× | 6/7 | 153.1ms | 26.7ms | 34.5 MB | 4/7 | 1638200 |
| elixir | 56.4ms | 3.7× | 3/7 | 270.7ms | 214.3ms | 70.2 MB | 6/7 | 1638200 |
| python | 99.5ms | 6.5× | 4/7 | 110.6ms | 11.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 24.2ms | 1.6× | 2/7 | 42.7ms | 18.5ms | 56.5 MB | 5/7 | 1638200 |
| ruby | 100.5ms | 6.6× | 5/7 | 143.8ms | 43.3ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 15.3ms | 1.0× | 1/7 | 38.1ms | 22.8ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 220.3ms | 3.3× | 6/7 | 247.0ms | 26.7ms | 129.9 MB | 5/7 | 46468819 |
| elixir | 183.5ms | 2.7× | 4/7 | 397.8ms | 214.3ms | 157.1 MB | 7/7 | 46468819 |
| python | 197.6ms | 2.9× | 5/7 | 208.7ms | 11.1ms | 26.0 MB | 1/7 | 46468819 |
| node | 111.6ms | 1.7× | 3/7 | 130.1ms | 18.5ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 74.8ms | 1.1× | 2/7 | 118.1ms | 43.3ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 67.5ms | 1.0× | 1/7 | 90.3ms | 22.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 140.2ms | 11.8× | 6/7 | 166.9ms | 26.7ms | 36.0 MB | 4/7 | 724 |
| elixir | 72.0ms | 6.1× | 4/7 | 286.3ms | 214.3ms | 70.4 MB | 6/7 | 724 |
| python | 55.3ms | 4.6× | 3/7 | 66.4ms | 11.1ms | 9.7 MB | 1/7 | 724 |
| node | 11.9ms | 1.0× | 1/7 | 30.4ms | 18.5ms | 51.2 MB | 5/7 | 724 |
| ruby | 132.2ms | 11.1× | 5/7 | 175.5ms | 43.3ms | 23.8 MB | 2/7 | 724 |
| dotnet | 20.1ms | 1.7× | 2/7 | 42.9ms | 22.8ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.9ms | 1.1× | 2/7 | 83.6ms | 26.7ms | 19.1 MB | 2/7 | 9900000 |
| elixir | 78.0ms | 1.6× | 3/7 | 292.3ms | 214.3ms | 70.1 MB | 6/7 | 9900000 |
| python | 50.0ms | 1.0× | 1/7 | 61.1ms | 11.1ms | 9.8 MB | 1/7 | 9900000 |
| node | 601.0ms | 12.0× | 6/7 | 619.5ms | 18.5ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 113.8ms | 2.3× | 4/7 | 157.1ms | 43.3ms | 26.1 MB | 3/7 | 9900000 |
| dotnet | 300.5ms | 6.0× | 5/7 | 323.3ms | 22.8ms | 32.6 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 134.6ms | 2.8× | 3/7 | 161.3ms | 26.7ms | 21.6 MB | 2/7 | 2475000 |
| elixir | 48.7ms | 1.0× | 1/7 | 263.0ms | 214.3ms | 69.9 MB | 6/7 | 2475000 |
| python | 226.3ms | 4.6× | 5/7 | 237.4ms | 11.1ms | 9.9 MB | 1/7 | 2475000 |
| node | 222.9ms | 4.6× | 4/7 | 241.4ms | 18.5ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 121.3ms | 2.5× | 2/7 | 164.6ms | 43.3ms | 30.3 MB | 3/7 | 2475000 |
| dotnet | 727.3ms | 14.9× | 6/7 | 750.1ms | 22.8ms | 32.5 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 45.2ms | 10.0× | 6/7 | 71.9ms | 26.7ms | 21.6 MB | 2/7 | 155553889038886 |
| elixir | 26.7ms | 5.9× | 5/7 | 241.0ms | 214.3ms | 70.9 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 1.0× | 1/7 | 15.6ms | 11.1ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.8ms | 2.4× | 4/7 | 29.3ms | 18.5ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 8.2ms | 1.8× | 3/7 | 51.5ms | 43.3ms | 24.0 MB | 3/7 | 155553889038886 |
| dotnet | 7.3ms | 1.6× | 2/7 | 30.1ms | 22.8ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 160.0ms | 160.0× | 5/7 | 186.7ms | 26.7ms | 73.0 MB | 4/7 | 6100000 |
| elixir | 16.8ms | 16.8× | 2/7 | 231.1ms | 214.3ms | 77.8 MB | 5/7 | 6100000 |
| python | 575.9ms | 575.9× | 6/7 | 587.0ms | 11.1ms | 28.1 MB | 1/7 | 6100000 |
| node | 56.2ms | 56.2× | 4/7 | 74.7ms | 18.5ms | 52.0 MB | 3/7 | 6100000 |
| ruby | 1.605s | 1605.5× | 7/7 | 1.649s | 43.3ms | 136.7 MB | 7/7 | 6100000 |
| dotnet | 17.5ms | 17.5× | 3/7 | 40.3ms | 22.8ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 432.2ms | 432.2× | 5/7 | 458.9ms | 26.7ms | 26.7 MB | 3/7 | 31781100 |
| elixir | 103.0ms | 103.0× | 3/7 | 317.3ms | 214.3ms | 71.9 MB | 5/7 | 31781100 |
| python | 737.0ms | 737.0× | 7/7 | 748.1ms | 11.1ms | 22.3 MB | 1/7 | 31781100 |
| node | 131.1ms | 131.1× | 4/7 | 149.6ms | 18.5ms | 182.7 MB | 7/7 | 31781100 |
| ruby | 510.9ms | 510.9× | 6/7 | 554.2ms | 43.3ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 37.0ms | 37.0× | 2/7 | 59.8ms | 22.8ms | 28.0 MB | 4/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 178.9ms | 1.4× | 4/7 | 205.6ms | 26.7ms | 115.3 MB | 5/7 | 500 |
| elixir | 668.8ms | 5.2× | 7/7 | 883.1ms | 214.3ms | 484.6 MB | 7/7 | 500 |
| python | 178.0ms | 1.4× | 3/7 | 189.1ms | 11.1ms | 44.2 MB | 1/7 | 500 |
| node | 129.4ms | 1.0× | 1/7 | 147.9ms | 18.5ms | 64.9 MB | 4/7 | 500 |
| ruby | 213.4ms | 1.6× | 5/7 | 256.7ms | 43.3ms | 50.2 MB | 3/7 | 500 |
| dotnet | 155.9ms | 1.2× | 2/7 | 178.7ms | 22.8ms | 48.3 MB | 2/7 | 500 |
