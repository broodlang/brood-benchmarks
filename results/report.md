# Brood vs Clojure vs Elixir vs Python vs Node vs Ruby vs .NET — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-28 21:06.
> **Runtimes:** Brood brood 0.1.0; Clojure Clojure 1.12.5 / JDK 25.0.3; Elixir Elixir 1.21.0-dev (b82c44a) (compiled with Erlang/OTP 28); Python Python 3.14.4; Node v22.21.0; Ruby ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu]; .NET 10.0.110.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## nbody — floating-point physics sim (N-body)  (N=50000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | cores | CPU·s | vs best CPU | checksum |
|------|---------|------------|-----|------|---------|----------|-----|-------|-------|-------------|----------|
| brood | — | 10.7× | 3/7 | 339.9ms | — | 50.9 MB | 5/7 | 1.1× | 0.36 | 11.3× | -169078071 |
| clojure | — | 16.8× | 6/7 | 536.6ms | — | 109.3 MB | 7/7 | 2.5× | 1.36 | 42.6× | -169078071 |
| elixir | — | 10.8× | 4/7 | 345.4ms | — | 71.7 MB | 6/7 | 1.4× | 0.50 | 15.6× | -169078071 |
| python | — | 23.2× | 7/7 | 739.0ms | — | 10.2 MB | 1/7 | 1.0× | 0.74 | 23.2× | -169078071 |
| node | — | 1.0× | 2/7 | 32.6ms | — | 50.3 MB | 4/7 | 1.1× | 0.04 | 1.2× | -169078071 |
| ruby | — | 11.2× | 5/7 | 356.6ms | — | 19.0 MB | 2/7 | 1.0× | 0.36 | 11.2× | -169078071 |
| dotnet | — | 1.0× | 1/7 | 31.9ms | — | 26.7 MB | 3/7 | 1.0× | 0.03 | 1.0× | -169078071 |

## pfib — parallel fib — 100 computed at once across cores  (N=31)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | cores | CPU·s | vs best CPU | checksum |
|------|---------|------------|-----|------|---------|----------|-----|-------|-------|-------------|----------|
| brood | — | 1.4× | 2/7 | 192.4ms | — | 24.7 MB | 3/7 | 9.9× | 1.91 | 1.8× | 134626900 |
| clojure | — | 5.5× | 5/7 | 743.3ms | — | 135.3 MB | 6/7 | 5.2× | 3.83 | 3.7× | 134626900 |
| elixir | — | 3.7× | 4/7 | 502.0ms | — | 72.6 MB | 5/7 | 3.2× | 1.63 | 1.6× | 134626900 |
| python | — | 18.0× | 7/7 | 2.444s | — | 16.8 MB | 1/7 | 10.7× | 26.07 | 25.0× | 134626900 |
| node | — | 2.3× | 3/7 | 317.5ms | — | 185.2 MB | 7/7 | 10.3× | 3.27 | 3.1× | 134626900 |
| ruby | — | 14.0× | 6/7 | 1.906s | — | 19.0 MB | 2/7 | 11.0× | 20.89 | 20.1× | 134626900 |
| dotnet | — | 1.0× | 1/7 | 136.0ms | — | 28.0 MB | 4/7 | 7.7× | 1.04 | 1.0× | 134626900 |
