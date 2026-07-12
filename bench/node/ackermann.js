// Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
// Checksum = N * ack(3,9) = N * 4093.
const N = parseInt(process.env.BENCH_N || "6", 10);

function ack(m, k) {
  if (m === 0) return k + 1;
  if (k === 0) return ack(m - 1, 1);
  return ack(m - 1, ack(m, k - 1));
}

let total = 0;
for (let i = 0; i < N; i++) total += ack(3, 9);
console.log(total);
