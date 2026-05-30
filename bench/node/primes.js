const N = parseInt(process.env.BENCH_N || "20000", 10);

function isPrime(n) {
  if (n < 2) return false;
  const limit = Math.floor(Math.sqrt(n));   // once — no d*d in the loop
  for (let d = 2; d <= limit; d++) {
    if (n % d === 0) return false;
  }
  return true;
}

let count = 0;
for (let n = 2; n < N; n++) {
  if (isPrime(n)) count++;
}

console.log(count);
