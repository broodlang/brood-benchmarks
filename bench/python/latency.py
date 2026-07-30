# Latency under a fixed arrival rate, open loop. See bench/brood/latency.blsp for the full
# rationale. CPython runs handlers on one thread (the GIL makes threads no help for CPU-bound
# work), so a fat request holds the interpreter and everything scheduled behind it waits —
# which is what a CPU-bound handler does to an asyncio server, and why such work belongs in a
# process pool in production.
import os, time

N = int(os.environ.get("BENCH_N", "50000"))
RATE = 20000
GAP_NS = 1_000_000_000 // RATE
CHEAP = 40
FAT_NS = 500_000

def work(k):
    acc = 0
    for j in range(k):
        v = [j, j + 1, j + 2, j + 3]
        acc += v[0] + v[1] + v[2] + v[3]
    return acc

now = time.perf_counter_ns


def best_work_ns(reps, k):
    best = 0
    for _ in range(reps):
        t = now()
        work(k)
        dt = now() - t
        if best == 0 or dt < best:
            best = dt
    return best


# Calibrate the fat request to ~500us of real work in THIS runtime (warm first — a cold
# sample would size it far too small on a JIT; CPython has no JIT but every port calibrates
# the same way). Reported below so a mis-calibration is visible rather than silent.
for _ in range(60):
    work(5000)
FAT_UNITS = 1000
while True:
    dt = best_work_ns(9, FAT_UNITS)
    if dt >= 200_000:
        FAT_UNITS = FAT_UNITS * FAT_NS // dt
        break
    FAT_UNITS *= 2
FAT_MEASURED_US = best_work_ns(5, FAT_UNITS) // 1000

# Ordinary requests only: a fat request's own latency is >=500us by construction.
lats = []
total = 0
t0 = now()
for i in range(N):
    sched = t0 + i * GAP_NS
    while now() < sched:
        pass
    total += work(CHEAP)
    fat = i % 20 == 0
    if fat:
        work(FAT_UNITS)
    else:
        lats.append((now() - sched) // 1000)
elapsed = now() - t0

lats.sort()
M = len(lats)
pct = lambda p: lats[min(M - 1, (p * M) // 100)]
print(f"#metric fat_units={FAT_UNITS}")
print(f"#metric fat_measured_us={FAT_MEASURED_US}")
print(f"#metric ordinary_n={M}")
print(f"#metric p50_us={pct(50)}")
print(f"#metric p99_us={pct(99)}")
print(f"#metric p999_us={lats[min(M - 1, (999 * M) // 1000)]}")
print(f"#metric max_us={lats[M - 1]}")
print(f"#metric sustained_rps={N * 1_000_000_000 // elapsed}")
print(total)
