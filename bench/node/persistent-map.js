// Read-modify-write churn on a hash map over a 50k key space.
// Checksum = sum of key*value over the map. BigInt LCG (product exceeds 2^53).
const N = parseInt(process.env.BENCH_N || "300000", 10);
const A = 1103515245n, C = 12345n, MASK = 0x7FFFFFFFn, M = 50000n;
let x = 123456789n;
const map = new Map();
for (let i = 0; i < N; i++) {
  x = (x * A + C) & MASK;
  const key = Number(x % M);
  const cur = map.get(key) || 0;
  map.set(key, cur + 1 + (key % 7));
}
let total = 0;
for (const [k, v] of map) total += k * v;
console.log(total);
