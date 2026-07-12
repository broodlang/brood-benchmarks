// Sieve of Eratosthenes to N, counting primes. Checksum = count of primes <= N.
const N = parseInt(process.env.BENCH_N || "1000000", 10);
const comp = new Uint8Array(N + 1);
for (let p = 2; p * p <= N; p++) {
  if (!comp[p]) for (let j = p * p; j <= N; j += p) comp[j] = 1;
}
let count = 0;
for (let k = 2; k <= N; k++) if (!comp[k]) count++;
console.log(count);
