const N = parseInt(process.env.BENCH_N || "5000000", 10);
function* range(n) { for (let i = 0; i < n; i++) yield i; }
const acc = range(N).reduce((a, b) => a + b, 0);
console.log(acc);
