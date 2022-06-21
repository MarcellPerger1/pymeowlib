import re

from .block_bases import DataContainer


ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {'n': 0, 's': "", 'b': True, }


class ProcScript(DataContainer):
    def __init__(self, spec, argNames, defaults=None, atomic=False):
        super().__init__(initProcScript(spec, argNames, defaults, atomic))


def initProcScript(spec, argNames, defaults=None, atomic=False):
    if(defaults is None):
        defaults = [TYPE_DEFAULTS[m[1]] for m in ARGSPEC_RE.findall(spec)]
    if len(defaults) != len(argNames):
        import warnings
        warnings.warn(SyntaxWarning("no. defaults doesn't match no. args"))
    return [[spec, argNames, defaults, atomic]]  #.append extra smts
