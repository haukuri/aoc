from dataclasses import dataclass

import utils

example_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

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

def solve_part_1(input: str):
    directions = parse_input(input)
    s = Vector2D(0, 0)
    h = s
    t = s
    t_path = { t }
    for step in directions:
        h += step
        d = h - t
        if are_adjacent(h, t):
            continue
        if d.x == 0: # up / down
            assert abs(d.y) == 2
            t += Vector2D(0, sign(d.y))
        elif d.y == 0: # right / left
            assert abs(d.x) == 2
            t += Vector2D(sign(d.x), 0)
        else: # diagonal
            assert d.manhattan_distance() <= 3
            t += Vector2D(sign(d.x), sign(d.y))
        t_path.add(t)
        assert are_adjacent(h, t)
    return len(t_path)

def test_parse_input_example():
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
    assert parse_input(example_input) == expected

def test_solve_part_1_example():
    assert solve_part_1(example_input) == 13

def test_solve_part_1_actual():
    actual_input = utils.read_text("d09input.txt")
    assert solve_part_1(actual_input) == 6332
