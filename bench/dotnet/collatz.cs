namespace Bench;
static class Collatz
{
    public static void Run(int n)
    {
        int best = 0;
        for (int start = 1; start < n; start++)
        {
            long m = start; int steps = 0;
            while (m != 1)
            {
                if (m % 2 == 0) m /= 2; else m = 3 * m + 1;
                steps++;
            }
            if (steps > best) best = steps;
        }
        Console.WriteLine(best);
    }
}
