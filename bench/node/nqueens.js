const N = parseInt(process.env.BENCH_N || "10", 10);

function safe(c, placed, d) {
  for (let i = 0; i < placed.length; i++) {
    const p = placed[i];
    if (p === c || p - c === d || p - c === -d) return false;
    d++;
  }
  return true;
}

function solve(row, placed) {
  if (row === N) return 1;
  let total = 0;
  for (let c = 0; c < N; c++) {
    if (safe(c, placed, 1)) total += solve(row + 1, [c, ...placed]);
  }
  return total;
}

console.log(solve(0, []));
