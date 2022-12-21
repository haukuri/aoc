import dataclasses

import utils

example_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@dataclasses.dataclass(frozen=True, order=True)
class File:
    path: tuple
    size: int

    def is_dir(self) -> bool:
        return self.size == -1

def parse_input(input: str) -> list[File]:
    lines = input.splitlines()
    assert lines[0] == "$ cd /"
    files = set()
    root = ("",)
    path = root
    for line in lines[1:]:
        parts = line.split(" ")
        if line == "$ cd /":
            path = root
        elif line == "$ cd ..":
            path = path[:-1]
        elif line.startswith("$ cd "):
            dirname = parts[2]
            path = (*path, dirname)
        elif line == "$ ls":
            pass  # does not matter
        elif parts[0] == "dir":
            pass  # does not matter
        elif parts[0].isnumeric():
            size = int(parts[0])
            filename = parts[1]
            file_path = (*path, filename)
            files.add(File(file_path, size))
        else:
            raise ValueError(f"Unhandled input line: '{line}'")
    files = list(files)
    files.sort()
    return files

def measure_dir_sizes(files: list[File]) -> dict[tuple, int]:
    dir_size = {}
    for file in files:
        dir_path = file.path[:-1]
        while dir_path:
            size = dir_size.get(dir_path, 0)
            size += file.size
            dir_size[dir_path] = size
            dir_path = dir_path[:-1]
    return dir_size

def solve_part_1(input: str) -> int:
    files = parse_input(input)
    dir_size = measure_dir_sizes(files)
    total = 0
    for dir_path, size in dir_size.items():
        if size > 100_000:
            continue
        total += size
    return total

def test_parse_input():
    expected = [
        File(path=("", "a", "e", "i"), size=584),
        File(path=("", "a", "f"), size=29116),
        File(path=("", "a", "g"), size=2557),
        File(path=("", "a", "h.lst"), size=62596),
        File(path=("", "b.txt",), size=14848514),
        File(path=("", "c.dat",), size=8504156),
        File(path=("", "d", "d.ext"), size=5626152),
        File(path=("", "d", "d.log"), size=8033020),
        File(path=("", "d", "j"), size=4060174),
        File(path=("", "d", "k"), size=7214296),
    ]
    actual = parse_input(example_input)

    assert actual == expected

def test_solve_part_1_example():
    expected = 95437
    actual = solve_part_1(example_input)
    assert actual == expected

def test_solve_part_1_actual():
    input = utils.read_text("d07input.txt")
    actual = solve_part_1(input)
    assert actual == 1749646
