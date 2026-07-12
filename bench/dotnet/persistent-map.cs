namespace Bench;
static class PersistentMap
{
    // Read-modify-write churn on a Dictionary over a 50k key space.
    // Checksum = sum of key*value over the map.
    public static void Run(int n)
    {
        const long MASK = 0x7FFFFFFF, M = 50000;
        long x = 123456789;
        var d = new Dictionary<long, long>();
        for (int i = 0; i < n; i++)
        {
            x = (x * 1103515245 + 12345) & MASK;
            long key = x % M;
            long delta = 1 + key % 7;
            d[key] = d.TryGetValue(key, out var c) ? c + delta : delta;
        }
        long total = 0;
        foreach (var kv in d) total += kv.Key * kv.Value;
        Console.WriteLine(total);
    }
}
