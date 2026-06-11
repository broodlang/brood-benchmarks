# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-11 18:31.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.0ms | 2.8× | 4/6 | 27.0ms | — | 14.4 MB | 2/6 | 0 |
| elixir | 254.8ms | 26.0× | 6/6 | 254.8ms | — | 78.0 MB | 6/6 | 0 |
| python | 9.8ms | 1.0× | 1/6 | 9.8ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.4ms | 1.8× | 2/6 | 17.4ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 40.1ms | 4.1× | 5/6 | 40.1ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.3ms | 2.2× | 3/6 | 21.3ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 218.4ms | 49.6× | 6/6 | 245.4ms | 27.0ms | 14.4 MB | 2/6 | 832040 |
| elixir | 46.7ms | 10.6× | 3/6 | 301.5ms | 254.8ms | 80.8 MB | 6/6 | 832040 |
| python | 65.9ms | 15.0× | 5/6 | 75.7ms | 9.8ms | 9.8 MB | 1/6 | 832040 |
| node | 7.2ms | 1.6× | 2/6 | 24.6ms | 17.4ms | 48.5 MB | 5/6 | 832040 |
| ruby | 53.7ms | 12.2× | 4/6 | 93.8ms | 40.1ms | 23.6 MB | 3/6 | 832040 |
| dotnet | 4.4ms | 1.0× | 1/6 | 25.7ms | 21.3ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.0ms | 10.8× | 3/6 | 53.0ms | 27.0ms | 15.4 MB | 2/6 | 3000000 |
| elixir | 45.4ms | 18.9× | 4/6 | 300.2ms | 254.8ms | 84.6 MB | 6/6 | 3000000 |
| python | 193.5ms | 80.6× | 6/6 | 203.3ms | 9.8ms | 9.8 MB | 1/6 | 3000000 |
| node | 3.6ms | 1.5× | 2/6 | 21.0ms | 17.4ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 63.5ms | 26.5× | 5/6 | 103.6ms | 40.1ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 2.4ms | 1.0× | 1/6 | 23.7ms | 21.3ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 21.9ms | 13.7× | 6/6 | 48.9ms | 27.0ms | 14.3 MB | 2/6 | 499999500000 |
| elixir | 3.4ms | 2.1× | 3/6 | 258.2ms | 254.8ms | 77.7 MB | 6/6 | 499999500000 |
| python | 6.6ms | 4.1× | 5/6 | 16.4ms | 9.8ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.4ms | 2.1× | 4/6 | 20.8ms | 17.4ms | 50.4 MB | 5/6 | 499999500000 |
| ruby | 2.4ms | 1.5× | 2/6 | 42.5ms | 40.1ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.6ms | 1.0× | 1/6 | 22.9ms | 21.3ms | 26.2 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 24.0ms | 14.1× | 5/6 | 51.0ms | 27.0ms | 14.4 MB | 2/6 | 2262 |
| elixir | 47.5ms | 27.9× | 6/6 | 302.3ms | 254.8ms | 81.4 MB | 6/6 | 2262 |
| python | 8.6ms | 5.1× | 3/6 | 18.4ms | 9.8ms | 9.9 MB | 1/6 | 2262 |
| node | 2.1ms | 1.2× | 2/6 | 19.5ms | 17.4ms | 49.0 MB | 5/6 | 2262 |
| ruby | 9.1ms | 5.4× | 4/6 | 49.2ms | 40.1ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.7ms | 1.0× | 1/6 | 23.0ms | 21.3ms | 26.2 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 76.6ms | 15.0× | 4/6 | 103.6ms | 27.0ms | 26.8 MB | 4/6 | 307 |
| elixir | 59.4ms | 11.6× | 3/6 | 314.2ms | 254.8ms | 81.1 MB | 6/6 | 307 |
| python | 241.1ms | 47.3× | 6/6 | 250.9ms | 9.8ms | 9.8 MB | 1/6 | 307 |
| node | 8.3ms | 1.6× | 2/6 | 25.7ms | 17.4ms | 48.6 MB | 5/6 | 307 |
| ruby | 86.8ms | 17.0× | 5/6 | 126.9ms | 40.1ms | 23.5 MB | 2/6 | 307 |
| dotnet | 5.1ms | 1.0× | 1/6 | 26.4ms | 21.3ms | 26.2 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 72.7ms | 33.0× | 5/6 | 99.7ms | 27.0ms | 14.2 MB | 2/6 | 345426 |
| elixir | 68.0ms | 30.9× | 4/6 | 322.8ms | 254.8ms | 81.7 MB | 6/6 | 345426 |
| python | 75.5ms | 34.3× | 6/6 | 85.3ms | 9.8ms | 10.1 MB | 1/6 | 345426 |
| node | 3.9ms | 1.8× | 2/6 | 21.3ms | 17.4ms | 50.6 MB | 5/6 | 345426 |
| ruby | 26.1ms | 11.9× | 3/6 | 66.2ms | 40.1ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 2.2ms | 1.0× | 1/6 | 23.5ms | 21.3ms | 26.2 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 106.6ms | 62.7× | 6/6 | 133.6ms | 27.0ms | 28.6 MB | 4/6 | 229499993 |
| elixir | 26.7ms | 15.7× | 3/6 | 281.5ms | 254.8ms | 79.2 MB | 6/6 | 229499993 |
| python | 44.2ms | 26.0× | 5/6 | 54.0ms | 9.8ms | 9.9 MB | 1/6 | 229499993 |
| node | 2.9ms | 1.7× | 2/6 | 20.3ms | 17.4ms | 49.1 MB | 5/6 | 229499993 |
| ruby | 28.5ms | 16.8× | 4/6 | 68.6ms | 40.1ms | 23.5 MB | 2/6 | 229499993 |
| dotnet | 1.7ms | 1.0× | 1/6 | 23.0ms | 21.3ms | 26.2 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 63.0ms | 13.4× | 6/6 | 90.0ms | 27.0ms | 29.9 MB | 3/6 | 288889 |
| elixir | 20.0ms | 4.3× | 5/6 | 274.8ms | 254.8ms | 90.2 MB | 6/6 | 288889 |
| python | 4.7ms | 1.0× | 1/6 | 14.5ms | 9.8ms | 12.8 MB | 1/6 | 288889 |
| node | 7.1ms | 1.5× | 3/6 | 24.5ms | 17.4ms | 52.6 MB | 5/6 | 288889 |
| ruby | 8.5ms | 1.8× | 4/6 | 48.6ms | 40.1ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.1ms | 1.1× | 2/6 | 26.4ms | 21.3ms | 30.1 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 159.8ms | 20.8× | 6/6 | 186.8ms | 27.0ms | 53.7 MB | 5/6 | 50038280 |
| elixir | 36.5ms | 4.7× | 5/6 | 291.3ms | 254.8ms | 78.9 MB | 6/6 | 50038280 |
| python | 23.2ms | 3.0× | 4/6 | 33.0ms | 9.8ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.7ms | 1.0× | 1/6 | 25.1ms | 17.4ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 10.4ms | 1.4× | 2/6 | 50.5ms | 40.1ms | 23.6 MB | 2/6 | 50038280 |
| dotnet | 10.7ms | 1.4× | 3/6 | 32.0ms | 21.3ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 344.9ms | 67.6× | 6/6 | 371.9ms | 27.0ms | 22.5 MB | 2/6 | 327640 |
| elixir | 51.9ms | 10.2× | 5/6 | 306.7ms | 254.8ms | 80.9 MB | 6/6 | 327640 |
| python | 19.6ms | 3.8× | 3/6 | 29.4ms | 9.8ms | 10.0 MB | 1/6 | 327640 |
| node | 7.3ms | 1.4× | 2/6 | 24.7ms | 17.4ms | 52.3 MB | 5/6 | 327640 |
| ruby | 22.8ms | 4.5× | 4/6 | 62.9ms | 40.1ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 5.1ms | 1.0× | 1/6 | 26.4ms | 21.3ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.8ms | 3.8× | 6/6 | 58.8ms | 27.0ms | 25.0 MB | 3/6 | 102632633 |
| elixir | 27.0ms | 3.2× | 5/6 | 281.8ms | 254.8ms | 89.7 MB | 6/6 | 102632633 |
| python | 18.8ms | 2.2× | 4/6 | 28.6ms | 9.8ms | 12.1 MB | 1/6 | 102632633 |
| node | 16.8ms | 2.0× | 3/6 | 34.2ms | 17.4ms | 51.4 MB | 5/6 | 102632633 |
| ruby | 8.4ms | 1.0× | 1/6 | 48.5ms | 40.1ms | 24.2 MB | 2/6 | 102632633 |
| dotnet | 12.9ms | 1.5× | 2/6 | 34.2ms | 21.3ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.372s | 59.6× | 5/6 | 1.399s | 27.0ms | 181.9 MB | 5/6 | 12200000 |
| elixir | 100.2ms | 4.4× | 2/6 | 355.0ms | 254.8ms | 90.7 MB | 4/6 | 12200000 |
| python | 1.094s | 47.6× | 4/6 | 1.104s | 9.8ms | 35.9 MB | 2/6 | 12200000 |
| node | 104.9ms | 4.6× | 3/6 | 122.3ms | 17.4ms | 56.0 MB | 3/6 | 12200000 |
| ruby | 4.957s | 215.5× | 6/6 | 4.997s | 40.1ms | 247.0 MB | 6/6 | 12200000 |
| dotnet | 23.0ms | 1.0× | 1/6 | 44.3ms | 21.3ms | 32.3 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.246s | 55.0× | 6/6 | 2.273s | 27.0ms | 14.6 MB | 1/6 | 31781100 |
| elixir | 136.3ms | 3.3× | 3/6 | 391.1ms | 254.8ms | 86.0 MB | 5/6 | 31781100 |
| python | 767.3ms | 18.8× | 5/6 | 777.1ms | 9.8ms | 22.2 MB | 2/6 | 31781100 |
| node | 134.2ms | 3.3× | 2/6 | 151.6ms | 17.4ms | 182.0 MB | 6/6 | 31781100 |
| ruby | 513.0ms | 12.6× | 4/6 | 553.1ms | 40.1ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 40.8ms | 1.0× | 1/6 | 62.1ms | 21.3ms | 28.1 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 186.0ms | 1.4× | 3/6 | 213.0ms | 27.0ms | 101.9 MB | 5/6 | 500 |
| elixir | 724.4ms | 5.6× | 6/6 | 979.2ms | 254.8ms | 579.1 MB | 6/6 | 500 |
| python | 187.1ms | 1.4× | 4/6 | 196.9ms | 9.8ms | 46.2 MB | 1/6 | 500 |
| node | 129.8ms | 1.0× | 1/6 | 147.2ms | 17.4ms | 65.4 MB | 4/6 | 500 |
| ruby | 214.6ms | 1.7× | 5/6 | 254.7ms | 40.1ms | 50.3 MB | 3/6 | 500 |
| dotnet | 154.0ms | 1.2× | 2/6 | 175.3ms | 21.3ms | 48.0 MB | 2/6 | 500 |
