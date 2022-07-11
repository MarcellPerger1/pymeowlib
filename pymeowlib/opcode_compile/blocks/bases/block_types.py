from abc import ABC, abstractmethod
from typing import overload

from .block_bases import ScratchBlock
from ..util.generic_block import generic


class Named:
    name: str

    def __init__(self, name=None):
        # guarantee that set on instance
        self.name = name or self.name
        if self.name is None:
            raise ValueError("name must not be None")


class BaseBlock(Named, ScratchBlock):  # impl ScratchBlock
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.data = [self.name, *self.args]


class BaseCBlock(BaseBlock, ABC):
    @abstractmethod
    def add(self, *blocks):
        pass


class BaseCondCBlock(BaseCBlock):
    def __init__(self, cond, blocks):
        super().__init__(cond, [])
        self.add(blocks)

    def add(self, *blocks):
        self.data[2].extend(blocks)


@overload
class Block(BaseBlock):
    def __init__(self, name: str, *args):
        self.name = name
        super().__init__(*args)


@generic
class Block(BaseBlock):
    pass


@generic
class CBlock(BaseCBlock):
    def add(self, *blocks):
        raise NotImplementedError(".add is not implemented for custom C blocks, "
                                  "consider making a subclass and implementing it there")


@generic
class CondCBlock(BaseCondCBlock):
    pass
