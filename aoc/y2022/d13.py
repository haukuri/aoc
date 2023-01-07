example_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def parse_input(input: str) -> list[tuple[list, list]]:
    lines = input.splitlines()
    lines.reverse()
    packet_pairs = []
    while lines:
        line_a = lines.pop()
        if line_a.strip() == "":
            continue
        line_b = lines.pop()
        packet_a = eval(line_a)
        packet_b = eval(line_b)
        pair = packet_a, packet_b
        packet_pairs.append(pair)
    return packet_pairs

def test_parse_input_example():
    pairs = parse_input(example_input)
    expected = [
        (
            [1,1,3,1,1],
            [1,1,5,1,1]
        ),
        (
            [[1],[2,3,4]],
            [[1],4]
        ),
        (
            [9],
            [[8,7,6]]
        ),
        (
            [[4,4],4,4],
            [[4,4],4,4,4]
        ),
        (
            [7,7,7,7],
            [7,7,7]
        ),
        (
            [],
            [3]
        ),
        (
            [[[]]],
            [[]]
        ),
        (
            [1,[2,[3,[4,[5,6,7]]]],8,9],
            [1,[2,[3,[4,[5,6,0]]]],8,9]
        )
    ]
    assert pairs == expected

