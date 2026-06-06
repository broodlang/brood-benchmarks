namespace Bench;
static class Wordcount
{
    public static void Run(int n)
    {
        const long K = 1000;
        long x = 123456789;
        var counts = new Dictionary<long, long>();
        for (int i = 0; i < n; i++)
        {
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
            long key = x % K;
            counts[key] = counts.TryGetValue(key, out var c) ? c + 1 : 1;
        }
        long total = 0;
        foreach (var kv in counts) total += kv.Key * kv.Value;
        Console.WriteLine(total);
    }
}
