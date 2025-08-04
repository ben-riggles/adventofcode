from __future__ import annotations
import aoc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Generator


class InvalidComboOperandException(Exception):
    pass

@dataclass
class Instruction(ABC):
    opcode: ClassVar[int] = None
    operand: int

    def execute(self, comp: Computer) -> int|None:
        return self._execute(comp)

    @abstractmethod
    def _execute(self, comp: Computer) -> int|None:
        pass

    @staticmethod
    def create(opcode: int, operand: int) -> Instruction:
        inst = [x for x in Instruction.__subclasses__() if x.opcode == opcode][0]
        return inst(operand)
    
class Adv(Instruction):
    opcode: int = 0

    def _execute(self, comp):
        comp.a = comp.a // (2 ** comp.evaluate_combo(self.operand))

class Bxl(Instruction):
    opcode: int = 1

    def _execute(self, comp):
        comp.b = comp.b ^ self.operand

class Bst(Instruction):
    opcode: int = 2

    def _execute(self, comp):
        comp.b = comp.evaluate_combo(self.operand) % 8

class Jnz(Instruction):
    opcode: int = 3

    def _execute(self, comp):
        if comp.a == 0:
            return
        comp.instruction_pointer = self.operand

class Bxc(Instruction):
    opcode: int = 4

    def _execute(self, comp):
        comp.b = comp.b ^ comp.c

class Out(Instruction):
    opcode: int = 5

    def _execute(self, comp):
        return comp.evaluate_combo(self.operand) % 8

class Bdv(Instruction):
    opcode: int = 6

    def _execute(self, comp):
        comp.b = comp.a // (2 ** comp.evaluate_combo(self.operand))

class Cdv(Instruction):
    opcode: int = 7

    def _execute(self, comp):
        comp.c = comp.a // (2 ** comp.evaluate_combo(self.operand))
    

@dataclass
class Computer:
    a: int = 0
    b: int = 0
    c: int = 0
    instruction_pointer: int = field(init=False, default=0)

    def reset(self, register_a: int = 0):
        self.instruction_pointer = 0
        self.a, self.b, self.c = register_a, 0, 0

    def evaluate_combo(self, operand: int) -> int:
        match operand:
            case 0|1|2|3: return operand
            case 4: return self.a
            case 5: return self.b
            case 6: return self.c
            case _: raise InvalidComboOperandException(f'Invalid combo operand value: {operand}')

    def execute(self, program: list[int]) -> Generator[int]:
        while True:
            try:
                opcode, operand = program[self.instruction_pointer:self.instruction_pointer+2]
            except ValueError:
                return
            
            save = self.instruction_pointer
            inst = Instruction.create(opcode, operand)
            retval = inst.execute(self)
            if retval is not None:
                yield retval

            if self.instruction_pointer == save:
                self.instruction_pointer += 2

    @staticmethod
    def from_string(register_data: str) -> Computer:
        lines = register_data.splitlines()
        a = int(lines[0].split(':')[1])
        b = int(lines[1].split(':')[1])
        c = int(lines[2].split(':')[1])
        return Computer(a=a, b=b, c=c)
    

def find_register_value(computer: Computer, program: list[int]) -> int:
    rev = program[::-1]

    def _find(target: list[int], val: int = 0) -> Generator[int]:
        for guess in range(0, 8):
            computer.reset(val + guess)
            output = list(computer.execute(program))
            new_val = val + guess

            if output == program:
                yield new_val
            elif output[0] == target[0]:
                yield from _find(target[1:], new_val << 3)

    return next(_find(rev))


@aoc.register(__file__)
def answers():
    registers, program = aoc.read_chunks()
    program = list(map(int, program.split(':')[1].split(',')))

    computer = Computer.from_string(registers)
    output = list(computer.execute(program))
    yield ','.join(map(str, (x for x in output)))
    yield find_register_value(computer, program)

if __name__ == '__main__':
    aoc.run()
