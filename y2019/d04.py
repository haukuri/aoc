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

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

    112233 meets these criteria because the digits never decrease and all 
    repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger 
    group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it 
    still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

Your puzzle input is still 123257-647015.
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

def collect(sequence):
    it = iter(sequence)
    try:
        current = next(it)
        count = 1
    except StopIteration:
        return
    while True:
        try:
            next_value = next(it)
            if next_value == current:
                count += 1
            else:
                yield current, count
                current = next_value
                count = 1
        except StopIteration:
            yield current, count
            break

def has_twin_digits(number):
    return any(count >= 2 for _, count in collect(digits(number)))

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

def has_twins_that_are_not_triplets(number):
    return any(count == 2 for _, count in collect(digits(number)))

@pytest.mark.parametrize(
    'number, expected',
    [(112233, True), (123444, False), (111122, True), (122234, False)]
)
def test_has_twins_that_are_not_triplets(number, expected):
    assert has_twins_that_are_not_triplets(number) == expected

def test_collect_works_for_empty_sequences():
    input = []
    output = list(collect(input))
    assert len(output) == 0

def test_collect():
    input = [7, 8, 8, 9, 9, 9]
    expected = ((7, 1), (8, 2), (9, 3))
    actual = tuple(collect(input))
    assert actual == expected

def part1():
    count = 0
    for candidate in range(123257, 647016):
        if has_increasing_digits(candidate) and has_twin_digits(candidate):
            count += 1
    return count

def part2():
    count = 0
    for candidate in range(123257, 647016):
        if has_increasing_digits(candidate) \
            and has_twin_digits(candidate) \
            and has_twins_that_are_not_triplets(candidate):
            count += 1
    return count

def test_part1():
    assert part1() == 2220

def test_part2():
    assert part2() == 1515

def main():
    print('Number of candidates (I):', part1()) # 2220
    print('Number of candidates (II):', part2()) # 1515

if __name__ == "__main__":
    main()


