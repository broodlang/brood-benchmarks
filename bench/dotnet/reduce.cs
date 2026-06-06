namespace Bench;
static class Reduce
{
    public static void Run(int n)
    {
        long acc = 0;
        for (int i = 0; i < n; i++) acc += i;
        Console.WriteLine(acc);
    }
}
