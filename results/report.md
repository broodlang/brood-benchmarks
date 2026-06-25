# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-25 10:35.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.2ms | 2.6× | 4/7 | 29.2ms | — | 22.0 MB | 2/7 | 0 |
| elixir | 212.2ms | 19.1× | 6/7 | 212.2ms | — | 69.7 MB | 6/7 | 0 |
| python | 11.1ms | 1.0× | 1/7 | 11.1ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.7ms | 1.7× | 2/7 | 18.7ms | — | 43.4 MB | 5/7 | 0 |
| ruby | 44.5ms | 4.0× | 5/7 | 44.5ms | — | 23.5 MB | 3/7 | 0 |
| dotnet | 23.1ms | 2.1× | 3/7 | 23.1ms | — | 25.9 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 241.5ms | 5.4× | 4/7 | 270.7ms | 29.2ms | 26.0 MB | 3/7 | 9227465 |
| elixir | 82.7ms | 1.9× | 3/7 | 294.9ms | 212.2ms | 69.9 MB | 6/7 | 9227465 |
| python | 824.5ms | 18.6× | 7/7 | 835.6ms | 11.1ms | 9.8 MB | 1/7 | 9227465 |
| node | 82.4ms | 1.9× | 2/7 | 101.1ms | 18.7ms | 48.8 MB | 5/7 | 9227465 |
| ruby | 687.6ms | 15.5× | 6/7 | 732.1ms | 44.5ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 44.4ms | 1.0× | 1/7 | 67.5ms | 23.1ms | 26.0 MB | 4/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 38.5ms | 3.0× | 3/7 | 67.7ms | 29.2ms | 25.3 MB | 3/7 | 449999985000000 |
| elixir | 69.4ms | 5.4× | 4/7 | 281.6ms | 212.2ms | 69.7 MB | 6/7 | 449999985000000 |
| python | 2.411s | 186.9× | 7/7 | 2.422s | 11.1ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 30.6ms | 2.4× | 2/7 | 49.3ms | 18.7ms | 50.7 MB | 5/7 | 449999985000000 |
| ruby | 590.8ms | 45.8× | 6/7 | 635.3ms | 44.5ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 12.9ms | 1.0× | 1/7 | 36.0ms | 23.1ms | 26.3 MB | 4/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.6ms | 1.0× | 1/7 | 31.8ms | 29.2ms | 22.0 MB | 2/7 | 12499997500000 |
| elixir | 32.1ms | 12.3× | 3/7 | 244.3ms | 212.2ms | 71.9 MB | 5/7 | 12499997500000 |
| python | 118.4ms | 45.5× | 4/7 | 129.5ms | 11.1ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 246.7ms | 94.9× | 5/7 | 265.4ms | 18.7ms | 90.8 MB | 6/7 | 12499997500000 |
| ruby | 251.7ms | 96.8× | 6/7 | 296.2ms | 44.5ms | 23.5 MB | 3/7 | 12499997500000 |
| dotnet | 13.0ms | 5.0× | 2/7 | 36.1ms | 23.1ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.8ms | 6.6× | 4/7 | 63.0ms | 29.2ms | 25.8 MB | 3/7 | 13848 |
| elixir | 5.1ms | 1.0× | 1/7 | 217.3ms | 212.2ms | 70.0 MB | 6/7 | 13848 |
| python | 122.1ms | 23.9× | 6/7 | 133.2ms | 11.1ms | 9.9 MB | 1/7 | 13848 |
| node | 9.7ms | 1.9× | 3/7 | 28.4ms | 18.7ms | 49.3 MB | 5/7 | 13848 |
| ruby | 116.8ms | 22.9× | 5/7 | 161.3ms | 44.5ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 8.3ms | 1.6× | 2/7 | 31.4ms | 23.1ms | 26.3 MB | 4/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 81.8ms | 1.8× | 2/7 | 111.0ms | 29.2ms | 25.4 MB | 3/7 | 442 |
| elixir | 94.0ms | 2.1× | 3/7 | 306.2ms | 212.2ms | 69.6 MB | 6/7 | 442 |
| python | 2.480s | 54.2× | 7/7 | 2.491s | 11.1ms | 9.8 MB | 1/7 | 442 |
| node | 181.9ms | 4.0× | 4/7 | 200.6ms | 18.7ms | 49.1 MB | 5/7 | 442 |
| ruby | 895.3ms | 19.5× | 6/7 | 939.8ms | 44.5ms | 23.5 MB | 2/7 | 442 |
| dotnet | 45.8ms | 1.0× | 1/7 | 68.9ms | 23.1ms | 26.3 MB | 4/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 219.5ms | 12.2× | 3/7 | 248.7ms | 29.2ms | 25.4 MB | 3/7 | 6129302 |
| elixir | 242.3ms | 13.5× | 4/7 | 454.5ms | 212.2ms | 69.9 MB | 6/7 | 6129302 |
| python | 1.377s | 76.5× | 7/7 | 1.388s | 11.1ms | 10.1 MB | 1/7 | 6129302 |
| node | 20.7ms | 1.1× | 2/7 | 39.4ms | 18.7ms | 49.9 MB | 5/7 | 6129302 |
| ruby | 431.9ms | 24.0× | 6/7 | 476.4ms | 44.5ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 18.0ms | 1.0× | 1/7 | 41.1ms | 23.1ms | 26.3 MB | 4/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.3ms | 21.1× | 4/7 | 130.5ms | 29.2ms | 40.3 MB | 4/7 | 654353666 |
| elixir | 48.7ms | 10.1× | 3/7 | 260.9ms | 212.2ms | 75.3 MB | 6/7 | 654353666 |
| python | 464.6ms | 96.8× | 6/7 | 475.7ms | 11.1ms | 10.4 MB | 1/7 | 654353666 |
| node | 23.8ms | 5.0× | 2/7 | 42.5ms | 18.7ms | 53.0 MB | 5/7 | 654353666 |
| ruby | 308.8ms | 64.3× | 5/7 | 353.3ms | 44.5ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 4.8ms | 1.0× | 1/7 | 27.9ms | 23.1ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 9.9ms | 1.0× | 1/7 | 39.1ms | 29.2ms | 31.1 MB | 1/7 | 3388889 |
| elixir | 101.6ms | 10.3× | 6/7 | 313.8ms | 212.2ms | 199.7 MB | 7/7 | 3388889 |
| python | 44.6ms | 4.5× | 3/7 | 55.7ms | 11.1ms | 39.9 MB | 2/7 | 3388889 |
| node | 59.5ms | 6.0× | 4/7 | 78.2ms | 18.7ms | 96.1 MB | 5/7 | 3388889 |
| ruby | 84.1ms | 8.5× | 5/7 | 128.6ms | 44.5ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 31.8ms | 3.2× | 2/7 | 54.9ms | 23.1ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 474.5ms | 11.7× | 6/7 | 503.7ms | 29.2ms | 95.5 MB | 6/7 | 374854840 |
| elixir | 220.9ms | 5.4× | 5/7 | 433.1ms | 212.2ms | 70.6 MB | 5/7 | 374854840 |
| python | 205.8ms | 5.1× | 4/7 | 216.9ms | 11.1ms | 9.9 MB | 1/7 | 374854840 |
| node | 40.6ms | 1.0× | 1/7 | 59.3ms | 18.7ms | 50.8 MB | 4/7 | 374854840 |
| ruby | 88.5ms | 2.2× | 3/7 | 133.0ms | 44.5ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 44.3ms | 1.1× | 2/7 | 67.4ms | 23.1ms | 27.4 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 116.2ms | 6.4× | 6/7 | 145.4ms | 29.2ms | 40.4 MB | 4/7 | 1638200 |
| elixir | 27.7ms | 1.5× | 2/7 | 239.9ms | 212.2ms | 70.4 MB | 6/7 | 1638200 |
| python | 111.2ms | 6.1× | 4/7 | 122.3ms | 11.1ms | 10.0 MB | 1/7 | 1638200 |
| node | 27.9ms | 1.5× | 3/7 | 46.6ms | 18.7ms | 56.8 MB | 5/7 | 1638200 |
| ruby | 115.1ms | 6.3× | 5/7 | 159.6ms | 44.5ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 18.2ms | 1.0× | 1/7 | 41.3ms | 23.1ms | 32.4 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 193.8ms | 2.6× | 5/7 | 223.0ms | 29.2ms | 136.0 MB | 5/7 | 46468819 |
| elixir | 137.7ms | 1.9× | 4/7 | 349.9ms | 212.2ms | 157.1 MB | 7/7 | 46468819 |
| python | 211.0ms | 2.8× | 6/7 | 222.1ms | 11.1ms | 26.0 MB | 1/7 | 46468819 |
| node | 124.9ms | 1.7× | 3/7 | 143.6ms | 18.7ms | 65.6 MB | 4/7 | 46468819 |
| ruby | 85.3ms | 1.1× | 2/7 | 129.8ms | 44.5ms | 29.2 MB | 2/7 | 46468819 |
| dotnet | 74.2ms | 1.0× | 1/7 | 97.3ms | 23.1ms | 29.7 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.5ms | 8.3× | 5/7 | 142.7ms | 29.2ms | 41.2 MB | 4/7 | 724 |
| elixir | 19.0ms | 1.4× | 2/7 | 231.2ms | 212.2ms | 69.8 MB | 6/7 | 724 |
| python | 60.4ms | 4.4× | 4/7 | 71.5ms | 11.1ms | 9.8 MB | 1/7 | 724 |
| node | 13.7ms | 1.0× | 1/7 | 32.4ms | 18.7ms | 51.3 MB | 5/7 | 724 |
| ruby | 140.9ms | 10.3× | 6/7 | 185.4ms | 44.5ms | 23.8 MB | 2/7 | 724 |
| dotnet | 22.3ms | 1.6× | 3/7 | 45.4ms | 23.1ms | 29.4 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 40.1ms | 1.4× | 2/7 | 69.3ms | 29.2ms | 22.4 MB | 2/7 | 9900000 |
| elixir | 28.9ms | 1.0× | 1/7 | 241.1ms | 212.2ms | 70.0 MB | 6/7 | 9900000 |
| python | 56.1ms | 1.9× | 3/7 | 67.2ms | 11.1ms | 9.8 MB | 1/7 | 9900000 |
| node | 655.5ms | 22.7× | 6/7 | 674.2ms | 18.7ms | 51.0 MB | 5/7 | 9900000 |
| ruby | 127.1ms | 4.4× | 4/7 | 171.6ms | 44.5ms | 26.1 MB | 3/7 | 9900000 |
| dotnet | 331.8ms | 11.5× | 5/7 | 354.9ms | 23.1ms | 32.6 MB | 4/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 54.9ms | 3.6× | 2/7 | 84.1ms | 29.2ms | 25.9 MB | 2/7 | 2475000 |
| elixir | 15.4ms | 1.0× | 1/7 | 227.6ms | 212.2ms | 69.9 MB | 6/7 | 2475000 |
| python | 252.6ms | 16.4× | 5/7 | 263.7ms | 11.1ms | 9.9 MB | 1/7 | 2475000 |
| node | 239.2ms | 15.5× | 4/7 | 257.9ms | 18.7ms | 50.8 MB | 5/7 | 2475000 |
| ruby | 129.8ms | 8.4× | 3/7 | 174.3ms | 44.5ms | 30.1 MB | 3/7 | 2475000 |
| dotnet | 787.6ms | 51.1× | 6/7 | 810.7ms | 23.1ms | 32.6 MB | 4/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 33.1ms | 6.2× | 6/7 | 62.3ms | 29.2ms | 25.5 MB | 3/7 | 155553889038886 |
| elixir | 12.1ms | 2.3× | 5/7 | 224.3ms | 212.2ms | 70.4 MB | 6/7 | 155553889038886 |
| python | 5.3ms | 1.0× | 1/7 | 16.4ms | 11.1ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 10.5ms | 2.0× | 4/7 | 29.2ms | 18.7ms | 52.6 MB | 5/7 | 155553889038886 |
| ruby | 9.8ms | 1.8× | 2/7 | 54.3ms | 44.5ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 9.9ms | 1.9× | 3/7 | 33.0ms | 23.1ms | 28.2 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 116.5ms | 116.5× | 5/7 | 145.7ms | 29.2ms | 85.3 MB | 5/7 | 6100000 |
| elixir | 0.0ms | < 1× | 2/7 | 209.5ms | 212.2ms | 75.4 MB | 4/7 | 6100000 |
| python | 556.7ms | 556.7× | 6/7 | 567.8ms | 11.1ms | 28.1 MB | 1/7 | 6100000 |
| node | 54.5ms | 54.5× | 4/7 | 73.2ms | 18.7ms | 52.1 MB | 3/7 | 6100000 |
| ruby | 1.618s | 1618.4× | 7/7 | 1.663s | 44.5ms | 137.0 MB | 7/7 | 6100000 |
| dotnet | 18.1ms | 18.1× | 3/7 | 41.2ms | 23.1ms | 30.8 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 384.1ms | 384.1× | 5/7 | 413.3ms | 29.2ms | 30.8 MB | 4/7 | 31781100 |
| elixir | 54.4ms | 54.4× | 3/7 | 266.6ms | 212.2ms | 71.9 MB | 5/7 | 31781100 |
| python | 725.9ms | 725.9× | 7/7 | 737.0ms | 11.1ms | 22.2 MB | 1/7 | 31781100 |
| node | 121.7ms | 121.7× | 4/7 | 140.4ms | 18.7ms | 183.2 MB | 7/7 | 31781100 |
| ruby | 499.0ms | 499.0× | 6/7 | 543.5ms | 44.5ms | 23.6 MB | 2/7 | 31781100 |
| dotnet | 35.9ms | 35.9× | 2/7 | 59.0ms | 23.1ms | 27.9 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 145.5ms | 1.1× | 2/7 | 174.7ms | 29.2ms | 122.3 MB | 5/7 | 500 |
| elixir | 564.1ms | 4.1× | 7/7 | 776.3ms | 212.2ms | 513.2 MB | 7/7 | 500 |
| python | 181.2ms | 1.3× | 3/7 | 192.3ms | 11.1ms | 45.2 MB | 1/7 | 500 |
| node | 136.7ms | 1.0× | 1/7 | 155.4ms | 18.7ms | 65.3 MB | 4/7 | 500 |
| ruby | 260.4ms | 1.9× | 5/7 | 304.9ms | 44.5ms | 50.2 MB | 3/7 | 500 |
| dotnet | 182.6ms | 1.3× | 4/7 | 205.7ms | 23.1ms | 48.3 MB | 2/7 | 500 |
