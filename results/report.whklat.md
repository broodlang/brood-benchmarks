# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-14 19:17.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.0ms | 2.6× | 4/6 | 28.0ms | — | 14.7 MB | 2/6 | 0 |
| elixir | 255.5ms | 23.7× | 6/6 | 255.5ms | — | 77.4 MB | 6/6 | 0 |
| python | 10.8ms | 1.0× | 1/6 | 10.8ms | — | 9.7 MB | 1/6 | 0 |
| node | 21.1ms | 2.0× | 2/6 | 21.1ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 44.4ms | 4.1× | 5/6 | 44.4ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.6ms | 2.0× | 3/6 | 21.6ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 653.6ms | 12.3× | 5/6 | 681.6ms | 28.0ms | 16.0 MB | 2/6 | 9227465 |
| elixir | 128.1ms | 2.4× | 3/6 | 383.6ms | 255.5ms | 80.6 MB | 6/6 | 9227465 |
| python | 754.1ms | 14.2× | 6/6 | 764.9ms | 10.8ms | 9.7 MB | 1/6 | 9227465 |
| node | 85.0ms | 1.6× | 2/6 | 106.1ms | 21.1ms | 48.7 MB | 5/6 | 9227465 |
| ruby | 628.1ms | 11.8× | 4/6 | 672.5ms | 44.4ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 53.2ms | 1.0× | 1/6 | 74.8ms | 21.6ms | 26.1 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 189.7ms | 15.1× | 4/6 | 217.7ms | 28.0ms | 15.9 MB | 2/6 | 449999985000000 |
| elixir | 92.7ms | 7.4× | 3/6 | 348.2ms | 255.5ms | 81.7 MB | 6/6 | 449999985000000 |
| python | 2.315s | 183.7× | 6/6 | 2.325s | 10.8ms | 9.7 MB | 1/6 | 449999985000000 |
| node | 27.5ms | 2.2× | 2/6 | 48.6ms | 21.1ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 603.5ms | 47.9× | 5/6 | 647.9ms | 44.4ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 12.6ms | 1.0× | 1/6 | 34.2ms | 21.6ms | 26.5 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.5ms | 4.0× | 3/6 | 131.5ms | 28.0ms | 14.7 MB | 2/6 | 12499997500000 |
| elixir | 50.8ms | 1.9× | 2/6 | 306.3ms | 255.5ms | 76.9 MB | 5/6 | 12499997500000 |
| python | 107.2ms | 4.1× | 4/6 | 118.0ms | 10.8ms | 10.4 MB | 1/6 | 12499997500000 |
| node | 229.4ms | 8.8× | 5/6 | 250.5ms | 21.1ms | 90.7 MB | 6/6 | 12499997500000 |
| ruby | 240.0ms | 9.2× | 6/6 | 284.4ms | 44.4ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 26.2ms | 1.0× | 1/6 | 47.8ms | 21.6ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 55.8ms | 4.6× | 3/6 | 83.8ms | 28.0ms | 15.9 MB | 2/6 | 13848 |
| elixir | 72.3ms | 6.0× | 4/6 | 327.8ms | 255.5ms | 81.0 MB | 6/6 | 13848 |
| python | 128.1ms | 10.7× | 6/6 | 138.9ms | 10.8ms | 9.8 MB | 1/6 | 13848 |
| node | 12.0ms | 1.0× | 1/6 | 33.1ms | 21.1ms | 49.3 MB | 5/6 | 13848 |
| ruby | 113.9ms | 9.5× | 5/6 | 158.3ms | 44.4ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 12.2ms | 1.0× | 2/6 | 33.8ms | 21.6ms | 26.4 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 485.8ms | 8.1× | 4/6 | 513.8ms | 28.0ms | 30.0 MB | 4/6 | 442 |
| elixir | 157.5ms | 2.6× | 2/6 | 413.0ms | 255.5ms | 81.7 MB | 6/6 | 442 |
| python | 2.447s | 40.9× | 6/6 | 2.457s | 10.8ms | 9.7 MB | 1/6 | 442 |
| node | 186.0ms | 3.1× | 3/6 | 207.1ms | 21.1ms | 49.0 MB | 5/6 | 442 |
| ruby | 882.3ms | 14.8× | 5/6 | 926.7ms | 44.4ms | 23.5 MB | 2/6 | 442 |
| dotnet | 59.8ms | 1.0× | 1/6 | 81.4ms | 21.6ms | 26.5 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 249.8ms | 14.2× | 3/6 | 277.8ms | 28.0ms | 16.2 MB | 2/6 | 6129302 |
| elixir | 296.5ms | 16.8× | 4/6 | 552.0ms | 255.5ms | 81.5 MB | 6/6 | 6129302 |
| python | 1.397s | 79.4× | 6/6 | 1.408s | 10.8ms | 9.9 MB | 1/6 | 6129302 |
| node | 17.6ms | 1.0× | 1/6 | 38.7ms | 21.1ms | 49.8 MB | 5/6 | 6129302 |
| ruby | 437.5ms | 24.9× | 5/6 | 481.9ms | 44.4ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 22.1ms | 1.3× | 2/6 | 43.7ms | 21.6ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 241.0ms | 38.9× | 4/6 | 269.0ms | 28.0ms | 23.1 MB | 2/6 | 654353666 |
| elixir | 85.8ms | 13.8× | 3/6 | 341.3ms | 255.5ms | 81.5 MB | 6/6 | 654353666 |
| python | 468.7ms | 75.6× | 6/6 | 479.5ms | 10.8ms | 10.3 MB | 1/6 | 654353666 |
| node | 31.7ms | 5.1× | 2/6 | 52.8ms | 21.1ms | 53.0 MB | 5/6 | 654353666 |
| ruby | 299.5ms | 48.3× | 5/6 | 343.9ms | 44.4ms | 23.8 MB | 3/6 | 654353666 |
| dotnet | 6.2ms | 1.0× | 1/6 | 27.8ms | 21.6ms | 26.9 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 807.2ms | 19.1× | 6/6 | 835.2ms | 28.0ms | 182.1 MB | 5/6 | 3388889 |
| elixir | 132.6ms | 3.1× | 5/6 | 388.1ms | 255.5ms | 198.6 MB | 6/6 | 3388889 |
| python | 42.3ms | 1.0× | 1/6 | 53.1ms | 10.8ms | 39.7 MB | 1/6 | 3388889 |
| node | 54.3ms | 1.3× | 3/6 | 75.4ms | 21.1ms | 95.9 MB | 4/6 | 3388889 |
| ruby | 94.0ms | 2.2× | 4/6 | 138.4ms | 44.4ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 45.6ms | 1.1× | 2/6 | 67.2ms | 21.6ms | 56.9 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 974.5ms | 33.4× | 6/6 | 1.002s | 28.0ms | 56.9 MB | 5/6 | 374854840 |
| elixir | 189.7ms | 6.5× | 5/6 | 445.2ms | 255.5ms | 78.5 MB | 6/6 | 374854840 |
| python | 186.4ms | 6.4× | 4/6 | 197.2ms | 10.8ms | 9.8 MB | 1/6 | 374854840 |
| node | 29.2ms | 1.0× | 1/6 | 50.3ms | 21.1ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 68.6ms | 2.3× | 3/6 | 113.0ms | 44.4ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 50.9ms | 1.7× | 2/6 | 72.5ms | 21.6ms | 27.6 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 452.4ms | 27.4× | 6/6 | 480.4ms | 28.0ms | 26.2 MB | 3/6 | 1638200 |
| elixir | 64.6ms | 3.9× | 3/6 | 320.1ms | 255.5ms | 81.3 MB | 6/6 | 1638200 |
| python | 109.8ms | 6.7× | 5/6 | 120.6ms | 10.8ms | 9.9 MB | 1/6 | 1638200 |
| node | 33.2ms | 2.0× | 2/6 | 54.3ms | 21.1ms | 56.7 MB | 5/6 | 1638200 |
| ruby | 107.3ms | 6.5× | 4/6 | 151.7ms | 44.4ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 16.5ms | 1.0× | 1/6 | 38.1ms | 21.6ms | 32.5 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 282.4ms | 4.3× | 6/6 | 310.4ms | 28.0ms | 86.6 MB | 5/6 | 46468819 |
| elixir | 132.5ms | 2.0× | 4/6 | 388.0ms | 255.5ms | 164.8 MB | 6/6 | 46468819 |
| python | 200.2ms | 3.0× | 5/6 | 211.0ms | 10.8ms | 25.9 MB | 1/6 | 46468819 |
| node | 118.1ms | 1.8× | 3/6 | 139.2ms | 21.1ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 83.5ms | 1.3× | 2/6 | 127.9ms | 44.4ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 65.7ms | 1.0× | 1/6 | 87.3ms | 21.6ms | 29.9 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 522.7ms | 27.1× | 6/6 | 550.7ms | 28.0ms | 24.2 MB | 3/6 | 724 |
| elixir | 64.7ms | 3.4× | 4/6 | 320.2ms | 255.5ms | 81.5 MB | 6/6 | 724 |
| python | 63.4ms | 3.3× | 3/6 | 74.2ms | 10.8ms | 9.7 MB | 1/6 | 724 |
| node | 21.4ms | 1.1× | 2/6 | 42.5ms | 21.1ms | 51.2 MB | 5/6 | 724 |
| ruby | 131.7ms | 6.8× | 5/6 | 176.1ms | 44.4ms | 23.8 MB | 2/6 | 724 |
| dotnet | 19.3ms | 1.0× | 1/6 | 40.9ms | 21.6ms | 29.3 MB | 4/6 | 724 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 121.9ms | 15.6× | 6/6 | 149.9ms | 28.0ms | 33.4 MB | 4/6 | 155553889038886 |
| elixir | 16.7ms | 2.1× | 3/6 | 272.2ms | 255.5ms | 79.1 MB | 6/6 | 155553889038886 |
| python | 9.0ms | 1.2× | 2/6 | 19.8ms | 10.8ms | 9.8 MB | 1/6 | 155553889038886 |
| node | 7.8ms | 1.0× | 1/6 | 28.9ms | 21.1ms | 52.5 MB | 5/6 | 155553889038886 |
| ruby | 17.9ms | 2.3× | 4/6 | 62.3ms | 44.4ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 22.3ms | 2.9× | 5/6 | 43.9ms | 21.6ms | 28.1 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 516.1ms | 27.9× | 4/6 | 544.1ms | 28.0ms | 118.9 MB | 5/6 | 6100000 |
| elixir | 67.0ms | 3.6× | 3/6 | 322.5ms | 255.5ms | 89.2 MB | 4/6 | 6100000 |
| python | 555.3ms | 30.0× | 5/6 | 566.1ms | 10.8ms | 27.9 MB | 1/6 | 6100000 |
| node | 51.4ms | 2.8× | 2/6 | 72.5ms | 21.1ms | 51.9 MB | 3/6 | 6100000 |
| ruby | 1.583s | 85.5× | 6/6 | 1.627s | 44.4ms | 137.2 MB | 6/6 | 6100000 |
| dotnet | 18.5ms | 1.0× | 1/6 | 40.1ms | 21.6ms | 30.7 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 403.9ms | 10.5× | 4/6 | 431.9ms | 28.0ms | 17.4 MB | 1/6 | 31781100 |
| elixir | 122.1ms | 3.2× | 3/6 | 377.6ms | 255.5ms | 81.8 MB | 5/6 | 31781100 |
| python | 705.1ms | 18.4× | 6/6 | 715.9ms | 10.8ms | 22.2 MB | 2/6 | 31781100 |
| node | 113.7ms | 3.0× | 2/6 | 134.8ms | 21.1ms | 183.2 MB | 6/6 | 31781100 |
| ruby | 443.9ms | 11.6× | 5/6 | 488.3ms | 44.4ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 38.3ms | 1.0× | 1/6 | 59.9ms | 21.6ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 148.1ms | 1.3× | 2/6 | 176.1ms | 28.0ms | 102.4 MB | 5/6 | 500 |
| elixir | 730.1ms | 6.3× | 6/6 | 985.6ms | 255.5ms | 552.9 MB | 6/6 | 500 |
| python | 179.4ms | 1.5× | 4/6 | 190.2ms | 10.8ms | 48.4 MB | 2/6 | 500 |
| node | 115.9ms | 1.0× | 1/6 | 137.0ms | 21.1ms | 65.1 MB | 4/6 | 500 |
| ruby | 208.3ms | 1.8× | 5/6 | 252.7ms | 44.4ms | 50.0 MB | 3/6 | 500 |
| dotnet | 151.6ms | 1.3× | 3/6 | 173.2ms | 21.6ms | 47.9 MB | 1/6 | 500 |
