# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-14 11:25.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.
> **Isolation:** taskset pin (compute→core 11, concurrency→0-11); 0.25s settle.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.0ms | 2.5× | 4/6 | 28.0ms | — | 13.7 MB | 2/6 | 0 |
| elixir | 262.1ms | 23.4× | 6/6 | 262.1ms | — | 78.8 MB | 6/6 | 0 |
| python | 11.2ms | 1.0× | 1/6 | 11.2ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.6ms | 1.6× | 2/6 | 17.6ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 40.9ms | 3.7× | 5/6 | 40.9ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 24.7ms | 2.2× | 3/6 | 24.7ms | — | 25.9 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=35)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 637.3ms | 12.7× | 5/6 | 665.3ms | 28.0ms | 14.2 MB | 2/6 | 9227465 |
| elixir | 121.1ms | 2.4× | 3/6 | 383.2ms | 262.1ms | 80.7 MB | 6/6 | 9227465 |
| python | 739.7ms | 14.7× | 6/6 | 750.9ms | 11.2ms | 9.8 MB | 1/6 | 9227465 |
| node | 74.2ms | 1.5× | 2/6 | 91.8ms | 17.6ms | 48.7 MB | 5/6 | 9227465 |
| ruby | 626.3ms | 12.5× | 4/6 | 667.2ms | 40.9ms | 23.5 MB | 3/6 | 9227465 |
| dotnet | 50.3ms | 1.0× | 1/6 | 75.0ms | 24.7ms | 25.9 MB | 4/6 | 9227465 |

## loop — raw iteration (tail recursion vs for-loop)  (N=30000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 192.9ms | 8.4× | 4/6 | 220.9ms | 28.0ms | 14.2 MB | 2/6 | 449999985000000 |
| elixir | 97.3ms | 4.2× | 3/6 | 359.4ms | 262.1ms | 81.8 MB | 6/6 | 449999985000000 |
| python | 2.383s | 104.0× | 6/6 | 2.394s | 11.2ms | 9.8 MB | 1/6 | 449999985000000 |
| node | 44.8ms | 2.0× | 2/6 | 62.4ms | 17.6ms | 50.5 MB | 5/6 | 449999985000000 |
| ruby | 598.7ms | 26.1× | 5/6 | 639.6ms | 40.9ms | 23.5 MB | 3/6 | 449999985000000 |
| dotnet | 22.9ms | 1.0× | 1/6 | 47.6ms | 24.7ms | 26.4 MB | 4/6 | 449999985000000 |

## reduce — higher-order fold over a range  (N=5000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 114.5ms | 10.1× | 4/6 | 142.5ms | 28.0ms | 13.5 MB | 2/6 | 12499997500000 |
| elixir | 36.2ms | 3.2× | 2/6 | 298.3ms | 262.1ms | 78.2 MB | 5/6 | 12499997500000 |
| python | 110.0ms | 9.7× | 3/6 | 121.2ms | 11.2ms | 10.5 MB | 1/6 | 12499997500000 |
| node | 234.7ms | 20.8× | 5/6 | 252.3ms | 17.6ms | 90.7 MB | 6/6 | 12499997500000 |
| ruby | 240.6ms | 21.3× | 6/6 | 281.5ms | 40.9ms | 23.5 MB | 3/6 | 12499997500000 |
| dotnet | 11.3ms | 1.0× | 1/6 | 36.0ms | 24.7ms | 27.7 MB | 4/6 | 12499997500000 |

## primes — integer arithmetic (trial division)  (N=150000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 350.6ms | 70.1× | 6/6 | 378.6ms | 28.0ms | 13.6 MB | 2/6 | 13848 |
| elixir | 50.7ms | 10.1× | 3/6 | 312.8ms | 262.1ms | 81.0 MB | 6/6 | 13848 |
| python | 135.0ms | 27.0× | 5/6 | 146.2ms | 11.2ms | 9.9 MB | 1/6 | 13848 |
| node | 16.2ms | 3.2× | 2/6 | 33.8ms | 17.6ms | 49.2 MB | 5/6 | 13848 |
| ruby | 131.2ms | 26.2× | 4/6 | 172.1ms | 40.9ms | 23.5 MB | 3/6 | 13848 |
| dotnet | 5.0ms | 1.0× | 1/6 | 29.7ms | 24.7ms | 26.4 MB | 4/6 | 13848 |

## collatz — integer arithmetic + tight inner loop  (N=250000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 464.9ms | 8.9× | 4/6 | 492.9ms | 28.0ms | 28.6 MB | 4/6 | 442 |
| elixir | 150.3ms | 2.9× | 2/6 | 412.4ms | 262.1ms | 81.8 MB | 6/6 | 442 |
| python | 2.612s | 49.9× | 6/6 | 2.623s | 11.2ms | 9.7 MB | 1/6 | 442 |
| node | 179.5ms | 3.4× | 3/6 | 197.1ms | 17.6ms | 49.0 MB | 5/6 | 442 |
| ruby | 871.2ms | 16.7× | 5/6 | 912.1ms | 40.9ms | 23.5 MB | 2/6 | 442 |
| dotnet | 52.3ms | 1.0× | 1/6 | 77.0ms | 24.7ms | 26.4 MB | 3/6 | 442 |

## mandelbrot — floating-point math (escape iterations)  (N=540)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.277s | 70.2× | 5/6 | 1.305s | 28.0ms | 13.6 MB | 2/6 | 6129302 |
| elixir | 279.3ms | 15.3× | 3/6 | 541.4ms | 262.1ms | 81.4 MB | 6/6 | 6129302 |
| python | 1.423s | 78.2× | 6/6 | 1.434s | 11.2ms | 10.0 MB | 1/6 | 6129302 |
| node | 33.7ms | 1.9× | 2/6 | 51.3ms | 17.6ms | 49.8 MB | 5/6 | 6129302 |
| ruby | 442.1ms | 24.3× | 4/6 | 483.0ms | 40.9ms | 23.6 MB | 3/6 | 6129302 |
| dotnet | 18.2ms | 1.0× | 1/6 | 42.9ms | 24.7ms | 26.4 MB | 4/6 | 6129302 |

## matmul — nested loops + indexing (integer NxN)  (N=175)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 538.6ms | 91.3× | 6/6 | 566.6ms | 28.0ms | 32.2 MB | 4/6 | 654353666 |
| elixir | 82.6ms | 14.0× | 3/6 | 344.7ms | 262.1ms | 81.7 MB | 6/6 | 654353666 |
| python | 456.2ms | 77.3× | 5/6 | 467.4ms | 11.2ms | 10.3 MB | 1/6 | 654353666 |
| node | 35.5ms | 6.0× | 2/6 | 53.1ms | 17.6ms | 52.8 MB | 5/6 | 654353666 |
| ruby | 312.5ms | 53.0× | 4/6 | 353.4ms | 40.9ms | 23.8 MB | 2/6 | 654353666 |
| dotnet | 5.9ms | 1.0× | 1/6 | 30.6ms | 24.7ms | 26.8 MB | 3/6 | 654353666 |

## strings — string building (join) + length  (N=500000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 795.2ms | 18.9× | 6/6 | 823.2ms | 28.0ms | 176.0 MB | 5/6 | 3388889 |
| elixir | 121.9ms | 2.9× | 5/6 | 384.0ms | 262.1ms | 198.7 MB | 6/6 | 3388889 |
| python | 48.4ms | 1.1× | 2/6 | 59.6ms | 11.2ms | 39.8 MB | 1/6 | 3388889 |
| node | 58.3ms | 1.4× | 3/6 | 75.9ms | 17.6ms | 96.0 MB | 4/6 | 3388889 |
| ruby | 86.9ms | 2.1× | 4/6 | 127.8ms | 40.9ms | 52.1 MB | 2/6 | 3388889 |
| dotnet | 42.1ms | 1.0× | 1/6 | 66.8ms | 24.7ms | 56.9 MB | 3/6 | 3388889 |

## wordcount — hash-map build (immutable vs mutable)  (N=750000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 982.6ms | 28.8× | 6/6 | 1.011s | 28.0ms | 55.5 MB | 5/6 | 374854840 |
| elixir | 186.6ms | 5.5× | 5/6 | 448.7ms | 262.1ms | 78.5 MB | 6/6 | 374854840 |
| python | 184.5ms | 5.4× | 4/6 | 195.7ms | 11.2ms | 9.9 MB | 1/6 | 374854840 |
| node | 46.1ms | 1.4× | 2/6 | 63.7ms | 17.6ms | 50.7 MB | 4/6 | 374854840 |
| ruby | 70.9ms | 2.1× | 3/6 | 111.8ms | 40.9ms | 23.5 MB | 2/6 | 374854840 |
| dotnet | 34.1ms | 1.0× | 1/6 | 58.8ms | 24.7ms | 27.5 MB | 3/6 | 374854840 |

## bintree — allocation / GC pressure (build+walk trees)  (N=200)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.123s | 43.3× | 6/6 | 1.151s | 28.0ms | 28.7 MB | 3/6 | 1638200 |
| elixir | 59.0ms | 2.3× | 3/6 | 321.1ms | 262.1ms | 82.1 MB | 6/6 | 1638200 |
| python | 108.0ms | 4.2× | 4/6 | 119.2ms | 11.2ms | 10.0 MB | 1/6 | 1638200 |
| node | 36.7ms | 1.4× | 2/6 | 54.3ms | 17.6ms | 56.7 MB | 5/6 | 1638200 |
| ruby | 113.9ms | 4.4× | 5/6 | 154.8ms | 40.9ms | 23.8 MB | 2/6 | 1638200 |
| dotnet | 25.9ms | 1.0× | 1/6 | 50.6ms | 24.7ms | 32.4 MB | 4/6 | 1638200 |

## sort — sort a list of ints + checksum walk  (N=375000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 244.0ms | 3.2× | 6/6 | 272.0ms | 28.0ms | 87.8 MB | 5/6 | 46468819 |
| elixir | 111.8ms | 1.5× | 4/6 | 373.9ms | 262.1ms | 166.1 MB | 6/6 | 46468819 |
| python | 184.9ms | 2.4× | 5/6 | 196.1ms | 11.2ms | 25.9 MB | 1/6 | 46468819 |
| node | 107.3ms | 1.4× | 3/6 | 124.9ms | 17.6ms | 65.5 MB | 4/6 | 46468819 |
| ruby | 76.5ms | 1.0× | 2/6 | 117.4ms | 40.9ms | 29.2 MB | 2/6 | 46468819 |
| dotnet | 75.9ms | 1.0× | 1/6 | 100.6ms | 24.7ms | 29.7 MB | 3/6 | 46468819 |

## nqueens — backtracking recursion — count N-queens solutions  (N=10)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 933.3ms | 68.1× | 6/6 | 961.3ms | 28.0ms | 24.7 MB | 3/6 | 724 |
| elixir | 48.8ms | 3.6× | 3/6 | 310.9ms | 262.1ms | 80.6 MB | 6/6 | 724 |
| python | 66.9ms | 4.9× | 4/6 | 78.1ms | 11.2ms | 9.8 MB | 1/6 | 724 |
| node | 13.7ms | 1.0× | 1/6 | 31.3ms | 17.6ms | 51.2 MB | 5/6 | 724 |
| ruby | 137.1ms | 10.0× | 5/6 | 178.0ms | 40.9ms | 23.8 MB | 2/6 | 724 |
| dotnet | 19.0ms | 1.4× | 2/6 | 43.7ms | 24.7ms | 29.3 MB | 4/6 | 724 |

## pipeline — filter/map/reduce pipeline over a range  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 562.6ms | 76.0× | 6/6 | 590.6ms | 28.0ms | 35.6 MB | 4/6 | 155553889038886 |
| elixir | 23.4ms | 3.2× | 4/6 | 285.5ms | 262.1ms | 78.0 MB | 6/6 | 155553889038886 |
| python | 7.4ms | 1.0× | 1/6 | 18.6ms | 11.2ms | 9.9 MB | 1/6 | 155553889038886 |
| node | 24.9ms | 3.4× | 5/6 | 42.5ms | 17.6ms | 52.5 MB | 5/6 | 155553889038886 |
| ruby | 7.7ms | 1.0× | 2/6 | 48.6ms | 40.9ms | 24.0 MB | 2/6 | 155553889038886 |
| dotnet | 19.4ms | 2.6× | 3/6 | 44.1ms | 24.7ms | 28.1 MB | 3/6 | 155553889038886 |

## spawn — lightweight concurrent units + result collection  (N=10000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 524.9ms | 23.9× | 4/6 | 552.9ms | 28.0ms | 116.9 MB | 5/6 | 6100000 |
| elixir | 58.0ms | 2.6× | 2/6 | 320.1ms | 262.1ms | 88.5 MB | 4/6 | 6100000 |
| python | 549.7ms | 25.0× | 5/6 | 560.9ms | 11.2ms | 28.1 MB | 1/6 | 6100000 |
| node | 62.3ms | 2.8× | 3/6 | 79.9ms | 17.6ms | 51.8 MB | 3/6 | 6100000 |
| ruby | 1.579s | 71.8× | 6/6 | 1.620s | 40.9ms | 136.4 MB | 6/6 | 6100000 |
| dotnet | 22.0ms | 1.0× | 1/6 | 46.7ms | 24.7ms | 30.7 MB | 2/6 | 6100000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 424.6ms | 11.0× | 4/6 | 452.6ms | 28.0ms | 15.8 MB | 1/6 | 31781100 |
| elixir | 105.6ms | 2.7× | 2/6 | 367.7ms | 262.1ms | 82.1 MB | 5/6 | 31781100 |
| python | 698.8ms | 18.1× | 6/6 | 710.0ms | 11.2ms | 22.1 MB | 2/6 | 31781100 |
| node | 116.6ms | 3.0× | 3/6 | 134.2ms | 17.6ms | 183.2 MB | 6/6 | 31781100 |
| ruby | 450.8ms | 11.6× | 5/6 | 491.7ms | 40.9ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 38.7ms | 1.0× | 1/6 | 63.4ms | 24.7ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 147.7ms | 1.2× | 2/6 | 175.7ms | 28.0ms | 102.7 MB | 5/6 | 500 |
| elixir | 674.9ms | 5.3× | 6/6 | 937.0ms | 262.1ms | 552.6 MB | 6/6 | 500 |
| python | 175.8ms | 1.4× | 4/6 | 187.0ms | 11.2ms | 47.2 MB | 1/6 | 500 |
| node | 128.1ms | 1.0× | 1/6 | 145.7ms | 17.6ms | 65.2 MB | 4/6 | 500 |
| ruby | 207.5ms | 1.6× | 5/6 | 248.4ms | 40.9ms | 50.3 MB | 3/6 | 500 |
| dotnet | 148.9ms | 1.2× | 3/6 | 173.6ms | 24.7ms | 48.3 MB | 2/6 | 500 |
