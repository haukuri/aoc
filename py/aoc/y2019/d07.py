import asyncio
from itertools import permutations

import pytest

from .computer import IntComputer
from .utils import read_csv_input

async def calculate_amplification(phase_setting, input_signal, program):
    computer = IntComputer()
    computer.load_program(program)
    await computer.evaluate(input=[phase_setting, input_signal])
    result = await computer.output.get()
    return result

async def total_amplification(phase_setting_sequence, program):
    amplification = 0
    for phase_setting in phase_setting_sequence:
        amplification = await calculate_amplification(phase_setting, amplification, program)
    return amplification

async def feedback_amplification(phase_setting_sequence, program):
    a = IntComputer(program=program)
    b = IntComputer(program=program, input=a.output)
    c = IntComputer(program=program, input=b.output)
    d = IntComputer(program=program, input=c.output)
    e = IntComputer(program=program, input=d.output)
    a.input = e.output
    amplifiers = [a, b, c, d, e]
    for amplifier, phase_setting in zip(amplifiers, phase_setting_sequence):
        await amplifier.input.put(phase_setting)
    runs = [amplifier.evaluate() for amplifier in amplifiers]
    await a.input.put(0)
    await asyncio.gather(*runs)
    result = e.output.get_nowait()
    return result

@pytest.mark.asyncio
async def test_total_amplification():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_setting_sequence = [4,3,2,1,0]
    actual = await total_amplification(phase_setting_sequence, program)
    assert actual == 43210

async def main():
    program = read_csv_input('d07input')[0]
    maximum = 0
    for phase_setting_sequence in permutations(range(5)):
        amplification = await total_amplification(phase_setting_sequence, program)
        maximum = amplification if amplification > maximum else maximum
    print('Maximum amplification', maximum)
    feedback_maximum = 0
    for phase_setting_sequence in permutations([5, 6, 7, 8, 9]):
        amplification = await feedback_amplification(phase_setting_sequence, program)
        feedback_maximum = amplification if amplification > feedback_maximum else feedback_maximum
    print('Maximum amplification with feedback', feedback_maximum)

if __name__ == '__main__':
    asyncio.run(main())
