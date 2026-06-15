namespace Bench;

// A value-carrying exception, recovered N times — the runtime's error path.
class BenchError : Exception
{
    public int V;
    public BenchError(int v) { V = v; }
}

static class Errors
{
    public static void Run(int n)
    {
        const long MOD = 1000000007;
        long acc = 0;
        for (int i = 0; i < n; i++)
        {
            try
            {
                throw new BenchError(i % 100);
            }
            catch (BenchError e)
            {
                acc += e.V;
            }
        }
        Console.WriteLine(acc % MOD);
    }
}
