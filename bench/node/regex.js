// Generate N decimal strings; count full matches of ^[0-9]+$. Checksum = count.
const N = parseInt(process.env.BENCH_N || "20000", 10);
const A = 1103515245n, C = 12345n, MASK = 0x7FFFFFFFn;
const RE = /^[0-9]+$/;
let x = 123456789n, count = 0;
for (let i = 0; i < N; i++) {
  x = (x * A + C) & MASK;
  let s = x.toString();
  if (x % 2n === 0n) s += "x";
  if (RE.test(s)) count++;
}
console.log(count);
