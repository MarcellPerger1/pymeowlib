import opcode


class _OpsType:
    def __getattr__(self, name):
        return opcode.opmap[name]

    def __getitem__(self, item):
        return opcode.opmap[item]


OPS = _OpsType()
