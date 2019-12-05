"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone threw
it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase 
    or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

Your puzzle input is 123257-647015.
"""
import math

import pytest

def digits(number):
    scale = math.floor(math.log10(number))
    remainder = number
    for power in range(scale, -1, -1):
        decimal = 10**power
        component = remainder // decimal
        yield component
        remainder = remainder % decimal

def has_twin_digits(number):
    last_digit = 0
    for digit in digits(number):
        if digit == last_digit:
            return True
        last_digit = digit
    return False

def has_increasing_digits(number):
    last_digit = 0
    for digit in digits(number):
        if digit < last_digit:
            return False
        last_digit = digit
    return True

@pytest.mark.parametrize(
    'number, expected',
    [(123257, (1,2,3,2,5,7)), (647016, (6,4,7,0,1,6))]
)
def test_digits(number, expected):
    actual = tuple(digits(number))
    assert actual == expected

@pytest.mark.parametrize(
    'number, expected',
    [(12345, False), (11234, True), (12335, True)]
)
def test_has_twin_digits(number, expected):
    assert has_twin_digits(number) == expected

@pytest.mark.parametrize(
    'number, expected',
    [(123257, False), (647016, False), (111111, True), (123456, True)]
)
def test_has_increasing_digits(number, expected):
    assert has_increasing_digits(number) == expected

def main():
    count = 0
    for candidate in range(123257, 647016):

        if has_increasing_digits(candidate) and has_twin_digits(candidate):
            count += 1
    print('Number of candidates:', count) # 2220

if __name__ == "__main__":
    main()


