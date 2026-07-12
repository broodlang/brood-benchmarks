namespace Bench;
using System.Text.RegularExpressions;
static class RegexBench
{
    // Generate N decimal strings; count full matches of \A[0-9]+\z. Checksum = count.
    public static void Run(int n)
    {
        var re = new Regex(@"\A[0-9]+\z", RegexOptions.Compiled);
        long x = 123456789;
        int count = 0;
        for (int i = 0; i < n; i++)
        {
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
            string s = x.ToString();
            if (x % 2 == 0) s += "x";
            if (re.IsMatch(s)) count++;
        }
        Console.WriteLine(count);
    }
}
