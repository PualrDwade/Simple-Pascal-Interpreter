from unittest import TestCase
from parser import Parser
from tokenizer import Tokenizer


class TestParser(TestCase):
    def test_parse_expr(self):
        code = """\
        program Main;
        var c : boolean;
        begin
            c := 1 > 2 and 3 + 4 * 5 < 6 = true or 4 < 6;
        end.
        """
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        ast = parser.parse()
        print(ast)
