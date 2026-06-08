# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 20:08.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_startup: best of 1; others: best of 3 runs; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 26.7ms | 2.3× | 4/6 | 26.7ms | — | 10.6 MB | 2/6 | 0 |
| elixir | 280.4ms | 24.6× | 6/6 | 280.4ms | — | 76.2 MB | 6/6 | 0 |
| python | 11.4ms | 1.0× | 1/6 | 11.4ms | — | 9.8 MB | 1/6 | 0 |
| node | 18.3ms | 1.6× | 2/6 | 18.3ms | — | 42.3 MB | 5/6 | 0 |
| ruby | 44.0ms | 3.9× | 5/6 | 44.0ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 22.4ms | 2.0× | 3/6 | 22.4ms | — | 25.6 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 250.6ms | 67.7× | 6/6 | 277.3ms | 26.7ms | 10.5 MB | 2/6 | 832040 |
| elixir | 37.2ms | 10.1× | 3/6 | 317.6ms | 280.4ms | 81.0 MB | 6/6 | 832040 |
| python | 65.4ms | 17.7× | 5/6 | 76.8ms | 11.4ms | 9.8 MB | 1/6 | 832040 |
| node | 6.9ms | 1.9× | 2/6 | 25.2ms | 18.3ms | 47.5 MB | 5/6 | 832040 |
| ruby | 53.7ms | 14.5× | 4/6 | 97.7ms | 44.0ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 3.7ms | 1.0× | 1/6 | 26.1ms | 22.4ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 199.1ms | 199.1× | 5/6 | 225.8ms | 26.7ms | 10.6 MB | 2/6 | 3000000 |
| elixir | 39.0ms | 39.0× | 3/6 | 319.4ms | 280.4ms | 80.2 MB | 6/6 | 3000000 |
| python | 208.4ms | 208.4× | 6/6 | 219.8ms | 11.4ms | 9.8 MB | 1/6 | 3000000 |
| node | 2.3ms | 2.3× | 2/6 | 20.6ms | 18.3ms | 47.3 MB | 5/6 | 3000000 |
| ruby | 58.9ms | 58.9× | 4/6 | 102.9ms | 44.0ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 0.5ms | < 1× | 1/6 | 22.9ms | 22.4ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 94.1ms | 94.1× | 6/6 | 120.8ms | 26.7ms | 10.7 MB | 2/6 | 499999500000 |
| elixir | 0.0ms | < 1× | 1/6 | 266.2ms | 280.4ms | 77.3 MB | 6/6 | 499999500000 |
| python | 5.6ms | 5.6× | 5/6 | 17.0ms | 11.4ms | 9.7 MB | 1/6 | 499999500000 |
| node | 2.8ms | 2.8× | 4/6 | 21.1ms | 18.3ms | 49.3 MB | 5/6 | 499999500000 |
| ruby | 0.8ms | < 1× | 2/6 | 44.8ms | 44.0ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.2ms | 1.2× | 3/6 | 23.6ms | 22.4ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.3ms | 23.1× | 5/6 | 59.0ms | 26.7ms | 10.6 MB | 2/6 | 2262 |
| elixir | 36.3ms | 25.9× | 6/6 | 316.7ms | 280.4ms | 80.7 MB | 6/6 | 2262 |
| python | 8.3ms | 5.9× | 4/6 | 19.7ms | 11.4ms | 9.9 MB | 1/6 | 2262 |
| node | 1.4ms | 1.0× | 1/6 | 19.7ms | 18.3ms | 48.0 MB | 5/6 | 2262 |
| ruby | 6.6ms | 4.7× | 3/6 | 50.6ms | 44.0ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.6ms | 1.1× | 2/6 | 24.0ms | 22.4ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 327.2ms | 72.7× | 6/6 | 353.9ms | 26.7ms | 18.4 MB | 2/6 | 307 |
| elixir | 33.0ms | 7.3× | 3/6 | 313.4ms | 280.4ms | 80.5 MB | 6/6 | 307 |
| python | 227.6ms | 50.6× | 5/6 | 239.0ms | 11.4ms | 9.8 MB | 1/6 | 307 |
| node | 6.9ms | 1.5× | 2/6 | 25.2ms | 18.3ms | 47.5 MB | 5/6 | 307 |
| ruby | 86.4ms | 19.2× | 4/6 | 130.4ms | 44.0ms | 23.5 MB | 3/6 | 307 |
| dotnet | 4.5ms | 1.0× | 1/6 | 26.9ms | 22.4ms | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 83.0ms | 48.8× | 6/6 | 109.7ms | 26.7ms | 10.6 MB | 2/6 | 345426 |
| elixir | 35.7ms | 21.0× | 4/6 | 316.1ms | 280.4ms | 84.1 MB | 6/6 | 345426 |
| python | 78.4ms | 46.1× | 5/6 | 89.8ms | 11.4ms | 10.0 MB | 1/6 | 345426 |
| node | 3.7ms | 2.2× | 2/6 | 22.0ms | 18.3ms | 49.7 MB | 5/6 | 345426 |
| ruby | 22.9ms | 13.5× | 3/6 | 66.9ms | 44.0ms | 23.6 MB | 3/6 | 345426 |
| dotnet | 1.7ms | 1.0× | 1/6 | 24.1ms | 22.4ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 613.5ms | 613.5× | 6/6 | 640.2ms | 26.7ms | 18.7 MB | 2/6 | 229499993 |
| elixir | 0.0ms | < 1× | 1/6 | 279.9ms | 280.4ms | 79.7 MB | 6/6 | 229499993 |
| python | 48.2ms | 48.2× | 5/6 | 59.6ms | 11.4ms | 9.9 MB | 1/6 | 229499993 |
| node | 2.5ms | 2.5× | 3/6 | 20.8ms | 18.3ms | 47.7 MB | 5/6 | 229499993 |
| ruby | 26.5ms | 26.5× | 4/6 | 70.5ms | 44.0ms | 23.6 MB | 3/6 | 229499993 |
| dotnet | 0.8ms | < 1× | 2/6 | 23.2ms | 22.4ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 128.1ms | 128.1× | 6/6 | 154.8ms | 26.7ms | 38.7 MB | 4/6 | 288889 |
| elixir | 0.0ms | < 1× | 1/6 | 274.6ms | 280.4ms | 86.7 MB | 6/6 | 288889 |
| python | 2.8ms | 2.8× | 2/6 | 14.2ms | 11.4ms | 12.8 MB | 1/6 | 288889 |
| node | 5.6ms | 5.6× | 4/6 | 23.9ms | 18.3ms | 51.7 MB | 5/6 | 288889 |
| ruby | 6.1ms | 6.1× | 5/6 | 50.1ms | 44.0ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.4ms | 5.4× | 3/6 | 27.8ms | 22.4ms | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 194.1ms | 29.0× | 6/6 | 220.8ms | 26.7ms | 27.1 MB | 3/6 | 50038280 |
| elixir | 18.5ms | 2.8× | 4/6 | 298.9ms | 280.4ms | 78.3 MB | 6/6 | 50038280 |
| python | 23.8ms | 3.6× | 5/6 | 35.2ms | 11.4ms | 9.9 MB | 1/6 | 50038280 |
| node | 6.7ms | 1.0× | 1/6 | 25.0ms | 18.3ms | 49.6 MB | 5/6 | 50038280 |
| ruby | 8.6ms | 1.3× | 2/6 | 52.6ms | 44.0ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.4ms | 1.6× | 3/6 | 32.8ms | 22.4ms | 27.2 MB | 4/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 369.3ms | 71.0× | 6/6 | 396.0ms | 26.7ms | 13.9 MB | 2/6 | 327640 |
| elixir | 30.5ms | 5.9× | 5/6 | 310.9ms | 280.4ms | 80.6 MB | 6/6 | 327640 |
| python | 19.9ms | 3.8× | 3/6 | 31.3ms | 11.4ms | 10.0 MB | 1/6 | 327640 |
| node | 7.1ms | 1.4× | 2/6 | 25.4ms | 18.3ms | 51.5 MB | 5/6 | 327640 |
| ruby | 22.3ms | 4.3× | 4/6 | 66.3ms | 44.0ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 5.2ms | 1.0× | 1/6 | 27.6ms | 22.4ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 29.2ms | 6.3× | 6/6 | 55.9ms | 26.7ms | 14.6 MB | 2/6 | 102632633 |
| elixir | 4.6ms | 1.0× | 1/6 | 285.0ms | 280.4ms | 86.0 MB | 6/6 | 102632633 |
| python | 19.9ms | 4.3× | 5/6 | 31.3ms | 11.4ms | 12.1 MB | 1/6 | 102632633 |
| node | 14.9ms | 3.2× | 4/6 | 33.2ms | 18.3ms | 50.5 MB | 5/6 | 102632633 |
| ruby | 6.6ms | 1.4× | 2/6 | 50.6ms | 44.0ms | 24.1 MB | 3/6 | 102632633 |
| dotnet | 11.7ms | 2.5× | 3/6 | 34.1ms | 22.4ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.054s | 48.1× | 4/6 | 1.080s | 26.7ms | 157.8 MB | 5/6 | 12200000 |
| elixir | 82.3ms | 3.8× | 2/6 | 362.7ms | 280.4ms | 91.4 MB | 4/6 | 12200000 |
| python | 1.104s | 50.4× | 5/6 | 1.115s | 11.4ms | 35.8 MB | 2/6 | 12200000 |
| node | 105.4ms | 4.8× | 3/6 | 123.7ms | 18.3ms | 54.9 MB | 3/6 | 12200000 |
| ruby | 5.087s | 232.3× | 6/6 | 5.131s | 44.0ms | 246.5 MB | 6/6 | 12200000 |
| dotnet | 21.9ms | 1.0× | 1/6 | 44.3ms | 22.4ms | 32.0 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.133s | 56.7× | 6/6 | 2.159s | 26.7ms | 10.6 MB | 1/6 | 31781100 |
| elixir | 113.4ms | 3.0× | 2/6 | 393.8ms | 280.4ms | 82.9 MB | 5/6 | 31781100 |
| python | 747.0ms | 19.9× | 5/6 | 758.4ms | 11.4ms | 22.1 MB | 2/6 | 31781100 |
| node | 131.8ms | 3.5× | 3/6 | 150.1ms | 18.3ms | 181.2 MB | 6/6 | 31781100 |
| ruby | 488.9ms | 13.0× | 4/6 | 532.9ms | 44.0ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 37.6ms | 1.0× | 1/6 | 60.0ms | 22.4ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 178.1ms | 1.4× | 3/6 | 204.8ms | 26.7ms | 82.3 MB | 5/6 | 500 |
| elixir | 715.9ms | 5.5× | 6/6 | 996.3ms | 280.4ms | 605.7 MB | 6/6 | 500 |
| python | 188.0ms | 1.4× | 4/6 | 199.4ms | 11.4ms | 44.4 MB | 1/6 | 500 |
| node | 130.9ms | 1.0× | 1/6 | 149.2ms | 18.3ms | 64.6 MB | 4/6 | 500 |
| ruby | 218.9ms | 1.7× | 5/6 | 262.9ms | 44.0ms | 50.1 MB | 2/6 | 500 |
| dotnet | 165.1ms | 1.3× | 2/6 | 187.5ms | 22.4ms | 50.8 MB | 3/6 | 500 |
