import re
import operator as op

from .block_bases import BlockContainer, ContainerProxy

ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {
    'n': 0,
    's': "",
    'b': True,
}


class ProcScript(BlockContainer):
    def __init__(self, spec, argNames, defaults=None, atomic=False):
        self.data = initProcScript(spec, argNames, defaults, atomic)

    def add(self, *blocks):
        self.data.extend(blocks)
        return self


def initProcScript(spec, argNames, defaults=None, atomic=False):
    if (defaults is None):
        defaults = [TYPE_DEFAULTS[m[1]] for m in ARGSPEC_RE.findall(spec)]
    if len(defaults) != len(argNames):
        import warnings
        warnings.warn(SyntaxWarning("no. defaults doesn't match no. args"))
    return [[spec, argNames, defaults, atomic]]  #.append extra smts


class AnyCBlock(BlockContainer):
    def __init__(self, name, cond, blocks=()):
        self.name = name
        self.data = [self.name, cond, []]
        self.add(blocks)

    def add(self, *blocks):
        self.data[2].extend(blocks)


class BaseCBlock(AnyCBlock):
    name: str = None
    
    def __init__(self, cond, blocks=()):
        if self.name is None:
            raise AttributeError("Subclasses must provide .name, ideally on class")
        super().__init__(self.name, cond, blocks)


class IfBlock(BaseCBlock):
    name = "DoIf"


class UntilBlock(BaseCBlock):
    name = "doUntil"



def _listitem_proxy(target, item):
    return ContainerProxy(lambda: target[item],
                          lambda v: op.setitem(target, item, v))


class IfElseBlock(BlockContainer):
    def __init__(self, cond):
        self.data = ["doIfElse", cond, [], []]
        self.if_ = _listitem_proxy(self.data, 2)
        self.else_ = _listitem_proxy(self.data, 3)

    def add(self, *blocks, target="if"):
        target_list = self.data[2] if target.lower() == 'if' else self.data[3]
        target_list.extend(blocks)

    def add_if(self, *blocks):
        self.add(*blocks, target='if')

    def add_else(self, *blocks):
        self.add(*blocks, target='else')





