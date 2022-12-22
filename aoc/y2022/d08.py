import utils

example_input = """30373
25512
65332
33549
35390"""

def solve_part_1(input: str) -> int:
    lines = input.splitlines()
    grid_height = len(lines)
    grid_width = len(lines[0])
    edge_rows = (0, grid_height - 1)
    edge_cols = (0, grid_width  - 1)
    grid = []
    num_visible = 0
    for r, line in enumerate(lines):
        row = []
        for c, digit in enumerate(line):
            tree_height = int(digit)
            row.append(tree_height)
        grid.append(row)
    for r, row in enumerate(grid):
        for c, tree_height in enumerate(row):
            if r in edge_rows or c in edge_cols:
                num_visible += 1
                continue
            visible_left     = tree_height > max(grid[r][oc] for oc in range(grid_width) if oc < c)
            visible_right    = tree_height > max(grid[r][oc] for oc in range(grid_width) if oc > c)
            visible_top      = tree_height > max(grid[_or][c] for _or in range(grid_height) if _or < r)
            visible_bottom   = tree_height > max(grid[_or][c] for _or in range(grid_height) if _or > r)
            is_visible = visible_left or visible_right or visible_bottom or visible_top
            num_visible += is_visible
    return num_visible

def test_solve_part_1_example():
    assert solve_part_1(example_input) == 21

def test_solve_part_1_actual():
    actual_input = utils.read_text("d08input.txt")
    assert solve_part_1(actual_input) == 1845
