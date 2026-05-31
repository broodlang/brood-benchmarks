# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._
> _`startup` and `http` are latency-sensitive; measured in isolation (best of 5–7) so neighbouring benchmarks' load doesn't inflate them. All other rows are best of 3 from the full suite._


## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 22.1ms | 1.8× | 10.6 MB | 0 |
| elixir | 307.6ms | 25.6× | 90.9 MB | 0 |
| python | 12.0ms | 1.0× | 9.4 MB | 0 |
| node | 21.3ms | 1.8× | 44.7 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 360.9ms | 11.3× | 10.9 MB | 832040 |
| elixir | 414.6ms | 13.0× | 95.3 MB | 832040 |
| python | 73.9ms | 2.3× | 9.5 MB | 832040 |
| node | 32.0ms | 1.0× | 50.4 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 425.9ms | 16.3× | 10.7 MB | 3000000 |
| elixir | 397.5ms | 15.2× | 96.2 MB | 3000000 |
| python | 184.7ms | 7.1× | 9.4 MB | 3000000 |
| node | 26.1ms | 1.0× | 50.6 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.454s | 82.6× | 139.6 MB | 499999500000 |
| elixir | 308.7ms | 17.5× | 91.6 MB | 499999500000 |
| python | 17.6ms | 1.0× | 9.4 MB | 499999500000 |
| node | 30.0ms | 1.7× | 52.7 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 87.4ms | 4.1× | 10.9 MB | 2262 |
| elixir | 345.9ms | 16.4× | 96.4 MB | 2262 |
| python | 21.1ms | 1.0× | 9.6 MB | 2262 |
| node | 25.8ms | 1.2× | 51.3 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.100s | 34.0× | 18.6 MB | 307 |
| elixir | 375.7ms | 11.6× | 95.8 MB | 307 |
| python | 227.7ms | 7.0× | 9.5 MB | 307 |
| node | 32.3ms | 1.0× | 50.7 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 351.5ms | 13.5× | 10.8 MB | 345426 |
| elixir | 385.8ms | 14.8× | 94.7 MB | 345426 |
| python | 75.5ms | 2.9× | 9.9 MB | 345426 |
| node | 26.1ms | 1.0× | 51.8 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 794.8ms | 32.7× | 18.7 MB | 229499993 |
| elixir | 332.9ms | 13.7× | 91.6 MB | 229499993 |
| python | 52.9ms | 2.2× | 9.8 MB | 229499993 |
| node | 24.3ms | 1.0× | 51.3 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 236.6ms | 13.8× | 32.8 MB | 288889 |
| elixir | 331.1ms | 19.4× | 100.7 MB | 288889 |
| python | 17.1ms | 1.0× | 12.6 MB | 288889 |
| node | 28.7ms | 1.7× | 55.5 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 609.2ms | 20.6× | 28.1 MB | 50038280 |
| elixir | 336.5ms | 11.4× | 91.3 MB | 50038280 |
| python | 29.6ms | 1.0× | 9.5 MB | 50038280 |
| node | 32.0ms | 1.1× | 53.0 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 472.5ms | 16.5× | 14.7 MB | 327640 |
| elixir | 347.3ms | 12.1× | 95.7 MB | 327640 |
| python | 29.5ms | 1.0× | 9.9 MB | 327640 |
| node | 28.6ms | 1.0× | 54.2 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 122.3ms | 4.2× | 20.2 MB | 102632633 |
| elixir | 305.2ms | 10.5× | 99.9 MB | 102632633 |
| python | 29.0ms | 1.0× | 11.9 MB | 102632633 |
| node | 37.5ms | 1.3× | 53.8 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 613.2ms | 1.8× | 37.1 MB | 199990000 |
| elixir | 343.9ms | 1.0× | 108.4 MB | 199990000 |

## pfib — parallel fib — 100 computed at once across cores  (N=28)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 3.844s | 29.6× | 102.4 MB | 31781100 |
| elixir | 366.3ms | 2.8× | 95.7 MB | 31781100 |
| python | 294.1ms | 2.3× | 21.6 MB | 31781100 |
| node | 129.9ms | 1.0× | 314.9 MB | 31781100 |

## http — concurrent HTTP — N in-flight GETs to a local server  (N=500)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 188.2ms | 1.2× | 63.6 MB | 500 |
| elixir | 615.4ms | 4.0× | 776.6 MB | 500 |
| python | 224.6ms | 1.5× | 51.5 MB | 500 |
| node | 152.3ms | 1.0× | 69.8 MB | 500 |
