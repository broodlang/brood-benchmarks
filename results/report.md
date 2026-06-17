# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-17 10:33.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 5 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 36.0ms | 3.4× | 4/6 | 36.0ms | — | 21.3 MB | 2/6 | 0 |
| elixir | 191.0ms | 18.2× | 6/6 | 191.0ms | — | 69.8 MB | 6/6 | 0 |
| python | 10.5ms | 1.0× | 1/6 | 10.5ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.0ms | 1.7× | 2/6 | 18.0ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 41.0ms | 3.9× | 5/6 | 41.0ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 26.4ms | 2.5× | 3/6 | 26.4ms | — | 26.0 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 501.9ms | 10.8× | 4/6 | 537.9ms | 36.0ms | 24.6 MB | 3/6 | 9227465 |
| elixir | 87.4ms | 1.9× | 3/6 | 278.4ms | 191.0ms | 69.7 MB | 6/6 | 9227465 |
| python | 763.2ms | 16.4× | 6/6 | 773.7ms | 10.5ms | 9.8 MB | 1/6 | 9227465 |
| node | 82.4ms | 1.8× | 2/6 | 100.4ms | 18.0ms | 48.8 MB | 5/6 | 9227465 |
| ruby | 626.4ms | 13.4× | 5/6 | 667.4ms | 41.0ms | 23.5 MB | 2/6 | 9227465 |
| dotnet | 46.6ms | 1.0× | 1/6 | 73.0ms | 26.4ms | 25.9 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 113.6ms | 13.9× | 4/6 | 149.6ms | 36.0ms | 24.7 MB | 3/6 | 449999985000000 |
| elixir | 63.5ms | 7.7× | 3/6 | 254.5ms | 191.0ms | 69.8 MB | 6/6 | 449999985000000 |
| python | 2.490s | 303.7× | 6/6 | 2.501s | 10.5ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 44.9ms | 5.5× | 2/6 | 62.9ms | 18.0ms | 50.6 MB | 5/6 | 449999985000000 |
| ruby | 608.0ms | 74.1× | 5/6 | 649.0ms | 41.0ms | 23.5 MB | 2/6 | 449999985000000 |
| dotnet | 8.2ms | 1.0× | 1/6 | 34.6ms | 26.4ms | 26.3 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 116.9ms | 5.5× | 3/6 | 152.9ms | 36.0ms | 21.5 MB | 2/6 | 12499997500000 |
| elixir | 43.6ms | 2.1× | 2/6 | 234.6ms | 191.0ms | 70.3 MB | 5/6 | 12499997500000 |
| python | 123.4ms | 5.8× | 4/6 | 133.9ms | 10.5ms | 10.6 MB | 1/6 | 12499997500000 |
| node | 241.6ms | 11.4× | 5/6 | 259.6ms | 18.0ms | 90.8 MB | 6/6 | 12499997500000 |
| ruby | 249.2ms | 11.8× | 6/6 | 290.2ms | 41.0ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 21.2ms | 1.0× | 1/6 | 47.6ms | 26.4ms | 27.8 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 53.9ms | 7.3× | 4/6 | 89.9ms | 36.0ms | 24.7 MB | 3/6 | 13848 |
| elixir | 16.8ms | 2.3× | 3/6 | 207.8ms | 191.0ms | 70.4 MB | 6/6 | 13848 |
| python | 131.3ms | 17.7× | 6/6 | 141.8ms | 10.5ms | 9.9 MB | 1/6 | 13848 |
| node | 11.8ms | 1.6× | 2/6 | 29.8ms | 18.0ms | 49.2 MB | 5/6 | 13848 |
| ruby | 122.8ms | 16.6× | 5/6 | 163.8ms | 41.0ms | 23.5 MB | 2/6 | 13848 |
| dotnet | 7.4ms | 1.0× | 1/6 | 33.8ms | 26.4ms | 26.3 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 494.1ms | 9.2× | 4/6 | 530.1ms | 36.0ms | 38.1 MB | 4/6 | 442 |
| elixir | 104.4ms | 2.0× | 2/6 | 295.4ms | 191.0ms | 69.7 MB | 6/6 | 442 |
| python | 2.450s | 45.8× | 6/6 | 2.460s | 10.5ms | 9.8 MB | 1/6 | 442 |
| node | 188.3ms | 3.5× | 3/6 | 206.3ms | 18.0ms | 49.1 MB | 5/6 | 442 |
| ruby | 891.7ms | 16.7× | 5/6 | 932.7ms | 41.0ms | 23.5 MB | 2/6 | 442 |
| dotnet | 53.5ms | 1.0× | 1/6 | 79.9ms | 26.4ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 233.6ms | 11.5× | 3/6 | 269.6ms | 36.0ms | 24.8 MB | 3/6 | 6129302 |
| elixir | 273.6ms | 13.4× | 4/6 | 464.6ms | 191.0ms | 70.5 MB | 6/6 | 6129302 |
| python | 1.373s | 67.3× | 6/6 | 1.384s | 10.5ms | 10.0 MB | 1/6 | 6129302 |
| node | 30.6ms | 1.5× | 2/6 | 48.6ms | 18.0ms | 49.9 MB | 5/6 | 6129302 |
| ruby | 446.3ms | 21.9× | 5/6 | 487.3ms | 41.0ms | 23.6 MB | 2/6 | 6129302 |
| dotnet | 20.4ms | 1.0× | 1/6 | 46.8ms | 26.4ms | 26.3 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 173.6ms | 144.7× | 4/6 | 209.6ms | 36.0ms | 36.1 MB | 4/6 | 654353666 |
| elixir | 74.3ms | 61.9× | 3/6 | 265.3ms | 191.0ms | 75.6 MB | 6/6 | 654353666 |
| python | 460.4ms | 383.7× | 6/6 | 470.9ms | 10.5ms | 10.3 MB | 1/6 | 654353666 |
| node | 37.7ms | 31.4× | 2/6 | 55.7ms | 18.0ms | 52.8 MB | 5/6 | 654353666 |
| ruby | 309.2ms | 257.7× | 5/6 | 350.2ms | 41.0ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 1.2ms | 1.0× | 1/6 | 27.6ms | 26.4ms | 26.9 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 10.8ms | 1.0× | 1/6 | 46.8ms | 36.0ms | 31.7 MB | 1/6 | 3388889 |
| elixir | 117.1ms | 10.8× | 6/6 | 308.1ms | 191.0ms | 199.3 MB | 6/6 | 3388889 |
| python | 51.2ms | 4.7× | 3/6 | 61.7ms | 10.5ms | 39.8 MB | 2/6 | 3388889 |
| node | 71.3ms | 6.6× | 4/6 | 89.3ms | 18.0ms | 96.0 MB | 5/6 | 3388889 |
| ruby | 96.4ms | 8.9× | 5/6 | 137.4ms | 41.0ms | 52.1 MB | 3/6 | 3388889 |
| dotnet | 25.7ms | 2.4× | 2/6 | 52.1ms | 26.4ms | 56.8 MB | 4/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 882.3ms | 19.7× | 6/6 | 918.3ms | 36.0ms | 90.6 MB | 6/6 | 374854840 |
| elixir | 179.9ms | 4.0× | 4/6 | 370.9ms | 191.0ms | 70.6 MB | 5/6 | 374854840 |
| python | 186.6ms | 4.2× | 5/6 | 197.1ms | 10.5ms | 9.9 MB | 1/6 | 374854840 |
| node | 44.9ms | 1.0× | 1/6 | 62.9ms | 18.0ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 86.9ms | 1.9× | 3/6 | 127.9ms | 41.0ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 45.8ms | 1.0× | 2/6 | 72.2ms | 26.4ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 408.0ms | 17.5× | 6/6 | 444.0ms | 36.0ms | 35.3 MB | 4/6 | 1638200 |
| elixir | 23.3ms | 1.0× | 1/6 | 214.3ms | 191.0ms | 70.2 MB | 6/6 | 1638200 |
| python | 109.0ms | 4.7× | 4/6 | 119.5ms | 10.5ms | 10.0 MB | 1/6 | 1638200 |
| node | 36.1ms | 1.5× | 3/6 | 54.1ms | 18.0ms | 56.8 MB | 5/6 | 1638200 |
| ruby | 110.4ms | 4.7× | 5/6 | 151.4ms | 41.0ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 23.5ms | 1.0× | 2/6 | 49.9ms | 26.4ms | 32.5 MB | 3/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 292.6ms | 4.8× | 6/6 | 328.6ms | 36.0ms | 120.5 MB | 5/6 | 46468819 |
| elixir | 120.7ms | 2.0× | 4/6 | 311.7ms | 191.0ms | 157.5 MB | 6/6 | 46468819 |
| python | 200.9ms | 3.3× | 5/6 | 211.4ms | 10.5ms | 26.0 MB | 1/6 | 46468819 |
| node | 117.8ms | 1.9× | 3/6 | 135.8ms | 18.0ms | 65.7 MB | 4/6 | 46468819 |
| ruby | 72.6ms | 1.2× | 2/6 | 113.6ms | 41.0ms | 29.1 MB | 2/6 | 46468819 |
| dotnet | 61.3ms | 1.0× | 1/6 | 87.7ms | 26.4ms | 29.8 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 568.7ms | 38.2× | 6/6 | 604.7ms | 36.0ms | 32.6 MB | 4/6 | 724 |
| elixir | 20.9ms | 1.4× | 2/6 | 211.9ms | 191.0ms | 70.3 MB | 6/6 | 724 |
| python | 68.1ms | 4.6× | 4/6 | 78.6ms | 10.5ms | 9.8 MB | 1/6 | 724 |
| node | 14.9ms | 1.0× | 1/6 | 32.9ms | 18.0ms | 51.3 MB | 5/6 | 724 |
| ruby | 137.6ms | 9.2× | 5/6 | 178.6ms | 41.0ms | 23.8 MB | 2/6 | 724 |
| dotnet | 27.6ms | 1.9× | 3/6 | 54.0ms | 26.4ms | 29.4 MB | 3/6 | 724 |

## errors — error handling — raise + recover a value N times  (N=200000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 190.7ms | 5.9× | 4/6 | 226.7ms | 36.0ms | 38.1 MB | 4/6 | 9900000 |
| elixir | 32.3ms | 1.0× | 1/6 | 223.3ms | 191.0ms | 69.9 MB | 6/6 | 9900000 |
| python | 59.7ms | 1.8× | 2/6 | 70.2ms | 10.5ms | 9.8 MB | 1/6 | 9900000 |
| node | 573.4ms | 17.8× | 6/6 | 591.4ms | 18.0ms | 51.0 MB | 5/6 | 9900000 |
| ruby | 123.7ms | 3.8× | 3/6 | 164.7ms | 41.0ms | 26.1 MB | 2/6 | 9900000 |
| dotnet | 295.6ms | 9.2× | 5/6 | 322.0ms | 26.4ms | 32.5 MB | 3/6 | 9900000 |

## errors-deep — error propagation — throw 50 frames deep, catch at top  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 271.3ms | 20.7× | 5/6 | 307.3ms | 36.0ms | 39.2 MB | 4/6 | 2475000 |
| elixir | 13.1ms | 1.0× | 1/6 | 204.1ms | 191.0ms | 73.0 MB | 6/6 | 2475000 |
| python | 223.5ms | 17.1× | 3/6 | 234.0ms | 10.5ms | 9.9 MB | 1/6 | 2475000 |
| node | 224.8ms | 17.2× | 4/6 | 242.8ms | 18.0ms | 50.8 MB | 5/6 | 2475000 |
| ruby | 110.8ms | 8.5× | 2/6 | 151.8ms | 41.0ms | 30.1 MB | 2/6 | 2475000 |
| dotnet | 704.7ms | 53.8× | 6/6 | 731.1ms | 26.4ms | 32.7 MB | 3/6 | 2475000 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 50.2ms | 11.2× | 6/6 | 86.2ms | 36.0ms | 24.8 MB | 3/6 | 155553889038886 |
| elixir | 7.5ms | 1.7× | 2/6 | 198.5ms | 191.0ms | 72.3 MB | 6/6 | 155553889038886 |
| python | 4.5ms | 1.0× | 1/6 | 15.0ms | 10.5ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 14.0ms | 3.1× | 3/6 | 32.0ms | 18.0ms | 52.7 MB | 5/6 | 155553889038886 |
| ruby | 22.2ms | 4.9× | 5/6 | 63.2ms | 41.0ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 17.1ms | 3.8× | 4/6 | 43.5ms | 26.4ms | 28.1 MB | 4/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.8ms | 7.6× | 4/6 | 139.8ms | 36.0ms | 69.9 MB | 4/6 | 6100000 |
| elixir | 14.0ms | 1.0× | 2/6 | 205.0ms | 191.0ms | 75.6 MB | 5/6 | 6100000 |
| python | 551.9ms | 40.6× | 5/6 | 562.4ms | 10.5ms | 28.1 MB | 1/6 | 6100000 |
| node | 59.1ms | 4.3× | 3/6 | 77.1ms | 18.0ms | 51.9 MB | 3/6 | 6100000 |
| ruby | 1.577s | 116.0× | 6/6 | 1.618s | 41.0ms | 138.0 MB | 6/6 | 6100000 |
| dotnet | 13.6ms | 1.0× | 1/6 | 40.0ms | 26.4ms | 30.9 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 340.1ms | 11.2× | 4/6 | 376.1ms | 36.0ms | 26.7 MB | 3/6 | 31781100 |
| elixir | 94.6ms | 3.1× | 2/6 | 285.6ms | 191.0ms | 72.4 MB | 5/6 | 31781100 |
| python | 675.9ms | 22.2× | 6/6 | 686.4ms | 10.5ms | 22.3 MB | 1/6 | 31781100 |
| node | 120.6ms | 4.0× | 3/6 | 138.6ms | 18.0ms | 183.0 MB | 6/6 | 31781100 |
| ruby | 439.9ms | 14.5× | 5/6 | 480.9ms | 41.0ms | 23.7 MB | 2/6 | 31781100 |
| dotnet | 30.4ms | 1.0× | 1/6 | 56.8ms | 26.4ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 143.7ms | 1.2× | 2/6 | 179.7ms | 36.0ms | 123.1 MB | 5/6 | 500 |
| elixir | 652.8ms | 5.3× | 6/6 | 843.8ms | 191.0ms | 520.3 MB | 6/6 | 500 |
| python | 177.9ms | 1.4× | 4/6 | 188.4ms | 10.5ms | 48.7 MB | 2/6 | 500 |
| node | 123.0ms | 1.0× | 1/6 | 141.0ms | 18.0ms | 65.2 MB | 4/6 | 500 |
| ruby | 208.3ms | 1.7× | 5/6 | 249.3ms | 41.0ms | 50.1 MB | 3/6 | 500 |
| dotnet | 153.8ms | 1.3× | 3/6 | 180.2ms | 26.4ms | 48.1 MB | 1/6 | 500 |
