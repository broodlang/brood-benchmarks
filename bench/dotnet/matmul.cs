namespace Bench;
static class Matmul
{
    public static void Run(int n)
    {
        const long MOD = 1000000007;
        var a = new int[n][];
        var b = new int[n][];
        for (int i = 0; i < n; i++)
        {
            a[i] = new int[n];
            b[i] = new int[n];
            for (int j = 0; j < n; j++)
            {
                a[i][j] = (i + j) % 100;
                b[i][j] = (i * j) % 100;
            }
        }
        long total = 0;
        for (int i = 0; i < n; i++)
        {
            var ai = a[i];
            for (int j = 0; j < n; j++)
            {
                long s = 0;
                for (int k = 0; k < n; k++) s += (long)ai[k] * b[k][j];
                total += s;
            }
        }
        Console.WriteLine(total % MOD);
    }
}
