from parser import Parser
from tokenizer import Tokenizer


def test_parser():
    text = """\
        program Main;

        procedure Alpha(a : integer; b : integer);
        var x : integer;
        begin
        x := (a + b ) * 2;
        end;

        begin { Main }

        Alpha(3 + 5, 7);  { procedure call }

        end.  { Main }
        """
    t = Tokenizer(text)

    p = Parser(t)

    p.parse()
