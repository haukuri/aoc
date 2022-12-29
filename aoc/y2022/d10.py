import utils

def solve_part_1(input: str) -> int:
    clock = 0
    x_register = 1
    signal_strength_sum = 0
    def increment_clock():
        nonlocal clock
        nonlocal x_register
        nonlocal signal_strength_sum
        clock += 1
        should_measure = clock in (20, 60, 100, 140, 180, 220)
        if should_measure:
            signal_strength = clock * x_register
            signal_strength_sum += signal_strength
    for line in input.splitlines():
        parts = line.split(" ")
        instruction = parts[0]
        if instruction == "noop":
            increment_clock()
        elif instruction == "addx":
            arg = int(parts[1])
            increment_clock()
            increment_clock()
            x_register += arg
    return signal_strength_sum

def test_solve_part_1_example_input():
    example_input = utils.read_text("d10_example_input.txt")
    assert solve_part_1(example_input) == 13140

def test_solve_part_1_actual():
    example_input = utils.read_text("d10_input.txt")
    assert solve_part_1(example_input) == 14220