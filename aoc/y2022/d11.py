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


def parse_input(input: str):
    lines = input.splitlines()
    while lines:
        line = lines.pop()
        if not line.strip():
            continue
        assert line.startswith("Monkey")
        _, monkey_id = line.split(" ")
        monkey_id = monkey_id.rstrip(":")
        monkey_id = int(monkey_id)
        line = lines.pop().strip()
        assert line.startswith("Starting items:")
        items = [int(item) for item in line.lstrip("Starting items: ").split(", ")]
        line = lines.pop().strip()
        assert line.startswith("Operation: new = ")
        operation_expression = line.lstrip("Operation: new = ")
        line = lines.pop().strip()
        assert line.startswith("Test: divisible by ")
        test_divisible_by = int(line.lstrip("Test: divisible by "))
        line = lines.pop().strip()
        assert line.startswith("If true: throw to monkey ")
        monkey_a_id = int(line.lstrip("If true: throw to monkey "))
        line = lines.pop().strip()
        assert line.startswith("If false: throw to monkey ")
        monkey_b_id = int(line.lstrip("If false: throw to monkey "))