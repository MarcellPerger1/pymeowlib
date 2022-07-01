from abc import ABC, abstractmethod
import re
import operator as op


ARGSPEC_RE = re.compile(r'(?:%%)*%(\w)')
TYPE_DEFAULTS = {
    'n': 0,
    's': "",
    'b': True,
}


# base classes

class ScratchBlock(ABC):
    data: list  # abstract inst

class BlockContainer(ScratchBlock, ABC):
    @abstractmethod
    def add(self, *blocks):
        pass


class Named:
    name: str
    def __init__(self, name=None):
        # guarantee that set on instance
        self.name = name or self.name  
        if self.name is not None:
            raise ValueError("name must not be None")


class Block(Named, ScratchBlock): # impl ScratchBlock
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.data = [self.name, self.args]

class CBlock(Block, ABC):
    @abstractmethod
    def add(self, *blocks):
        pass

class ConditionalCBlock(CBlock):
    def __init__(self, cond, blocks):
        super()._init__(cond, blocks)

    def add(self, *blocks):
        self.data[2].extend(blocks)

# concrete classes
pass
class ForeverBlock(CBlock):
    name = "doForever"

    def __init__(self, blocks):
        super().__init__([])
        self.add(*blocks)

        def add(self, *blocks):
            self.data[0].extend(blocks)


# new
# ==========
# old


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


class LateCBlockMixin:
    def __init__(self, cond, blocks=()):
        self.data = [self.name, cond, []]
        self.add(blocks)

    def add(self, *blocks):
        self.data[2].extend(blocks)


class AnyCBlock(NamedBlock, LateCBlockMixin):
    def __init__(self, name, cond, blocks=()):
        NamedBlock.__init__(self, name)
        LateCBlockMixin.__init__(self, cond, blocks)


class BaseCBlock(BaseNamedBlock, LateCBlockMixin):
    def __init__(self, cond, blocks=()):
        BaseNamedBlock.__init__(self)
        LateCBlockMixin.__init__(self, cond, blocks)

# class AnyCBlock(NamedBlock):
#     def __init__(self, name, cond, blocks=()):
#         super().__init__(name)
#         self.data = [self.name, cond, []]
#         self.add(blocks)

#     def add(self, *blocks):
#         self.data[2].extend(blocks)


# class BaseCBlock(AnyCBlock):
#     name: str = None
    
#     def __init__(self, cond, blocks=()):
#         if self.name is None:
#             raise AttributeError("Subclasses must provide .name, ideally on class")
#         super().__init__(self.name, cond, blocks)


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





