// Hold N units alive, then hand each a message it must COPY, and collect each result
// through a queue the parent drains one at a time — mirroring a mailbox.
//
// Fairness fix (2026-07-30): the result path was `Promise.all` over a pre-allocated
// array, i.e. a reference store per unit. Brood and Elixir send a reply *message* the
// parent receives individually, so they were paying 2 copied messages per unit against
// Node's 1 delivery + 0. Draining a queue is the honest analogue. (The inbound copy was
// already here: a promise resolution passes a REFERENCE, which is a different and much
// cheaper operation than `send`, so the port copies explicitly to match.)
//
// Node's unit is still not an isolated process — one shared heap, no mailbox, no
// preemption, and a unit that loops starves every other unit on the thread. Its
// concurrency is cooperative microtasks on ONE thread. See BENCHMARKS.md.
// Checksum = N * (sum(payload) + 1).
const N = parseInt(process.env.BENCH_N || "300000", 10);
const payload = Array.from({ length: 16 }, (_, i) => i);
const wake = new Array(N);

// A minimal mailbox: units push, the parent awaits one item at a time. An index cursor
// rather than shift(), which would be O(n) per read and measure the array, not the queue.
const box = [];
let cursor = 0;
let waiting = null;
function deliver(v) {
  box.push(v);
  if (waiting) { const w = waiting; waiting = null; w(); }
}
async function receive() {
  while (cursor >= box.length) await new Promise((r) => { waiting = r; });
  return box[cursor++];
}

for (let i = 0; i < N; i++) {
  new Promise((res) => { wake[i] = res; }).then((p) => {
    let s = 0;
    for (const v of p) s += v;
    deliver(s + 1);                     // reply as a message, not a return value
  });
}
for (let i = 0; i < N; i++) wake[i](payload.slice());   // copy, as `send` would

(async () => {
  let total = 0;
  for (let i = 0; i < N; i++) total += await receive();
  console.log(total);
})();
