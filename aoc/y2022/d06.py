import pytest

import utils

examples = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11)
]


def solve_part_1(input: str) -> int:
    for start_idx in range(0, len(input) - 4):
        end_idx = start_idx + 4
        section = input[start_idx:end_idx]
        seen = set()
        has_duplicates = False
        for c in section:
            has_duplicates = has_duplicates or c in seen
            seen.add(c)
        if not has_duplicates:
            return end_idx
    return -1


@pytest.mark.parametrize("input, expected", examples)
def test_solve_part_1_example(input, expected):
    actual = solve_part_1(input)
    assert actual == expected

def test_solve_part_1_input():
    input = utils.read_text("d06input.txt")
    actual = solve_part_1(input)
    assert actual == 1757
