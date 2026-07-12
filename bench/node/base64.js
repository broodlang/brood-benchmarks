// Generate N bytes, base64 encode+decode. Checksum = (sum enc char codes + sum
// decoded bytes) mod 2^31.
const N = parseInt(process.env.BENCH_N || "50000", 10);
const A = 1103515245n, C = 12345n, MASK = 0x7FFFFFFFn;
let x = 123456789n;
const bytes = Buffer.alloc(N);
for (let i = 0; i < N; i++) { x = (x * A + C) & MASK; bytes[i] = Number(x % 256n); }
const enc = bytes.toString("base64");
const dec = Buffer.from(enc, "base64");
let encSum = 0;
for (let i = 0; i < enc.length; i++) encSum = (encSum + enc.charCodeAt(i)) % 2147483647;
let decSum = 0;
for (let i = 0; i < dec.length; i++) decSum = (decSum + dec[i]) % 2147483647;
console.log((encSum + decSum) % 2147483647);
