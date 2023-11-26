namespace AdventOfCode.Year2022
{
    public class Day01 : ISolution<Day01Solution>
    {
        public Day01Solution Solve(TextReader reader)
        {
            var currentCalories = 0;
            var maxCalories = 0;
            var maxCalorieHolder = 0;
            var elfNumber = 1;

            foreach (var line in reader.IterLines())
            {
                if (string.IsNullOrEmpty(line))
                {
                    currentCalories = 0;
                    elfNumber++;
                }
                else
                {
                    currentCalories += Convert.ToInt32(line);
                    if (currentCalories > maxCalories)
                    {
                        maxCalories = currentCalories;
                        maxCalorieHolder = elfNumber;
                    }
                }
            }

            var solution = new Day01Solution(maxCalories, maxCalorieHolder);
            return solution;
        }
    }

    public record Day01Solution(int MaxCalories, int ElfNumber);

    public interface ISolution<T>
    {
        T Solve(TextReader reader);
    }

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
