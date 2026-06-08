// Fan out N promises, each resolving with its index; collect and sum.
// Promises are Node's lightest concurrent unit — all run on the same event-loop
// thread via the microtask queue. Checksum = N*(N-1)/2.
const N = parseInt(process.env.BENCH_N || "20000", 10);

Promise.all(Array.from({ length: N }, (_, i) => Promise.resolve(i))).then(
  (results) => {
    let total = 0;
    for (const v of results) total += v;
    console.log(total);
  }
);
