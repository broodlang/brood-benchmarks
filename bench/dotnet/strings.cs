using System.Linq;
namespace Bench;
static class Strings
{
    public static void Run(int n)
    {
        // `string.Join`'s IEnumerable<T> overload formats each element itself, so this
        // neither materialises a string[] nor calls ToString() explicitly — the same
        // lazy shape the other ports use.
        string s = string.Join(",", Enumerable.Range(0, n));
        Console.WriteLine(s.Length);
    }
}
