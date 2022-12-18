import enum

import utils

Move = enum.Enum("Move", ["ROCK", "PAPER", "SCISSORS"])
Strategy = tuple[Move, Move]
class Outcome(enum.IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6

move_encoding = {
    "A": Move.ROCK,
    "B": Move.PAPER,
    "C": Move.SCISSORS,
    "X": Move.ROCK,
    "Y": Move.PAPER,
    "Z": Move.SCISSORS,
}

outcome_encoding = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

move_outcome = {
    (Move.ROCK, Move.ROCK): Outcome.DRAW,
    (Move.ROCK, Move.SCISSORS): Outcome.WIN,
    (Move.ROCK, Move.PAPER): Outcome.LOSS,
    (Move.PAPER, Move.PAPER): Outcome.DRAW,
    (Move.PAPER, Move.ROCK): Outcome.WIN,
    (Move.PAPER, Move.SCISSORS): Outcome.LOSS,
    (Move.SCISSORS, Move.SCISSORS): Outcome.DRAW,
    (Move.SCISSORS, Move.PAPER): Outcome.WIN,
    (Move.SCISSORS, Move.ROCK): Outcome.LOSS,
}

countermove_for_outcome = {}
for (countermove, move), outcome in move_outcome.items():
    countermove_for_outcome[(move, outcome)] = countermove

move_score = {
    Move.ROCK: 1,
    Move.PAPER: 2,
    Move.SCISSORS: 3
}

example_input = """
A Y
B X
C Z
"""

def parse_input_part_1(input: str) -> list[Strategy]:
    strategies = []
    input = input.strip()
    for line in input.splitlines():
        line = line.strip()
        parts = line.split(" ")
        a, b = parts
        move_a = move_encoding[a]
        move_b = move_encoding[b]
        strategy = (move_a, move_b)
        strategies.append(strategy)
    return strategies


def solve_part_1(input_data: str):
    strategy_guide = parse_input_part_1(input_data)
    scores = []
    for move_a, move_b in strategy_guide:
        outcome = move_outcome[(move_b, move_a)]
        score = int(outcome) + move_score[move_b]
        scores.append(score)
    total = sum(scores)
    return total

def solve_part_2(input_data: str):
    input_data = input_data.strip()
    total_score = 0
    for line in input_data.splitlines():
        line = line.strip()
        a, b = line.split(" ")
        move = move_encoding[a]
        outcome = outcome_encoding[b]
        countermove = countermove_for_outcome[(move, outcome)]
        score = int(outcome) + move_score[countermove]
        total_score += score
    return total_score


def test_part_1_example():
    result = solve_part_1(example_input)
    assert result == 15

def test_part_1_actual():
    input = utils.read_text("d02input.txt")
    result = solve_part_1(input)
    assert result == 14375

def test_part_2_example():
    result = solve_part_2(example_input)
    assert result == 12

def test_part_2_actual():
    input = utils.read_text("d02input.txt")
    result = solve_part_2(input)
    assert result == 10274