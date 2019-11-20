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

    def test_funccall(self):
        code = """\
        program main;
        
        var result:integer;
        
        function sum(a,b:integer):integer;
        begin
            sum := a + b;
        end;
        
        begin
            result := sum(2,5); 
        end.
        """
        run_code(code)

    def test_recursion(self):
        code = """\
        program main;
        
        var result:integer;
        
        function fibonacci(n:integer):integer;
        begin
            if n = 0 or n = 1 then fibonacci := n
            else fibonacci := fibonacci(n-1) + fibonacci(n-2)
        end; 
        
        begin
            result := fibonacci(10);
        end.
        """
        run_code(code)

    def test_while_loop(self):
        code = """\
        program main;
        var a:integer;
        begin
            a := 0;
            while a <> 10 do
            begin
                a := a + 1;
                if a = 8 then break;
            end;
        end.
        """
        run_code(code)
