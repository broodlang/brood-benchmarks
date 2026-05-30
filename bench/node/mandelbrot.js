const N = parseInt(process.env.BENCH_N || "128", 10);
const MAXITER = 100;

let total = 0;
for (let py = 0; py < N; py++) {
  const y0 = (py / N) * 3.0 - 1.5;
  for (let px = 0; px < N; px++) {
    const x0 = (px / N) * 3.0 - 2.0;
    let x = 0.0, y = 0.0, i = 0, xx = 0.0, yy = 0.0;
    while (xx + yy <= 4.0 && i < MAXITER) {
      y = 2.0 * x * y + y0;   // uses old x, old y
      x = xx - yy + x0;       // uses old xx, yy
      xx = x * x;
      yy = y * y;
      i++;
    }
    total += i;
  }
}

console.log(total);
