const N = parseInt(process.env.BENCH_N || "750000", 10);
const MOD = 1000000007;

// LCG with BigInt (product exceeds 2^53); values themselves fit in a double.
const A = 1103515245n, C = 12345n, M = 0x7FFFFFFFn;
let x = 123456789n;
const data = new Array(N);
for (let i = 0; i < N; i++) {
  x = (x * A + C) & M;
  data[i] = Number(x);
}

data.sort((a, b) => a - b);

let h = 0;
for (const v of data) h = (h * 31 + v) % MOD;

console.log(h);
