from interpreter import BinOp, Num, UnaryOp
from interpreter import INTEGER_CONST, MINUS, MUL, PLUS
from interpreter import Token
from interpreter import Tokenizer
from interpreter import Parser
from interpreter import Interpreter


def test_binop():
    # 2 * 7 + 3
    mul_node = BinOp(left=Num(Token(INTEGER_CONST, 2)), op=Token(
        MUL, '*'), right=Num(Token(INTEGER_CONST, 7)))

    plus_node = BinOp(left=mul_node, op=Token(
        PLUS, '+'), right=Num(Token(INTEGER_CONST, 3)))

    interpreter = Interpreter(None)

    res = interpreter.visit(plus_node)

    assert res is 17


def test_unaryop():
    # 5 - -2
    unary_node = UnaryOp(Token(MINUS, '-'), Num(Token(INTEGER_CONST, 2)))

    minus_node = BinOp(left=Num(Token(INTEGER_CONST, 5)),
                       op=Token(MINUS, '-'), right=unary_node)

    interpreter = Interpreter(None)

    res = interpreter.visit(minus_node)

    assert res is 7


def test_newparser():
    text = """\
    PROGRAM Part10AST;
    VAR
        a, b : INTEGER;
        y    : REAL;

    BEGIN
        a := 2;
        b := 10 * a + 10 * a // 4;
        y := 20 / 7 + 3.14;
    END.
    """
    t = Tokenizer(text)
    p = Parser(t)
    res = p.parse()
    assert res is not None
