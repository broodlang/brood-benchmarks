const N = parseInt(process.env.BENCH_N || "2000", 10);
let x = 123456789;
const arr = [];
for (let i = 0; i < N; i++) {
  x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF;
  arr.push({ id: i, v: x, name: "item", ok: x % 2 === 0 });
}
const parsed = JSON.parse(JSON.stringify(arr));
let acc = 0;
for (const o of parsed) acc = (acc + o.v) % 2147483647;
console.log(acc);
