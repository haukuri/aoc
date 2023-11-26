using System.Reflection;

namespace AdventOfCode.Year2022
{
    public class TestDataReader
    {
        public static TextReader Read(string name)
        {
            var assemblyPath = Assembly.GetExecutingAssembly().Location;
            var assemblyDirectory = Path.GetDirectoryName(assemblyPath)!;
            var testDataFolder = Path.Combine(assemblyDirectory, "TestData");
            var filePath = Path.Combine(testDataFolder, name);
            var reader = new StreamReader(filePath);
            return reader;
        }
    }
}
