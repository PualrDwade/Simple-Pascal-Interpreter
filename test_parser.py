from unittest import TestCase

from astnodes import AST
from parser import Parser
from tokenizer import Tokenizer


def run_parser(code: str) -> AST:
    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    ast = parser.parse()
    return ast


class TestParser(TestCase):
    def test_parse_expr(self):
        code = """\
        program Main;
        var c : boolean;
        begin
            c := 1 > 2 and 3 + 4 * 5 < 6 = true or 4 < 6;
        end.
        """
        ast = run_parser(code)
        assert ast is not None
        print(ast)

    def test_parse_condition(self):
        code = """\
        program main;
        var a : boolean;
        begin
            a := 3;
            if a <= 2 and a + 3 <= 5 == true then
                a := 6;
            else if a + 4 <= 9 or a >= 7 then
                begin
                    a := 7;
                end
            else
                a := 8;
        end.
        """
        ast = run_parser(code)
        assert ast is not None
        print(ast)
