namespace Bench;
static class Primes
{
    static bool IsPrime(int n)
    {
        if (n < 2) return false;
        int limit = (int)Math.Floor(Math.Sqrt(n));
        for (int d = 2; d <= limit; d++)
            if (n % d == 0) return false;
        return true;
    }
    public static void Run(int n)
    {
        int count = 0;
        for (int k = 2; k < n; k++) if (IsPrime(k)) count++;
        Console.WriteLine(count);
    }
}
