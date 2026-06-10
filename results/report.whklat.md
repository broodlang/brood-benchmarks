# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-10 09:26.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.4ms | 2.9× | 4/6 | 28.4ms | — | 14.1 MB | 2/6 | 0 |
| elixir | 262.8ms | 26.8× | 6/6 | 262.8ms | — | 76.5 MB | 6/6 | 0 |
| python | 9.8ms | 1.0× | 1/6 | 9.8ms | — | 9.7 MB | 1/6 | 0 |
| node | 17.4ms | 1.8× | 2/6 | 17.4ms | — | 43.4 MB | 5/6 | 0 |
| ruby | 41.9ms | 4.3× | 5/6 | 41.9ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.1ms | 2.2× | 3/6 | 21.1ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 225.2ms | 53.6× | 6/6 | 253.6ms | 28.4ms | 14.2 MB | 2/6 | 832040 |
| elixir | 46.9ms | 11.2× | 3/6 | 309.7ms | 262.8ms | 80.3 MB | 6/6 | 832040 |
| python | 70.2ms | 16.7× | 5/6 | 80.0ms | 9.8ms | 9.8 MB | 1/6 | 832040 |
| node | 8.4ms | 2.0× | 2/6 | 25.8ms | 17.4ms | 48.7 MB | 5/6 | 832040 |
| ruby | 53.8ms | 12.8× | 4/6 | 95.7ms | 41.9ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.2ms | 1.0× | 1/6 | 25.3ms | 21.1ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 132.9ms | 69.9× | 5/6 | 161.3ms | 28.4ms | 14.2 MB | 2/6 | 3000000 |
| elixir | 39.9ms | 21.0× | 3/6 | 302.7ms | 262.8ms | 84.2 MB | 6/6 | 3000000 |
| python | 196.3ms | 103.3× | 6/6 | 206.1ms | 9.8ms | 9.8 MB | 1/6 | 3000000 |
| node | 3.2ms | 1.7× | 2/6 | 20.6ms | 17.4ms | 48.5 MB | 5/6 | 3000000 |
| ruby | 60.4ms | 31.8× | 4/6 | 102.3ms | 41.9ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.9ms | 1.0× | 1/6 | 23.0ms | 21.1ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 98.3ms | 61.4× | 6/6 | 126.7ms | 28.4ms | 14.2 MB | 2/6 | 499999500000 |
| elixir | 2.3ms | 1.4× | 3/6 | 265.1ms | 262.8ms | 79.7 MB | 6/6 | 499999500000 |
| python | 6.7ms | 4.2× | 5/6 | 16.5ms | 9.8ms | 9.7 MB | 1/6 | 499999500000 |
| node | 3.4ms | 2.1× | 4/6 | 20.8ms | 17.4ms | 50.5 MB | 5/6 | 499999500000 |
| ruby | 1.9ms | 1.2× | 2/6 | 43.8ms | 41.9ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.6ms | 1.0× | 1/6 | 22.7ms | 21.1ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.3ms | 12.3× | 5/6 | 51.7ms | 28.4ms | 14.1 MB | 2/6 | 2262 |
| elixir | 39.9ms | 21.0× | 6/6 | 302.7ms | 262.8ms | 81.2 MB | 6/6 | 2262 |
| python | 9.9ms | 5.2× | 4/6 | 19.7ms | 9.8ms | 9.9 MB | 1/6 | 2262 |
| node | 1.9ms | 1.0× | 1/6 | 19.3ms | 17.4ms | 49.0 MB | 5/6 | 2262 |
| ruby | 6.7ms | 3.5× | 3/6 | 48.6ms | 41.9ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 2.4ms | 1.3× | 2/6 | 23.5ms | 21.1ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 267.7ms | 52.5× | 6/6 | 296.1ms | 28.4ms | 26.4 MB | 4/6 | 307 |
| elixir | 51.0ms | 10.0× | 3/6 | 313.8ms | 262.8ms | 80.7 MB | 6/6 | 307 |
| python | 238.0ms | 46.7× | 5/6 | 247.8ms | 9.8ms | 9.8 MB | 1/6 | 307 |
| node | 7.6ms | 1.5× | 2/6 | 25.0ms | 17.4ms | 48.7 MB | 5/6 | 307 |
| ruby | 83.3ms | 16.3× | 4/6 | 125.2ms | 41.9ms | 23.5 MB | 2/6 | 307 |
| dotnet | 5.1ms | 1.0× | 1/6 | 26.2ms | 21.1ms | 26.2 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 72.3ms | 26.8× | 5/6 | 100.7ms | 28.4ms | 14.1 MB | 2/6 | 345426 |
| elixir | 54.8ms | 20.3× | 4/6 | 317.6ms | 262.8ms | 81.0 MB | 6/6 | 345426 |
| python | 76.9ms | 28.5× | 6/6 | 86.7ms | 9.8ms | 10.1 MB | 1/6 | 345426 |
| node | 4.3ms | 1.6× | 2/6 | 21.7ms | 17.4ms | 50.8 MB | 5/6 | 345426 |
| ruby | 22.6ms | 8.4× | 3/6 | 64.5ms | 41.9ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 2.7ms | 1.0× | 1/6 | 23.8ms | 21.1ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 661.3ms | 300.6× | 6/6 | 689.7ms | 28.4ms | 28.3 MB | 4/6 | 229499993 |
| elixir | 16.9ms | 7.7× | 3/6 | 279.7ms | 262.8ms | 80.6 MB | 6/6 | 229499993 |
| python | 44.7ms | 20.3× | 5/6 | 54.5ms | 9.8ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.3ms | 1.5× | 2/6 | 20.7ms | 17.4ms | 48.9 MB | 5/6 | 229499993 |
| ruby | 28.2ms | 12.8× | 4/6 | 70.1ms | 41.9ms | 23.6 MB | 2/6 | 229499993 |
| dotnet | 2.2ms | 1.0× | 1/6 | 23.3ms | 21.1ms | 26.2 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 140.3ms | 31.9× | 6/6 | 168.7ms | 28.4ms | 44.8 MB | 4/6 | 288889 |
| elixir | 11.3ms | 2.6× | 5/6 | 274.1ms | 262.8ms | 86.5 MB | 6/6 | 288889 |
| python | 4.4ms | 1.0× | 1/6 | 14.2ms | 9.8ms | 12.9 MB | 1/6 | 288889 |
| node | 6.4ms | 1.5× | 3/6 | 23.8ms | 17.4ms | 52.8 MB | 5/6 | 288889 |
| ruby | 7.3ms | 1.7× | 4/6 | 49.2ms | 41.9ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.5ms | 1.3× | 2/6 | 26.6ms | 21.1ms | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 210.8ms | 28.5× | 6/6 | 239.2ms | 28.4ms | 38.0 MB | 4/6 | 50038280 |
| elixir | 22.1ms | 3.0× | 4/6 | 284.9ms | 262.8ms | 82.2 MB | 6/6 | 50038280 |
| python | 24.2ms | 3.3× | 5/6 | 34.0ms | 9.8ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.4ms | 1.0× | 1/6 | 24.8ms | 17.4ms | 50.6 MB | 5/6 | 50038280 |
| ruby | 8.8ms | 1.2× | 2/6 | 50.7ms | 41.9ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.8ms | 1.5× | 3/6 | 31.9ms | 21.1ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 401.2ms | 85.4× | 6/6 | 429.6ms | 28.4ms | 20.1 MB | 2/6 | 327640 |
| elixir | 32.9ms | 7.0× | 5/6 | 295.7ms | 262.8ms | 81.2 MB | 6/6 | 327640 |
| python | 19.8ms | 4.2× | 3/6 | 29.6ms | 9.8ms | 10.0 MB | 1/6 | 327640 |
| node | 6.8ms | 1.4× | 2/6 | 24.2ms | 17.4ms | 52.6 MB | 5/6 | 327640 |
| ruby | 20.6ms | 4.4× | 4/6 | 62.5ms | 41.9ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 4.7ms | 1.0× | 1/6 | 25.8ms | 21.1ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.0ms | 4.2× | 6/6 | 60.4ms | 28.4ms | 21.4 MB | 2/6 | 102632633 |
| elixir | 15.2ms | 2.0× | 3/6 | 278.0ms | 262.8ms | 86.7 MB | 6/6 | 102632633 |
| python | 20.4ms | 2.6× | 5/6 | 30.2ms | 9.8ms | 12.1 MB | 1/6 | 102632633 |
| node | 17.5ms | 2.3× | 4/6 | 34.9ms | 17.4ms | 51.7 MB | 5/6 | 102632633 |
| ruby | 7.7ms | 1.0× | 1/6 | 49.6ms | 41.9ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 13.7ms | 1.8× | 2/6 | 34.8ms | 21.1ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.322s | 62.9× | 5/6 | 1.350s | 28.4ms | 183.5 MB | 5/6 | 12200000 |
| elixir | 78.0ms | 3.7× | 2/6 | 340.8ms | 262.8ms | 91.9 MB | 4/6 | 12200000 |
| python | 1.075s | 51.2× | 4/6 | 1.085s | 9.8ms | 36.0 MB | 2/6 | 12200000 |
| node | 105.0ms | 5.0× | 3/6 | 122.4ms | 17.4ms | 56.0 MB | 3/6 | 12200000 |
| ruby | 4.891s | 232.9× | 6/6 | 4.932s | 41.9ms | 246.4 MB | 6/6 | 12200000 |
| dotnet | 21.0ms | 1.0× | 1/6 | 42.1ms | 21.1ms | 32.1 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.202s | 54.5× | 6/6 | 2.230s | 28.4ms | 14.6 MB | 1/6 | 31781100 |
| elixir | 119.4ms | 3.0× | 2/6 | 382.2ms | 262.8ms | 84.6 MB | 5/6 | 31781100 |
| python | 749.2ms | 18.5× | 5/6 | 759.0ms | 9.8ms | 22.3 MB | 2/6 | 31781100 |
| node | 128.3ms | 3.2× | 3/6 | 145.7ms | 17.4ms | 182.0 MB | 6/6 | 31781100 |
| ruby | 487.1ms | 12.1× | 4/6 | 529.0ms | 41.9ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 40.4ms | 1.0× | 1/6 | 61.5ms | 21.1ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 179.6ms | 1.5× | 3/6 | 208.0ms | 28.4ms | 94.7 MB | 5/6 | 500 |
| elixir | 682.5ms | 5.5× | 6/6 | 945.3ms | 262.8ms | 562.3 MB | 6/6 | 500 |
| python | 184.6ms | 1.5× | 4/6 | 194.4ms | 9.8ms | 47.6 MB | 1/6 | 500 |
| node | 123.2ms | 1.0× | 1/6 | 140.6ms | 17.4ms | 65.6 MB | 4/6 | 500 |
| ruby | 210.5ms | 1.7× | 5/6 | 252.4ms | 41.9ms | 50.1 MB | 3/6 | 500 |
| dotnet | 154.5ms | 1.3× | 2/6 | 175.6ms | 21.1ms | 48.4 MB | 2/6 | 500 |
