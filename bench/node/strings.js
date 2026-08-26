const N = parseInt(process.env.BENCH_N || "500000", 10);
const parts = new Array(N);
for (let i = 0; i < N; i++) parts[i] = i;
const s = parts.join(",");
console.log(s.length);
