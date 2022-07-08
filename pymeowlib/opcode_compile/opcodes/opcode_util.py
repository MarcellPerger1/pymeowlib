import opcode


class _OpsType:
    def __getattr__(self, name):
        return opcode.opmap[name]

    def __getitem__(self, item):
        return opcode.opmap[item]


OPS = _OpsType()


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
