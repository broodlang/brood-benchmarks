# Brood — benchmark results

> **Machine:** `whklat` (12 cores), Linux-7.0.0-28-generic-x86_64-with-glibc2.43 — 2026-07-30 12:50.
> **Runtimes:** Brood brood 0.1.0.
> **Isolation:** taskset pin (compute→cores 8-11, concurrency→0-11); 0.25s settle.
> **Warmup:** one discarded startup run per language.

_best of 3 runs; startup best of 9; spawn/pfib/http best of 7 per program; full sizes. **compute = wall − startup** (startup is that language's own boot time from its `startup`-row wall). Rankings and ratios are by **compute** so a slow-booting runtime's real work speed is visible (e.g. the BEAM boots ~400ms but computes fast). On the `startup` row itself rankings are by wall (compute ≈ 0). RSS = peak resident memory. `pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the languages with a port._

## spawn-live — hold N units alive, then wake each with a copied message  (N=300000)

| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | cores | CPU·s | vs best CPU | checksum |
|------|---------|------------|-----|------|---------|----------|-----|-------|-------|-------------|----------|
| brood | — | 1.0× | 1/1 | 2.854s | — | 1703.3 MB | 1/1 | 2.5× | 7.19 | 1.0× | 36300000 |
