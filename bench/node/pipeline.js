const N = parseInt(process.env.BENCH_N || "100000", 10);

// map / filter / reduce pipeline: square the multiples of 3 or 5, sum the squares.
const total = Array.from({ length: N }, (_, i) => i)
  .filter((i) => i % 3 === 0 || i % 5 === 0)
  .map((i) => i * i)
  .reduce((a, b) => a + b, 0);

console.log(total);
