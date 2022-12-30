from dataclasses import dataclass

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


def parse_input(input: str):
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