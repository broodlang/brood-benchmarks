const N = parseInt(process.env.BENCH_N || "50000", 10);

const parts = [];
for (let i = 0; i < N; i++) parts.push(String(i));
const s = parts.join(",");

console.log(s.length);
