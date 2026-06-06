namespace Bench;
static class Loop
{
    public static void Run(int n)
    {
        long acc = 0;
        for (int i = 0; i < n; i++) acc += 1;
        Console.WriteLine(acc);
    }
}
