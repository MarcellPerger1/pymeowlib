from __future__ import annotations


class Tokenizer:
    def __init__(self, src: str):
        self.src = src
        self.token = None

    def tokenize(self):
        self._tokenize()
        return self

    def _tokenize(self):
        self.i = 0
        while self.i < len(self.src):
            self.char = self.src[self.i]
            self._handle_next_char()
            self.i += 1

    def _handle_next_char(self):
        if self.char.isspace():
            pass



