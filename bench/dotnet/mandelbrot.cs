namespace Bench;
static class Mandelbrot
{
    public static void Run(int n)
    {
        const int MAXITER = 100;
        long total = 0;
        for (int py = 0; py < n; py++)
        {
            double y0 = ((double)py / n) * 3.0 - 1.5;
            for (int px = 0; px < n; px++)
            {
                double x0 = ((double)px / n) * 3.0 - 2.0;
                double x = 0.0, y = 0.0, xx = 0.0, yy = 0.0; int i = 0;
                while (xx + yy <= 4.0 && i < MAXITER)
                {
                    y = 2.0 * x * y + y0;
                    x = xx - yy + x0;
                    xx = x * x;
                    yy = y * y;
                    i++;
                }
                total += i;
            }
        }
        Console.WriteLine(total);
    }
}
