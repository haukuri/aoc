from . import utils

example_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()

lower_case_alphabet = "abcdefghijklmnopqrstuvwxyz"
upper_case_alphabet = lower_case_alphabet.upper()
alphabet = lower_case_alphabet + upper_case_alphabet

def find_misplaced_item_type(contents: str) -> str:
    n = len(contents)
    pivot = n // 2
    a = contents[:pivot]
    b = contents[pivot:]
    assert len(a) == len(b)
    a_types = set(a)
    b_types = set(b)
    common = a_types.intersection(b_types)
    assert len(common) == 1
    for common_type in common:
        return common_type

def type_value(item_type: str) -> int:
    assert len(item_type) == 1
    position = alphabet.find(item_type)
    assert position >= 0
    return position + 1

def solve_part_1(input: str):
    total_value = 0
    for line in input.splitlines():
        misplaced_type = find_misplaced_item_type(line)
        misplaced_type_value = type_value(misplaced_type)
        total_value += misplaced_type_value
    return total_value

def solve_part_2(input: str):
    batch = []
    total_value = 0
    for i, line in enumerate(input.splitlines()):
        bag = set(line)
        batch.append(bag)
        if (i+1) % 3 == 0:
            a, b, c = batch
            common = a & b & c
            assert len(common) == 1
            common_type = next(iter(common))
            common_type_value = type_value(common_type)
            total_value += common_type_value
            batch = []
    return total_value


def test_find_misplaced_item_type():
    assert find_misplaced_item_type("vJrwpWtwJgWrhcsFMMfFFhFp") == "p"
    assert find_misplaced_item_type("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL") == "L"

def test_type_value():
    assert type_value("p") == 16
    assert type_value("L") == 38
    assert type_value("P") == 42
    assert type_value("v") == 22
    assert type_value("t") == 20
    assert type_value("s") == 19

def test_part_1_example():
    assert solve_part_1(example_input) == 157

def test_part_1_actual():
    input = utils.read_text("d03_input.txt")
    assert solve_part_1(input) == 7553

def test_part_2_example():
    assert solve_part_2(example_input) == 70

def test_part_2_actual():
    input = utils.read_text("d03_input.txt")
    assert solve_part_2(input) == 2758
