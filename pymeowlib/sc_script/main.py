if __name__ == '__main__':
    from tokenizer.tokenizer import Tokenizer, print_token_stream
else:
    from .tokenizer.tokenizer import Tokenizer, print_token_stream


def main():
    print_token_stream(Tokenizer("abc0d  45 i9 ~~@!\n   o6").tokenize().tokens, True)


if __name__ == '__main__':
    main()
