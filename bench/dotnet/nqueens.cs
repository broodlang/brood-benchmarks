using System.Collections.Generic;

namespace Bench;
static class Nqueens
{
    static bool Safe(int c, List<int> placed, int d)
    {
        foreach (var p in placed)
        {
            if (p == c || p - c == d || p - c == -d) return false;
            d++;
        }
        return true;
    }

    static long Solve(int row, int n, List<int> placed)
    {
        if (row == n) return 1;
        long total = 0;
        for (int c = 0; c < n; c++)
        {
            if (Safe(c, placed, 1))
            {
                var next = new List<int>(placed.Count + 1) { c };
                next.AddRange(placed);
                total += Solve(row + 1, n, next);
            }
        }
        return total;
    }

    public static void Run(int n)
    {
        Console.WriteLine(Solve(0, n, new List<int>()));
    }
}
