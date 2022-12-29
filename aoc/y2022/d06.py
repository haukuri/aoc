import pytest

from . import utils

examples_part_1 = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11)
]

examples_part_2 = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26)
]

def find_end_of_first_unique_substring(input: str, length: int) -> int:
    for start_idx in range(0, len(input) - length):
        end_idx = start_idx + length
        section = input[start_idx:end_idx]
        seen = set()
        has_duplicates = False
        for c in section:
            has_duplicates = has_duplicates or c in seen
            seen.add(c)
        if not has_duplicates:
            return end_idx
    return -1

def solve_part_1(input: str) -> int:
    return find_end_of_first_unique_substring(input, 4)

def solve_part_2(input: str) -> int:
    return find_end_of_first_unique_substring(input, 14)

@pytest.mark.parametrize("input, expected", examples_part_1)
def test_solve_part_1_example(input, expected):
    actual = solve_part_1(input)
    assert actual == expected

def test_solve_part_1_input():
    input = utils.read_text("d06input.txt")
    actual = solve_part_1(input)
    assert actual == 1757

@pytest.mark.parametrize("input, expected", examples_part_2)
def test_solve_part_2_example(input, expected):
    actual = solve_part_2(input)
    assert actual == expected

def test_solve_part_2_input():
    input = utils.read_text("d06input.txt")
    actual = solve_part_2(input)
    assert actual == 2950
