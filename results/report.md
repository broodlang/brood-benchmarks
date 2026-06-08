# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

_Best of 3 runs per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 27.9ms | 2.4× | 4/6 | 27.9ms | — | 11.3 MB | 2/6 | 0 |
| elixir | 345.4ms | 30.3× | 6/6 | 345.4ms | — | 91.6 MB | 6/6 | 0 |
| python | 11.4ms | 1.0× | 1/6 | 11.4ms | — | 9.5 MB | 1/6 | 0 |
| node | 21.1ms | 1.9× | 2/6 | 21.1ms | — | 44.7 MB | 5/6 | 0 |
| ruby | 43.6ms | 3.8× | 5/6 | 43.6ms | — | 23.2 MB | 3/6 | 0 |
| dotnet | 23.5ms | 2.1× | 3/6 | 23.5ms | — | 25.5 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 469.3ms | 63.4× | 6/6 | 497.2ms | 27.9ms | 11.4 MB | 2/6 | 832040 |
| elixir | 27.7ms | 3.7× | 3/6 | 373.1ms | 345.4ms | 94.2 MB | 6/6 | 832040 |
| python | 61.6ms | 8.3× | 5/6 | 73.0ms | 11.4ms | 9.5 MB | 1/6 | 832040 |
| node | 9.8ms | 1.3× | 2/6 | 30.9ms | 21.1ms | 50.1 MB | 5/6 | 832040 |
| ruby | 57.2ms | 7.7× | 4/6 | 100.8ms | 43.6ms | 23.3 MB | 3/6 | 832040 |
| dotnet | 7.4ms | 1.0× | 1/6 | 30.9ms | 23.5ms | 25.2 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 516.3ms | 77.1× | 6/6 | 544.2ms | 27.9ms | 11.4 MB | 2/6 | 3000000 |
| elixir | 29.4ms | 4.4× | 3/6 | 374.8ms | 345.4ms | 94.4 MB | 6/6 | 3000000 |
| python | 179.9ms | 26.9× | 5/6 | 191.3ms | 11.4ms | 9.6 MB | 1/6 | 3000000 |
| node | 6.7ms | 1.0× | 1/6 | 27.8ms | 21.1ms | 51.0 MB | 5/6 | 3000000 |
| ruby | 74.7ms | 11.1× | 4/6 | 118.3ms | 43.6ms | 23.2 MB | 3/6 | 3000000 |
| dotnet | 10.7ms | 1.6× | 2/6 | 34.2ms | 23.5ms | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 244.0ms | 244.0× | 6/6 | 271.9ms | 27.9ms | 20.2 MB | 2/6 | 499999500000 |
| elixir | 4.3ms | 4.3× | 3/6 | 349.7ms | 345.4ms | 93.2 MB | 6/6 | 499999500000 |
| python | 7.6ms | 7.6× | 4/6 | 19.0ms | 11.4ms | 9.5 MB | 1/6 | 499999500000 |
| node | 8.7ms | 8.7× | 5/6 | 29.8ms | 21.1ms | 52.6 MB | 5/6 | 499999500000 |
| ruby | 0.0ms | < 1× | 1/6 | 42.5ms | 43.6ms | 23.2 MB | 3/6 | 499999500000 |
| dotnet | 1.5ms | 1.5× | 2/6 | 25.0ms | 23.5ms | 25.8 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 67.8ms | 10.1× | 6/6 | 95.7ms | 27.9ms | 11.1 MB | 2/6 | 2262 |
| elixir | 26.7ms | 4.0× | 5/6 | 372.1ms | 345.4ms | 94.7 MB | 6/6 | 2262 |
| python | 11.1ms | 1.7× | 4/6 | 22.5ms | 11.4ms | 9.6 MB | 1/6 | 2262 |
| node | 9.8ms | 1.5× | 2/6 | 30.9ms | 21.1ms | 51.4 MB | 5/6 | 2262 |
| ruby | 10.2ms | 1.5× | 3/6 | 53.8ms | 43.6ms | 23.2 MB | 3/6 | 2262 |
| dotnet | 6.7ms | 1.0× | 1/6 | 30.2ms | 23.5ms | 25.9 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 853.0ms | 177.7× | 6/6 | 880.9ms | 27.9ms | 18.8 MB | 2/6 | 307 |
| elixir | 26.3ms | 5.5× | 3/6 | 371.7ms | 345.4ms | 95.3 MB | 6/6 | 307 |
| python | 226.9ms | 47.3× | 5/6 | 238.3ms | 11.4ms | 9.4 MB | 1/6 | 307 |
| node | 11.4ms | 2.4× | 2/6 | 32.5ms | 21.1ms | 50.4 MB | 5/6 | 307 |
| ruby | 92.6ms | 19.3× | 4/6 | 136.2ms | 43.6ms | 23.2 MB | 3/6 | 307 |
| dotnet | 4.8ms | 1.0× | 1/6 | 28.3ms | 23.5ms | 26.0 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 357.5ms | 96.6× | 6/6 | 385.4ms | 27.9ms | 11.5 MB | 2/6 | 345426 |
| elixir | 73.5ms | 19.9× | 5/6 | 418.9ms | 345.4ms | 94.8 MB | 6/6 | 345426 |
| python | 65.3ms | 17.6× | 4/6 | 76.7ms | 11.4ms | 9.9 MB | 1/6 | 345426 |
| node | 7.2ms | 1.9× | 2/6 | 28.3ms | 21.1ms | 51.6 MB | 5/6 | 345426 |
| ruby | 27.0ms | 7.3× | 3/6 | 70.6ms | 43.6ms | 23.3 MB | 3/6 | 345426 |
| dotnet | 3.7ms | 1.0× | 1/6 | 27.2ms | 23.5ms | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 867.3ms | 867.3× | 6/6 | 895.2ms | 27.9ms | 19.2 MB | 2/6 | 229499993 |
| elixir | 25.7ms | 25.7× | 4/6 | 371.1ms | 345.4ms | 92.3 MB | 6/6 | 229499993 |
| python | 39.8ms | 39.8× | 5/6 | 51.2ms | 11.4ms | 9.6 MB | 1/6 | 229499993 |
| node | 4.1ms | 4.1× | 2/6 | 25.2ms | 21.1ms | 51.1 MB | 5/6 | 229499993 |
| ruby | 23.9ms | 23.9× | 3/6 | 67.5ms | 43.6ms | 23.4 MB | 3/6 | 229499993 |
| dotnet | 0.1ms | < 1× | 1/6 | 23.6ms | 23.5ms | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 258.9ms | 258.9× | 6/6 | 286.8ms | 27.9ms | 36.1 MB | 4/6 | 288889 |
| elixir | 0.0ms | < 1× | 1/6 | 310.5ms | 345.4ms | 101.7 MB | 6/6 | 288889 |
| python | 3.5ms | 3.5× | 3/6 | 14.9ms | 11.4ms | 12.4 MB | 1/6 | 288889 |
| node | 9.7ms | 9.7× | 5/6 | 30.8ms | 21.1ms | 55.3 MB | 5/6 | 288889 |
| ruby | 5.0ms | 5.0× | 4/6 | 48.6ms | 43.6ms | 25.5 MB | 2/6 | 288889 |
| dotnet | 3.3ms | 3.3× | 2/6 | 26.8ms | 23.5ms | 30.2 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 638.7ms | 638.7× | 6/6 | 666.6ms | 27.9ms | 28.6 MB | 4/6 | 50038280 |
| elixir | 0.0ms | < 1× | 1/6 | 321.8ms | 345.4ms | 92.6 MB | 6/6 | 50038280 |
| python | 21.7ms | 21.7× | 5/6 | 33.1ms | 11.4ms | 9.6 MB | 1/6 | 50038280 |
| node | 7.7ms | 7.7× | 2/6 | 28.8ms | 21.1ms | 52.8 MB | 5/6 | 50038280 |
| ruby | 8.1ms | 8.1× | 3/6 | 51.7ms | 43.6ms | 23.2 MB | 2/6 | 50038280 |
| dotnet | 8.6ms | 8.6× | 4/6 | 32.1ms | 23.5ms | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 557.4ms | 103.2× | 6/6 | 585.3ms | 27.9ms | 15.3 MB | 2/6 | 327640 |
| elixir | 10.1ms | 1.9× | 3/6 | 355.5ms | 345.4ms | 97.3 MB | 6/6 | 327640 |
| python | 17.9ms | 3.3× | 5/6 | 29.3ms | 11.4ms | 9.9 MB | 1/6 | 327640 |
| node | 6.3ms | 1.2× | 2/6 | 27.4ms | 21.1ms | 54.5 MB | 5/6 | 327640 |
| ruby | 17.8ms | 3.3× | 4/6 | 61.4ms | 43.6ms | 23.6 MB | 3/6 | 327640 |
| dotnet | 5.4ms | 1.0× | 1/6 | 28.9ms | 23.5ms | 30.5 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 112.1ms | 112.1× | 6/6 | 140.0ms | 27.9ms | 20.6 MB | 2/6 | 102632633 |
| elixir | 0.0ms | < 1× | 1/6 | 336.4ms | 345.4ms | 98.8 MB | 6/6 | 102632633 |
| python | 17.7ms | 17.7× | 4/6 | 29.1ms | 11.4ms | 11.9 MB | 1/6 | 102632633 |
| node | 24.3ms | 24.3× | 5/6 | 45.4ms | 21.1ms | 53.4 MB | 5/6 | 102632633 |
| ruby | 12.8ms | 12.8× | 2/6 | 56.4ms | 43.6ms | 23.8 MB | 3/6 | 102632633 |
| dotnet | 16.9ms | 16.9× | 3/6 | 40.4ms | 23.5ms | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 299.0ms | 66.4× | 2/2 | 326.9ms | 27.9ms | 37.2 MB | 1/2 | 199990000 |
| elixir | 4.5ms | 1.0× | 1/2 | 349.9ms | 345.4ms | 112.5 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 928.9ms | 41.1× | 6/6 | 956.8ms | 27.9ms | 27.2 MB | 3/6 | 31781100 |
| elixir | 41.2ms | 1.8× | 2/6 | 386.6ms | 345.4ms | 96.5 MB | 5/6 | 31781100 |
| python | 285.3ms | 12.6× | 5/6 | 296.7ms | 11.4ms | 22.0 MB | 1/6 | 31781100 |
| node | 114.3ms | 5.1× | 3/6 | 135.4ms | 21.1ms | 342.5 MB | 6/6 | 31781100 |
| ruby | 133.3ms | 5.9× | 4/6 | 176.9ms | 43.6ms | 23.3 MB | 2/6 | 31781100 |
| dotnet | 22.6ms | 1.0× | 1/6 | 46.1ms | 23.5ms | 27.8 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |
|------|---------|------------|-----|------|---------|----------|-----|----------|
| brood | 228.5ms | 1.2× | 2/6 | 256.4ms | 27.9ms | 85.1 MB | 5/6 | 500 |
| elixir | 307.6ms | 1.6× | 6/6 | 653.0ms | 345.4ms | 723.9 MB | 6/6 | 500 |
| python | 298.8ms | 1.6× | 4/6 | 310.2ms | 11.4ms | 46.8 MB | 2/6 | 500 |
| node | 187.6ms | 1.0× | 1/6 | 208.7ms | 21.1ms | 69.3 MB | 4/6 | 500 |
| ruby | 299.3ms | 1.6× | 5/6 | 342.9ms | 43.6ms | 49.8 MB | 3/6 | 500 |
| dotnet | 276.3ms | 1.5× | 3/6 | 299.8ms | 23.5ms | 46.1 MB | 1/6 | 500 |
