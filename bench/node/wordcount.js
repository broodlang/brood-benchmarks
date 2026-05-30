const N = parseInt(process.env.BENCH_N || "100000", 10);
const K = 1000n;

// LCG: the x*1103515245 product exceeds 2^53, so use BigInt for exactness.
const A = 1103515245n, C = 12345n, M = 0x7FFFFFFFn;
let x = 123456789n;
const counts = new Map();
for (let i = 0; i < N; i++) {
  x = (x * A + C) & M;
  const key = Number(x % K);
  counts.set(key, (counts.get(key) || 0) + 1);
}

let total = 0;
for (const [k, v] of counts) total += k * v;

console.log(total);
