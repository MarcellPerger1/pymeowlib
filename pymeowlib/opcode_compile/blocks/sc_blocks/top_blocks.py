import re
from ..bases import BaseBlock


ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {
    'n': 0,
    's': "",
    'b': True,
}


class ProcDefBlock(BaseBlock):
    def __init__(self, spec, argNames, defaults=None, atomic=False):
        self.data = initProcDef(spec, argNames, defaults, atomic)

    def add(self, *blocks):
        self.data.extend(blocks)
        return self


def initProcDef(spec, argNames, defaults=None, atomic=False):
    if (defaults is None):
        defaults = [TYPE_DEFAULTS[m] for m in ARGSPEC_RE.findall(spec)]
    if len(defaults) != len(argNames):
        import warnings
        warnings.warn(SyntaxWarning("no. defaults doesn't match no. args"))
    # this is just for the define block at the top
    return [spec, argNames, defaults, atomic]

