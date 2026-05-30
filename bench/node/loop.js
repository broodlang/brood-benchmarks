const N = parseInt(process.env.BENCH_N || "3000000", 10);

let acc = 0;
for (let i = 0; i < N; i++) {
  acc += 1;
}

console.log(acc);
