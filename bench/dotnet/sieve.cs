namespace Bench;
static class Sieve
{
    // Sieve of Eratosthenes to N. Checksum = count of primes <= N.
    public static void Run(int n)
    {
        var comp = new bool[n + 1];
        for (long p = 2; p * p <= n; p++)
        {
            if (!comp[p])
                for (long j = p * p; j <= n; j += p) comp[j] = true;
        }
        int count = 0;
        for (int k = 2; k <= n; k++) if (!comp[k]) count++;
        Console.WriteLine(count);
    }
}
