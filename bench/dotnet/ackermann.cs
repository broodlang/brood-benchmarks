namespace Bench;
static class Ackermann
{
    // Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
    // Checksum = N * ack(3,9) = N * 4093.
    static long Ack(long m, long k)
    {
        if (m == 0) return k + 1;
        if (k == 0) return Ack(m - 1, 1);
        return Ack(m - 1, Ack(m, k - 1));
    }

    public static void Run(int n)
    {
        long total = 0;
        // large-stack thread so depth ~4093 never overflows the default 1MB stack
        var t = new System.Threading.Thread(() =>
        {
            for (int i = 0; i < n; i++) total += Ack(3, 9);
        }, 256 * 1024 * 1024);
        t.Start();
        t.Join();
        Console.WriteLine(total);
    }
}
