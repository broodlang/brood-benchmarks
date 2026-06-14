// Fan out N promises; each computes fib(15) and resolves with the result.
// Tests promise fan-out under real CPU work per unit.
// Checksum = N * fib(15) = N * 610.
const N = parseInt(process.env.BENCH_N || "10000", 10);

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

Promise.all(Array.from({ length: N }, () => Promise.resolve(fib(15)))).then(
  (results) => {
    let total = 0;
    for (const v of results) total += v;
    console.log(total);
  }
);
