import pathlib

_parent_dir = pathlib.Path(__file__).parent


def read_text(filename: str) -> str:
    path = _parent_dir / filename
    return path.read_text()
