from dataclasses import dataclass

from . import utils

example_input_a = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

example_input_b = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

@dataclass(frozen=True)
class Vector2D:
    x: int
    y: int
    
    def __add__(self, other):
        nx = self.x + other.x
        ny = self.y + other.y
        return Vector2D(nx, ny)
    
    def __sub__(self, other):
        nx = self.x - other.x
        ny = self.y - other.y
        return Vector2D(nx, ny)
    
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)
    
def are_adjacent(a, b):
    d = a - b
    return abs(d.x) <= 1 and abs(d.y) <= 1

unit_vectors = {
    "U": Vector2D(0, 1),
    "D": Vector2D(0, -1),
    "L": Vector2D(-1, 0),
    "R": Vector2D(1, 0),
}

def parse_input(input: str) -> list[Vector2D]:
    result = []
    for line in input.splitlines():
        direction, count = line.split(" ")
        v = unit_vectors[direction]
        count = int(count)
        for _ in range(count):
            result.append(v)
    return result

def sign(x: int):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        raise ValueError

def move_tail(h, t):
    d = h - t
    if are_adjacent(h, t):
        nt = t
    elif d.x == 0: # up / down
        assert abs(d.y) == 2
        nt =  t + Vector2D(0, sign(d.y))
    elif d.y == 0: # right / left
        assert abs(d.x) == 2
        nt =  t + Vector2D(sign(d.x), 0)
    else: # diagonal
        nt =  t + Vector2D(sign(d.x), sign(d.y))
        assert (h - nt).manhattan_distance() <= 3
    assert are_adjacent(h, nt)
    return nt

def solve_part_1(input: str):
    directions = parse_input(input)
    s = Vector2D(0, 0)
    h = s
    t = s
    t_path = { t }
    for step in directions:
        h += step
        t = move_tail(h, t)
        t_path.add(t)
    return len(t_path)

def solve_part_2(input: str):
    directions = parse_input(input)
    s = Vector2D(0, 0)
    n = 10
    rope = [s for _ in range(n)]
    t_path = { s }
    for step in directions:
        rope[0] += step
        for k in range(1, n):
            rope[k] = move_tail(rope[k-1], rope[k])
        t_path.add(rope[-1])
    return len(t_path)


def test_parse_input_example_a():
    r = Vector2D(1, 0)
    l = Vector2D(-1, 0)
    u = Vector2D(0, 1)
    d = Vector2D(0, -1)
    expected = [
        r, r, r, r,
        u, u, u, u,
        l, l, l,
        d,
        r, r, r, r,
        d, 
        l, l, l, l, l,
        r, r,
    ]
    assert parse_input(example_input_a) == expected

def test_solve_part_1_example_a():
    assert solve_part_1(example_input_a) == 13

def test_solve_part_1_actual():
    actual_input = utils.read_text("d09_input.txt")
    assert solve_part_1(actual_input) == 6332

def test_solve_part_2_example_a():
    assert solve_part_2(example_input_a) == 1

def test_solve_part_2_example_b():
    assert solve_part_2(example_input_b) == 36

def test_solve_part_2_actual():
    actual_input = utils.read_text("d09_input.txt")
    assert solve_part_2(actual_input) == 2511
