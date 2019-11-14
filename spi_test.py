from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def test_proccall():
    text = """\
    program Main;

    var 
    a : integer;
    b : integer;
    c : integer;

    procedure alpha(a, b : integer);
    begin
    end;

    begin
        a := 1;
        b := 2;
        alpha(a,b);
    end.
    """
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
