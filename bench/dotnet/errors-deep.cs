namespace Bench;

static class ErrorsDeep
{
    const int DEPTH = 50;

    static int Descend(int d, int i)
    {
        if (d == 0) throw new BenchError(i % 100);
        return 1 + Descend(d - 1, i);
    }

    public static void Run(int n)
    {
        const long MOD = 1000000007;
        long acc = 0;
        for (int i = 0; i < n; i++)
        {
            try { Descend(DEPTH, i); }
            catch (BenchError e) { acc += e.V; }
        }
        Console.WriteLine(acc % MOD);
    }
}
