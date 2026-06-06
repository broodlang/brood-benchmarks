namespace Bench;
static class Fib
{
    static long Run0(int n) => n < 2 ? n : Run0(n - 1) + Run0(n - 2);
    public static void Run(int n) => Console.WriteLine(Run0(n));
}
