namespace Bench;
sealed class Node { public Node L, R; }
static class Bintree
{
    static Node Make(int d) => d == 0 ? null : new Node { L = Make(d - 1), R = Make(d - 1) };
    static long Check(Node node) => node == null ? 1 : 1 + Check(node.L) + Check(node.R);
    public static void Run(int n)
    {
        const int DEPTH = 12;
        long total = 0;
        for (int i = 0; i < n; i++) total += Check(Make(DEPTH));
        Console.WriteLine(total);
    }
}
