from interpreter import BinOp, Num, INTEGER, Token, Interpreter, UnaryOp, MINUS, MUL, PLUS


def test_binop():
    # 2 * 7 + 3
    mul_node = BinOp(left=Num(Token(INTEGER, 2)), op=Token(
        MUL, '*'), right=Num(Token(INTEGER, 7)))

    plus_node = BinOp(left=mul_node, op=Token(
        PLUS, '+'), right=Num(Token(INTEGER, 3)))

    interpreter = Interpreter(None)

    res = interpreter.visit(plus_node)

    print(res)


def test_unaryop():
    # 5 - -2
    unary_node = UnaryOp(Token(MINUS, '-'), Num(Token(INTEGER, 2)))

    minus_node = BinOp(left=Num(Token(INTEGER, 5)),
                       op=Token(MINUS, '-'), right=unary_node)

    interpreter = Interpreter(None)

    res = interpreter.visit(minus_node)

    print(res)


if __name__ == "__main__":
    test_binop()
    test_unaryop()
