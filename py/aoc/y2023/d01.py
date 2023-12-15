import re

import utils

import pytest

example_input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example_input_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

digits_pattern = "[0-9]"
extended_digits_pattern = "[0-9]|one|two|three|four|five|six|seven|eight|nine"
digit_to_int_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def extract_digits(line: str, extended: bool = False) -> list[int]:
    pattern = extended_digits_pattern if extended else digits_pattern
    return [digit_to_int_map[digit] for digit in re.findall(pattern, line)]


def extract_digits2(line: str):
    length = len(line)
    result = []
    if length == 0:
        return result
    pos = 0
    while pos < length:
        for key, value in digit_to_int_map.items():
            if line.startswith(key, pos):
                result.append(value)    
        pos += 1
    return result


def compute_line_value(line: str, extended: bool) -> int:
    digits = extract_digits2(line) if extended else extract_digits(line)
    length = len(digits)
    if length == 0:
        return 0
    else:
        return digits[0] * 10 + digits[-1]


def solve_part_1(input_data: str) -> int:
    acc = 0
    for line in input_data.splitlines():
        value = compute_line_value(line, extended=False)
        acc += value
    return acc


def solve_part_2(input_data: str) -> int:
    acc = 0
    for line in input_data.splitlines():
        value = compute_line_value(line, extended=True)
        acc += value
    return acc


def test_solve_part_1_example():
    actual = solve_part_1(example_input)
    assert actual == 142


def test_solve_part_1_input():
    input_text = utils.read_text("d01_input.txt")
    actual = solve_part_1(input_text)
    assert actual == 54450


def test_solve_part_2_example():
    actual = solve_part_2(example_input_2)
    assert actual == 281


def test_solve_part_2_input():
    input_text = utils.read_text("d01_input.txt")
    actual = solve_part_2(input_text)
    assert actual == 54265


def test_string_find():
    example = "seven4eight5one"
    match = re.findall(extended_digits_pattern, example)
    assert match == ["seven", "4", "eight", "5", "one"]


def test_extract_digits():
    example = "seven4eight5one"
    actual = extract_digits(example, extended_digits_pattern)
    assert actual == [7, 4, 8, 5, 1]


def test_compute_line_when_there_are_multiple_digits():
    example = "seven4eight5one"
    actual = compute_line_value(example, True)
    assert actual == 71


def test_compute_line_when_there_is_one_digit():
    example = "onerass"
    actual = compute_line_value(example, True)
    assert actual == 11


def test_compute_line_value_when_there_is_no_digit():
    example = "rass"
    actual = compute_line_value(example, True)
    assert actual == 0


def test_extract_digits_for_two2tdjdfbqtqxrs119r():
    example = "two2tdjdfbqtqxrs119r"
    actual = extract_digits(example, True)
    assert actual == [2, 2, 1, 1, 9]


@pytest.mark.parametrize(
    "line,expected",
    [
        ("two1nine", [2, 1, 9]),
        ("eightwothree", [8, 2, 3]),
        ("abcone2threexyz", [1, 2, 3]),
        ("xtwone3four", [2, 1, 3, 4]),
        ("4nineeightseven2", [4, 9, 8, 7, 2]),
        ("zoneight234", [1, 8, 2, 3, 4]),
        ("7pqrstsixteen", [7, 6]),
    ],
)
def test_extract_digits2(line, expected):
    actual = extract_digits2(line)
    assert actual == expected
2