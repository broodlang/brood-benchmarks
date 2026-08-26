const N = parseInt(process.env.BENCH_N || "20000", 10);
const RE = /^[0-9]+$/;
let x = 123456789, count = 0;
for (let i = 0; i < N; i++) {
  x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF;
  let s = x.toString();
  if (x % 2 === 0) s += "x";
  if (RE.test(s)) count++;
}
console.log(count);
