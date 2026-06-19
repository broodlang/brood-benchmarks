# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-19 15:40.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 35.6ms | 3.4× | 4/7 | 35.6ms | — | 24.1 MB | 3/7 | 0 |
| elixir | 194.6ms | 18.5× | 6/7 | 194.6ms | — | 70.4 MB | 6/7 | 0 |
| python | 10.5ms | 1.0× | 1/7 | 10.5ms | — | 9.8 MB | 1/7 | 0 |
| node | 18.1ms | 1.7× | 2/7 | 18.1ms | — | 42.7 MB | 5/7 | 0 |
| ruby | 41.8ms | 4.0× | 5/7 | 41.8ms | — | 23.5 MB | 2/7 | 0 |
| dotnet | 21.6ms | 2.1× | 3/7 | 21.6ms | — | 26.0 MB | 4/7 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 275.7ms | 6.8× | 4/7 | 311.3ms | 35.6ms | 27.8 MB | 4/7 | 9227465 |
| elixir | 78.3ms | 1.9× | 3/7 | 272.9ms | 194.6ms | 70.0 MB | 6/7 | 9227465 |
| python | 763.9ms | 18.7× | 7/7 | 774.4ms | 10.5ms | 9.8 MB | 1/7 | 9227465 |
| node | 75.7ms | 1.9× | 2/7 | 93.8ms | 18.1ms | 48.1 MB | 5/7 | 9227465 |
| ruby | 626.6ms | 15.4× | 6/7 | 668.4ms | 41.8ms | 23.5 MB | 2/7 | 9227465 |
| dotnet | 40.8ms | 1.0× | 1/7 | 62.4ms | 21.6ms | 26.0 MB | 3/7 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 56.9ms | 4.7× | 3/7 | 92.5ms | 35.6ms | 27.6 MB | 4/7 | 449999985000000 |
| elixir | 67.4ms | 5.6× | 4/7 | 262.0ms | 194.6ms | 69.8 MB | 6/7 | 449999985000000 |
| python | 2.335s | 194.6× | 7/7 | 2.345s | 10.5ms | 9.8 MB | 1/7 | 449999985000000 |
| node | 32.5ms | 2.7× | 2/7 | 50.6ms | 18.1ms | 50.1 MB | 5/7 | 449999985000000 |
| ruby | 604.3ms | 50.4× | 6/7 | 646.1ms | 41.8ms | 23.5 MB | 2/7 | 449999985000000 |
| dotnet | 12.0ms | 1.0× | 1/7 | 33.6ms | 21.6ms | 26.3 MB | 3/7 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 107.0ms | 4.8× | 3/7 | 142.6ms | 35.6ms | 24.2 MB | 3/7 | 12499997500000 |
| elixir | 33.1ms | 1.5× | 2/7 | 227.7ms | 194.6ms | 69.8 MB | 5/7 | 12499997500000 |
| python | 109.9ms | 5.0× | 4/7 | 120.4ms | 10.5ms | 10.6 MB | 1/7 | 12499997500000 |
| node | 229.5ms | 10.4× | 5/7 | 247.6ms | 18.1ms | 90.2 MB | 6/7 | 12499997500000 |
| ruby | 235.5ms | 10.7× | 6/7 | 277.3ms | 41.8ms | 23.5 MB | 2/7 | 12499997500000 |
| dotnet | 22.1ms | 1.0× | 1/7 | 43.7ms | 21.6ms | 27.6 MB | 4/7 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.3ms | 4.2× | 4/7 | 74.9ms | 35.6ms | 27.6 MB | 4/7 | 13848 |
| elixir | 23.5ms | 2.5× | 3/7 | 218.1ms | 194.6ms | 69.8 MB | 6/7 | 13848 |
| python | 125.7ms | 13.4× | 6/7 | 136.2ms | 10.5ms | 9.9 MB | 1/7 | 13848 |
| node | 11.3ms | 1.2× | 2/7 | 29.4ms | 18.1ms | 49.4 MB | 5/7 | 13848 |
| ruby | 122.6ms | 13.0× | 5/7 | 164.4ms | 41.8ms | 23.5 MB | 2/7 | 13848 |
| dotnet | 9.4ms | 1.0× | 1/7 | 31.0ms | 21.6ms | 26.4 MB | 3/7 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 459.7ms | 9.5× | 4/7 | 495.3ms | 35.6ms | 43.9 MB | 4/7 | 442 |
| elixir | 109.8ms | 2.3× | 2/7 | 304.4ms | 194.6ms | 70.3 MB | 6/7 | 442 |
| python | 2.438s | 50.5× | 7/7 | 2.448s | 10.5ms | 9.8 MB | 1/7 | 442 |
| node | 180.9ms | 3.7× | 3/7 | 199.0ms | 18.1ms | 48.6 MB | 5/7 | 442 |
| ruby | 888.8ms | 18.4× | 6/7 | 930.6ms | 41.8ms | 23.5 MB | 2/7 | 442 |
| dotnet | 48.3ms | 1.0× | 1/7 | 69.9ms | 21.6ms | 26.3 MB | 3/7 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 219.9ms | 10.8× | 3/7 | 255.5ms | 35.6ms | 27.7 MB | 4/7 | 6129302 |
| elixir | 264.9ms | 13.0× | 4/7 | 459.5ms | 194.6ms | 70.7 MB | 6/7 | 6129302 |
| python | 1.346s | 66.3× | 7/7 | 1.357s | 10.5ms | 10.1 MB | 1/7 | 6129302 |
| node | 20.8ms | 1.0× | 2/7 | 38.9ms | 18.1ms | 49.4 MB | 5/7 | 6129302 |
| ruby | 438.1ms | 21.6× | 5/7 | 479.9ms | 41.8ms | 23.6 MB | 2/7 | 6129302 |
| dotnet | 20.3ms | 1.0× | 1/7 | 41.9ms | 21.6ms | 26.3 MB | 3/7 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.1ms | 23.5× | 4/7 | 185.7ms | 35.6ms | 39.7 MB | 4/7 | 654353666 |
| elixir | 62.7ms | 9.8× | 3/7 | 257.3ms | 194.6ms | 75.3 MB | 6/7 | 654353666 |
| python | 470.1ms | 73.5× | 6/7 | 480.6ms | 10.5ms | 10.4 MB | 1/7 | 654353666 |
| node | 32.9ms | 5.1× | 2/7 | 51.0ms | 18.1ms | 52.5 MB | 5/7 | 654353666 |
| ruby | 304.6ms | 47.6× | 5/7 | 346.4ms | 41.8ms | 23.8 MB | 2/7 | 654353666 |
| dotnet | 6.4ms | 1.0× | 1/7 | 28.0ms | 21.6ms | 26.7 MB | 3/7 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 17.9ms | 1.0× | 1/7 | 53.5ms | 35.6ms | 34.3 MB | 1/7 | 3388889 |
| elixir | 121.0ms | 6.8× | 6/7 | 315.6ms | 194.6ms | 199.3 MB | 7/7 | 3388889 |
| python | 44.6ms | 2.5× | 3/7 | 55.1ms | 10.5ms | 39.9 MB | 2/7 | 3388889 |
| node | 62.5ms | 3.5× | 4/7 | 80.6ms | 18.1ms | 95.5 MB | 5/7 | 3388889 |
| ruby | 86.5ms | 4.8× | 5/7 | 128.3ms | 41.8ms | 52.1 MB | 3/7 | 3388889 |
| dotnet | 33.3ms | 1.9× | 2/7 | 54.9ms | 21.6ms | 56.8 MB | 4/7 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 422.5ms | 12.9× | 6/7 | 458.1ms | 35.6ms | 99.1 MB | 6/7 | 374854840 |
| elixir | 171.8ms | 5.3× | 4/7 | 366.4ms | 194.6ms | 71.0 MB | 5/7 | 374854840 |
| python | 175.6ms | 5.4× | 5/7 | 186.1ms | 10.5ms | 9.9 MB | 1/7 | 374854840 |
| node | 32.7ms | 1.0× | 1/7 | 50.8ms | 18.1ms | 50.2 MB | 4/7 | 374854840 |
| ruby | 80.3ms | 2.5× | 3/7 | 122.1ms | 41.8ms | 23.5 MB | 2/7 | 374854840 |
| dotnet | 37.7ms | 1.2× | 2/7 | 59.3ms | 21.6ms | 27.3 MB | 3/7 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 383.7ms | 32.5× | 6/7 | 419.3ms | 35.6ms | 40.3 MB | 4/7 | 1638200 |
| elixir | 11.8ms | 1.0× | 1/7 | 206.4ms | 194.6ms | 70.2 MB | 6/7 | 1638200 |
| python | 96.2ms | 8.2× | 4/7 | 106.7ms | 10.5ms | 10.0 MB | 1/7 | 1638200 |
| node | 23.0ms | 1.9× | 3/7 | 41.1ms | 18.1ms | 56.3 MB | 5/7 | 1638200 |
| ruby | 98.6ms | 8.4× | 5/7 | 140.4ms | 41.8ms | 23.8 MB | 2/7 | 1638200 |
| dotnet | 13.9ms | 1.2× | 2/7 | 35.5ms | 21.6ms | 32.3 MB | 3/7 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 259.2ms | 4.0× | 6/7 | 294.8ms | 35.6ms | 130.8 MB | 5/7 | 46468819 |
| elixir | 109.8ms | 1.7× | 4/7 | 304.4ms | 194.6ms | 156.7 MB | 7/7 | 46468819 |
| python | 208.6ms | 3.2× | 5/7 | 219.1ms | 10.5ms | 26.0 MB | 1/7 | 46468819 |
| node | 109.7ms | 1.7× | 3/7 | 127.8ms | 18.1ms | 65.4 MB | 4/7 | 46468819 |
| ruby | 72.8ms | 1.1× | 2/7 | 114.6ms | 41.8ms | 29.2 MB | 2/7 | 46468819 |
| dotnet | 65.1ms | 1.0× | 1/7 | 86.7ms | 21.6ms | 29.6 MB | 3/7 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 504.5ms | 76.4× | 6/7 | 540.1ms | 35.6ms | 41.9 MB | 4/7 | 724 |
| elixir | 6.6ms | 1.0× | 1/7 | 201.2ms | 194.6ms | 69.8 MB | 6/7 | 724 |
| python | 53.7ms | 8.1× | 4/7 | 64.2ms | 10.5ms | 9.8 MB | 1/7 | 724 |
| node | 10.3ms | 1.6× | 2/7 | 28.4ms | 18.1ms | 50.9 MB | 5/7 | 724 |
| ruby | 126.1ms | 19.1× | 5/7 | 167.9ms | 41.8ms | 23.8 MB | 2/7 | 724 |
| dotnet | 20.4ms | 3.1× | 3/7 | 42.0ms | 21.6ms | 29.3 MB | 3/7 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 208.5ms | 8.4× | 4/7 | 244.1ms | 35.6ms | 41.5 MB | 4/7 | 9900000 |
| elixir | 24.7ms | 1.0× | 1/7 | 219.3ms | 194.6ms | 69.9 MB | 6/7 | 9900000 |
| python | 50.7ms | 2.1× | 2/7 | 61.2ms | 10.5ms | 9.8 MB | 1/7 | 9900000 |
| node | 598.4ms | 24.2× | 6/7 | 616.5ms | 18.1ms | 50.6 MB | 5/7 | 9900000 |
| ruby | 111.6ms | 4.5× | 3/7 | 153.4ms | 41.8ms | 26.1 MB | 2/7 | 9900000 |
| dotnet | 296.5ms | 12.0× | 5/7 | 318.1ms | 21.6ms | 32.4 MB | 3/7 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 272.1ms | 25.9× | 5/7 | 307.7ms | 35.6ms | 41.5 MB | 4/7 | 2475000 |
| elixir | 10.5ms | 1.0× | 1/7 | 205.1ms | 194.6ms | 69.8 MB | 6/7 | 2475000 |
| python | 227.3ms | 21.6× | 4/7 | 237.8ms | 10.5ms | 9.9 MB | 1/7 | 2475000 |
| node | 221.1ms | 21.1× | 3/7 | 239.2ms | 18.1ms | 50.4 MB | 5/7 | 2475000 |
| ruby | 122.8ms | 11.7× | 2/7 | 164.6ms | 41.8ms | 30.1 MB | 2/7 | 2475000 |
| dotnet | 715.6ms | 68.2× | 6/7 | 737.2ms | 21.6ms | 32.5 MB | 3/7 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 43.6ms | 10.4× | 6/7 | 79.2ms | 35.6ms | 27.7 MB | 3/7 | 155553889038886 |
| elixir | 10.8ms | 2.6× | 4/7 | 205.4ms | 194.6ms | 70.4 MB | 6/7 | 155553889038886 |
| python | 4.2ms | 1.0× | 1/7 | 14.7ms | 10.5ms | 9.9 MB | 1/7 | 155553889038886 |
| node | 12.0ms | 2.9× | 5/7 | 30.1ms | 18.1ms | 52.2 MB | 5/7 | 155553889038886 |
| ruby | 7.4ms | 1.8× | 2/7 | 49.2ms | 41.8ms | 24.0 MB | 2/7 | 155553889038886 |
| dotnet | 9.2ms | 2.2× | 3/7 | 30.8ms | 21.6ms | 28.1 MB | 4/7 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 105.0ms | 105.0× | 5/7 | 140.6ms | 35.6ms | 76.2 MB | 4/7 | 6100000 |
| elixir | 12.0ms | 12.0× | 2/7 | 206.6ms | 194.6ms | 78.1 MB | 5/7 | 6100000 |
| python | 556.7ms | 556.7× | 6/7 | 567.2ms | 10.5ms | 28.1 MB | 1/7 | 6100000 |
| node | 57.2ms | 57.2× | 4/7 | 75.3ms | 18.1ms | 51.6 MB | 3/7 | 6100000 |
| ruby | 1.633s | 1632.7× | 7/7 | 1.675s | 41.8ms | 137.5 MB | 7/7 | 6100000 |
| dotnet | 18.9ms | 18.9× | 3/7 | 40.5ms | 21.6ms | 30.9 MB | 2/7 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 402.8ms | 402.8× | 5/7 | 438.4ms | 35.6ms | 31.8 MB | 4/7 | 31781100 |
| elixir | 66.4ms | 66.4× | 3/7 | 261.0ms | 194.6ms | 71.7 MB | 5/7 | 31781100 |
| python | 678.0ms | 678.0× | 7/7 | 688.5ms | 10.5ms | 22.3 MB | 1/7 | 31781100 |
| node | 111.7ms | 111.7× | 4/7 | 129.8ms | 18.1ms | 182.8 MB | 7/7 | 31781100 |
| ruby | 427.9ms | 427.9× | 6/7 | 469.7ms | 41.8ms | 23.7 MB | 2/7 | 31781100 |
| dotnet | 33.6ms | 33.6× | 2/7 | 55.2ms | 21.6ms | 28.1 MB | 3/7 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 150.3ms | 1.1× | 2/7 | 185.9ms | 35.6ms | 127.7 MB | 5/7 | 500 |
| elixir | 586.2ms | 4.5× | 7/7 | 780.8ms | 194.6ms | 530.3 MB | 7/7 | 500 |
| python | 182.0ms | 1.4× | 4/7 | 192.5ms | 10.5ms | 44.6 MB | 1/7 | 500 |
| node | 131.2ms | 1.0× | 1/7 | 149.3ms | 18.1ms | 65.3 MB | 4/7 | 500 |
| ruby | 213.3ms | 1.6× | 5/7 | 255.1ms | 41.8ms | 50.1 MB | 3/7 | 500 |
| dotnet | 155.9ms | 1.2× | 3/7 | 177.5ms | 21.6ms | 48.0 MB | 2/7 | 500 |
