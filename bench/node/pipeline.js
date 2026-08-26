const N = parseInt(process.env.BENCH_N || "100000", 10);
function* range(n) { for (let i = 0; i < n; i++) yield i; }
const total = range(N)
  .filter((i) => i % 3 === 0 || i % 5 === 0)
  .map((i) => i * i)
  .reduce((a, b) => a + b, 0);
console.log(total);
