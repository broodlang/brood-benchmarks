const N = parseInt(process.env.BENCH_N || "375000", 10);
const MOD = 1000000007;
let x = 123456789;
const data = new Array(N);
for (let i = 0; i < N; i++) {
  x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF;
  data[i] = x;
}
data.sort((a, b) => a - b);
let h = 0;
for (const v of data) h = (h * 31 + v) % MOD;
console.log(h);
