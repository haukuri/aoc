import math
import pathlib

import pytest

def digits(number):
    scale = math.floor(math.log10(number))
    remainder = number
    for power in range(scale, -1, -1):
        decimal = 10**power
        component = remainder // decimal
        yield component
        remainder = remainder % decimal

@pytest.mark.parametrize(
    'number, expected',
    [(123257, (1,2,3,2,5,7)), (647016, (6,4,7,0,1,6))]
)
def test_digits(number, expected):
    actual = tuple(digits(number))
    assert actual == expected

def read_csv_input(filename: str):
    path = pathlib.Path(__file__).parent / filename
    output = []
    for line in path.open().readlines():
        row = [int(value) for value in line.split(',')]
        output.append(row)
    return output