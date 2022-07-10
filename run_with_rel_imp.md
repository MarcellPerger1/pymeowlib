# How to run a file directly when it requires relative imports

Use this to be able to run a file directly that uses `from .x import y`

```python
try:
    # noinspection PyUnboundLocalVariable
    pkg = __package__
except NameError:
    pkg = None
PKG_LEVEL = 1  # how many dots to support

if not pkg:
    import sys
    from pathlib import Path

    top = Path(__file__).parents[PKG_LEVEL]
    __package__ = top.name
    # make sure package can be found by search in sys.path
    # so add parent of package root
    # so that <parent>/<name> is the package
    sys.path.append(str(top.parent))
```
