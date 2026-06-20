# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-20 07:15.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 25.4ms | 2.3× | 4/7 | 25.4ms | — | 18.2 MB | 2/7 | 0 |
| elixir | 202.3ms | 18.2× | 6/7 | 202.3ms | — | 69.7 MB | 6/7 | 0 |
| python | 11.1ms | 1.0× | 1/7 | 11.1ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.5ms | 1.7× | 2/7 | 18.5ms | — | 43.1 MB | 5/7 | 0 |
| ruby | 43.3ms | 3.9× | 5/7 | 43.3ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 22.8ms | 2.1× | 3/7 | 22.8ms | — | 25.8 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 280.9ms | 6.4× | 4/7 | 306.3ms | 25.4ms | 21.8 MB | 2/7 | 9227465 |
| elixir | 80.6ms | 1.8× | 3/7 | 282.9ms | 202.3ms | 69.7 MB | 6/7 | 9227465 |
| python | 776.2ms | 17.6× | 7/7 | 787.3ms | 11.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 80.4ms | 1.8× | 2/7 | 98.9ms | 18.5ms | 48.6 MB | 5/7 | 9227465 |
| ruby | 654.4ms | 14.9× | 6/7 | 697.7ms | 43.3ms | 23.5 MB | 3/7 | 9227465 |
| dotnet | 44.0ms | 1.0× | 1/7 | 66.8ms | 22.8ms | 25.9 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.9ms | 2.9× | 3/7 | 64.3ms | 25.4ms | 21.7 MB | 2/7 | 449999985000000 |
| elixir | 69.9ms | 5.1× | 4/7 | 272.2ms | 202.3ms | 69.7 MB | 6/7 | 449999985000000 |
| python | 2.637s | 193.9× | 7/7 | 2.648s | 11.1ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 32.8ms | 2.4× | 2/7 | 51.3ms | 18.5ms | 50.5 MB | 5/7 | 449999985000000 |
| ruby | 626.6ms | 46.1× | 6/7 | 669.9ms | 43.3ms | 23.5 MB | 3/7 | 449999985000000 |
| dotnet | 13.6ms | 1.0× | 1/7 | 36.4ms | 22.8ms | 26.2 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.7ms | 8.6× | 3/7 | 136.1ms | 25.4ms | 18.2 MB | 2/7 | 12499997500000 |
| elixir | 29.5ms | 2.3× | 2/7 | 231.8ms | 202.3ms | 69.7 MB | 5/7 | 12499997500000 |
| python | 113.0ms | 8.8× | 4/7 | 124.1ms | 11.1ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 236.9ms | 18.5× | 5/7 | 255.4ms | 18.5ms | 90.6 MB | 6/7 | 12499997500000 |
| ruby | 237.7ms | 18.6× | 6/7 | 281.0ms | 43.3ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 12.8ms | 1.0× | 1/7 | 35.6ms | 22.8ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.9ms | 4.8× | 4/7 | 66.3ms | 25.4ms | 21.7 MB | 2/7 | 13848 |
| elixir | 17.8ms | 2.1× | 3/7 | 220.1ms | 202.3ms | 69.7 MB | 6/7 | 13848 |
| python | 127.8ms | 14.9× | 6/7 | 138.9ms | 11.1ms | 9.9 MB | 1/7 | 13848 |
| node | 11.9ms | 1.4× | 2/7 | 30.4ms | 18.5ms | 49.1 MB | 5/7 | 13848 |
| ruby | 121.9ms | 14.2× | 5/7 | 165.2ms | 43.3ms | 23.5 MB | 3/7 | 13848 |
| dotnet | 8.6ms | 1.0× | 1/7 | 31.4ms | 22.8ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 321.1ms | 6.6× | 4/7 | 346.5ms | 25.4ms | 35.6 MB | 4/7 | 442 |
| elixir | 105.7ms | 2.2× | 2/7 | 308.0ms | 202.3ms | 69.7 MB | 6/7 | 442 |
| python | 2.486s | 51.5× | 7/7 | 2.497s | 11.1ms | 9.8 MB | 1/7 | 442 |
| node | 187.7ms | 3.9× | 3/7 | 206.2ms | 18.5ms | 48.9 MB | 5/7 | 442 |
| ruby | 925.8ms | 19.2× | 6/7 | 969.1ms | 43.3ms | 23.5 MB | 2/7 | 442 |
| dotnet | 48.3ms | 1.0× | 1/7 | 71.1ms | 22.8ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 223.6ms | 10.9× | 3/7 | 249.0ms | 25.4ms | 21.8 MB | 2/7 | 6129302 |
| elixir | 266.2ms | 12.9× | 4/7 | 468.5ms | 202.3ms | 70.2 MB | 6/7 | 6129302 |
| python | 1.412s | 68.5× | 7/7 | 1.423s | 11.1ms | 10.1 MB | 1/7 | 6129302 |
| node | 23.0ms | 1.1× | 2/7 | 41.5ms | 18.5ms | 49.8 MB | 5/7 | 6129302 |
| ruby | 464.1ms | 22.5× | 6/7 | 507.4ms | 43.3ms | 23.6 MB | 3/7 | 6129302 |
| dotnet | 20.6ms | 1.0× | 1/7 | 43.4ms | 22.8ms | 26.2 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 97.1ms | 23.7× | 4/7 | 122.5ms | 25.4ms | 34.4 MB | 4/7 | 654353666 |
| elixir | 65.1ms | 15.9× | 3/7 | 267.4ms | 202.3ms | 75.2 MB | 6/7 | 654353666 |
| python | 492.2ms | 120.0× | 6/7 | 503.3ms | 11.1ms | 10.4 MB | 1/7 | 654353666 |
| node | 27.0ms | 6.6× | 2/7 | 45.5ms | 18.5ms | 52.8 MB | 5/7 | 654353666 |
| ruby | 304.4ms | 74.2× | 5/7 | 347.7ms | 43.3ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.1ms | 1.0× | 1/7 | 26.9ms | 22.8ms | 26.8 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 13.3ms | 1.0× | 1/7 | 38.7ms | 25.4ms | 28.4 MB | 1/7 | 3388889 |
| elixir | 127.7ms | 9.6× | 6/7 | 330.0ms | 202.3ms | 199.1 MB | 7/7 | 3388889 |
| python | 45.9ms | 3.5× | 3/7 | 57.0ms | 11.1ms | 39.8 MB | 2/7 | 3388889 |
| node | 64.6ms | 4.9× | 4/7 | 83.1ms | 18.5ms | 95.8 MB | 5/7 | 3388889 |
| ruby | 91.1ms | 6.8× | 5/7 | 134.4ms | 43.3ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 32.7ms | 2.5× | 2/7 | 55.5ms | 22.8ms | 56.9 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 429.9ms | 12.7× | 6/7 | 455.3ms | 25.4ms | 91.0 MB | 6/7 | 374854840 |
| elixir | 176.2ms | 5.2× | 4/7 | 378.5ms | 202.3ms | 70.6 MB | 5/7 | 374854840 |
| python | 178.3ms | 5.3× | 5/7 | 189.4ms | 11.1ms | 9.9 MB | 1/7 | 374854840 |
| node | 33.9ms | 1.0× | 1/7 | 52.4ms | 18.5ms | 50.6 MB | 4/7 | 374854840 |
| ruby | 74.1ms | 2.2× | 3/7 | 117.4ms | 43.3ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 38.7ms | 1.1× | 2/7 | 61.5ms | 22.8ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.2ms | 9.1× | 6/7 | 128.6ms | 25.4ms | 36.3 MB | 4/7 | 1638200 |
| elixir | 11.4ms | 1.0× | 1/7 | 213.7ms | 202.3ms | 70.2 MB | 6/7 | 1638200 |
| python | 99.5ms | 8.7× | 4/7 | 110.6ms | 11.1ms | 10.1 MB | 1/7 | 1638200 |
| node | 24.2ms | 2.1× | 3/7 | 42.7ms | 18.5ms | 56.5 MB | 5/7 | 1638200 |
| ruby | 100.5ms | 8.8× | 5/7 | 143.8ms | 43.3ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 15.3ms | 1.3× | 2/7 | 38.1ms | 22.8ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 172.7ms | 2.6× | 5/7 | 198.1ms | 25.4ms | 130.0 MB | 5/7 | 46468819 |
| elixir | 118.3ms | 1.8× | 4/7 | 320.6ms | 202.3ms | 156.7 MB | 7/7 | 46468819 |
| python | 197.6ms | 2.9× | 6/7 | 208.7ms | 11.1ms | 26.0 MB | 1/7 | 46468819 |
| node | 111.6ms | 1.7× | 3/7 | 130.1ms | 18.5ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 74.8ms | 1.1× | 2/7 | 118.1ms | 43.3ms | 29.1 MB | 2/7 | 46468819 |
| dotnet | 67.5ms | 1.0× | 1/7 | 90.3ms | 22.8ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 139.5ms | 20.5× | 6/7 | 164.9ms | 25.4ms | 32.1 MB | 4/7 | 724 |
| elixir | 6.8ms | 1.0× | 1/7 | 209.1ms | 202.3ms | 69.6 MB | 6/7 | 724 |
| python | 55.3ms | 8.1× | 4/7 | 66.4ms | 11.1ms | 9.7 MB | 1/7 | 724 |
| node | 11.9ms | 1.8× | 2/7 | 30.4ms | 18.5ms | 51.2 MB | 5/7 | 724 |
| ruby | 132.2ms | 19.4× | 5/7 | 175.5ms | 43.3ms | 23.8 MB | 2/7 | 724 |
| dotnet | 20.1ms | 3.0× | 3/7 | 42.9ms | 22.8ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 190.7ms | 8.0× | 4/7 | 216.1ms | 25.4ms | 33.7 MB | 4/7 | 9900000 |
| elixir | 23.8ms | 1.0× | 1/7 | 226.1ms | 202.3ms | 69.8 MB | 6/7 | 9900000 |
| python | 50.0ms | 2.1× | 2/7 | 61.1ms | 11.1ms | 9.8 MB | 1/7 | 9900000 |
| node | 601.0ms | 25.3× | 6/7 | 619.5ms | 18.5ms | 50.9 MB | 5/7 | 9900000 |
| ruby | 113.8ms | 4.8× | 3/7 | 157.1ms | 43.3ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 300.5ms | 12.6× | 5/7 | 323.3ms | 22.8ms | 32.6 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 273.7ms | 36.0× | 5/7 | 299.1ms | 25.4ms | 34.2 MB | 4/7 | 2475000 |
| elixir | 7.6ms | 1.0× | 1/7 | 209.9ms | 202.3ms | 69.8 MB | 6/7 | 2475000 |
| python | 226.3ms | 29.8× | 4/7 | 237.4ms | 11.1ms | 9.9 MB | 1/7 | 2475000 |
| node | 222.9ms | 29.3× | 3/7 | 241.4ms | 18.5ms | 50.7 MB | 5/7 | 2475000 |
| ruby | 121.3ms | 16.0× | 2/7 | 164.6ms | 43.3ms | 30.3 MB | 2/7 | 2475000 |
| dotnet | 727.3ms | 95.7× | 6/7 | 750.1ms | 22.8ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.1ms | 8.7× | 6/7 | 64.5ms | 25.4ms | 21.7 MB | 2/7 | 155553889038886 |
| elixir | 7.1ms | 1.6× | 2/7 | 209.4ms | 202.3ms | 70.4 MB | 6/7 | 155553889038886 |
| python | 4.5ms | 1.0× | 1/7 | 15.6ms | 11.1ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.8ms | 2.4× | 5/7 | 29.3ms | 18.5ms | 52.4 MB | 5/7 | 155553889038886 |
| ruby | 8.2ms | 1.8× | 4/7 | 51.5ms | 43.3ms | 24.0 MB | 3/7 | 155553889038886 |
| dotnet | 7.3ms | 1.6× | 3/7 | 30.1ms | 22.8ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.5ms | 119.5× | 5/7 | 144.9ms | 25.4ms | 72.7 MB | 4/7 | 6100000 |
| elixir | 22.4ms | 22.4× | 3/7 | 224.7ms | 202.3ms | 75.7 MB | 5/7 | 6100000 |
| python | 575.9ms | 575.9× | 6/7 | 587.0ms | 11.1ms | 28.1 MB | 1/7 | 6100000 |
| node | 56.2ms | 56.2× | 4/7 | 74.7ms | 18.5ms | 52.0 MB | 3/7 | 6100000 |
| ruby | 1.605s | 1605.5× | 7/7 | 1.649s | 43.3ms | 136.7 MB | 7/7 | 6100000 |
| dotnet | 17.5ms | 17.5× | 2/7 | 40.3ms | 22.8ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 458.6ms | 458.6× | 5/7 | 484.0ms | 25.4ms | 26.9 MB | 3/7 | 31781100 |
| elixir | 65.5ms | 65.5× | 3/7 | 267.8ms | 202.3ms | 73.0 MB | 5/7 | 31781100 |
| python | 737.0ms | 737.0× | 7/7 | 748.1ms | 11.1ms | 22.3 MB | 1/7 | 31781100 |
| node | 131.1ms | 131.1× | 4/7 | 149.6ms | 18.5ms | 182.7 MB | 7/7 | 31781100 |
| ruby | 510.9ms | 510.9× | 6/7 | 554.2ms | 43.3ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 37.0ms | 37.0× | 2/7 | 59.8ms | 22.8ms | 28.0 MB | 4/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.6ms | 1.1× | 2/7 | 171.0ms | 25.4ms | 115.7 MB | 5/7 | 500 |
| elixir | 595.1ms | 4.6× | 7/7 | 797.4ms | 202.3ms | 531.0 MB | 7/7 | 500 |
| python | 178.0ms | 1.4× | 4/7 | 189.1ms | 11.1ms | 44.2 MB | 1/7 | 500 |
| node | 129.4ms | 1.0× | 1/7 | 147.9ms | 18.5ms | 64.9 MB | 4/7 | 500 |
| ruby | 213.4ms | 1.6× | 5/7 | 256.7ms | 43.3ms | 50.2 MB | 3/7 | 500 |
| dotnet | 155.9ms | 1.2× | 3/7 | 178.7ms | 22.8ms | 48.3 MB | 2/7 | 500 |
