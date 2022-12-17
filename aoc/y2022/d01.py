import pathlib

example_input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def split_batches(text: str):
    batch = []
    for line in text.splitlines():
        line = line.strip()
        if line == "":
            if batch:
                yield batch
                batch = []
        else:
            batch.append(line)
    if batch:
        yield batch

def count_calories(input_data: str) -> list[int]:
    max_sum = 0
    calories = []
    for batch in split_batches(input_data):
        numbers = [int(line) for line in batch]
        current_sum = sum(numbers)
        calories.append(current_sum)
    return calories

def solve_part_1(input_data: str) -> int:
    calories = count_calories(input_data)
    return max(calories)

def solve_part_2(input_data: str) -> int:
    calories = count_calories(input_data)
    calories.sort(reverse=True)
    top_3 = calories[:3]
    return sum(top_3)


def test_example_part_1():
    assert solve_part_1(example_input) == 24_000

def test_example_part_2():
    assert solve_part_2(example_input) == 45_000

def run():
    input_path = pathlib.Path(__file__).parent / "d01input.txt"
    input_text = input_path.read_text()
    output_1 = solve_part_1(input_text)
    print("Part 1", output_1)

    output_2 = solve_part_2(input_text)
    print("Part 2", output_2)



if __name__ == "__main__":
    run()
