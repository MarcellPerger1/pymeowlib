from ..bases import ScratchBlock


def generic(clsarg=None, target=None):
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
    if clsarg is None:
        if target is not None:
            return decor
        return generic
    if target is None:
        for b in clsarg.__bases__:
            if issubclass(b, ScratchBlock):
                target = b
                return decor(clsarg)
    return decor(clsarg)
