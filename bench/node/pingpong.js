// Two worker_threads bounce a token N round trips (isolated message passing, the
// honest Node analog of processes). Checksum = N.
const { Worker, isMainThread, parentPort } = require("worker_threads");
if (!isMainThread) {
  parentPort.on("message", (m) => {
    if (m < 0) process.exit(0);
    parentPort.postMessage(m);
  });
} else {
  const N = parseInt(process.env.BENCH_N || "100000", 10);
  const w = new Worker(__filename);
  let k = 0;
  w.on("message", () => {
    k++;
    if (k >= N) { w.postMessage(-1); console.log(k); w.terminate(); }
    else w.postMessage(k);
  });
  w.postMessage(0);
}
