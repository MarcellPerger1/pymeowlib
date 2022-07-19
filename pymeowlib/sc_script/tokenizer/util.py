from typing import Iterable, TypeVar


T = TypeVar('T')


def some(it: Iterable[T]) -> bool:
    """Like the builtin `any` but returns False for empty iterables"""
    for v in it:
        if v:
            return True
    return False

