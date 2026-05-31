# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 10.8ms | 1.0× | 8.6 MB | 0 |
| elixir | 353.4ms | 32.7× | 91.6 MB | 0 |
| python | 12.2ms | 1.1× | 9.5 MB | 0 |
| node | 27.3ms | 2.5× | 44.7 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 823.9ms | 25.0× | 8.6 MB | 832040 |
| elixir | 446.8ms | 13.5× | 93.7 MB | 832040 |
| python | 72.9ms | 2.2× | 9.6 MB | 832040 |
| node | 33.0ms | 1.0× | 50.4 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.062s | 44.6× | 8.9 MB | 3000000 |
| elixir | 332.9ms | 14.0× | 93.8 MB | 3000000 |
| python | 184.4ms | 7.7× | 9.5 MB | 3000000 |
| node | 23.8ms | 1.0× | 50.8 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.788s | 102.2× | 138.9 MB | 499999500000 |
| elixir | 321.0ms | 18.3× | 91.6 MB | 499999500000 |
| python | 17.5ms | 1.0× | 9.5 MB | 499999500000 |
| node | 27.1ms | 1.5× | 52.4 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 159.9ms | 7.9× | 8.9 MB | 2262 |
| elixir | 394.9ms | 19.5× | 94.2 MB | 2262 |
| python | 20.3ms | 1.0× | 9.6 MB | 2262 |
| node | 23.7ms | 1.2× | 51.1 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.951s | 59.7× | 17.1 MB | 307 |
| elixir | 383.1ms | 11.7× | 94.7 MB | 307 |
| python | 228.5ms | 7.0× | 9.6 MB | 307 |
| node | 32.7ms | 1.0× | 50.6 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 433.3ms | 14.5× | 8.8 MB | 345426 |
| elixir | 394.5ms | 13.2× | 96.3 MB | 345426 |
| python | 79.9ms | 2.7× | 10.1 MB | 345426 |
| node | 29.8ms | 1.0× | 51.7 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.188s | 48.7× | 18.0 MB | 229499993 |
| elixir | 331.9ms | 13.6× | 91.8 MB | 229499993 |
| python | 53.8ms | 2.2× | 9.8 MB | 229499993 |
| node | 24.4ms | 1.0× | 51.7 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 249.4ms | 15.6× | 32.9 MB | 288889 |
| elixir | 325.6ms | 20.4× | 101.6 MB | 288889 |
| python | 16.0ms | 1.0× | 12.5 MB | 288889 |
| node | 31.3ms | 2.0× | 55.5 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 545.0ms | 18.4× | 27.6 MB | 50038280 |
| elixir | 339.8ms | 11.4× | 92.0 MB | 50038280 |
| python | 29.7ms | 1.0× | 9.8 MB | 50038280 |
| node | 32.4ms | 1.1× | 53.3 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 690.9ms | 25.4× | 18.9 MB | 327640 |
| elixir | 385.1ms | 14.2× | 94.9 MB | 327640 |
| python | 31.2ms | 1.1× | 10.0 MB | 327640 |
| node | 27.2ms | 1.0× | 52.7 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 123.3ms | 4.1× | 18.8 MB | 102632633 |
| elixir | 357.0ms | 11.8× | 100.0 MB | 102632633 |
| python | 30.3ms | 1.0× | 11.8 MB | 102632633 |
| node | 37.4ms | 1.2× | 53.9 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 612.9ms | 1.6× | 31.3 MB | 199990000 |
| elixir | 378.3ms | 1.0× | 110.3 MB | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 3.986s | 30.3× | 953.9 MB | 31781100 |
| elixir | 394.2ms | 3.0× | 95.8 MB | 31781100 |
| python | 304.0ms | 2.3× | 21.6 MB | 31781100 |
| node | 131.5ms | 1.0× | 318.9 MB | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 234.9ms | 1.1× | 64.5 MB | 500 |
| elixir | 606.1ms | 2.8× | 781.5 MB | 500 |
| python | 324.9ms | 1.5× | 48.7 MB | 500 |
| node | 214.7ms | 1.0× | 69.4 MB | 500 |
