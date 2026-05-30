# Brood vs Elixir vs Python vs Node — benchmark results

_Best of 3 runs per program; full sizes. Wall = total process time (startup + compute). RSS = peak resident memory._

## startup — interpreter/VM startup + base memory  (N=0)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 8.8ms | 1.0× | 8.7 MB | 0 |
| elixir | 311.8ms | 35.4× | 90.6 MB | 0 |
| python | 10.3ms | 1.2× | 9.6 MB | 0 |
| node | 23.3ms | 2.6× | 44.9 MB | 0 |

## fib — naive recursion / function-call overhead  (N=30)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.706s | 55.6× | 15.9 MB | 832040 |
| elixir | 338.3ms | 11.0× | 94.0 MB | 832040 |
| python | 72.9ms | 2.4× | 9.6 MB | 832040 |
| node | 30.7ms | 1.0× | 50.4 MB | 832040 |

## loop — raw iteration (tail recursion vs for-loop)  (N=3000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 2.218s | 77.3× | 16.0 MB | 3000000 |
| elixir | 362.0ms | 12.6× | 95.4 MB | 3000000 |
| python | 186.9ms | 6.5× | 9.6 MB | 3000000 |
| node | 28.7ms | 1.0× | 50.6 MB | 3000000 |

## reduce — higher-order fold over a range  (N=1000000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 3.539s | 204.6× | 124.7 MB | 499999500000 |
| elixir | 311.1ms | 18.0× | 94.1 MB | 499999500000 |
| python | 17.3ms | 1.0× | 9.4 MB | 499999500000 |
| node | 25.0ms | 1.4× | 52.7 MB | 499999500000 |

## primes — integer arithmetic (trial division)  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 348.0ms | 17.3× | 15.8 MB | 2262 |
| elixir | 368.0ms | 18.3× | 95.5 MB | 2262 |
| python | 20.1ms | 1.0× | 9.8 MB | 2262 |
| node | 24.4ms | 1.2× | 51.5 MB | 2262 |

## collatz — integer arithmetic + tight inner loop  (N=30000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 4.246s | 133.9× | 15.8 MB | 307 |
| elixir | 356.4ms | 11.2× | 98.4 MB | 307 |
| python | 235.4ms | 7.4× | 9.4 MB | 307 |
| node | 31.7ms | 1.0× | 50.6 MB | 307 |

## mandelbrot — floating-point math (escape iterations)  (N=128)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.049s | 42.5× | 19.8 MB | 345426 |
| elixir | 358.1ms | 14.5× | 95.6 MB | 345426 |
| python | 76.8ms | 3.1× | 10.1 MB | 345426 |
| node | 24.7ms | 1.0× | 51.9 MB | 345426 |

## matmul — nested loops + indexing (integer NxN)  (N=80)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 2.626s | 105.5× | 18.7 MB | 229499993 |
| elixir | 307.7ms | 12.4× | 91.0 MB | 229499993 |
| python | 55.9ms | 2.2× | 9.8 MB | 229499993 |
| node | 24.9ms | 1.0× | 51.3 MB | 229499993 |

## strings — string building (join) + length  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 487.5ms | 29.7× | 40.2 MB | 288889 |
| elixir | 317.3ms | 19.3× | 100.7 MB | 288889 |
| python | 16.4ms | 1.0× | 12.6 MB | 288889 |
| node | 28.1ms | 1.7× | 55.3 MB | 288889 |

## wordcount — hash-map build (immutable vs mutable)  (N=100000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 539.8ms | 19.2× | 27.3 MB | 50038280 |
| elixir | 336.9ms | 12.0× | 92.4 MB | 50038280 |
| python | 30.8ms | 1.1× | 9.8 MB | 50038280 |
| node | 28.1ms | 1.0× | 52.9 MB | 50038280 |

## bintree — allocation / GC pressure (build+walk trees)  (N=40)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 1.244s | 47.3× | 28.3 MB | 327640 |
| elixir | 371.2ms | 14.1× | 98.1 MB | 327640 |
| python | 32.0ms | 1.2× | 10.0 MB | 327640 |
| node | 26.3ms | 1.0× | 52.7 MB | 327640 |

## sort — sort a list of ints + checksum walk  (N=50000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 163.6ms | 5.7× | 24.1 MB | 102632633 |
| elixir | 495.2ms | 17.4× | 101.3 MB | 102632633 |
| python | 28.5ms | 1.0× | 12.0 MB | 102632633 |
| node | 34.5ms | 1.2× | 54.0 MB | 102632633 |

## spawn — lightweight processes + messaging  (N=20000)

| lang | wall | vs fastest | peak RSS | checksum |
|------|------|-----------|----------|----------|
| brood | 634.1ms | 1.8× | 32.0 MB | 199990000 |
| elixir | 354.9ms | 1.0× | 111.4 MB | 199990000 |
