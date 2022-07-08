import re
from .block_proxy import ListitemProxy
from .block_bases import BlockContainer
from .block_types import BaseCBlock, BaseCondCBlock, BaseBlock


ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {
    'n': 0,
    's': "",
    'b': True,
}

# loops
class ForeverBlock(BaseCBlock):
    name = "doForever"

    def __init__(self, blocks=()):
        super().__init__([])
        self.add(*blocks)

    def add(self, *blocks):
        self.data[1].extend(blocks)


class UntilBlock(BaseCondCBlock):
    name = "doUntil"


class RepeatBlock(BaseCondCBlock):
    name = "doRepeat"


# conditions
class IfBlock(BaseCondCBlock):
    name = "doIf"


class IfElseBlock(IfBlock):
    name = "doIfElse"

    def __init__(self, cond, if_=(), else_=()):
        super(BaseCondCBlock, self).__init__(cond, [], [])
        self.if_ = ListitemProxy(self.data, 2)
        self.else_ = ListitemProxy(self.data, 3)
        self.add_if(if_)
        self.add_else(else_)

    def add(self, *blocks, target="if"):
        if target == "if":
            self.add_if(*blocks)
        else:
            self.add_else(*blocks)

    def add_if(self, *blocks):
        self.data[2].extend(*blocks)

    def add_else(self, *blocks):
        self.data[3].extend(blocks)


# other (TODO)
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


class ScriptBody(BlockContainer):
    def __init__(self, top, *blocks):
        self.top = top
        self.data = [self.top]
        self.add(*blocks)

    def add(self, *blocks):
        self.data.extend(blocks)


class Script(BlockContainer):
    def __init__(self, body, pos=(10, 10)):
        self.pos = self.x, self.y = pos
        self.data = [self.x, self.y, body]

    def add(self, *blocks):
        self.data[2].add(*blocks)
