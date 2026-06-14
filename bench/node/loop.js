const N = parseInt(process.env.BENCH_N || "30000000", 10);

let acc = 0;
for (let i = 0; i < N; i++) {
  acc += i;
}

console.log(acc);
