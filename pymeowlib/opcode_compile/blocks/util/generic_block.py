from ..bases import ScratchBlock


def get_base_block_class(cls):
    for b in cls.__bases__:
        if issubclass(b, ScratchBlock):
            return b


def generic(clsarg=None, target=None):
    """Sets the __init__ to a generic version with the signature 
    __init__(name, *args, **kwargs) with args and kwargs being the
    arguments of passed to the target __init__. target is the 
    'base' sprite class, the new __init__ will call the __init__
    of this class after setting the name. If not set, target is
    the first base that is a ScratchBlock"""
    def decor(cls):
        assert issubclass(cls, target) and cls is not target

        def init(self, name, *args, **kwargs):
            self.name = name
            # noinspection PyArgumentList
            target.__init__(self, *args, **kwargs)
        init.__name__ = "__init__"
        init.__qualname__ = cls.__qualname__ + "." + init.__name__
        cls.__init__ = init
        return cls
    if clsarg is not None:
        if target is None:
            target = get_base_block_class(clsarg)
        return decor(clsarg)
    if target is not None:
        return decor
    return generic
