# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-13 10:29.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.109.

_best of 5 runs; startup best of 15; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.9ms | 3.0× | 4/6 | 27.9ms | — | 14.5 MB | 2/6 | 0 |
| elixir | 250.7ms | 27.0× | 6/6 | 250.7ms | — | 78.6 MB | 6/6 | 0 |
| python | 9.3ms | 1.0× | 1/6 | 9.3ms | — | 9.8 MB | 1/6 | 0 |
| node | 17.5ms | 1.9× | 2/6 | 17.5ms | — | 43.2 MB | 5/6 | 0 |
| ruby | 39.6ms | 4.3× | 5/6 | 39.6ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 21.2ms | 2.3× | 3/6 | 21.2ms | — | 25.8 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 65.9ms | 14.6× | 6/6 | 93.8ms | 27.9ms | 15.3 MB | 2/6 | 832040 |
| elixir | 56.0ms | 12.4× | 3/6 | 306.7ms | 250.7ms | 82.2 MB | 6/6 | 832040 |
| python | 65.8ms | 14.6× | 5/6 | 75.1ms | 9.3ms | 9.8 MB | 1/6 | 832040 |
| node | 7.3ms | 1.6× | 2/6 | 24.8ms | 17.5ms | 48.5 MB | 5/6 | 832040 |
| ruby | 58.5ms | 13.0× | 4/6 | 98.1ms | 39.6ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 4.5ms | 1.0× | 1/6 | 25.7ms | 21.2ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 17.7ms | 7.7× | 3/6 | 45.6ms | 27.9ms | 15.3 MB | 2/6 | 3000000 |
| elixir | 53.1ms | 23.1× | 4/6 | 303.8ms | 250.7ms | 81.9 MB | 6/6 | 3000000 |
| python | 192.2ms | 83.6× | 6/6 | 201.5ms | 9.3ms | 9.8 MB | 1/6 | 3000000 |
| node | 3.5ms | 1.5× | 2/6 | 21.0ms | 17.5ms | 48.4 MB | 5/6 | 3000000 |
| ruby | 63.5ms | 27.6× | 5/6 | 103.1ms | 39.6ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 2.3ms | 1.0× | 1/6 | 23.5ms | 21.2ms | 26.2 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 19.9ms | 15.3× | 6/6 | 47.8ms | 27.9ms | 14.5 MB | 2/6 | 499999500000 |
| elixir | 17.6ms | 13.5× | 5/6 | 268.3ms | 250.7ms | 77.0 MB | 6/6 | 499999500000 |
| python | 7.2ms | 5.5× | 4/6 | 16.5ms | 9.3ms | 9.8 MB | 1/6 | 499999500000 |
| node | 3.0ms | 2.3× | 3/6 | 20.5ms | 17.5ms | 50.4 MB | 5/6 | 499999500000 |
| ruby | 1.3ms | 1.0× | 1/6 | 40.9ms | 39.6ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 1.5ms | 1.2× | 2/6 | 22.7ms | 21.2ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.0ms | 10.0× | 5/6 | 50.9ms | 27.9ms | 14.5 MB | 2/6 | 2262 |
| elixir | 48.8ms | 21.2× | 6/6 | 299.5ms | 250.7ms | 80.7 MB | 6/6 | 2262 |
| python | 10.3ms | 4.5× | 3/6 | 19.6ms | 9.3ms | 10.0 MB | 1/6 | 2262 |
| node | 2.4ms | 1.0× | 2/6 | 19.9ms | 17.5ms | 49.1 MB | 5/6 | 2262 |
| ruby | 11.0ms | 4.8× | 4/6 | 50.6ms | 39.6ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 2.3ms | 1.0× | 1/6 | 23.5ms | 21.2ms | 26.2 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 62.6ms | 12.8× | 3/6 | 90.5ms | 27.9ms | 27.2 MB | 4/6 | 307 |
| elixir | 65.4ms | 13.3× | 4/6 | 316.1ms | 250.7ms | 83.4 MB | 6/6 | 307 |
| python | 261.7ms | 53.4× | 6/6 | 271.0ms | 9.3ms | 9.8 MB | 1/6 | 307 |
| node | 7.9ms | 1.6× | 2/6 | 25.4ms | 17.5ms | 48.6 MB | 5/6 | 307 |
| ruby | 86.2ms | 17.6× | 5/6 | 125.8ms | 39.6ms | 23.5 MB | 2/6 | 307 |
| dotnet | 4.9ms | 1.0× | 1/6 | 26.1ms | 21.2ms | 26.1 MB | 3/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 75.3ms | 25.1× | 5/6 | 103.2ms | 27.9ms | 14.5 MB | 2/6 | 345426 |
| elixir | 60.4ms | 20.1× | 4/6 | 311.1ms | 250.7ms | 85.2 MB | 6/6 | 345426 |
| python | 80.9ms | 27.0× | 6/6 | 90.2ms | 9.3ms | 10.1 MB | 1/6 | 345426 |
| node | 3.0ms | 1.0× | 1/6 | 20.5ms | 17.5ms | 50.7 MB | 5/6 | 345426 |
| ruby | 31.5ms | 10.5× | 3/6 | 71.1ms | 39.6ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 3.0ms | 1.0× | 2/6 | 24.2ms | 21.2ms | 26.2 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 103.6ms | 38.4× | 6/6 | 131.5ms | 27.9ms | 28.7 MB | 4/6 | 229499993 |
| elixir | 27.5ms | 10.2× | 3/6 | 278.2ms | 250.7ms | 79.5 MB | 6/6 | 229499993 |
| python | 45.3ms | 16.8× | 5/6 | 54.6ms | 9.3ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.9ms | 1.4× | 2/6 | 21.4ms | 17.5ms | 49.2 MB | 5/6 | 229499993 |
| ruby | 31.6ms | 11.7× | 4/6 | 71.2ms | 39.6ms | 23.7 MB | 2/6 | 229499993 |
| dotnet | 2.7ms | 1.0× | 1/6 | 23.9ms | 21.2ms | 26.2 MB | 3/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 64.1ms | 11.2× | 6/6 | 92.0ms | 27.9ms | 30.0 MB | 3/6 | 288889 |
| elixir | 28.2ms | 4.9× | 5/6 | 278.9ms | 250.7ms | 86.7 MB | 6/6 | 288889 |
| python | 5.7ms | 1.0× | 1/6 | 15.0ms | 9.3ms | 12.9 MB | 1/6 | 288889 |
| node | 7.4ms | 1.3× | 3/6 | 24.9ms | 17.5ms | 52.6 MB | 5/6 | 288889 |
| ruby | 9.7ms | 1.7× | 4/6 | 49.3ms | 39.6ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 5.7ms | 1.0× | 2/6 | 26.9ms | 21.2ms | 30.1 MB | 4/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 162.6ms | 22.6× | 6/6 | 190.5ms | 27.9ms | 53.4 MB | 5/6 | 50038280 |
| elixir | 39.8ms | 5.5× | 5/6 | 290.5ms | 250.7ms | 80.7 MB | 6/6 | 50038280 |
| python | 23.6ms | 3.3× | 4/6 | 32.9ms | 9.3ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.2ms | 1.0× | 1/6 | 24.7ms | 17.5ms | 50.4 MB | 4/6 | 50038280 |
| ruby | 12.3ms | 1.7× | 3/6 | 51.9ms | 39.6ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 10.2ms | 1.4× | 2/6 | 31.4ms | 21.2ms | 27.3 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 282.1ms | 50.4× | 6/6 | 310.0ms | 27.9ms | 20.2 MB | 2/6 | 327640 |
| elixir | 56.9ms | 10.2× | 5/6 | 307.6ms | 250.7ms | 84.0 MB | 6/6 | 327640 |
| python | 22.8ms | 4.1× | 3/6 | 32.1ms | 9.3ms | 10.0 MB | 1/6 | 327640 |
| node | 7.1ms | 1.3× | 2/6 | 24.6ms | 17.5ms | 52.3 MB | 5/6 | 327640 |
| ruby | 23.2ms | 4.1× | 4/6 | 62.8ms | 39.6ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 5.6ms | 1.0× | 1/6 | 26.8ms | 21.2ms | 30.8 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 32.2ms | 2.8× | 6/6 | 60.1ms | 27.9ms | 25.1 MB | 3/6 | 102632633 |
| elixir | 28.6ms | 2.5× | 5/6 | 279.3ms | 250.7ms | 86.8 MB | 6/6 | 102632633 |
| python | 18.8ms | 1.6× | 4/6 | 28.1ms | 9.3ms | 12.2 MB | 1/6 | 102632633 |
| node | 16.6ms | 1.4× | 3/6 | 34.1ms | 17.5ms | 51.6 MB | 5/6 | 102632633 |
| ruby | 11.5ms | 1.0× | 1/6 | 51.1ms | 39.6ms | 24.2 MB | 2/6 | 102632633 |
| dotnet | 12.8ms | 1.1× | 2/6 | 34.0ms | 21.2ms | 27.2 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.281s | 57.2× | 5/6 | 1.309s | 27.9ms | 200.1 MB | 5/6 | 12200000 |
| elixir | 83.3ms | 3.7× | 2/6 | 334.0ms | 250.7ms | 90.4 MB | 4/6 | 12200000 |
| python | 1.101s | 49.2× | 4/6 | 1.111s | 9.3ms | 36.0 MB | 2/6 | 12200000 |
| node | 109.2ms | 4.9× | 3/6 | 126.7ms | 17.5ms | 55.9 MB | 3/6 | 12200000 |
| ruby | 5.095s | 227.4× | 6/6 | 5.134s | 39.6ms | 246.4 MB | 6/6 | 12200000 |
| dotnet | 22.4ms | 1.0× | 1/6 | 43.6ms | 21.2ms | 32.1 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 459.7ms | 11.1× | 4/6 | 487.6ms | 27.9ms | 17.3 MB | 1/6 | 31781100 |
| elixir | 133.2ms | 3.2× | 3/6 | 383.9ms | 250.7ms | 84.2 MB | 5/6 | 31781100 |
| python | 754.2ms | 18.2× | 6/6 | 763.5ms | 9.3ms | 22.3 MB | 2/6 | 31781100 |
| node | 128.5ms | 3.1× | 2/6 | 146.0ms | 17.5ms | 181.8 MB | 6/6 | 31781100 |
| ruby | 479.5ms | 11.6× | 5/6 | 519.1ms | 39.6ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 41.5ms | 1.0× | 1/6 | 62.7ms | 21.2ms | 28.0 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 182.6ms | 1.4× | 3/6 | 210.5ms | 27.9ms | 97.1 MB | 5/6 | 500 |
| elixir | 736.0ms | 5.8× | 6/6 | 986.7ms | 250.7ms | 555.9 MB | 6/6 | 500 |
| python | 187.7ms | 1.5× | 4/6 | 197.0ms | 9.3ms | 46.2 MB | 1/6 | 500 |
| node | 127.9ms | 1.0× | 1/6 | 145.4ms | 17.5ms | 65.3 MB | 4/6 | 500 |
| ruby | 225.2ms | 1.8× | 5/6 | 264.8ms | 39.6ms | 50.2 MB | 3/6 | 500 |
| dotnet | 158.1ms | 1.2× | 2/6 | 179.3ms | 21.2ms | 48.2 MB | 2/6 | 500 |
