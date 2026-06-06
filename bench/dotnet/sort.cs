namespace Bench;
static class Sort
{
    public static void Run(int n)
    {
        const long MOD = 1000000007;
        // LCG: x*1103515245 fits in long (x < 2^31), so no BigInt needed.
        long x = 123456789;
        var data = new long[n];
        for (int i = 0; i < n; i++)
        {
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
            data[i] = x;
        }
        Array.Sort(data);
        long h = 0;
        foreach (var v in data) h = (h * 31 + v) % MOD;
        Console.WriteLine(h);
    }
}
