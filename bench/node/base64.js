const N = parseInt(process.env.BENCH_N || "50000", 10);
let x = 123456789;
const bytes = Buffer.alloc(N);
for (let i = 0; i < N; i++) { x = (Math.imul(x, 1103515245) + 12345) & 0x7FFFFFFF; bytes[i] = x % 256; }
const enc = bytes.toString("base64");
const dec = Buffer.from(enc, "base64");
let encSum = 0;
for (let i = 0; i < enc.length; i++) encSum = (encSum + enc.charCodeAt(i)) % 2147483647;
let decSum = 0;
for (let i = 0; i < dec.length; i++) decSum = (decSum + dec[i]) % 2147483647;
console.log((encSum + decSum) % 2147483647);
