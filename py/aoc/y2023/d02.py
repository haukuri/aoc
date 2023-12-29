from dataclasses import dataclass

import utils

example_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


@dataclass
class Game:
    id: int
    turns: list[dict[str, int]]


def parse_game_line(line: str) -> Game:
    if not line.startswith("Game "):
        raise ValueError(f"Invalid game line: {str}")
    line = line.removeprefix("Game ")
    game_id_str, turns_str = line.split(": ")
    game_id = int(game_id_str)
    turns = []
    for turn_str in turns_str.split("; "):
        turn = {}
        turns.append(turn)
        colors = turn_str.split(", ")
        for color in colors:
            color = color.strip()
            count, color = color.split(" ")
            count = int(count)
            turn[color] = count
    return Game(id=game_id, turns=turns)


def parse_input(input_data: str) -> list[Game]:
    return [parse_game_line(line) for line in input_data.splitlines()]


def solve_part_1(input_data: str) -> int:
    "12 red cubes, 13 green cubes, and 14 blue cubes"
    target_max_colors = {"red": 12, "green": 13, "blue": 14}
    games = parse_input(input_data)
    possible_game_ids = []
    for game in games:
        max_color_counts = {}
        for turn in game.turns:
            for color, count in turn.items():
                max_color_counts[color] = max(max_color_counts.get(color, 0), count)
        possible = True
        for color, count in max_color_counts.items():
            if count > target_max_colors[color]:
                possible = False
        if possible:
            possible_game_ids.append(game.id)
    return sum(possible_game_ids)


def game_power_set(game: Game) -> int:
    min_color_counts = {}
    for turn in game.turns:
        for color, count in turn.items():
            existing_min = min_color_counts.get(color, 0)
            min_color_counts[color] = max(existing_min, count)
    power_set = 1
    for count in min_color_counts.values():
        power_set *= count
    return power_set


def solve_part_2(input_data: str) -> int:
    games = parse_input(input_data)
    game_power_sets = [game_power_set(game) for game in games]
    return sum(game_power_sets)


def test_solve_part_2_example():
    actual = solve_part_2(example_input)
    assert actual == 2286


def test_solve_part_2_actual():
    actual_input = utils.read_text("d02_input.txt")
    actual = solve_part_2(actual_input)
    assert actual == 56322


def test_game_power_set():
    game_line = (
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    )
    game = parse_game_line(game_line)
    assert game_power_set(game) == 20 * 13 * 6


def test_parse_game_line():
    line = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    game = parse_game_line(line)
    assert game.id == 2
    assert game.turns == [
        {"blue": 1, "green": 2},
        {"green": 3, "blue": 4, "red": 1},
        {"green": 1, "blue": 1},
    ]


def test_solve_part_1_example():
    actual = solve_part_1(example_input)
    assert actual == 8


def test_solve_part_1_actual():
    actual_input = utils.read_text("d02_input.txt")
    actual = solve_part_1(actual_input)
    assert actual == 2447
