from abc import ABC, abstractmethod

from .block_bases import ScratchBlock
from ..util.generic_block import generic


class Named:
    name: str

    def __init__(self, name=None):
        # guarantee that set on instance
        self.name = name or self.name
        if self.name is not None:
            raise ValueError("name must not be None")


class BaseBlock(Named, ScratchBlock):  # impl ScratchBlock
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.data = [self.name, self.args]

class BaseCBlock(BaseBlock, ABC):
    @abstractmethod
    def add(self, *blocks):
        pass

class BaseCondCBlock(BaseCBlock):
    def __init__(self, cond, blocks):
        super()._init__(cond, [])
        self.add(blocks)

    def add(self, *blocks):
        self.data[2].extend(blocks)


@generic
class AnyBlock(BaseBlock):
    pass

@generic
class CBlock(BaseCBlock):
    pass

@generic
class CondCBlock(BaseCondCBlock):
    pass
