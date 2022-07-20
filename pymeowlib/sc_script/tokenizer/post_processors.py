from abc import ABC, abstractmethod

from .base_classes import UsesTokenizer
from .tokens import InvalidToken
from .token import Token


POST_PROCESSORS: 'list[TokenPostProcessor]' = []


class TokenPostProcessor(UsesTokenizer, ABC):
    def __init__(self, tokenizer):
        super().__init__(tokenizer)

    @abstractmethod
    def process(self, tokens: 'list[Token]') -> 'list[Token]':
        pass


def register(cls):
    POST_PROCESSORS.append(cls)
    return cls


@register
class InvalidJoiner(TokenPostProcessor):
    """Joins invalid tokens into one invalid token"""

    def process(self, tokens: 'list[Token]'):
        new = []
        current_text = ''
        for tok in tokens:
            # todo strict type equality ??
            if isinstance(tok.type, InvalidToken):
                current_text += tok.text
                continue
            if current_text:
                # end of InvalidToken
                new.append(Token(self.tokenizer, current_text).set_type(InvalidToken))
                current_text = ''
            new.append(tok)
        return new
