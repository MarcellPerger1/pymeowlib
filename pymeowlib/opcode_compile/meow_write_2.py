import dis
from abc import ABC, abstractmethod
from .opcode_util import OPS, for_op




class PyWriter:
    pass


class OpcodeWriter(ABC):
    def __init__(self, writer):
        self.writer = writer
    
    @abstractmethod
    def write(self):
        pass






class PyParser:
    def __init__(self, prog):
        self.prog = prog
        self.instr_list = list(dis.get_instructions(self.prog))

    def parse(self):
        for instr in self.instr_list:
            self.instr: dis.Instruction = instr
            opc = self.instr.opcode
            if opc == OPS.NOP:
                pass
            elif opc == OPS.POP_TOP:
                pass


def addBlock(target, block):
    target.append(block)


@for_op(OPS.NOP)
def nop(_arg=None):
    pass

@for_op(OPS.POP_TOP)
def pop_top(arg=None):
    ...

