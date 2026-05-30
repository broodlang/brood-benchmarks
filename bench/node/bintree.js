const N = parseInt(process.env.BENCH_N || "40", 10);   // repetitions
const DEPTH = 12;

function make(d) {
  if (d === 0) return null;
  return [make(d - 1), make(d - 1)];
}

function check(node) {
  if (node === null) return 1;
  return 1 + check(node[0]) + check(node[1]);
}

let total = 0;
for (let i = 0; i < N; i++) total += check(make(DEPTH));

console.log(total);
