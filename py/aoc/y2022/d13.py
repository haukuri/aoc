import pytest
import functools

from typing import Union

from . import utils

example_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def parse_input(input: str) -> list[tuple[list, list]]:
    lines = input.splitlines()
    lines.reverse()
    packet_pairs = []
    while lines:
        line_a = lines.pop()
        if line_a.strip() == "":
            continue
        line_b = lines.pop()
        packet_a = eval(line_a)
        packet_b = eval(line_b)
        pair = packet_a, packet_b
        packet_pairs.append(pair)
    return packet_pairs

def test_parse_input_example():
    pairs = parse_input(example_input)
    expected = [
        (
            [1,1,3,1,1],
            [1,1,5,1,1]
        ),
        (
            [[1],[2,3,4]],
            [[1],4]
        ),
        (
            [9],
            [[8,7,6]]
        ),
        (
            [[4,4],4,4],
            [[4,4],4,4,4]
        ),
        (
            [7,7,7,7],
            [7,7,7]
        ),
        (
            [],
            [3]
        ),
        (
            [[[]]],
            [[]]
        ),
        (
            [1,[2,[3,[4,[5,6,7]]]],8,9],
            [1,[2,[3,[4,[5,6,0]]]],8,9]
        )
    ]
    assert pairs == expected

def compare(a, b) -> Union[bool, None]:
    a_int = isinstance(a, int)
    b_int = isinstance(b, int)
    a_list = isinstance(a, list)
    b_list = isinstance(b, list)
    assert a_int or a_list
    assert b_int or b_list
    if a_int and b_int:
        if a == b:
            return None
        else:
            return a < b
    if a_list and b_list:
        for a_item, b_item in zip(a, b):
            c = compare(a_item, b_item)
            if c is None:
                continue
            else:
                return c
        len_a = len(a)
        len_b = len(b)
        if len_a == len_b:
            return None
        else:
            return len_a < len_b
    if a_int and b_list:
        return compare([a], b)
    if a_list and b_int:
        return compare(a, [b])
    raise ValueError("Invalid comparison")

compare_test_data = [
    ([1,1,3,1,1], [1,1,5,1,1], True),
    ([[1],[2,3,4]], [[1],4], True),
    ([9], [[8,7,6]], False),
    ([[4,4],4,4], [[4,4],4,4,4], True),
    ([7,7,7,7], [7,7,7], False),
    ([], [3], True),
    ([[[]]], [[]], False),
    ([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9], False)
]

@pytest.mark.parametrize("a, b, expected", compare_test_data)
def test_compare(a, b, expected):
    actual = compare(a, b)
    assert actual == expected

def solve_part_1(input: str) -> int:
    pairs = parse_input(input)
    indices = []
    for i, (a, b) in enumerate(pairs):
        c = compare(a, b)
        assert c is not None
        if c is True:
            indices.append(i + 1)
    return sum(indices)

@functools.total_ordering
class Packet:
    def __init__(self, value):
        self.value = value
    
    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return compare(self.value, other.value)

def solve_part_2(input: str) -> int:
    pairs = parse_input(input)
    packets = []
    dividers = ([[2]], [[6]])
    for a, b in pairs:
        packets.append(a)
        packets.append(b)
    packets.extend(dividers)
    packets.sort(key=Packet)
    index = None
    decoder_key = None
    for k, packet in enumerate(packets):
        current_index = k + 1
        if packet in dividers:
            if index is None:
                index = current_index
            else:
                decoder_key = index * current_index
                break
    assert decoder_key is not None
    return decoder_key

def test_solve_part_1_example_input():
    assert solve_part_1(example_input) == 13

def test_solve_part_1_actual_input():
    actual_input = utils.read_text("d13_input.txt")
    assert solve_part_1(actual_input) == 6484

def test_solve_part_2_example_input():
    assert solve_part_2(example_input) == 140

def test_solve_part_2_actual_input():
    actual_input = utils.read_text("d13_input.txt")
    assert solve_part_2(actual_input) == 19305
