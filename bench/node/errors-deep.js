const n = parseInt(process.env.BENCH_N || "50000", 10);
const md = 1000000007;
const DEPTH = 50;

class BenchError extends Error {
  constructor(v) { super(); this.v = v; }
}

function descend(d, i) {
  if (d === 0) throw new BenchError(i % 100);
  return 1 + descend(d - 1, i);
}

let acc = 0;
for (let i = 0; i < n; i++) {
  try { descend(DEPTH, i); }
  catch (e) { acc += e.v; }
}
console.log(acc % md);
