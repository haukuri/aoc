using System.Reflection;

namespace AdventOfCode.Year2022
{
    [TestClass]
    public class Day01Tests
    {

        [TestMethod]
        public void TestPart1WithExampleInput()
        {
            var solver = new Day01();
            var reader = TestDataReader.Read("Y2023D01P01E.txt");
            var solution = solver.Solve(reader);

            Assert.AreEqual(4, solution.ElfNumber);
            Assert.AreEqual(24_000, solution.MaxCalories);
        }

    }

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
