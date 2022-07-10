import re
from ..bases import BaseBlock

ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {
    'n': 0,
    's': "",
    'b': True,
}


class ProcDefBlock(BaseBlock):
    name = "procDef"

    def __init__(self, spec, arg_names, defaults=None, atomic=False):
        super().__init__(*init_proc_def(spec, arg_names, defaults, atomic))

    def add(self, *blocks):
        self.data.extend(blocks)
        return self


def init_proc_def(spec, arg_names, defaults=None, atomic=False):
    if defaults is None:
        defaults = [TYPE_DEFAULTS[m] for m in ARGSPEC_RE.findall(spec)]
    if len(defaults) != len(arg_names):
        import warnings
        warnings.warn(SyntaxWarning("no. defaults doesn't match no. args"))
    # this is just for the define block at the top
    return [spec, arg_names, defaults, atomic]
