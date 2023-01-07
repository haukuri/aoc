from collections import defaultdict
from dataclasses import dataclass
from typing import TypeAlias, Iterable, TypeVar

from . import utils

example_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

Coordinates: TypeAlias = tuple[int, int]
EdgesOut: TypeAlias = dict[Coordinates, set[Coordinates]]
T = TypeVar("T")


@dataclass
class Node:
    elevation: int
    labels: set


@dataclass
class HikingGraph:
    edges_out = dict[Coordinates, set[Coordinates]]
    nodes = dict[Coordinates, Node]


NodeMap: TypeAlias = dict[Coordinates, Node]


def parse_input(input: str) -> NodeMap:
    lower_case_alphabet = "abcdefghijklmnopqrstuvwxyz"
    character_elevation = {c: e for e, c in enumerate(lower_case_alphabet)}
    character_elevation["S"] = 0
    character_elevation["E"] = character_elevation["z"]
    lines = input.splitlines()
    nodes = {}
    for r, line in enumerate(lines):
        for c, character in enumerate(line):
            elevation = character_elevation[character]
            labels = set()
            if character in ("S", "E"):
                labels.add(character)
            node = Node(elevation=elevation, labels=labels)
            nodes[(r, c)] = node
    return nodes


def test_parse_input():
    test_input = "Sbc\n" "Eed"
    expected = {
        (0, 0): Node(0, {"S"}),
        (0, 1): Node(1, set()),
        (0, 2): Node(2, set()),
        (1, 2): Node(3, set()),
        (1, 1): Node(4, set()),
        (1, 0): Node(25, {"E"}),
    }
    assert parse_input(test_input) == expected


def can_traverse(from_node: Node, to_node: Node):
    return from_node.elevation >= (to_node.elevation - 1)


def find_edges(nodes: NodeMap) -> EdgesOut:
    reachable = defaultdict(set)
    max_r = max(r for r, _ in nodes.keys())
    max_c = max(c for _, c in nodes.keys())

    def neighborhood_of(r, c):
        if r >= 1:
            yield (r - 1), c
        if r < max_r:
            yield (r + 1), c
        if c >= 1:
            yield r, (c - 1)
        if c < max_c:
            yield r, (c + 1)

    for (r, c), node in nodes.items():
        node_location = r, c
        for neighbor_location in neighborhood_of(r, c):
            neighbor = nodes[neighbor_location]
            if can_traverse(node, neighbor):
                reachable[node_location].add(neighbor_location)
    return reachable


def reverse_edges(edges: EdgesOut) -> EdgesOut:
    reachable = defaultdict(set)
    for src_node, dst_nodes in edges.items():
        for dst_node in dst_nodes:
            reachable[dst_node].add(src_node)
    return reachable


def shortest_path(
    start_loc: Coordinates, 
    end_locs: Iterable[Coordinates], 
    reachable: EdgesOut
) -> int:
    end_locs = set(end_locs)
    distance = {start_loc: 0}
    previous = {}
    frontier = {start_loc}
    while frontier:
        new_frontier = set()
        for node in frontier:
            src_dist = distance[node]
            for dst in reachable[node]:
                new_dst_dist = src_dist + 1
                old_dst_dist = distance.get(dst, None)
                if old_dst_dist is None or new_dst_dist < old_dst_dist:
                    new_frontier.add(dst)
                    distance[dst] = new_dst_dist
                    previous[dst] = node
        frontier = new_frontier
    shortest_path_length = float("inf")
    shortest_path_end = None
    for end_loc in end_locs:
        try:
            end_loc_shortest_path_length = distance[end_loc]
        except KeyError:
            # there is no path to this destination
            continue
        if end_loc_shortest_path_length < shortest_path_length:
            shortest_path_end = end_loc
            shortest_path_length = end_loc_shortest_path_length
    assert shortest_path_end is not None
    assert isinstance(shortest_path_length, int)
    return shortest_path_length


def solve_part_1(input):
    nodes = parse_input(input)
    reachable = find_edges(nodes)
    start_loc = None
    end_loc = None
    for loc, node in nodes.items():
        if "S" in node.labels:
            start_loc = loc
        if "E" in node.labels:
            end_loc = loc
    assert start_loc is not None
    assert end_loc is not None
    shortest_path_length = shortest_path(
        start_loc=start_loc, end_locs=[end_loc], reachable=reachable
    )
    return shortest_path_length


def single(iterable: Iterable[T]) -> T:
    for x in iterable:
        return x
    raise ValueError("Single is undefined for an empty iterable")


def solve_part_2(input: str) -> int:
    nodes = parse_input(input)
    start_locs = [loc for loc, node in nodes.items() if node.elevation == 0]
    end_loc = single(loc for loc, node in nodes.items() if "E" in node.labels)
    reachable = find_edges(nodes)
    reverse_reachable = reverse_edges(reachable)
    path_length = shortest_path(
        start_loc=end_loc,
        end_locs=start_locs,
        reachable=reverse_reachable,
    )
    return path_length


def test_solve_part_1_example_input():
    assert solve_part_1(example_input) == 31


def test_solve_part_1_actual_input():
    actual_input = utils.read_text("d12_input.txt")
    assert solve_part_1(actual_input) == 440


def test_solve_part_2_example_input():
    assert solve_part_2(example_input) == 29


def test_solve_part_2_actual_input():
    actual_input = utils.read_text("d12_input.txt")
    assert solve_part_2(actual_input) == 439
