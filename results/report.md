# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-15 21:37.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.1ms | 3.2× | 4/6 | 36.1ms | — | 12.8 MB | 2/6 | 0 |
| elixir | 282.0ms | 25.0× | 6/6 | 282.0ms | — | 76.1 MB | 6/6 | 0 |
| python | 11.3ms | 1.0× | 1/6 | 11.3ms | — | 9.7 MB | 1/6 | 0 |
| node | 19.4ms | 1.7× | 2/6 | 19.4ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 46.5ms | 4.1× | 5/6 | 46.5ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 23.8ms | 2.1× | 3/6 | 23.8ms | — | 25.8 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 692.7ms | 15.4× | 5/6 | 728.8ms | 36.1ms | 13.2 MB | 2/6 | 9227465 |
| elixir | 137.0ms | 3.1× | 3/6 | 419.0ms | 282.0ms | 80.6 MB | 6/6 | 9227465 |
| python | 805.4ms | 17.9× | 6/6 | 816.7ms | 11.3ms | 9.7 MB | 1/6 | 9227465 |
| node | 80.2ms | 1.8× | 2/6 | 99.6ms | 19.4ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 668.8ms | 14.9× | 4/6 | 715.3ms | 46.5ms | 23.6 MB | 3/6 | 9227465 |
| dotnet | 44.9ms | 1.0× | 1/6 | 68.7ms | 23.8ms | 26.1 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 168.0ms | 12.8× | 4/6 | 204.1ms | 36.1ms | 13.2 MB | 2/6 | 449999985000000 |
| elixir | 103.5ms | 7.9× | 3/6 | 385.5ms | 282.0ms | 80.7 MB | 6/6 | 449999985000000 |
| python | 2.496s | 190.5× | 6/6 | 2.507s | 11.3ms | 9.7 MB | 1/6 | 449999985000000 |
| node | 34.7ms | 2.6× | 2/6 | 54.1ms | 19.4ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 594.2ms | 45.4× | 5/6 | 640.7ms | 46.5ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 13.1ms | 1.0× | 1/6 | 36.9ms | 23.8ms | 26.5 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 110.0ms | 8.1× | 3/6 | 146.1ms | 36.1ms | 12.7 MB | 2/6 | 12499997500000 |
| elixir | 49.1ms | 3.6× | 2/6 | 331.1ms | 282.0ms | 76.9 MB | 5/6 | 12499997500000 |
| python | 119.5ms | 8.8× | 4/6 | 130.8ms | 11.3ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 240.5ms | 17.7× | 6/6 | 259.9ms | 19.4ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 240.3ms | 17.7× | 5/6 | 286.8ms | 46.5ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 13.6ms | 1.0× | 1/6 | 37.4ms | 23.8ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 44.0ms | 4.2× | 3/6 | 80.1ms | 36.1ms | 13.3 MB | 2/6 | 13848 |
| elixir | 78.9ms | 7.4× | 4/6 | 360.9ms | 282.0ms | 81.1 MB | 6/6 | 13848 |
| python | 134.8ms | 12.7× | 6/6 | 146.1ms | 11.3ms | 9.9 MB | 1/6 | 13848 |
| node | 11.3ms | 1.1× | 2/6 | 30.7ms | 19.4ms | 49.2 MB | 5/6 | 13848 |
| ruby | 125.0ms | 11.8× | 5/6 | 171.5ms | 46.5ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 10.6ms | 1.0× | 1/6 | 34.4ms | 23.8ms | 26.3 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 543.0ms | 11.0× | 4/6 | 579.1ms | 36.1ms | 27.9 MB | 4/6 | 442 |
| elixir | 166.2ms | 3.4× | 2/6 | 448.2ms | 282.0ms | 80.8 MB | 6/6 | 442 |
| python | 2.643s | 53.7× | 6/6 | 2.655s | 11.3ms | 9.7 MB | 1/6 | 442 |
| node | 191.1ms | 3.9× | 3/6 | 210.5ms | 19.4ms | 49.1 MB | 5/6 | 442 |
| ruby | 937.6ms | 19.1× | 5/6 | 984.1ms | 46.5ms | 23.5 MB | 2/6 | 442 |
| dotnet | 49.2ms | 1.0× | 1/6 | 73.0ms | 23.8ms | 26.3 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 252.8ms | 12.5× | 3/6 | 288.9ms | 36.1ms | 13.5 MB | 2/6 | 6129302 |
| elixir | 321.6ms | 15.8× | 4/6 | 603.6ms | 282.0ms | 82.0 MB | 6/6 | 6129302 |
| python | 1.423s | 70.1× | 6/6 | 1.435s | 11.3ms | 10.0 MB | 1/6 | 6129302 |
| node | 22.8ms | 1.1× | 2/6 | 42.2ms | 19.4ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 457.9ms | 22.6× | 5/6 | 504.4ms | 46.5ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 20.3ms | 1.0× | 1/6 | 44.1ms | 23.8ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 192.1ms | 35.6× | 4/6 | 228.2ms | 36.1ms | 20.6 MB | 2/6 | 654353666 |
| elixir | 92.1ms | 17.1× | 3/6 | 374.1ms | 282.0ms | 81.4 MB | 6/6 | 654353666 |
| python | 523.9ms | 97.0× | 6/6 | 535.2ms | 11.3ms | 10.4 MB | 1/6 | 654353666 |
| node | 26.1ms | 4.8× | 2/6 | 45.5ms | 19.4ms | 52.9 MB | 5/6 | 654353666 |
| ruby | 317.2ms | 58.7× | 5/6 | 363.7ms | 46.5ms | 23.8 MB | 3/6 | 654353666 |
| dotnet | 5.4ms | 1.0× | 1/6 | 29.2ms | 23.8ms | 26.8 MB | 4/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.4ms | 1.0× | 1/6 | 46.5ms | 36.1ms | 16.4 MB | 1/6 | 3388889 |
| elixir | 162.3ms | 15.6× | 6/6 | 444.3ms | 282.0ms | 198.6 MB | 6/6 | 3388889 |
| python | 46.7ms | 4.5× | 3/6 | 58.0ms | 11.3ms | 39.8 MB | 2/6 | 3388889 |
| node | 63.9ms | 6.1× | 4/6 | 83.3ms | 19.4ms | 96.1 MB | 5/6 | 3388889 |
| ruby | 90.5ms | 8.7× | 5/6 | 137.0ms | 46.5ms | 52.1 MB | 3/6 | 3388889 |
| dotnet | 35.2ms | 3.4× | 2/6 | 59.0ms | 23.8ms | 56.9 MB | 4/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.092s | 31.1× | 6/6 | 1.129s | 36.1ms | 54.5 MB | 5/6 | 374854840 |
| elixir | 197.7ms | 5.6× | 5/6 | 479.7ms | 282.0ms | 78.4 MB | 6/6 | 374854840 |
| python | 189.6ms | 5.4× | 4/6 | 200.9ms | 11.3ms | 9.9 MB | 1/6 | 374854840 |
| node | 35.1ms | 1.0× | 1/6 | 54.5ms | 19.4ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 76.8ms | 2.2× | 3/6 | 123.3ms | 46.5ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 39.0ms | 1.1× | 2/6 | 62.8ms | 23.8ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 480.5ms | 32.9× | 6/6 | 516.6ms | 36.1ms | 23.4 MB | 2/6 | 1638200 |
| elixir | 72.2ms | 4.9× | 3/6 | 354.2ms | 282.0ms | 81.2 MB | 6/6 | 1638200 |
| python | 102.3ms | 7.0× | 4/6 | 113.6ms | 11.3ms | 10.0 MB | 1/6 | 1638200 |
| node | 25.7ms | 1.8× | 2/6 | 45.1ms | 19.4ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 105.7ms | 7.2× | 5/6 | 152.2ms | 46.5ms | 23.8 MB | 3/6 | 1638200 |
| dotnet | 14.6ms | 1.0× | 1/6 | 38.4ms | 23.8ms | 32.4 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 309.5ms | 4.3× | 6/6 | 345.6ms | 36.1ms | 84.2 MB | 5/6 | 46468819 |
| elixir | 140.8ms | 2.0× | 4/6 | 422.8ms | 282.0ms | 164.8 MB | 6/6 | 46468819 |
| python | 229.4ms | 3.2× | 5/6 | 240.7ms | 11.3ms | 25.9 MB | 1/6 | 46468819 |
| node | 119.4ms | 1.7× | 3/6 | 138.8ms | 19.4ms | 65.6 MB | 4/6 | 46468819 |
| ruby | 81.1ms | 1.1× | 2/6 | 127.6ms | 46.5ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 72.2ms | 1.0× | 1/6 | 96.0ms | 23.8ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 599.9ms | 56.6× | 6/6 | 636.0ms | 36.1ms | 21.3 MB | 2/6 | 724 |
| elixir | 65.4ms | 6.2× | 4/6 | 347.4ms | 282.0ms | 80.6 MB | 6/6 | 724 |
| python | 60.0ms | 5.7× | 3/6 | 71.3ms | 11.3ms | 9.7 MB | 1/6 | 724 |
| node | 10.6ms | 1.0× | 1/6 | 30.0ms | 19.4ms | 51.3 MB | 5/6 | 724 |
| ruby | 138.6ms | 13.1× | 5/6 | 185.1ms | 46.5ms | 23.8 MB | 3/6 | 724 |
| dotnet | 21.0ms | 2.0× | 2/6 | 44.8ms | 23.8ms | 29.5 MB | 4/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 212.6ms | 3.9× | 4/6 | 248.7ms | 36.1ms | 33.1 MB | 4/6 | 9900000 |
| elixir | 99.1ms | 1.8× | 2/6 | 381.1ms | 282.0ms | 81.5 MB | 6/6 | 9900000 |
| python | 54.1ms | 1.0× | 1/6 | 65.4ms | 11.3ms | 9.7 MB | 1/6 | 9900000 |
| node | 632.9ms | 11.7× | 6/6 | 652.3ms | 19.4ms | 51.0 MB | 5/6 | 9900000 |
| ruby | 119.4ms | 2.2× | 3/6 | 165.9ms | 46.5ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 319.0ms | 5.9× | 5/6 | 342.8ms | 23.8ms | 32.7 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 302.1ms | 3.2× | 5/6 | 338.2ms | 36.1ms | 29.6 MB | 2/6 | 2475000 |
| elixir | 95.6ms | 1.0× | 1/6 | 377.6ms | 282.0ms | 82.9 MB | 6/6 | 2475000 |
| python | 236.5ms | 2.5× | 4/6 | 247.8ms | 11.3ms | 9.8 MB | 1/6 | 2475000 |
| node | 229.3ms | 2.4× | 3/6 | 248.7ms | 19.4ms | 50.8 MB | 5/6 | 2475000 |
| ruby | 128.1ms | 1.3× | 2/6 | 174.6ms | 46.5ms | 30.1 MB | 3/6 | 2475000 |
| dotnet | 758.5ms | 7.9× | 6/6 | 782.3ms | 23.8ms | 32.6 MB | 4/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 37.5ms | 7.5× | 6/6 | 73.6ms | 36.1ms | 13.4 MB | 2/6 | 155553889038886 |
| elixir | 27.4ms | 5.5× | 5/6 | 309.4ms | 282.0ms | 79.1 MB | 6/6 | 155553889038886 |
| python | 5.0ms | 1.0× | 1/6 | 16.3ms | 11.3ms | 9.8 MB | 1/6 | 155553889038886 |
| node | 10.8ms | 2.2× | 4/6 | 30.2ms | 19.4ms | 52.5 MB | 5/6 | 155553889038886 |
| ruby | 6.9ms | 1.4× | 2/6 | 53.4ms | 46.5ms | 24.0 MB | 3/6 | 155553889038886 |
| dotnet | 8.4ms | 1.7× | 3/6 | 32.2ms | 23.8ms | 28.1 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 574.8ms | 29.8× | 4/6 | 610.9ms | 36.1ms | 116.3 MB | 5/6 | 6100000 |
| elixir | 62.2ms | 3.2× | 3/6 | 344.2ms | 282.0ms | 89.9 MB | 4/6 | 6100000 |
| python | 606.0ms | 31.4× | 5/6 | 617.3ms | 11.3ms | 28.1 MB | 1/6 | 6100000 |
| node | 57.8ms | 3.0× | 2/6 | 77.2ms | 19.4ms | 52.0 MB | 3/6 | 6100000 |
| ruby | 1.750s | 90.7× | 6/6 | 1.797s | 46.5ms | 136.1 MB | 6/6 | 6100000 |
| dotnet | 19.3ms | 1.0× | 1/6 | 43.1ms | 23.8ms | 30.8 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 447.5ms | 11.8× | 4/6 | 483.6ms | 36.1ms | 15.3 MB | 1/6 | 31781100 |
| elixir | 151.6ms | 4.0× | 3/6 | 433.6ms | 282.0ms | 83.7 MB | 5/6 | 31781100 |
| python | 799.5ms | 21.0× | 6/6 | 810.8ms | 11.3ms | 22.2 MB | 2/6 | 31781100 |
| node | 134.7ms | 3.5× | 2/6 | 154.1ms | 19.4ms | 183.4 MB | 6/6 | 31781100 |
| ruby | 495.7ms | 13.0× | 5/6 | 542.2ms | 46.5ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 38.0ms | 1.0× | 1/6 | 61.8ms | 23.8ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 165.2ms | 1.2× | 3/6 | 201.3ms | 36.1ms | 104.5 MB | 5/6 | 500 |
| elixir | 779.4ms | 5.6× | 6/6 | 1.061s | 282.0ms | 579.4 MB | 6/6 | 500 |
| python | 200.4ms | 1.4× | 4/6 | 211.7ms | 11.3ms | 46.9 MB | 1/6 | 500 |
| node | 138.3ms | 1.0× | 1/6 | 157.7ms | 19.4ms | 65.3 MB | 4/6 | 500 |
| ruby | 234.8ms | 1.7× | 5/6 | 281.3ms | 46.5ms | 50.0 MB | 3/6 | 500 |
| dotnet | 165.2ms | 1.2× | 2/6 | 189.0ms | 23.8ms | 48.1 MB | 2/6 | 500 |
