from ..bases import BaseCBlock, BaseCondCBlock
from ..util import ListitemProxy

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
