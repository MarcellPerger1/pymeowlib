from tokenizer.tokenizer import Tokenizer, print_token_stream


if __name__ == '__main__':
    print_token_stream(Tokenizer("abc0d  45 i9 ~   o6").tokenize().tokens, True)
