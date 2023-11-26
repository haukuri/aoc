namespace AdventOfCode.Year2022
{
    public static class TextReaderExtensions
    {
        public static IEnumerable<string> IterLines(this TextReader reader)
        {
            while (true)
            {
                var line = reader.ReadLine();
                if (line == null) break;
                yield return line;
            }
        }
    }
}
