from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Callable, Mapping
from enum import IntEnum

import pytest

from .utils import read_csv_input

class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

class Opcode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    READ_INPUT = 3
    WRITE_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

@dataclass
class Instruction:
    opcode: Opcode
    modes: Tuple[Mode]

    @staticmethod
    def decode(instruction: int) -> 'Instruction':
        a = instruction // 10_000
        rest = instruction % 10_000
        b = rest // 1_000
        rest = rest % 1_000
        c = rest // 100
        opcode = Opcode(rest % 100)
        modes = (Mode(c), Mode(b), Mode(a))
        return Instruction(opcode=opcode, modes=modes)

class HaltExecution(Exception):
    pass

class IntComputer:
    memory: List[int]
    pc: int
    opcode: Opcode
    modes: Tuple[Mode]

    def __init__(self, debug=False):
        self.debug = bool(debug)
        self.pc = 0
        self.opcode = Opcode.HALT
        self.modes = (Mode.IMMEDIATE, Mode.IMMEDIATE, Mode.IMMEDIATE)

    def decode(self):
        instruction = self.memory[self.pc]
        c = instruction // 10_000
        rest = instruction % 10_000
        b = rest // 1_000
        rest = rest % 1_000
        a = rest // 100
        self.opcode = Opcode(rest % 100)
        self.modes = (Mode(a), Mode(b), Mode(c))
        if self.debug:
            print(self.pc, self.opcode.name, *(m.name for m in self.modes))

    def load(self, offset: int) -> int:
        address = self.pc + offset
        value = self.memory[address]
        mode = self.modes[offset-1]
        if (mode == Mode.IMMEDIATE):
            return value
        elif (mode == Mode.POSITION):
            return self.memory[value]
        else:
            raise ValueError('Invalid mode', mode)

    def store(self, offset: int, value: int) -> None:
        address = self.pc + offset
        mode = self.modes[offset-1]
        if (mode == Mode.IMMEDIATE):
            self.memory[address] = value
        elif (mode == Mode.POSITION):
            pointer = self.memory[address]
            self.memory[pointer] = value

    def load_program(self, program):
        self.memory = list(program) if program else []

    def evaluate(self, input=None) -> List[int]:
        self.pc = 0
        input = deque(input) if input else deque()
        output = []
        halt = False
        while not halt:
            self.decode()
            if self.opcode == Opcode.ADD:
                a = self.load(1)
                b = self.load(2)
                c = a + b
                self.store(3, c)
                self.pc += 4
            elif self.opcode == Opcode.MULTIPLY:
                a = self.load(1)
                b = self.load(2)
                c = a * b
                self.store(3, c)
                self.pc += 4
            elif self.opcode == Opcode.READ_INPUT:
                c = input.popleft()
                self.store(1, c)
                self.pc += 2
            elif self.opcode == Opcode.WRITE_OUTPUT:
                a = self.load(1)
                output.append(a)
                self.pc += 2
            elif self.opcode == Opcode.JUMP_IF_TRUE:
                a = self.load(1)
                if a:
                    b = self.load(2)
                    self.pc = b
                else:
                    self.pc += 3
            elif self.opcode == Opcode.JUMP_IF_FALSE:
                a = self.load(1)
                if not a:
                    b = self.load(2)
                    self.pc = b
                else:
                    self.pc += 3
            elif self.opcode == Opcode.LESS_THAN:
                a = self.load(1)
                b = self.load(2)
                c = int(a < b)
                self.store(3, c)
                self.pc += 4
            elif self.opcode == Opcode.EQUALS:
                a = self.load(1)
                b = self.load(2)
                c = int(a == b)
                self.store(3, c)
                self.pc += 4
            elif self.opcode == Opcode.HALT:
                halt = True
            else:
                raise ValueError('Unknown opcode', self.opcode)
        return output
