from .computer import IntComputer, Opcode, Mode

import pytest

@pytest.mark.parametrize(
    'initial_state, expected_halt_state',
    [
        ([1,0,0,0,99], [2,0,0,0,99]),
        ([2,3,0,3,99], [2,3,0,6,99]),
        ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
        ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
    ])
def test_evaluate(initial_state, expected_halt_state):
    computer = IntComputer()
    computer.load_program(initial_state)
    computer.evaluate()
    halt_state = computer.memory
    assert halt_state == expected_halt_state

@pytest.mark.parametrize(
    'instruction, opcode, modes',
    [
        (1101, Opcode.ADD, (Mode.IMMEDIATE, Mode.IMMEDIATE, Mode.POSITION))
    ]
)
def test_decode(instruction, opcode, modes):
    instance = IntComputer()
    instance.load_program([instruction, 1, 1, 0])
    instance.decode()
    assert instance.opcode == opcode
    assert instance.modes == modes