from abc import ABC, abstractmethod


class ScriptsRoot:
    def __init__(self):
        self.scripts=[]
    
    def add(self, script):
        self.scripts.append(script)


class BlockContainer(ABC):
    data: list

    @abstractmethod
    def add(self, *blocks):
        pass

class ContainerProxy(BlockContainer):
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter
    
    def add(self, *blocks):
        self.data.extend(*blocks)

    @property
    def data(self):
        return self.getter()

    @data.setter
    def data(self, value):
        if self.setter is not None:
            self.setter(value)
        else:
            self.data.clear()
            self.data.extend(value)


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
