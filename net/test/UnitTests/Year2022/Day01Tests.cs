namespace AdventOfCode.Year2022
{
    [TestClass]
    public class Day01Tests
    {

        [TestMethod]
        public void TestPart1WithExampleInput()
        {
            var reader = TestDataReader.Read("Y2023D01P01E.txt");
            var solution = Day01.SolvePart01(reader);

            Assert.AreEqual(24_000, solution);
        }

        [TestMethod]
        public void TestPart1WithActualInput()
        {
            var reader = TestDataReader.Read("Y2023D01.txt");
            var solution = Day01.SolvePart01(reader);

            Assert.AreEqual(71124, solution);
        }

        [TestMethod]
        public void TestPart2WithExampleInput()
        {
            var reader = TestDataReader.Read("Y2023D01P01E.txt");
            var solution = Day01.SolvePart02(reader);

            Assert.AreEqual(45_000, solution);
        }

        [TestMethod]
        public void TestPart2WithActualInput()
        {
            var reader = TestDataReader.Read("Y2023D01.txt");
            var solution = Day01.SolvePart02(reader);

            Assert.AreEqual(204_639, solution);
        }

    }
}
