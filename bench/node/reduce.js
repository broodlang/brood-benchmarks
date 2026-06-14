const N = parseInt(process.env.BENCH_N || "5000000", 10);

// higher-order fold: a per-element callback over a materialised range (mirrors
// Brood's (reduce + 0 (range n))), not a hand-rolled for-loop (that's `loop`).
const acc = Array.from({ length: N }, (_, i) => i).reduce((a, b) => a + b, 0);

console.log(acc);
