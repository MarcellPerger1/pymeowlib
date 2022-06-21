import dis
import re
from abc import ABC, abstractmethod
from .opcode_util import OPS




class PyWriter:
    pass


class OpcodeWriter(ABC):
    def __init__(self, writer):
        self.writer = writer
    
    @abstractmethod
    def write(self):
        pass


OP_TO_FUNC = {}

def for_op(o):
    name = o
    def set_as_op(f):
        OP_TO_FUNC[_to_opcode(name)] = f
        return f
    if callable(o):
        name = o.__name__
        return set_as_op(o)
    return set_as_op

def _to_opcode(o):
    if isinstance(o, int):
        return o
    else:
        return to_snake_case(o, True)

# upper: bool or None(=preserve) 
def to_snake_case(name: str, upper=False):
    res = ''
    i = 0
    while i < len(name):
        if i == 0:
            res += name[i]
            i += 1
            continue
        if name[i] in ' -_':
            res += '_'
        if name[i-1].islower() and name[i].isupper():
            res += '_' + name[i]
        else:
            res += name[i]
        i += 1
    if upper is None:
        return res
    return res.upper() if upper else res.lower()



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

