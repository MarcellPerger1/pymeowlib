import operator as op

from ..bases import BlockContainer


class ContainerProxy(BlockContainer):
    def __init__(self, getter, setter=None):
        self.getter = getter
        # if the user is able to provide a setter,
        # they should as the default setter implementation
        # is not ideal (clearing, then extending) as it
        # doesn't preserve referential identity, this is undesirable
        # and has bad complexity (n is len(new), m is len(old)):
        #   it is O(n) when not considering the
        #     DECREF needed for each item of the list when clearing
        #   it is O(n+m) with the coefficient of m being **tiny**
        #     when considering this small technicality
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
            self._default_setter(value)

    def _default_setter(self, value):
        data = self.data
        data.clear()
        data.extend(value)


class ListitemProxy(ContainerProxy):
    def __init__(self, target, item):
        super().__init__(lambda: target[item],
                         lambda v: op.setitem(target, item, v))
