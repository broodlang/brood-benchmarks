const N = parseInt(process.env.BENCH_N || "750000", 10);
const K = 1000;
let x = 123456789;
const counts = new Map();
for (let i = 0; i < N; i++) {
  x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF;
  const key = x % K;
  counts.set(key, (counts.get(key) || 0) + 1);
}
let total = 0;
for (const [k, v] of counts) total += k * v;
console.log(total);
