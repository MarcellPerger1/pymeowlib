from .opcode_util import OPS, for_op

@for_op(OPS.NOP)
def nop(_arg=None):
    pass

@for_op(OPS.POP_TOP)
def pop_top(arg=None):
    ...

