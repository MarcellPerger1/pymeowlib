from __future__ import annotations

from typing import Iterable

from .state import State
from .token import Token, TOKEN_TYPES, TokenType
from .tokens import WhitespaceToken
from .post_processors import POST_PROCESSORS


class Tokenizer:
    def __init__(self, text: str):
        self.text: str = text

        self.index = 0
        self.char = ''

        self.token: Token | None = None
        self.state = State.NONE

        self.tokens: 'list[Token]' = []

    def tokenize(self):
        self._tokenize()
        return self

    @property
    def next_index(self):
        return self.index + 1

    @next_index.setter
    def next_index(self, value):
        self.index = value - 1

    def _tokenize(self):
        while self.index < len(self.text):
            self.char = self.text[self.index]
            self.next_char()
            self.index += 1
        if self.token is not None:
            self.end_token()
        self.call_post_processors()

    def call_post_processors(self):
        for p in POST_PROCESSORS:
            self.tokens = p(self).process(self.tokens)

    def next_char(self):
        if self.token is None:
            return self.new_token()
        if not self.cont_token():
            return self.new_token()

    def new_token(self):
        self.token = Token(self)
        self.token.set_type(self.new_token_type())

    def new_token_type(self) -> TokenType:
        for t in TOKEN_TYPES:
            tok = t(self, self.token)
            if tok.start():
                tok.accept()
                return tok
        raise SyntaxError("Unknown character")

    def _cont_token(self):
        return self.token.type.cont()

    def cont_token(self):
        cont = self._cont_token()
        if cont:
            self.token.accept()
        else:
            self.end_token()
        return cont

    def end_token(self):
        tokens = self.token.type.end()
        if tokens:
            self.tokens.extend(tokens)
        else:
            self.tokens.append(self.token)
        self.token: Token | None = None


def print_token_stream(tks: Iterable[Token], print_ws=False, widths=(15, None)):
    for _tok in tks:
        if not print_ws and isinstance(_tok.type, WhitespaceToken):
            continue
        tp_repr = _tok.type.type_repr(True).rjust(widths[0])
        text_repr = _tok.type.text_repr()
        if widths[1] is not None:
            text_repr = text_repr.rjust(widths[1])
        print(tp_repr, ' | ', text_repr)
