const N = parseInt(process.env.BENCH_N || "175", 10);
const MOD = 1000000007;

const A = [], B = [];
for (let i = 0; i < N; i++) {
  const ra = [], rb = [];
  for (let j = 0; j < N; j++) {
    ra.push((i + j) % 100);
    rb.push((i * j) % 100);
  }
  A.push(ra);
  B.push(rb);
}

let total = 0;
for (let i = 0; i < N; i++) {
  const Ai = A[i];
  for (let j = 0; j < N; j++) {
    let s = 0;
    for (let k = 0; k < N; k++) s += Ai[k] * B[k][j];
    total += s;
  }
}

console.log(total % MOD);
