/* Floating-point math (escape iterations). n x n grid, MAXITER=100.
 * Checksum = total iterations summed over every pixel.
 *
 * No barrier: `total` depends on a data-dependent escape test, so there is no
 * closed form. GCC will vectorise parts of the inner loop, which is correct and
 * left alone — the JITs in this suite vectorise too, and this row is where an AOT
 * compiler's floating-point codegen is supposed to show. */
#include "bench.h"

int main(void) {
    long n = bench_n(540);
    const int MAXITER = 100;
    long total = 0;
    for (long py = 0; py < n; py++) {
        double y0 = ((double)py / (double)n) * 3.0 - 1.5;
        for (long px = 0; px < n; px++) {
            double x0 = ((double)px / (double)n) * 3.0 - 2.0;
            double x = 0.0, y = 0.0, xx = 0.0, yy = 0.0;
            int i = 0;
            while (xx + yy <= 4.0 && i < MAXITER) {
                y = 2.0 * x * y + y0;
                x = xx - yy + x0;
                xx = x * x;
                yy = y * y;
                i++;
            }
            total += i;
        }
    }
    printf("%ld\n", total);
    return 0;
}
