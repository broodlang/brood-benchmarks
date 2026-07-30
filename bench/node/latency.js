// Latency under a fixed arrival rate, open loop. See bench/brood/latency.blsp for the full
// rationale. Every 20th request occupies ~500us of CPU, calibrated per runtime at startup as
// real work; percentiles cover the other 95%, so the question is what a busy handler does to
// everyone else. Node has one JS thread, so a CPU-bound handler runs to completion before
// anything else can — which is what such a handler does to an event loop, and the reason that
// work belongs on a worker_thread in production. Checksum covers only the cheap round.
const N = parseInt(process.env.BENCH_N || "50000", 10);
const RATE = 20000, GAP_NS = Math.floor(1e9 / RATE), CHEAP = 40, FAT_NS = 500000;

function work(k) {
  let acc = 0;
  for (let j = 0; j < k; j++) { const v = [j, j + 1, j + 2, j + 3]; acc += v[0] + v[1] + v[2] + v[3]; }
  return acc;
}
const nowNs = () => performance.now() * 1e6;

function bestWorkNs(reps, k) {
  let best = 0;
  for (let i = 0; i < reps; i++) {
    const t = nowNs(); work(k); const dt = nowNs() - t;
    if (best === 0 || dt < best) best = dt;
  }
  return best;
}
// Warm before calibrating: on a JIT a cold sample sizes the fat request far too small.
for (let i = 0; i < 60; i++) work(5000);
let FAT_UNITS = 1000;
for (;;) { const dt = bestWorkNs(9, FAT_UNITS); if (dt >= 200000) { FAT_UNITS = Math.floor(FAT_UNITS * FAT_NS / dt); break; } FAT_UNITS *= 2; }
const fatMeasured = Math.floor(bestWorkNs(5, FAT_UNITS) / 1000);

const lats = [];
let sum = 0;
const t0 = nowNs();
for (let i = 0; i < N; i++) {
  const sched = t0 + i * GAP_NS;
  while (nowNs() < sched) { /* spin to the scheduled instant */ }
  sum += work(CHEAP);
  const fat = i % 20 === 0;
  if (fat) work(FAT_UNITS);
  else lats.push((nowNs() - sched) / 1000);
}
const elapsed = nowNs() - t0;
lats.sort((a, b) => a - b);
const M = lats.length;
const pct = (p) => Math.floor(lats[Math.min(M - 1, Math.floor((p * M) / 100))]);
console.log(`#metric fat_units=${FAT_UNITS}`);
console.log(`#metric fat_measured_us=${fatMeasured}`);
console.log(`#metric ordinary_n=${M}`);
console.log(`#metric p50_us=${pct(50)}`);
console.log(`#metric p99_us=${pct(99)}`);
console.log(`#metric p999_us=${Math.floor(lats[Math.min(M - 1, Math.floor((999 * M) / 1000))])}`);
console.log(`#metric max_us=${Math.floor(lats[M - 1])}`);
console.log(`#metric sustained_rps=${Math.floor((N * 1e9) / elapsed)}`);
console.log(sum);
