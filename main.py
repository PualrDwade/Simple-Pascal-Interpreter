import sys
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def show_help():
    print('simple pascal interpret for version 1.0')


def main():
    if len(sys.argv) is 1:
        show_help()
        return
    text = open(sys.argv[1], 'r').read()
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == "__main__":
    main()
