from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def run(code: str):
    """run code helper function"""
    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


def test_simple_proccall():
    code = """\
    program Main;

    var 
        a : integer;
        b : integer;
        c : integer;

    procedure alpha(a, b : integer);
    begin
        c := a + b;
    end;

    begin
        a := 1;
        b := 2;
        alpha(a,b);
    end.
    """
    run(code)
