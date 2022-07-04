# Scratch blocks class hierarchy (in pseudo-python)

## Decent one:
### Base classes:
```python
class Named:
    name: str
    def __init__(self):
        if self.name is not None:
            raise ValueError("name must not be None")
        self.name = self.name  # set on instance

abstract class ScratchBlock:
    abstract inst data: list {getter, ?setter}

class Block(Named, impl ScratchBlock):
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.data = [self.name, *self.args]

abstract class CBlock(Block):
    abstract def add(self, *blocks):  #  + any kwargs
        pass

class ConditionalCBlock(CBlock):
    def __init__(self, cond, blocks):
        super().__init__(cond, blocks)
    
    impl def add(self, *blocks):
        self.data[2].extend(blocks)
```

### Concrete classes
```python

class ForeverBlock(CBlock):
    impl name
    def __init__(self, blocks):
        super().__init__([])
        self.add(blocks)

    impl def add(self, *blocks):
        self.data[1].extend(blocks)


class IfBlock(ConditionalCBlock):
    impl name
...

# don't inherit from ConditionalCBlock.__init__ as it doesn't support extra args
class IfElseBlock(CBlock):
    def __init__(self, cond, if_, else_):
        super().__init__(cond, [], [])

    impl def add(self, *blocks, target="if"):
        (self.data[2] if target == "if" else self.data[3]).extend(blocks)
```

### Any-ify Decorator
```python
decor def generic(target: BaseClasses, for cls):
    target ??= target.__bases__[0]
    def cls.__init__(self, name, *args):
        # override on inst first so that 
        # Named detects this (not the one on the cls)
        self.name = name  
        super().__init__(self, *args)
    
```

### Generic block classes
```python
@generic
class ...
```
