from unittest import TestCase
from interpreter import Interpreter
from parser import Parser
from tokenizer import Tokenizer


def run_code(code: str):
    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


class TestInterpreter(TestCase):
    def test_interpret(self):
        code = """\
        program main;
        var 
            a,b,c : integer;
            
            procedure sum(x,y:integer);
            begin
                c := x + y;
            end;
            
        begin
            a := 1;
            c := (2+3)*4;
            b := 2;
            sum(a,b);
            if c = 2 then
            begin
                c := 5;
                c := 10;
                c := 20;
            end
            else if c = 3 then
                c := 5
            else
                c := 6;
            
            c := 10
        end.
        """
        run_code(code)
