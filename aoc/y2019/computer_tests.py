from .computer import IntComputer

import pytest

@pytest.mark.parametrize(
    'instruction, opcode, modes',
    [
        (1101, Opcode.ADD, (Mode.IMMEDIATE, Mode.IMMEDIATE, Mode.POSITION))
    ]
)
def test_intcomputer_decode(instruction, opcode, modes):
    instance = IntComputer(program=[instruction, 1, 1, 0])
    instance.decode()
    assert instance.opcode == opcode
    assert instance.modes == modes