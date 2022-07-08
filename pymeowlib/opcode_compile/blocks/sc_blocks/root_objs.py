from ..bases import BlockContainer


class ScriptBody(BlockContainer):
    def __init__(self, top, *blocks):
        self.top = top
        self.data = [self.top]
        self.add(*blocks)

    def add(self, *blocks):
        self.data.extend(blocks)


class Script(BlockContainer):
    def __init__(self, body, pos=(10, 10)):
        self.pos = self.x, self.y = pos
        self.data = [self.x, self.y, body]

    def add(self, *blocks):
        self.data[2].add(*blocks)
