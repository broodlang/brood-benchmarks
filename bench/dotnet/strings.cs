namespace Bench;
static class Strings
{
    public static void Run(int n)
    {
        var parts = new string[n];
        for (int i = 0; i < n; i++) parts[i] = i.ToString();
        string s = string.Join(",", parts);
        Console.WriteLine(s.Length);
    }
}
