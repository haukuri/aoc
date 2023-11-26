namespace AdventOfCode.Year2022
{
    [TestClass]
    public class Day01Tests
    {
        private const string ExampleInputData = "Y2022D01P01E.txt";
        private const string ActualInputData = "Y2022D01.txt";

        [TestMethod]
        public void TestPart1WithExampleInput()
        {
            var reader = TestDataReader.Read(ExampleInputData);
            var solution = Day01.SolvePart01(reader);

            Assert.AreEqual(24_000, solution);
        }

        [TestMethod]
        public void TestPart1WithActualInput()
        {
            var reader = TestDataReader.Read(ActualInputData);
            var solution = Day01.SolvePart01(reader);

            Assert.AreEqual(71124, solution);
        }

        [TestMethod]
        public void TestPart2WithExampleInput()
        {
            var reader = TestDataReader.Read(ExampleInputData);
            var solution = Day01.SolvePart02(reader);

            Assert.AreEqual(45_000, solution);
        }

        [TestMethod]
        public void TestPart2WithActualInput()
        {
            var reader = TestDataReader.Read(ActualInputData);
            var solution = Day01.SolvePart02(reader);

            Assert.AreEqual(204_639, solution);
        }

    }
}
