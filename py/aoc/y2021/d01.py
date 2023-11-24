from pathlib import Path

def skip(n, iterable):
    it = iter(iterable)
    try:
        for _ in range(n):
            next(it)
        while True:
            yield next(it)
    except StopIteration:
        pass

def count_increases(measurements: list[int]) -> int:
    pairs = zip(skip(1, measurements), measurements)
    increases = sum(
        1 for current, last in pairs
        if current > last
    )
    return increases

def count_sliding_window_increases(values):
    triplets = zip(values, skip(1, values), skip(2, values))
    window_sums = [sum(triplet) for triplet in triplets]
    increases = count_increases(window_sums)
    return increases

def read_input(filename: str):
    file_path = Path(__file__).parent / filename
    lines = [
        line.strip() 
        for line in file_path.read_text().splitlines()
    ]
    numbers = [int(line) for line in lines if line]
    return numbers


def test_part_1_example_1():
    measurements = read_input('d01_example.txt')
    assert count_increases(measurements) == 7

def test_part_1_solution():
    measurements = read_input('d01_input.txt')
    assert count_increases(measurements) == 1298

def test_part_2_example_1():
    measurements = read_input('d01_example.txt')
    assert count_sliding_window_increases(measurements) == 5

def test_part_1_solution():
    measurements = read_input('d01_input.txt')
    assert count_sliding_window_increases(measurements) == 1248