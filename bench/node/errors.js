const n = parseInt(process.env.BENCH_N || "200000", 10);
const md = 1000000007;

class BenchError extends Error {
  constructor(v) { super(); this.v = v; }
}

let acc = 0;
for (let i = 0; i < n; i++) {
  try {
    throw new BenchError(i % 100);
  } catch (e) {
    acc += e.v;
  }
}

console.log(acc % md);
