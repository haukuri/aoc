import utils

example_input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def solve_part_1(input_data: str) -> int:
    acc = 0
    for line in input_data.splitlines():
        first_found = False
        first_digit = 0
        second_digit = 0
        for char in line:
            try:
                digit = int(char)
            except ValueError:
                continue
            if not first_found:
                first_digit = digit
                second_digit = digit
                first_found = True
            else:
                second_digit = digit
        value = 10 * first_digit + second_digit
        acc += value
        print(value)
    return acc


def test_solve_part_1_example():
    actual = solve_part_1(example_input)
    assert actual == 142


def test_solve_part_1_input():
    input_text = utils.read_text("d01_input.txt")
    actual = solve_part_1(input_text)
    assert actual == 54450
