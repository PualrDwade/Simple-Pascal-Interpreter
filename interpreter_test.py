from interpreter import BinOp, Num, UnaryOp
from interpreter import INTEGER, MINUS, MUL, PLUS
from interpreter import Token
from interpreter import Tokenizer
from interpreter import Parser
from interpreter import Interpreter


def test_binop():
    # 2 * 7 + 3
    mul_node = BinOp(left=Num(Token(INTEGER, 2)), op=Token(
        MUL, '*'), right=Num(Token(INTEGER, 7)))

    plus_node = BinOp(left=mul_node, op=Token(
        PLUS, '+'), right=Num(Token(INTEGER, 3)))

    interpreter = Interpreter(None)

    res = interpreter.visit(plus_node)

    assert res is 17


def test_unaryop():
    # 5 - -2
    unary_node = UnaryOp(Token(MINUS, '-'), Num(Token(INTEGER, 2)))

    minus_node = BinOp(left=Num(Token(INTEGER, 5)),
                       op=Token(MINUS, '-'), right=unary_node)

    interpreter = Interpreter(None)

    res = interpreter.visit(minus_node)

    assert res is 7


def test_newparser():
    # BEGIN a := 3; b := 4; c := a + b; END
    t = Tokenizer('BEGIN a := 3; BEGIN b := 4 END; c := a + b END.')
    p = Parser(t)
    res = p.parse()
    assert res is not None
