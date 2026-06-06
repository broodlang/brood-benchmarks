# Brood vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). `compute` ≈ wall − that language's own `startup` (so a slow-booting runtime's real compute speed is visible — e.g. the BEAM). RSS = peak resident memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of the languages with a port._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 27.9ms | — | 2.4× | 4/6 | 11.3 MB | 2/6 | 0 |
| elixir | 345.4ms | — | 30.3× | 6/6 | 91.6 MB | 6/6 | 0 |
| python | 11.4ms | — | 1.0× | 1/6 | 9.5 MB | 1/6 | 0 |
| node | 21.1ms | — | 1.9× | 2/6 | 44.7 MB | 5/6 | 0 |
| ruby | 43.6ms | — | 3.8× | 5/6 | 23.2 MB | 3/6 | 0 |
| dotnet | 23.5ms | — | 2.1× | 3/6 | 25.5 MB | 4/6 | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 497.2ms | 469.3ms | 16.1× | 6/6 | 11.4 MB | 2/6 | 832040 |
| elixir | 373.1ms | 27.7ms | 12.1× | 5/6 | 94.2 MB | 6/6 | 832040 |
| python | 73.0ms | 61.6ms | 2.4× | 3/6 | 9.5 MB | 1/6 | 832040 |
| node | 30.9ms | 9.8ms | 1.0× | 1/6 | 50.1 MB | 5/6 | 832040 |
| ruby | 100.8ms | 57.2ms | 3.3× | 4/6 | 23.3 MB | 3/6 | 832040 |
| dotnet | 30.9ms | 7.4ms | 1.0× | 2/6 | 25.2 MB | 4/6 | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 544.2ms | 516.3ms | 19.6× | 6/6 | 11.4 MB | 2/6 | 3000000 |
| elixir | 374.8ms | 29.4ms | 13.5× | 5/6 | 94.4 MB | 6/6 | 3000000 |
| python | 191.3ms | 179.9ms | 6.9× | 4/6 | 9.6 MB | 1/6 | 3000000 |
| node | 27.8ms | 6.7ms | 1.0× | 1/6 | 51.0 MB | 5/6 | 3000000 |
| ruby | 118.3ms | 74.7ms | 4.3× | 3/6 | 23.2 MB | 3/6 | 3000000 |
| dotnet | 34.2ms | 10.7ms | 1.2× | 2/6 | 26.1 MB | 4/6 | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 271.9ms | 244.0ms | 14.3× | 5/6 | 20.2 MB | 2/6 | 499999500000 |
| elixir | 349.7ms | 4.3ms | 18.4× | 6/6 | 93.2 MB | 6/6 | 499999500000 |
| python | 19.0ms | 7.6ms | 1.0× | 1/6 | 9.5 MB | 1/6 | 499999500000 |
| node | 29.8ms | 8.7ms | 1.6× | 3/6 | 52.6 MB | 5/6 | 499999500000 |
| ruby | 42.5ms | 0.0ms | 2.2× | 4/6 | 23.2 MB | 3/6 | 499999500000 |
| dotnet | 25.0ms | 1.5ms | 1.3× | 2/6 | 25.8 MB | 4/6 | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 95.7ms | 67.8ms | 4.3× | 5/6 | 11.1 MB | 2/6 | 2262 |
| elixir | 372.1ms | 26.7ms | 16.5× | 6/6 | 94.7 MB | 6/6 | 2262 |
| python | 22.5ms | 11.1ms | 1.0× | 1/6 | 9.6 MB | 1/6 | 2262 |
| node | 30.9ms | 9.8ms | 1.4× | 3/6 | 51.4 MB | 5/6 | 2262 |
| ruby | 53.8ms | 10.2ms | 2.4× | 4/6 | 23.2 MB | 3/6 | 2262 |
| dotnet | 30.2ms | 6.7ms | 1.3× | 2/6 | 25.9 MB | 4/6 | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 880.9ms | 853.0ms | 31.1× | 6/6 | 18.8 MB | 2/6 | 307 |
| elixir | 371.7ms | 26.3ms | 13.1× | 5/6 | 95.3 MB | 6/6 | 307 |
| python | 238.3ms | 226.9ms | 8.4× | 4/6 | 9.4 MB | 1/6 | 307 |
| node | 32.5ms | 11.4ms | 1.1× | 2/6 | 50.4 MB | 5/6 | 307 |
| ruby | 136.2ms | 92.6ms | 4.8× | 3/6 | 23.2 MB | 3/6 | 307 |
| dotnet | 28.3ms | 4.8ms | 1.0× | 1/6 | 26.0 MB | 4/6 | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 385.4ms | 357.5ms | 14.2× | 5/6 | 11.5 MB | 2/6 | 345426 |
| elixir | 418.9ms | 73.5ms | 15.4× | 6/6 | 94.8 MB | 6/6 | 345426 |
| python | 76.7ms | 65.3ms | 2.8× | 4/6 | 9.9 MB | 1/6 | 345426 |
| node | 28.3ms | 7.2ms | 1.0× | 2/6 | 51.6 MB | 5/6 | 345426 |
| ruby | 70.6ms | 27.0ms | 2.6× | 3/6 | 23.3 MB | 3/6 | 345426 |
| dotnet | 27.2ms | 3.7ms | 1.0× | 1/6 | 26.1 MB | 4/6 | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 895.2ms | 867.3ms | 37.9× | 6/6 | 19.2 MB | 2/6 | 229499993 |
| elixir | 371.1ms | 25.7ms | 15.7× | 5/6 | 92.3 MB | 6/6 | 229499993 |
| python | 51.2ms | 39.8ms | 2.2× | 3/6 | 9.6 MB | 1/6 | 229499993 |
| node | 25.2ms | 4.1ms | 1.1× | 2/6 | 51.1 MB | 5/6 | 229499993 |
| ruby | 67.5ms | 23.9ms | 2.9× | 4/6 | 23.4 MB | 3/6 | 229499993 |
| dotnet | 23.6ms | 0.1ms | 1.0× | 1/6 | 26.2 MB | 4/6 | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 286.8ms | 258.9ms | 19.2× | 5/6 | 36.1 MB | 4/6 | 288889 |
| elixir | 310.5ms | 0.0ms | 20.8× | 6/6 | 101.7 MB | 6/6 | 288889 |
| python | 14.9ms | 3.5ms | 1.0× | 1/6 | 12.4 MB | 1/6 | 288889 |
| node | 30.8ms | 9.7ms | 2.1× | 3/6 | 55.3 MB | 5/6 | 288889 |
| ruby | 48.6ms | 5.0ms | 3.3× | 4/6 | 25.5 MB | 2/6 | 288889 |
| dotnet | 26.8ms | 3.3ms | 1.8× | 2/6 | 30.2 MB | 3/6 | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 666.6ms | 638.7ms | 23.1× | 6/6 | 28.6 MB | 4/6 | 50038280 |
| elixir | 321.8ms | 0.0ms | 11.2× | 5/6 | 92.6 MB | 6/6 | 50038280 |
| python | 33.1ms | 21.7ms | 1.1× | 3/6 | 9.6 MB | 1/6 | 50038280 |
| node | 28.8ms | 7.7ms | 1.0× | 1/6 | 52.8 MB | 5/6 | 50038280 |
| ruby | 51.7ms | 8.1ms | 1.8× | 4/6 | 23.2 MB | 2/6 | 50038280 |
| dotnet | 32.1ms | 8.6ms | 1.1× | 2/6 | 27.2 MB | 3/6 | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 585.3ms | 557.4ms | 21.4× | 6/6 | 15.3 MB | 2/6 | 327640 |
| elixir | 355.5ms | 10.1ms | 13.0× | 5/6 | 97.3 MB | 6/6 | 327640 |
| python | 29.3ms | 17.9ms | 1.1× | 3/6 | 9.9 MB | 1/6 | 327640 |
| node | 27.4ms | 6.3ms | 1.0× | 1/6 | 54.5 MB | 5/6 | 327640 |
| ruby | 61.4ms | 17.8ms | 2.2× | 4/6 | 23.6 MB | 3/6 | 327640 |
| dotnet | 28.9ms | 5.4ms | 1.1× | 2/6 | 30.5 MB | 4/6 | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 140.0ms | 112.1ms | 4.8× | 5/6 | 20.6 MB | 2/6 | 102632633 |
| elixir | 336.4ms | 0.0ms | 11.6× | 6/6 | 98.8 MB | 6/6 | 102632633 |
| python | 29.1ms | 17.7ms | 1.0× | 1/6 | 11.9 MB | 1/6 | 102632633 |
| node | 45.4ms | 24.3ms | 1.6× | 3/6 | 53.4 MB | 5/6 | 102632633 |
| ruby | 56.4ms | 12.8ms | 1.9× | 4/6 | 23.8 MB | 3/6 | 102632633 |
| dotnet | 40.4ms | 16.9ms | 1.4× | 2/6 | 27.1 MB | 4/6 | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 326.9ms | 299.0ms | 1.0× | 1/2 | 37.2 MB | 1/2 | 199990000 |
| elixir | 349.9ms | 4.5ms | 1.1× | 2/2 | 112.5 MB | 2/2 | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 956.8ms | 928.9ms | 20.8× | 6/6 | 27.2 MB | 3/6 | 31781100 |
| elixir | 386.6ms | 41.2ms | 8.4× | 5/6 | 96.5 MB | 5/6 | 31781100 |
| python | 296.7ms | 285.3ms | 6.4× | 4/6 | 22.0 MB | 1/6 | 31781100 |
| node | 135.4ms | 114.3ms | 2.9× | 2/6 | 342.5 MB | 6/6 | 31781100 |
| ruby | 176.9ms | 133.3ms | 3.8× | 3/6 | 23.3 MB | 2/6 | 31781100 |
| dotnet | 46.1ms | 22.6ms | 1.0× | 1/6 | 27.8 MB | 4/6 | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |
|------|------|---------|-----------|-----|----------|-----|----------|
| brood | 256.4ms | 228.5ms | 1.2× | 2/6 | 85.1 MB | 5/6 | 500 |
| elixir | 653.0ms | 307.6ms | 3.1× | 6/6 | 723.9 MB | 6/6 | 500 |
| python | 310.2ms | 298.8ms | 1.5× | 4/6 | 46.8 MB | 2/6 | 500 |
| node | 208.7ms | 187.6ms | 1.0× | 1/6 | 69.3 MB | 4/6 | 500 |
| ruby | 342.9ms | 299.3ms | 1.6× | 5/6 | 49.8 MB | 3/6 | 500 |
| dotnet | 299.8ms | 276.3ms | 1.4× | 3/6 | 46.1 MB | 1/6 | 500 |
