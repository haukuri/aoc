namespace AdventOfCode.Year2022
{
    public class Day01
    {
        public static int SolvePart01(TextReader reader)
        {
            var caloriesPerElf = CaloriesPerElf(reader);
            caloriesPerElf.Sort();
            return caloriesPerElf[caloriesPerElf.Count - 1];
        }

        public static int SolvePart02(TextReader reader)
        {
            var caloriesPerElf = CaloriesPerElf(reader);
            caloriesPerElf.Sort();
            var sum = 0;
            for (int i = 0; i < 3; i++)
            {
                var index = caloriesPerElf.Count - 1 - i;
                sum += caloriesPerElf[index];
            }
            return sum;
        }

        private static List<int> CaloriesPerElf(TextReader reader)
        {
            var result = new List<int>();
            var calories = 0;
            foreach (var line in reader.IterLines())
            {
                if (string.IsNullOrEmpty(line))
                {
                    // new elf
                    result.Add(calories);
                    calories = 0;
                }
                else
                {
                    calories += Convert.ToInt32(line);
                }
            }
            if (calories > 0)
            {
                result.Add(calories);
            }
            return result;
        }
    }
}
