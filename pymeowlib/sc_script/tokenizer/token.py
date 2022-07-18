from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from inspect import isclass
from typing import Type, Optional

from .base_classes import UsesTokenizer
from .str_util import to_snake_case, remove_suffix
from .tokenizer import Tokenizer


class TokenType(UsesTokenizer, ABC):
    def __init__(self, tokenizer: Tokenizer, token: Token):
        super().__init__(tokenizer)
        self.token = token

    def __repr__(self):
        return f'<{type(self).__qualname__}>'

    # region props
    @property
    def text(self):
        return self.token.text

    # endregion

    def accept(self):
        self.token.accept()

    def set_type(self, c: TokenType | Type[TokenType]):
        if isclass(c):
            self.token.set_class(c)
        else:
            self.token.set_type(c)

    def make_token(self, text: str = None, t=None):
        tok = Token(self.tokenizer, text if text is not None else self.text)
        tok.set_type(t if t is not None else self)
        return tok

    # region start
    @abstractmethod
    def do_start(self) -> bool:
        return False

    def start(self):
        return self.do_start()

    # endregion

    # region continue
    @abstractmethod
    def do_cont(self) -> bool:
        return False

    def cont(self) -> bool:
        return self.do_cont()

    # endregion

    def end(self) -> 'Optional[list[Token]]':
        pass

    def text_repr(self) -> str:
        return self.text

    @classmethod
    def type_repr(cls, upper=False) -> str:
        return to_snake_case(remove_suffix(cls.__name__, 'Token'), upper)


@dataclass
class Token(UsesTokenizer):
    tokenizer: Tokenizer = field(repr=False)
    text: str = ''
    type: TokenType = None

    def set_type(self, t: TokenType | Type[TokenType]):
        if isclass(t):
            self.set_class(t)
        else:
            self.type = t

    def set_class(self, c: Type[TokenType]):
        self.set_type(c(self.tokenizer, self))

    def accept(self):
        self.text += self.char
