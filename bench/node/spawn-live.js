// Hold N units alive, then hand each a message it must COPY.
//
// The copy is not decoration — it is what makes this comparable to a process runtime.
// On the BEAM and in Brood, `send` copies: the receiver cannot observe the sender's
// later mutations. A promise resolution passes a REFERENCE, which is a different and
// much cheaper operation, so the port copies explicitly to match the semantics.
// (Without it this row scored 0.15s by doing nothing at all.)
//
// Node's unit is still not an isolated process — one shared heap, no mailbox, and a
// unit that loops starves every other unit on the thread. See BENCHMARKS.md.
// Checksum = N * (sum(payload) + 1).
const N = parseInt(process.env.BENCH_N || "300000", 10);
const payload = Array.from({ length: 16 }, (_, i) => i);
const wake = new Array(N);
const units = new Array(N);
for (let i = 0; i < N; i++) {
  units[i] = new Promise((res) => { wake[i] = res; }).then((p) => {
    let s = 0;
    for (const v of p) s += v;
    return s + 1;
  });
}
for (let i = 0; i < N; i++) wake[i](payload.slice());   // copy, as `send` would
Promise.all(units).then((rs) => {
  let total = 0;
  for (const v of rs) total += v;
  console.log(total);
});
