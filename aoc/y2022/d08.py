from collections import namedtuple

from . import utils

example_input = """30373
25512
65332
33549
35390"""



Grid = namedtuple("Grid", "rows height width")
ViewingDistance = namedtuple("ViewingDistance", "left right up down")

def parse_grid(input: str) -> Grid:
    lines = input.splitlines()
    height = len(lines)
    width = len(lines[0])
    rows = []
    for r, line in enumerate(lines):
        row = []
        for c, digit in enumerate(line):
            tree_height = int(digit)
            row.append(tree_height)
        rows.append(row)
    return Grid(rows, height, width)
    

def solve_part_1(input: str) -> int:
    grid = parse_grid(input)
    num_visible = 0
    edge_rows = (0, grid.height - 1)
    edge_cols = (0, grid.width  - 1)
    for r, row in enumerate(grid.rows):
        for c, tree_height in enumerate(row):
            if r in edge_rows or c in edge_cols:
                num_visible += 1
                continue
            visible_left     = tree_height > max(grid.rows[r][oc] for oc in range(grid.width) if oc < c)
            visible_right    = tree_height > max(grid.rows[r][oc] for oc in range(grid.width) if oc > c)
            visible_top      = tree_height > max(grid.rows[_or][c] for _or in range(grid.height) if _or < r)
            visible_bottom   = tree_height > max(grid.rows[_or][c] for _or in range(grid.height) if _or > r)
            is_visible = visible_left or visible_right or visible_bottom or visible_top
            num_visible += is_visible
    return num_visible

def viewing_distances(grid, r, c):
    tree_height = grid.rows[r][c]
    # search left
    left_distance = 0
    for k in range(c-1, -1, -1):
        other_height = grid.rows[r][k]
        left_distance = c - k
        if other_height >= tree_height:
            break
    # search right
    right_distance = 0
    for k in range(c+1, grid.width):
        other_height = grid.rows[r][k]
        right_distance = k - c
        if other_height >= tree_height:
            break
    # search up
    up_distance = 0
    for k in range(r-1, -1, -1):
        other_height = grid.rows[k][c]
        up_distance = r - k
        if other_height >= tree_height:
            break
    # search down
    down_distance = 0
    for k in range(r+1, grid.height):
        other_height = grid.rows[k][c]
        down_distance = k - r
        if other_height >= tree_height:
            break
    return ViewingDistance(
        left=left_distance,
        right=right_distance,
        up=up_distance,
        down=down_distance
    )

def solve_part_2(input: str) -> int:
    grid = parse_grid(input)
    max_scenic_score = 0
    for r, row in enumerate(grid.rows):
        for c, tree_height in enumerate(row):
            view = viewing_distances(grid, r, c)
            scenic_score = 1
            for distance in view:
                scenic_score *= distance
            if c == 0 or r == 0:
                assert scenic_score == 0
            max_scenic_score = max(scenic_score, max_scenic_score)
    return max_scenic_score



def test_solve_part_1_example():
    assert solve_part_1(example_input) == 21

def test_solve_part_1_actual():
    actual_input = utils.read_text("d08_input.txt")
    assert solve_part_1(actual_input) == 1845

def test_viewing_distance_a():
    grid = parse_grid(example_input)
    r, c = 1, 2
    dist = viewing_distances(grid, r, c)
    assert dist.up == 1
    assert dist.left == 1
    assert dist.right == 2
    assert dist.down == 2

def test_viewing_distance_b():
    grid = parse_grid(example_input)
    r, c = 3, 2
    dist = viewing_distances(grid, r, c)
    assert dist.up == 2
    assert dist.left == 2
    assert dist.right == 2
    assert dist.down == 1

def test_solve_part_2_example():
    assert solve_part_2(example_input) == 8

def test_solve_part_2_actual():
    actual_input = utils.read_text("d08_input.txt")
    assert solve_part_2(actual_input) == 230112
