import re

TOKENS_RE = re.compile("""\
()""", re.VERBOSE)


class NewTokenizer:
    def __init__(self, src: str):
        self.src = src

    def tokenize(self):
        self._tokenize()
        return self

    def _tokenize(self):
        pass
