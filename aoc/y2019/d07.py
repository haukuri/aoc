from itertools import permutations

from .computer import IntComputer
from .utils import read_csv_input

def calculate_amplification(phase_setting, input_signal, program):
    computer = IntComputer()
    computer.load_program(program)
    output = computer.evaluate(input=[phase_setting, input_signal])
    return output[0]

def total_amplification(phase_setting_sequence, program):
    amplification = 0
    for phase_setting in phase_setting_sequence:
        amplification = calculate_amplification(phase_setting, amplification, program)
    return amplification

def test_total_amplification():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_setting_sequence = [4,3,2,1,0]
    actual = total_amplification(phase_setting_sequence, program)
    assert actual == 43210

def main():
    program = read_csv_input('d07input')[0]
    maximum = max(
        total_amplification(phase_setting_sequence, program) 
        for phase_setting_sequence in permutations(range(5)))
    print('Maximum amplification', maximum)

if __name__ == '__main__':
    main()
