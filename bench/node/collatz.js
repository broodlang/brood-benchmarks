const N = parseInt(process.env.BENCH_N || "500000", 10);

let best = 0;
for (let start = 1; start < N; start++) {
  let n = start, steps = 0;
  while (n !== 1) {
    if (n % 2 === 0) n = n / 2;
    else n = 3 * n + 1;
    steps++;
  }
  if (steps > best) best = steps;
}

console.log(best);
