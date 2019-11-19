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

    def test_parse_condition(self):
        code = """\
        program main;
        var a : boolean;
        begin
            a := 3;
            if a <= 2 and a + 3 <= 5 = true then
                a := 6
            else if a + 4 <= 9 or a >= 7 then
                begin
                    a := 7;
                end
            else if a <> 9 then
                a := 9
            else
                a := 8;
        end.
        """
        ast = run_parser(code)
        assert ast is not None

    def test_parse_procdecl(self):
        code = """\
        program main;
        var 
            a:boolean;
        procedure add(a:integer;b:integer);
        begin
        end;
        
        procedure set;
        begin
        end;
        
        begin
        end.
        """
        ast = run_parser(code)
        assert ast is not None

    def test_parse_funcdecl(self):
        code = """\
        program main;
        
        function add(a:integer;b:integer):boolean;
        begin
        end;
        
        function delete(item:real):integer;
        begin
        end;
        
        begin {program}
        end. {program}
        """
        ast = run_parser(code)
        assert ast is not None

    def test_parse_funccall(self):
        code = """\
        program main;
        var a: integer;
        function add(a:integer;b:integer):integer;
        begin
        end;
        
        begin {program}
            a := add(2+3,add(1,5));
        end. {program}
        """
        ast = run_parser(code)
        assert ast is not None

    def test_parse_while_loop(self):
        code = """\
        program main;
        var a,b:integer;
        begin
            a := 0;
            while a < 10 do
            begin
                a := a + 1;
            end;
            
            b := 0;
            while b <> 10 do
                b := b + 2
        end.
        """
        ast = run_parser(code)
        assert ast is not None
