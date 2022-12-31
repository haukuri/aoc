from dataclasses import dataclass

from . import utils

example_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass(frozen=True)
class Monkey:
    id: int
    items: list[int]
    update_expression: str
    test_divisor: int
    test_true_monkey_id: int
    test_false_monkey_id: int


def parse_input(input: str) -> list[Monkey]:
    lines = input.splitlines()
    lines.reverse()
    monkeys = []
    while lines:
        line = lines.pop().strip()
        if not line:
            continue
        assert line.startswith("Monkey")
        _, monkey_id = line.split(" ")
        monkey_id = monkey_id.rstrip(":")
        monkey_id = int(monkey_id)
        line = lines.pop().strip()
        assert line.startswith("Starting items:")
        items = [int(item) for item in line.removeprefix("Starting items: ").split(", ")]
        line = lines.pop().strip()
        assert line.startswith("Operation: new = ")
        operation_expression = line.removeprefix("Operation: new = ")
        line = lines.pop().strip()
        assert line.startswith("Test: divisible by ")
        test_divisible_by = int(line.removeprefix("Test: divisible by "))
        line = lines.pop().strip()
        assert line.startswith("If true: throw to monkey ")
        monkey_a_id = int(line.removeprefix("If true: throw to monkey "))
        line = lines.pop().strip()
        assert line.startswith("If false: throw to monkey ")
        monkey_b_id = int(line.removeprefix("If false: throw to monkey "))
        monkey = Monkey(
            id=monkey_id,
            items=items,
            update_expression=operation_expression,
            test_divisor=test_divisible_by,
            test_true_monkey_id=monkey_a_id,
            test_false_monkey_id=monkey_b_id
        )
        monkeys.append(monkey)
    return monkeys

def test_parse_input():
    actual = parse_input(example_input)
    expected = [
        Monkey(
            id=0,
            items=[79, 98],
            update_expression="old * 19",
            test_divisor=23,
            test_true_monkey_id=2,
            test_false_monkey_id=3
        ),
        Monkey(
            id=1,
            items=[54, 65, 75, 74],
            update_expression="old + 6",
            test_divisor=19,
            test_true_monkey_id=2,
            test_false_monkey_id=0
        ),
        Monkey(
            id=2,
            items=[79, 60, 97],
            update_expression="old * old",
            test_divisor=13,
            test_true_monkey_id=1,
            test_false_monkey_id=3
        ),
        Monkey(
            id=3,
            items=[74],
            update_expression="old + 3",
            test_divisor=17,
            test_true_monkey_id=0,
            test_false_monkey_id=1
        )
    ]
    assert actual == expected

def solve_part_1(input: str) -> int:
    monkeys = parse_input(input)
    monkeys_by_id = { m.id: m for m in monkeys}
    monkey_activity = { m.id: 0 for m in monkeys }
    for _ in range(20):
        for monkey in monkeys:
            monkey.items.reverse()
            while monkey.items:
                monkey_activity[monkey.id] += 1
                worry = monkey.items.pop()
                worry = eval(
                    monkey.update_expression,
                    None,            # globals
                    { "old": worry }  # locals
                )
                worry = worry // 3
                divisible = worry % monkey.test_divisor == 0
                if divisible:
                    other_monkey_id = monkey.test_true_monkey_id
                else:
                    other_monkey_id = monkey.test_false_monkey_id
                monkeys_by_id[other_monkey_id].items.append(worry)
    activity = list(monkey_activity.values())
    activity.sort(reverse=True)
    monkey_business = activity[0] * activity[1]
    return monkey_business

def solve_part_2(input: str) -> int:
    monkeys = parse_input(input)
    monkeys_by_id = { m.id: m for m in monkeys}
    monkey_activity = { m.id: 0 for m in monkeys }
    for _ in range(500):
        for monkey in monkeys:
            monkey.items.reverse()
            while monkey.items:
                monkey_activity[monkey.id] += 1
                worry = monkey.items.pop()
                worry = eval(
                    monkey.update_expression,
                    None,            # globals
                    { "old": worry }  # locals
                )
                divisible = worry % monkey.test_divisor == 0
                if divisible:
                    other_monkey_id = monkey.test_true_monkey_id
                else:
                    other_monkey_id = monkey.test_false_monkey_id
                monkeys_by_id[other_monkey_id].items.append(worry)
    activity = list(monkey_activity.values())
    activity.sort(reverse=True)
    monkey_business = activity[0] * activity[1]
    return monkey_business


def test_solve_part_1_example():
    assert solve_part_1(example_input) == 10_605

def test_solve_part_1_actual():
    input = utils.read_text("d11_input.txt")
    assert solve_part_1(input) == 57348

def test_solve_part_2_example():
    assert solve_part_2(example_input) == 2713310158