// Parallel fib: compute fib(N) in 100 tasks at once, summed. Node is
// single-threaded, so using cores for CPU work means worker_threads — a pool
// sized to the core count, with the 100 tasks split across the workers.
// Checksum = 100*fib(N).
const { Worker, isMainThread, parentPort, workerData } = require("worker_threads");
const os = require("os");

const N = parseInt(process.env.BENCH_N || "31", 10);
const TASKS = 100;

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

if (isMainThread) {
  const P = Math.min(TASKS, os.cpus().length);
  let pending = P;
  let total = 0;
  for (let w = 0; w < P; w++) {
    // strided assignment: how many of the 100 tasks this worker owns
    let count = 0;
    for (let i = w; i < TASKS; i += P) count++;
    const worker = new Worker(__filename, { workerData: { count, n: N } });
    worker.on("message", (sub) => {
      total += sub;
      if (--pending === 0) console.log(total);
    });
    worker.on("error", (e) => {
      throw e;
    });
  }
} else {
  const { count, n } = workerData;
  let sub = 0;
  for (let i = 0; i < count; i++) sub += fib(n);
  parentPort.postMessage(sub);
}
