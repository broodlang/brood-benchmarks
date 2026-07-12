// Build N records, JSON.stringify then JSON.parse, checksum sum of "v" mod 2^31.
const N = parseInt(process.env.BENCH_N || "2000", 10);
const A = 1103515245n, C = 12345n, MASK = 0x7FFFFFFFn;
let x = 123456789n;
const arr = [];
for (let i = 0; i < N; i++) {
  x = (x * A + C) & MASK;
  const v = Number(x);
  arr.push({ id: i, v: v, name: "item", ok: v % 2 === 0 });
}
const parsed = JSON.parse(JSON.stringify(arr));
let acc = 0;
for (const o of parsed) acc = (acc + o.v) % 2147483647;
console.log(acc);
