const N = parseInt(process.env.BENCH_N || "300000", 10);
const M = 50000;
let x = 123456789;
const map = new Map();
for (let i = 0; i < N; i++) {
  x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF;
  const key = x % M;
  const cur = map.get(key) || 0;
  map.set(key, cur + 1 + (key % 7));
}
let total = 0;
for (const [k, v] of map) total += k * v;
console.log(total);
