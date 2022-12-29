from . import utils

example_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".strip()

class Assignment:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    @classmethod
    def from_encoded_range(cls, encoded_range: str):
        s, e = encoded_range.split("-")
        s, e = int(s), int(e)
        return cls(s, e)

    def overlaps(self, other: "Assignment") -> bool:
        return (
            self.start <= other.start and self.end >= other.start or
            self.fully_contains(other) or
            other.fully_contains(self) or
            self.start <= other.end and self.end >= other.end
        )

    def fully_contains(self, other: "Assignment") -> bool:
        return self.start <= other.start and self.end >= other.end

def parse_input_to_assignment_pairs(input: str):
    for line in input.splitlines():
        a, b = line.split(",")
        assignment_a = Assignment.from_encoded_range(a)
        assignment_b = Assignment.from_encoded_range(b)
        yield assignment_a, assignment_b

def solve_part_1(input: str):
    num_full_containments = 0
    pairs = parse_input_to_assignment_pairs(input)
    for a, b in pairs:
        full_containment = a.fully_contains(b) or b.fully_contains(a)
        if full_containment:
            num_full_containments += 1
    return num_full_containments
        

def solve_part_2(input: str):
    num_overlaps = 0
    pairs = parse_input_to_assignment_pairs(input)
    for a, b in pairs:
        if a.overlaps(b):
            num_overlaps += 1
    return num_overlaps

def test_part_1_example():
    assert solve_part_1(example_input) == 2

def test_part_1_actual():
    input = utils.read_text("d04input.txt")
    assert solve_part_1(input) == 487

def test_part_2_example():
    assert solve_part_2(example_input) == 4

def test_part_2_actual():
    input = utils.read_text("d04input.txt")
    assert solve_part_2(input) == 849
