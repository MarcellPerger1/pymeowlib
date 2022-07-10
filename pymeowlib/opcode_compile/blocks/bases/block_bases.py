from abc import ABC, abstractmethod


class ScratchBlock(ABC):
    data: list  # abstract inst

    def get_data(self):
        return [
            i.get_data() if isinstance(i, ScratchBlock) else i
            for i in self.data
        ]


class BlockContainer(ScratchBlock, ABC):
    @abstractmethod
    def add(self, *blocks):
        pass
