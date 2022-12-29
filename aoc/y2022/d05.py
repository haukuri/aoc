import re

from collections import namedtuple
from typing import Mapping

from . import utils


example_input = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

example_instructions = """
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip().splitlines()

example_stacks = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """.splitlines()

Stacks = Mapping[str, list[str]]
Instruction = namedtuple("Instruction", "num_boxes src_stack dst_stack")

def split_equally(src: str, segment_length: int) -> list[str]:
    src_len = len(src)
    segments = []
    from_pos = 0
    while from_pos < src_len:
        to_pos = from_pos + segment_length
        part = src[from_pos:to_pos]
        segments.append(part)
        from_pos = to_pos
    return segments

def parse_stacks(lines: list[str]) -> Stacks:
    stacks = []
    # the stack labels are on the last line
    stack_numbers = lines[-1]
    stack_labels = []
    for part in split_equally(stack_numbers, 4):
        stack_label = part.strip()
        stack_labels.append(stack_label)
        stacks.append([])
    # go through the stacks
    box_lines = lines[:-1]
    # we iterate through the lines bottom up to build the stacks
    # in the correct order
    box_lines.reverse()
    for line in box_lines:
        parts = split_equally(line, 4)
        for idx, part in enumerate(parts):
            # part should be on the form "[X] " if the corresponding stack
            # has a box at this level. If it does not it should be "    ".
            box_label = part[1]
            if box_label.isalnum():
                stacks[idx].append(box_label)
    result = {
        stack_label: stack 
        for stack_label, stack 
        in zip(stack_labels, stacks)
    }
    return result

def parse_instruction(line: str) -> Instruction:
    m = re.match(r"move (\d+) from (\d+) to (\d+)\s*", line)
    num = int(m.group(1))
    src = m.group(2)
    dst = m.group(3)
    return Instruction(num, src, dst)

def parse_instructions(lines: list[str]) -> list[Instruction]:
    result = []
    for line in lines:
        instruction = parse_instruction(line)
        result.append(instruction)
    return result

def is_empty_or_whitespace(s: str) -> bool:
    return s.isspace() or len(s) == 0

def parse_input(input: str) -> tuple[Stacks, list[Instruction]]:
    lines = input.splitlines()
    # get rid of the first line if it is empty
    if is_empty_or_whitespace(lines[0]):
        lines = lines[1:]
    # also get rid of the last line if it is empty
    if is_empty_or_whitespace(lines[-1]):
        lines.pop()
    stack_lines = []
    instruction_lines = []
    current = stack_lines
    for line in lines:
        if line.isspace() or len(line) == 0:
            current = instruction_lines
        else:
            current.append(line)
    stacks = parse_stacks(stack_lines)
    instructions = parse_instructions(instruction_lines)
    return stacks, instructions

def solve_part_1(input: str) -> str:
    stacks, instructions = parse_input(input)
    for i in instructions:
        src = stacks[i.src_stack]
        dst = stacks[i.dst_stack]
        for _ in range(i.num_boxes):
            crate = src.pop()
            dst.append(crate)
    top_crates = []
    for stack_label in sorted(stacks.keys()):
        stack = stacks[stack_label]
        top_crate = stack[-1]
        top_crates.append(top_crate)
    return "".join(top_crates)

def solve_part_2(input: str) -> str:
    stacks, instructions = parse_input(input)
    for i in instructions:
        src = stacks[i.src_stack]
        dst = stacks[i.dst_stack]
        crates = []
        for _ in range(i.num_boxes):
            crate = src.pop()
            crates.append(crate)
        crates.reverse()
        dst.extend(crates)
    top_crates = []
    for stack_label in sorted(stacks.keys()):
        stack = stacks[stack_label]
        top_crate = stack[-1]
        top_crates.append(top_crate)
    return "".join(top_crates)

def test_split_equally():
    input = "abcdefghijk"
    expected = ["abc", "def", "ghi", "jk"]
    assert split_equally(input, 3) == expected

def test_parse_stacks():
    expected = {
        "1": ["Z", "N"],
        "2": ["M", "C", "D"],
        "3": ["P"]
    }
    assert parse_stacks(example_stacks) == expected

def test_parse_instruction():
    assert parse_instruction("move 3 from 1 to 3") == Instruction(3, "1", "3")

def test_parse_instructions():
    actual = parse_instructions(example_instructions)
    expected = [
        Instruction(1, "2", "1"),
        Instruction(3, "1", "3"),
        Instruction(2, "2", "1"),
        Instruction(1, "1", "2"),
    ]
    assert actual == expected

def test_parse_input():
    actual_stacks, actual_instructions = parse_input(example_input)
    expected_stacks = {
        "1": ["Z", "N"],
        "2": ["M", "C", "D"],
        "3": ["P"]
    }
    expected_instructions = [
        Instruction(1, "2", "1"),
        Instruction(3, "1", "3"),
        Instruction(2, "2", "1"),
        Instruction(1, "1", "2"),
    ]
    assert actual_stacks == expected_stacks
    assert actual_instructions == expected_instructions

def test_solve_part_1_example():
    assert solve_part_1(example_input) == "CMZ"

def test_solve_part_1_actual():
    input = utils.read_text("d05_input.txt")
    actual = solve_part_1(input)
    assert actual == "FZCMJCRHZ"

def test_solve_part_2_example():
    assert solve_part_2(example_input) == "MCD"

def test_solve_part_2_actual():
    input = utils.read_text("d05_input.txt")
    actual = solve_part_2(input)
    assert actual == "JSDHQMZGF"