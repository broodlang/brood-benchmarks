# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-14 16:33.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.6ms | 2.7× | 4/6 | 28.6ms | — | 13.8 MB | 2/6 | 0 |
| elixir | 258.4ms | 24.4× | 6/6 | 258.4ms | — | 77.4 MB | 6/6 | 0 |
| python | 10.6ms | 1.0× | 1/6 | 10.6ms | — | 9.8 MB | 1/6 | 0 |
| node | 19.4ms | 1.8× | 2/6 | 19.4ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 40.4ms | 3.8× | 5/6 | 40.4ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 23.4ms | 2.2× | 3/6 | 23.4ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 634.8ms | 12.5× | 5/6 | 663.4ms | 28.6ms | 14.2 MB | 2/6 | 9227465 |
| elixir | 128.2ms | 2.5× | 3/6 | 386.6ms | 258.4ms | 81.7 MB | 6/6 | 9227465 |
| python | 755.7ms | 14.9× | 6/6 | 766.3ms | 10.6ms | 9.8 MB | 1/6 | 9227465 |
| node | 85.6ms | 1.7× | 2/6 | 105.0ms | 19.4ms | 48.7 MB | 5/6 | 9227465 |
| ruby | 627.6ms | 12.4× | 4/6 | 668.0ms | 40.4ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 50.8ms | 1.0× | 1/6 | 74.2ms | 23.4ms | 26.1 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 189.6ms | 14.4× | 4/6 | 218.2ms | 28.6ms | 14.3 MB | 2/6 | 449999985000000 |
| elixir | 87.2ms | 6.6× | 3/6 | 345.6ms | 258.4ms | 80.8 MB | 6/6 | 449999985000000 |
| python | 2.284s | 173.1× | 6/6 | 2.295s | 10.6ms | 9.7 MB | 1/6 | 449999985000000 |
| node | 43.7ms | 3.3× | 2/6 | 63.1ms | 19.4ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 585.0ms | 44.3× | 5/6 | 625.4ms | 40.4ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 13.2ms | 1.0× | 1/6 | 36.6ms | 23.4ms | 26.3 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 119.1ms | 11.6× | 3/6 | 147.7ms | 28.6ms | 13.8 MB | 2/6 | 12499997500000 |
| elixir | 48.1ms | 4.7× | 2/6 | 306.5ms | 258.4ms | 76.9 MB | 5/6 | 12499997500000 |
| python | 122.2ms | 11.9× | 4/6 | 132.8ms | 10.6ms | 10.6 MB | 1/6 | 12499997500000 |
| node | 234.5ms | 22.8× | 5/6 | 253.9ms | 19.4ms | 90.7 MB | 6/6 | 12499997500000 |
| ruby | 234.8ms | 22.8× | 6/6 | 275.2ms | 40.4ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 10.3ms | 1.0× | 1/6 | 33.7ms | 23.4ms | 27.6 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 41.8ms | 2.0× | 3/6 | 70.4ms | 28.6ms | 14.5 MB | 2/6 | 13848 |
| elixir | 68.7ms | 3.3× | 4/6 | 327.1ms | 258.4ms | 81.0 MB | 6/6 | 13848 |
| python | 135.9ms | 6.6× | 6/6 | 146.5ms | 10.6ms | 9.9 MB | 1/6 | 13848 |
| node | 23.1ms | 1.1× | 2/6 | 42.5ms | 19.4ms | 49.2 MB | 5/6 | 13848 |
| ruby | 120.9ms | 5.8× | 5/6 | 161.3ms | 40.4ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 20.7ms | 1.0× | 1/6 | 44.1ms | 23.4ms | 26.4 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 479.1ms | 8.4× | 4/6 | 507.7ms | 28.6ms | 28.8 MB | 4/6 | 442 |
| elixir | 154.8ms | 2.7× | 2/6 | 413.2ms | 258.4ms | 80.8 MB | 6/6 | 442 |
| python | 2.465s | 43.0× | 6/6 | 2.475s | 10.6ms | 9.8 MB | 1/6 | 442 |
| node | 178.4ms | 3.1× | 3/6 | 197.8ms | 19.4ms | 49.0 MB | 5/6 | 442 |
| ruby | 893.8ms | 15.6× | 5/6 | 934.2ms | 40.4ms | 23.5 MB | 2/6 | 442 |
| dotnet | 57.3ms | 1.0× | 1/6 | 80.7ms | 23.4ms | 26.3 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.326s | 69.8× | 5/6 | 1.355s | 28.6ms | 14.6 MB | 2/6 | 6129302 |
| elixir | 295.6ms | 15.6× | 3/6 | 554.0ms | 258.4ms | 81.6 MB | 6/6 | 6129302 |
| python | 1.343s | 70.7× | 6/6 | 1.353s | 10.6ms | 10.0 MB | 1/6 | 6129302 |
| node | 19.0ms | 1.0× | 1/6 | 38.4ms | 19.4ms | 49.8 MB | 5/6 | 6129302 |
| ruby | 431.2ms | 22.7× | 4/6 | 471.6ms | 40.4ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 24.2ms | 1.3× | 2/6 | 47.6ms | 23.4ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 242.7ms | 78.3× | 4/6 | 271.3ms | 28.6ms | 21.5 MB | 2/6 | 654353666 |
| elixir | 81.1ms | 26.2× | 3/6 | 339.5ms | 258.4ms | 82.6 MB | 6/6 | 654353666 |
| python | 475.8ms | 153.5× | 6/6 | 486.4ms | 10.6ms | 10.4 MB | 1/6 | 654353666 |
| node | 34.0ms | 11.0× | 2/6 | 53.4ms | 19.4ms | 53.0 MB | 5/6 | 654353666 |
| ruby | 302.0ms | 97.4× | 5/6 | 342.4ms | 40.4ms | 23.8 MB | 3/6 | 654353666 |
| dotnet | 3.1ms | 1.0× | 1/6 | 26.5ms | 23.4ms | 26.9 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 813.5ms | 18.9× | 6/6 | 842.1ms | 28.6ms | 180.7 MB | 5/6 | 3388889 |
| elixir | 130.0ms | 3.0× | 5/6 | 388.4ms | 258.4ms | 200.3 MB | 6/6 | 3388889 |
| python | 54.1ms | 1.3× | 2/6 | 64.7ms | 10.6ms | 39.8 MB | 1/6 | 3388889 |
| node | 69.1ms | 1.6× | 3/6 | 88.5ms | 19.4ms | 96.0 MB | 4/6 | 3388889 |
| ruby | 98.6ms | 2.3× | 4/6 | 139.0ms | 40.4ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 43.1ms | 1.0× | 1/6 | 66.5ms | 23.4ms | 56.9 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 995.0ms | 24.6× | 6/6 | 1.024s | 28.6ms | 55.5 MB | 5/6 | 374854840 |
| elixir | 179.9ms | 4.5× | 5/6 | 438.3ms | 258.4ms | 79.8 MB | 6/6 | 374854840 |
| python | 174.8ms | 4.3× | 4/6 | 185.4ms | 10.6ms | 9.9 MB | 1/6 | 374854840 |
| node | 40.4ms | 1.0× | 1/6 | 59.8ms | 19.4ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 84.4ms | 2.1× | 3/6 | 124.8ms | 40.4ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 48.4ms | 1.2× | 2/6 | 71.8ms | 23.4ms | 27.4 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 443.4ms | 26.4× | 6/6 | 472.0ms | 28.6ms | 24.8 MB | 3/6 | 1638200 |
| elixir | 48.5ms | 2.9× | 3/6 | 306.9ms | 258.4ms | 81.2 MB | 6/6 | 1638200 |
| python | 100.4ms | 6.0× | 4/6 | 111.0ms | 10.6ms | 10.0 MB | 1/6 | 1638200 |
| node | 35.3ms | 2.1× | 2/6 | 54.7ms | 19.4ms | 56.7 MB | 5/6 | 1638200 |
| ruby | 110.0ms | 6.5× | 5/6 | 150.4ms | 40.4ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 16.8ms | 1.0× | 1/6 | 40.2ms | 23.4ms | 32.4 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 288.2ms | 4.6× | 6/6 | 316.8ms | 28.6ms | 85.3 MB | 5/6 | 46468819 |
| elixir | 127.9ms | 2.0× | 4/6 | 386.3ms | 258.4ms | 165.3 MB | 6/6 | 46468819 |
| python | 197.1ms | 3.1× | 5/6 | 207.7ms | 10.6ms | 26.0 MB | 1/6 | 46468819 |
| node | 119.4ms | 1.9× | 3/6 | 138.8ms | 19.4ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 86.8ms | 1.4× | 2/6 | 127.2ms | 40.4ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 63.2ms | 1.0× | 1/6 | 86.6ms | 23.4ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 510.3ms | 21.6× | 6/6 | 538.9ms | 28.6ms | 22.8 MB | 2/6 | 724 |
| elixir | 62.0ms | 2.6× | 3/6 | 320.4ms | 258.4ms | 80.5 MB | 6/6 | 724 |
| python | 67.9ms | 2.9× | 4/6 | 78.5ms | 10.6ms | 9.8 MB | 1/6 | 724 |
| node | 23.6ms | 1.0× | 1/6 | 43.0ms | 19.4ms | 51.2 MB | 5/6 | 724 |
| ruby | 135.9ms | 5.8× | 5/6 | 176.3ms | 40.4ms | 23.8 MB | 3/6 | 724 |
| dotnet | 31.4ms | 1.3× | 2/6 | 54.8ms | 23.4ms | 29.4 MB | 4/6 | 724 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 134.2ms | 21.3× | 6/6 | 162.8ms | 28.6ms | 32.0 MB | 4/6 | 155553889038886 |
| elixir | 28.2ms | 4.5× | 5/6 | 286.6ms | 258.4ms | 77.9 MB | 6/6 | 155553889038886 |
| python | 9.0ms | 1.4× | 3/6 | 19.6ms | 10.6ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 14.6ms | 2.3× | 4/6 | 34.0ms | 19.4ms | 52.6 MB | 5/6 | 155553889038886 |
| ruby | 8.0ms | 1.3× | 2/6 | 48.4ms | 40.4ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 6.3ms | 1.0× | 1/6 | 29.7ms | 23.4ms | 28.2 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 512.2ms | 21.3× | 4/6 | 540.8ms | 28.6ms | 118.3 MB | 5/6 | 6100000 |
| elixir | 56.4ms | 2.4× | 3/6 | 314.8ms | 258.4ms | 88.1 MB | 4/6 | 6100000 |
| python | 543.9ms | 22.7× | 5/6 | 554.5ms | 10.6ms | 28.0 MB | 1/6 | 6100000 |
| node | 52.7ms | 2.2× | 2/6 | 72.1ms | 19.4ms | 51.9 MB | 3/6 | 6100000 |
| ruby | 1.582s | 65.9× | 6/6 | 1.623s | 40.4ms | 136.4 MB | 6/6 | 6100000 |
| dotnet | 24.0ms | 1.0× | 1/6 | 47.4ms | 23.4ms | 30.9 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 409.7ms | 8.4× | 4/6 | 438.3ms | 28.6ms | 16.0 MB | 1/6 | 31781100 |
| elixir | 113.8ms | 2.3× | 2/6 | 372.2ms | 258.4ms | 85.3 MB | 5/6 | 31781100 |
| python | 705.3ms | 14.5× | 6/6 | 715.9ms | 10.6ms | 22.1 MB | 2/6 | 31781100 |
| node | 123.2ms | 2.5× | 3/6 | 142.6ms | 19.4ms | 183.1 MB | 6/6 | 31781100 |
| ruby | 436.2ms | 9.0× | 5/6 | 476.6ms | 40.4ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 48.7ms | 1.0× | 1/6 | 72.1ms | 23.4ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.4ms | 1.3× | 3/6 | 179.0ms | 28.6ms | 100.7 MB | 5/6 | 500 |
| elixir | 643.8ms | 5.5× | 6/6 | 902.2ms | 258.4ms | 527.2 MB | 6/6 | 500 |
| python | 177.7ms | 1.5× | 4/6 | 188.3ms | 10.6ms | 47.0 MB | 1/6 | 500 |
| node | 116.1ms | 1.0× | 1/6 | 135.5ms | 19.4ms | 65.3 MB | 4/6 | 500 |
| ruby | 222.1ms | 1.9× | 5/6 | 262.5ms | 40.4ms | 50.1 MB | 3/6 | 500 |
| dotnet | 144.8ms | 1.2× | 2/6 | 168.2ms | 23.4ms | 48.2 MB | 2/6 | 500 |
