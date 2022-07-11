from .opcode_util import OPS, for_op
from ..blocks import Block


@for_op(OPS.NOP)
def nop(_arg=None):
    return []


@for_op(OPS.POP_TOP)
def pop_top(_arg=None):
    return [Block("deleteLine:ofList:", "1", "__STACK__")]

@for_op(OPS.ROT_TWO)
def rot_two(_arg=None):
    return ...
