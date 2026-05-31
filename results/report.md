# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 9.1ms | 1.0× | 9.0 MB | 0 |
| elixir | 301.8ms | 33.2× | 90.6 MB | 0 |
| python | 12.2ms | 1.3× | 9.6 MB | 0 |
| node | 22.9ms | 2.5× | 44.8 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 828.0ms | 25.5× | 9.0 MB | 832040 |
| elixir | 366.8ms | 11.3× | 95.2 MB | 832040 |
| python | 77.5ms | 2.4× | 9.6 MB | 832040 |
| node | 32.5ms | 1.0× | 50.4 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.051s | 40.7× | 9.1 MB | 3000000 |
| elixir | 352.6ms | 13.7× | 94.7 MB | 3000000 |
| python | 184.4ms | 7.1× | 9.5 MB | 3000000 |
| node | 25.8ms | 1.0× | 50.8 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.775s | 91.5× | 138.8 MB | 499999500000 |
| elixir | 303.3ms | 15.6× | 93.3 MB | 499999500000 |
| python | 19.4ms | 1.0× | 9.4 MB | 499999500000 |
| node | 24.7ms | 1.3× | 52.7 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 162.0ms | 8.0× | 9.0 MB | 2262 |
| elixir | 347.2ms | 17.1× | 94.1 MB | 2262 |
| python | 20.3ms | 1.0× | 9.7 MB | 2262 |
| node | 25.5ms | 1.3× | 51.3 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 2.004s | 64.2× | 17.1 MB | 307 |
| elixir | 369.0ms | 11.8× | 97.4 MB | 307 |
| python | 233.1ms | 7.5× | 9.7 MB | 307 |
| node | 31.2ms | 1.0× | 50.4 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 439.3ms | 17.8× | 8.9 MB | 345426 |
| elixir | 395.5ms | 16.0× | 94.5 MB | 345426 |
| python | 81.8ms | 3.3× | 9.6 MB | 345426 |
| node | 24.7ms | 1.0× | 51.4 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.183s | 48.9× | 18.0 MB | 229499993 |
| elixir | 326.5ms | 13.5× | 91.6 MB | 229499993 |
| python | 55.7ms | 2.3× | 9.8 MB | 229499993 |
| node | 24.2ms | 1.0× | 51.3 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 251.4ms | 14.5× | 32.5 MB | 288889 |
| elixir | 374.5ms | 21.6× | 102.7 MB | 288889 |
| python | 17.3ms | 1.0× | 12.7 MB | 288889 |
| node | 28.4ms | 1.6× | 55.3 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 557.2ms | 20.0× | 27.4 MB | 50038280 |
| elixir | 368.6ms | 13.2× | 92.0 MB | 50038280 |
| python | 32.6ms | 1.2× | 9.6 MB | 50038280 |
| node | 27.9ms | 1.0× | 52.7 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 691.3ms | 25.8× | 20.7 MB | 327640 |
| elixir | 394.2ms | 14.7× | 95.1 MB | 327640 |
| python | 29.2ms | 1.1× | 9.8 MB | 327640 |
| node | 26.8ms | 1.0× | 54.2 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 123.7ms | 4.1× | 18.7 MB | 102632633 |
| elixir | 386.9ms | 12.8× | 102.8 MB | 102632633 |
| python | 30.2ms | 1.0× | 11.8 MB | 102632633 |
| node | 41.0ms | 1.4× | 53.9 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 621.7ms | 1.7× | 32.4 MB | 199990000 |
| elixir | 369.9ms | 1.0× | 111.8 MB | 199990000 |
