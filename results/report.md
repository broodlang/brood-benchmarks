# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-22-generic-x86_64-with-glibc2.43 — 2026-06-08 23:22.
> **Runtimes:** Brood brood 0.1.0; Elixir Elixir 1.20.0 (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.108.

_best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.7ms | 2.8× | 4/6 | 27.7ms | — | 14.0 MB | 2/6 | 0 |
| elixir | 269.1ms | 27.5× | 6/6 | 269.1ms | — | 76.5 MB | 6/6 | 0 |
| python | 9.8ms | 1.0× | 1/6 | 9.8ms | — | 9.7 MB | 1/6 | 0 |
| node | 17.7ms | 1.8× | 2/6 | 17.7ms | — | 43.3 MB | 5/6 | 0 |
| ruby | 43.4ms | 4.4× | 5/6 | 43.4ms | — | 23.5 MB | 3/6 | 0 |
| dotnet | 22.6ms | 2.3× | 3/6 | 22.6ms | — | 25.7 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 227.7ms | 75.9× | 6/6 | 255.4ms | 27.7ms | 13.9 MB | 2/6 | 832040 |
| elixir | 56.7ms | 18.9× | 3/6 | 325.8ms | 269.1ms | 82.4 MB | 6/6 | 832040 |
| python | 73.7ms | 24.6× | 5/6 | 83.5ms | 9.8ms | 9.8 MB | 1/6 | 832040 |
| node | 9.2ms | 3.1× | 2/6 | 26.9ms | 17.7ms | 48.5 MB | 5/6 | 832040 |
| ruby | 72.8ms | 24.3× | 4/6 | 116.2ms | 43.4ms | 23.5 MB | 3/6 | 832040 |
| dotnet | 3.0ms | 1.0× | 1/6 | 25.6ms | 22.6ms | 25.8 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 138.3ms | 125.7× | 5/6 | 166.0ms | 27.7ms | 14.1 MB | 2/6 | 3000000 |
| elixir | 63.0ms | 57.3× | 3/6 | 332.1ms | 269.1ms | 81.0 MB | 6/6 | 3000000 |
| python | 194.0ms | 176.4× | 6/6 | 203.8ms | 9.8ms | 9.7 MB | 1/6 | 3000000 |
| node | 3.2ms | 2.9× | 2/6 | 20.9ms | 17.7ms | 48.3 MB | 5/6 | 3000000 |
| ruby | 64.1ms | 58.3× | 4/6 | 107.5ms | 43.4ms | 23.5 MB | 3/6 | 3000000 |
| dotnet | 1.1ms | 1.0× | 1/6 | 23.7ms | 22.6ms | 26.2 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 101.7ms | 101.7× | 6/6 | 129.4ms | 27.7ms | 14.2 MB | 2/6 | 499999500000 |
| elixir | 3.0ms | 3.0× | 3/6 | 272.1ms | 269.1ms | 78.6 MB | 6/6 | 499999500000 |
| python | 7.8ms | 7.8× | 5/6 | 17.6ms | 9.8ms | 9.7 MB | 1/6 | 499999500000 |
| node | 3.6ms | 3.6× | 4/6 | 21.3ms | 17.7ms | 50.2 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 41.4ms | 43.4ms | 23.5 MB | 3/6 | 499999500000 |
| dotnet | 0.4ms | < 1× | 2/6 | 23.0ms | 22.6ms | 26.1 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 23.6ms | 12.4× | 5/6 | 51.3ms | 27.7ms | 14.1 MB | 2/6 | 2262 |
| elixir | 43.0ms | 22.6× | 6/6 | 312.1ms | 269.1ms | 84.7 MB | 6/6 | 2262 |
| python | 9.8ms | 5.2× | 4/6 | 19.6ms | 9.8ms | 9.9 MB | 1/6 | 2262 |
| node | 2.1ms | 1.1× | 2/6 | 19.8ms | 17.7ms | 48.8 MB | 5/6 | 2262 |
| ruby | 7.8ms | 4.1× | 3/6 | 51.2ms | 43.4ms | 23.5 MB | 3/6 | 2262 |
| dotnet | 1.9ms | 1.0× | 1/6 | 24.5ms | 22.6ms | 26.1 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 261.2ms | 30.4× | 6/6 | 288.9ms | 27.7ms | 24.1 MB | 3/6 | 307 |
| elixir | 57.4ms | 6.7× | 3/6 | 326.5ms | 269.1ms | 80.7 MB | 6/6 | 307 |
| python | 234.9ms | 27.3× | 5/6 | 244.7ms | 9.8ms | 9.8 MB | 1/6 | 307 |
| node | 8.6ms | 1.0× | 2/6 | 26.3ms | 17.7ms | 48.5 MB | 5/6 | 307 |
| ruby | 92.5ms | 10.8× | 4/6 | 135.9ms | 43.4ms | 23.5 MB | 2/6 | 307 |
| dotnet | 8.6ms | 1.0× | 1/6 | 31.2ms | 22.6ms | 26.1 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 71.5ms | 71.5× | 5/6 | 99.2ms | 27.7ms | 14.1 MB | 2/6 | 345426 |
| elixir | 50.4ms | 50.4× | 4/6 | 319.5ms | 269.1ms | 83.2 MB | 6/6 | 345426 |
| python | 83.9ms | 83.9× | 6/6 | 93.7ms | 9.8ms | 9.9 MB | 1/6 | 345426 |
| node | 3.3ms | 3.3× | 2/6 | 21.0ms | 17.7ms | 50.6 MB | 5/6 | 345426 |
| ruby | 23.4ms | 23.4× | 3/6 | 66.8ms | 43.4ms | 23.7 MB | 3/6 | 345426 |
| dotnet | 1.0ms | 1.0× | 1/6 | 23.6ms | 22.6ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 672.3ms | 280.1× | 6/6 | 700.0ms | 27.7ms | 25.2 MB | 3/6 | 229499993 |
| elixir | 37.7ms | 15.7× | 4/6 | 306.8ms | 269.1ms | 78.2 MB | 6/6 | 229499993 |
| python | 46.3ms | 19.3× | 5/6 | 56.1ms | 9.8ms | 9.9 MB | 1/6 | 229499993 |
| node | 3.3ms | 1.4× | 2/6 | 21.0ms | 17.7ms | 49.1 MB | 5/6 | 229499993 |
| ruby | 28.4ms | 11.8× | 3/6 | 71.8ms | 43.4ms | 23.5 MB | 2/6 | 229499993 |
| dotnet | 2.4ms | 1.0× | 1/6 | 25.0ms | 22.6ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.4ms | 31.4× | 6/6 | 172.1ms | 27.7ms | 45.2 MB | 4/6 | 288889 |
| elixir | 12.6ms | 2.7× | 5/6 | 281.7ms | 269.1ms | 88.0 MB | 6/6 | 288889 |
| python | 5.3ms | 1.2× | 2/6 | 15.1ms | 9.8ms | 12.8 MB | 1/6 | 288889 |
| node | 6.3ms | 1.4× | 3/6 | 24.0ms | 17.7ms | 52.5 MB | 5/6 | 288889 |
| ruby | 9.0ms | 2.0× | 4/6 | 52.4ms | 43.4ms | 25.8 MB | 2/6 | 288889 |
| dotnet | 4.6ms | 1.0× | 1/6 | 27.2ms | 22.6ms | 30.0 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 213.5ms | 29.2× | 6/6 | 241.2ms | 27.7ms | 35.7 MB | 4/6 | 50038280 |
| elixir | 41.7ms | 5.7× | 5/6 | 310.8ms | 269.1ms | 78.1 MB | 6/6 | 50038280 |
| python | 27.3ms | 3.7× | 4/6 | 37.1ms | 9.8ms | 9.9 MB | 1/6 | 50038280 |
| node | 7.3ms | 1.0× | 1/6 | 25.0ms | 17.7ms | 50.4 MB | 5/6 | 50038280 |
| ruby | 9.9ms | 1.4× | 3/6 | 53.3ms | 43.4ms | 23.5 MB | 2/6 | 50038280 |
| dotnet | 8.9ms | 1.2× | 2/6 | 31.5ms | 22.6ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 417.0ms | 139.0× | 6/6 | 444.7ms | 27.7ms | 19.9 MB | 2/6 | 327640 |
| elixir | 33.3ms | 11.1× | 5/6 | 302.4ms | 269.1ms | 80.7 MB | 6/6 | 327640 |
| python | 20.4ms | 6.8× | 3/6 | 30.2ms | 9.8ms | 10.0 MB | 1/6 | 327640 |
| node | 7.0ms | 2.3× | 2/6 | 24.7ms | 17.7ms | 52.3 MB | 5/6 | 327640 |
| ruby | 21.0ms | 7.0× | 4/6 | 64.4ms | 43.4ms | 23.8 MB | 3/6 | 327640 |
| dotnet | 3.0ms | 1.0× | 1/6 | 25.6ms | 22.6ms | 30.7 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 31.8ms | 3.5× | 6/6 | 59.5ms | 27.7ms | 21.1 MB | 2/6 | 102632633 |
| elixir | 19.1ms | 2.1× | 4/6 | 288.2ms | 269.1ms | 85.8 MB | 6/6 | 102632633 |
| python | 20.0ms | 2.2× | 5/6 | 29.8ms | 9.8ms | 12.2 MB | 1/6 | 102632633 |
| node | 15.0ms | 1.6× | 3/6 | 32.7ms | 17.7ms | 51.4 MB | 5/6 | 102632633 |
| ruby | 9.1ms | 1.0× | 1/6 | 52.5ms | 43.4ms | 24.0 MB | 3/6 | 102632633 |
| dotnet | 12.8ms | 1.4× | 2/6 | 35.4ms | 22.6ms | 27.2 MB | 4/6 | 102632633 |

## spawn — lightweight concurrent units + result collection  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 1.112s | 55.1× | 5/6 | 1.140s | 27.7ms | 170.1 MB | 5/6 | 12200000 |
| elixir | 79.5ms | 3.9× | 2/6 | 348.6ms | 269.1ms | 88.2 MB | 4/6 | 12200000 |
| python | 1.102s | 54.5× | 4/6 | 1.111s | 9.8ms | 35.9 MB | 2/6 | 12200000 |
| node | 125.4ms | 6.2× | 3/6 | 143.1ms | 17.7ms | 56.0 MB | 3/6 | 12200000 |
| ruby | 4.979s | 246.5× | 6/6 | 5.022s | 43.4ms | 246.4 MB | 6/6 | 12200000 |
| dotnet | 20.2ms | 1.0× | 1/6 | 42.8ms | 22.6ms | 32.2 MB | 1/6 | 12200000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 2.272s | 54.5× | 6/6 | 2.299s | 27.7ms | 14.1 MB | 1/6 | 31781100 |
| elixir | 131.8ms | 3.2× | 2/6 | 400.9ms | 269.1ms | 82.2 MB | 5/6 | 31781100 |
| python | 794.9ms | 19.1× | 5/6 | 804.7ms | 9.8ms | 22.1 MB | 2/6 | 31781100 |
| node | 133.7ms | 3.2× | 3/6 | 151.4ms | 17.7ms | 182.1 MB | 6/6 | 31781100 |
| ruby | 555.7ms | 13.3× | 4/6 | 599.1ms | 43.4ms | 23.7 MB | 3/6 | 31781100 |
| dotnet | 41.7ms | 1.0× | 1/6 | 64.3ms | 22.6ms | 27.9 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 144.3ms | 1.4× | 3/5 | 172.0ms | 27.7ms | 71.9 MB | 4/5 | 0 |
| elixir | 595.4ms | 5.6× | 5/5 | 864.5ms | 269.1ms | 532.1 MB | 5/5 | 0 |
| python | — | — | — | — | — | — | — | ERROR |
| node | 110.1ms | 1.0× | 2/5 | 127.8ms | 17.7ms | 64.5 MB | 3/5 | 0 |
| ruby | 207.3ms | 2.0× | 4/5 | 250.7ms | 43.4ms | 50.6 MB | 2/5 | 0 |
| dotnet | 106.0ms | 1.0× | 1/5 | 128.6ms | 22.6ms | 48.2 MB | 1/5 | 0 |
