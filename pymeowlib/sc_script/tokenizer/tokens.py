import string

from .const import IDENT_CHARS
from .token import register_token, TokenType


@register_token
class IntToken(TokenType):
    def do_cont(self) -> bool:
        return self.char in string.digits

    def do_start(self) -> bool:
        return self.char in string.digits


@register_token
class IdentToken(TokenType):
    def do_start(self) -> bool:
        return self.char in IDENT_CHARS

    def do_cont(self) -> bool:
        return self.char in IDENT_CHARS


@register_token
class WhitespaceToken(TokenType):
    def do_start(self) -> bool:
        return self.char.isspace()

    def do_cont(self) -> bool:
        return self.char.isspace()

    def text_repr(self) -> str:
        return repr(self.text)


@register_token
class InvalidToken(TokenType):
    invalid = True

    def do_start(self) -> bool:
        return True

    def do_cont(self) -> bool:
        return False


def init_tokens():
    """Call this function to make sure that all the token classes are loaded"""
    pass
