from abc import ABC, abstractmethod


class ScriptsRoot:
    def __init__(self):
        self.scripts=[]
    
    def add(self, script):
        self.scripts.append(script)


class BlockContainer(ABC):
    @abstractmethod
    def add(self, *blocks):
        pass


class DataContainer(BlockContainer):
    """Class implmenting utils for adding to BlockContainers
    
    --- USAGE ---
    
    class ...(DataContainer):
    
        def __init__(self, ...):
    
            data = ... # [compute initial `data` value using args]
            super().__init__(data)"""
    @abstractmethod
    def __init__(self, data):
        self.data = data
    
    def add(self, *blocks):
        self.data.extend(blocks)
