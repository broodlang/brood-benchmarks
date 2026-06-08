# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 18:49.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0-rc.4 (e39a1ca) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.9ms | 2.6× | 2/6 | 27.9ms | — | 11.9 MB | 2/6 | 0 |
| elixir | 270.5ms | 25.3× | 6/6 | 270.5ms | — | 76.4 MB | 6/6 | 0 |
| python | 10.7ms | 1.0× | 1/6 | 10.7ms | — | 9.7 MB | 1/6 | 0 |
| node | 68.4ms | 6.4× | 5/6 | 68.4ms | — | 40.9 MB | 5/6 | 0 |
| ruby | 55.7ms | 5.2× | 4/6 | 55.7ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 28.0ms | 2.6× | 3/6 | 28.0ms | — | 25.3 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 266.2ms | 266.2× | 6/6 | 294.1ms | 27.9ms | 12.0 MB | 2/6 | 832040 |
| elixir | 54.1ms | 54.1× | 4/6 | 324.6ms | 270.5ms | 81.6 MB | 6/6 | 832040 |
| python | 70.5ms | 70.5× | 5/6 | 81.2ms | 10.7ms | 9.8 MB | 1/6 | 832040 |
| node | 0.0ms | < 1× | 1/6 | 26.5ms | 68.4ms | 47.1 MB | 5/6 | 832040 |
| ruby | 47.2ms | 47.2× | 3/6 | 102.9ms | 55.7ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 0.0ms | < 1× | 2/6 | 26.5ms | 28.0ms | 25.7 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 329.4ms | 329.4× | 6/6 | 357.3ms | 27.9ms | 12.1 MB | 2/6 | 3000000 |
| elixir | 40.2ms | 40.2× | 3/6 | 310.7ms | 270.5ms | 80.7 MB | 6/6 | 3000000 |
| python | 218.1ms | 218.1× | 5/6 | 228.8ms | 10.7ms | 9.8 MB | 1/6 | 3000000 |
| node | 0.0ms | < 1× | 1/6 | 21.3ms | 68.4ms | 50.1 MB | 5/6 | 3000000 |
| ruby | 56.1ms | 56.1× | 4/6 | 111.8ms | 55.7ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 0.0ms | < 1× | 2/6 | 24.8ms | 28.0ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 99.4ms | 99.4× | 6/6 | 127.3ms | 27.9ms | 12.1 MB | 2/6 | 499999500000 |
| elixir | 27.7ms | 27.7× | 5/6 | 298.2ms | 270.5ms | 78.3 MB | 6/6 | 499999500000 |
| python | 7.3ms | 7.3× | 4/6 | 18.0ms | 10.7ms | 9.8 MB | 1/6 | 499999500000 |
| node | 0.0ms | < 1× | 1/6 | 22.0ms | 68.4ms | 52.1 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 2/6 | 45.1ms | 55.7ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 0.0ms | < 1× | 3/6 | 24.1ms | 28.0ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 39.0ms | 39.0× | 5/6 | 66.9ms | 27.9ms | 12.2 MB | 2/6 | 2262 |
| elixir | 40.9ms | 40.9× | 6/6 | 311.4ms | 270.5ms | 80.7 MB | 6/6 | 2262 |
| python | 9.7ms | 9.7× | 4/6 | 20.4ms | 10.7ms | 9.9 MB | 1/6 | 2262 |
| node | 0.0ms | < 1× | 1/6 | 20.8ms | 68.4ms | 50.8 MB | 5/6 | 2262 |
| ruby | 0.0ms | < 1× | 2/6 | 54.7ms | 55.7ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 0.0ms | < 1× | 3/6 | 24.2ms | 28.0ms | 26.2 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 512.2ms | 512.2× | 6/6 | 540.1ms | 27.9ms | 19.8 MB | 2/6 | 307 |
| elixir | 45.5ms | 45.5× | 3/6 | 316.0ms | 270.5ms | 80.8 MB | 6/6 | 307 |
| python | 285.4ms | 285.4× | 5/6 | 296.1ms | 10.7ms | 9.8 MB | 1/6 | 307 |
| node | 0.0ms | < 1× | 1/6 | 26.1ms | 68.4ms | 50.2 MB | 5/6 | 307 |
| ruby | 80.4ms | 80.4× | 4/6 | 136.1ms | 55.7ms | 23.5 MB | 3/6 | 307 |
| dotnet | 0.3ms | < 1× | 2/6 | 28.3ms | 28.0ms | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 96.4ms | 96.4× | 6/6 | 124.3ms | 27.9ms | 12.1 MB | 2/6 | 345426 |
| elixir | 47.8ms | 47.8× | 4/6 | 318.3ms | 270.5ms | 80.7 MB | 6/6 | 345426 |
| python | 79.2ms | 79.2× | 5/6 | 89.9ms | 10.7ms | 10.0 MB | 1/6 | 345426 |
| node | 0.0ms | < 1× | 1/6 | 21.8ms | 68.4ms | 52.1 MB | 5/6 | 345426 |
| ruby | 12.5ms | 12.5× | 3/6 | 68.2ms | 55.7ms | 23.6 MB | 3/6 | 345426 |
| dotnet | 0.0ms | < 1× | 2/6 | 23.7ms | 28.0ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 598.1ms | 598.1× | 6/6 | 626.0ms | 27.9ms | 19.9 MB | 2/6 | 229499993 |
| elixir | 11.4ms | 11.4× | 3/6 | 281.9ms | 270.5ms | 77.7 MB | 6/6 | 229499993 |
| python | 48.6ms | 48.6× | 5/6 | 59.3ms | 10.7ms | 9.9 MB | 1/6 | 229499993 |
| node | 0.0ms | < 1× | 1/6 | 21.8ms | 68.4ms | 50.6 MB | 5/6 | 229499993 |
| ruby | 19.0ms | 19.0× | 4/6 | 74.7ms | 55.7ms | 23.6 MB | 3/6 | 229499993 |
| dotnet | 0.0ms | < 1× | 2/6 | 23.2ms | 28.0ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 125.7ms | 125.7× | 6/6 | 153.6ms | 27.9ms | 36.0 MB | 4/6 | 288889 |
| elixir | 7.2ms | 7.2× | 5/6 | 277.7ms | 270.5ms | 87.6 MB | 6/6 | 288889 |
| python | 4.5ms | 4.5× | 4/6 | 15.2ms | 10.7ms | 12.9 MB | 1/6 | 288889 |
| node | 0.0ms | < 1× | 1/6 | 24.9ms | 68.4ms | 54.4 MB | 5/6 | 288889 |
| ruby | 0.0ms | < 1× | 2/6 | 50.7ms | 55.7ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 0.0ms | < 1× | 3/6 | 27.1ms | 28.0ms | 30.1 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 181.7ms | 181.7× | 6/6 | 209.6ms | 27.9ms | 28.6 MB | 4/6 | 50038280 |
| elixir | 19.1ms | 19.1× | 4/6 | 289.6ms | 270.5ms | 78.1 MB | 6/6 | 50038280 |
| python | 23.7ms | 23.7× | 5/6 | 34.4ms | 10.7ms | 9.9 MB | 1/6 | 50038280 |
| node | 0.0ms | < 1× | 1/6 | 25.3ms | 68.4ms | 52.3 MB | 5/6 | 50038280 |
| ruby | 0.0ms | < 1× | 2/6 | 53.3ms | 55.7ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 3.9ms | 3.9× | 3/6 | 31.9ms | 28.0ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 342.8ms | 342.8× | 6/6 | 370.7ms | 27.9ms | 16.2 MB | 2/6 | 327640 |
| elixir | 25.5ms | 25.5× | 5/6 | 296.0ms | 270.5ms | 83.6 MB | 6/6 | 327640 |
| python | 20.6ms | 20.6× | 4/6 | 31.3ms | 10.7ms | 10.1 MB | 1/6 | 327640 |
| node | 0.0ms | < 1× | 1/6 | 25.6ms | 68.4ms | 54.2 MB | 5/6 | 327640 |
| ruby | 8.2ms | 8.2× | 3/6 | 63.9ms | 55.7ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 0.0ms | < 1× | 2/6 | 26.4ms | 28.0ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 28.6ms | 28.6× | 6/6 | 56.5ms | 27.9ms | 16.9 MB | 2/6 | 102632633 |
| elixir | 17.8ms | 17.8× | 4/6 | 288.3ms | 270.5ms | 86.1 MB | 6/6 | 102632633 |
| python | 20.6ms | 20.6× | 5/6 | 31.3ms | 10.7ms | 12.1 MB | 1/6 | 102632633 |
| node | 0.0ms | < 1× | 1/6 | 35.9ms | 68.4ms | 53.2 MB | 5/6 | 102632633 |
| ruby | 0.0ms | < 1× | 2/6 | 55.0ms | 55.7ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 9.8ms | 9.8× | 3/6 | 37.8ms | 28.0ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 163.7ms | 5.1× | 2/2 | 191.6ms | 27.9ms | 35.1 MB | 1/2 | 199990000 |
| elixir | 32.2ms | 1.0× | 1/2 | 302.7ms | 270.5ms | 87.8 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.144s | 52.3× | 6/6 | 2.172s | 27.9ms | 12.1 MB | 1/6 | 31781100 |
| elixir | 112.4ms | 2.7× | 3/6 | 382.9ms | 270.5ms | 81.5 MB | 5/6 | 31781100 |
| python | 750.8ms | 18.3× | 5/6 | 761.5ms | 10.7ms | 22.2 MB | 2/6 | 31781100 |
| node | 77.0ms | 1.9× | 2/6 | 145.4ms | 68.4ms | 185.1 MB | 6/6 | 31781100 |
| ruby | 469.4ms | 11.4× | 4/6 | 525.1ms | 55.7ms | 23.6 MB | 3/6 | 31781100 |
| dotnet | 41.0ms | 1.0× | 1/6 | 69.0ms | 28.0ms | 27.7 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 171.9ms | 2.0× | 3/6 | 199.8ms | 27.9ms | 83.8 MB | 5/6 | 500 |
| elixir | 731.7ms | 8.5× | 6/6 | 1.002s | 270.5ms | 506.2 MB | 6/6 | 500 |
| python | 186.6ms | 2.2× | 4/6 | 197.3ms | 10.7ms | 44.3 MB | 1/6 | 500 |
| node | 85.7ms | 1.0× | 1/6 | 154.1ms | 68.4ms | 67.2 MB | 4/6 | 500 |
| ruby | 188.3ms | 2.2× | 5/6 | 244.0ms | 55.7ms | 50.1 MB | 3/6 | 500 |
| dotnet | 153.1ms | 1.8× | 2/6 | 181.1ms | 28.0ms | 48.5 MB | 2/6 | 500 |
