import sys

# Tokens for Tokenizer analysis result
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_DIV = 'INTEGER_DIV'     # //
FLOAT_DIV = 'FLOAT_DIV'         # /
LPAREN = 'LPAREN'       # (
RPAREN = 'RPAREN'       # )
EOF = 'EOF'
DOT = 'DOT'             # .
ID = 'ID'
ASSIGN = 'ASSIGN'       # :=
SEMI = 'SEMI'           # ;
COLON = 'COLON'         # :
COMMA = 'COMMA'         # ,


class Token(object):
    '''
    Token is base unit for gamma
    '''

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


# reserved keywords
RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}


class Tokenizer(object):
    '''
    Tokenizer analysis given text and parse it to tokens
    it also names Lexer
    '''

    def __init__(self, text: str):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def skip_comment(self):
        while self.current_char is not '}':
            self.advance()
        self.advance()

    def peek(self) -> str:
        """peek return the next character but don't change the pos."""
        peek_pos = self.pos + 1
        if peek_pos is len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def identify(self) -> Token:
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char is '_'):
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        self.current_char.isspace()
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char is '.':
            # combine float value
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(REAL_CONST, float(result))
        else:
            return Token(INTEGER_CONST, int(result))

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char is '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char is '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char is '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char is '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char is '/' and self.peek() is not '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char is '/' and self.peek() is '/':
                self.advance()
                self.advance()
                return Token(INTEGER_DIV, '//')

            if self.current_char is '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char is ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char.isalpha() or self.current_char is '_':
                return self.identify()

            if self.current_char is ':' and self.peek() is not '=':
                self.advance()
                return Token(COLON, ':')

            if self.current_char is ':' and self.peek() is '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char is ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char is ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char is '.':
                self.advance()
                return Token(DOT, '.')

            self.error()

        return Token(EOF, None)


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, factor: AST):
        self.token = self.op = op
        self.factor = factor


class Num(AST):
    def __init__(self, token: Token):
        self.token = token


class Compound(AST):
    def __init__(self):
        self.childrens = []  # use list to combine many compound


class Var(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value  # self.value holds the variable's name


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right


class NoOp(AST):
    pass


class Parser(object):
    '''
    Parser parse given tokens to AST

    gramma is here:

    program : compound_statement DOT

    compound_statement : BEGIN statement_list END

    statement_list : statement
                   | statement SEMI statement_list

    statement : compound_statement
              | assignment_statement
              | empty

    assignment_statement : variable ASSIGN expr

    empty :

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV) factor)*

    factor : PLUS factor
           | MINUS factor
           | INTEGER
           | LPAREN expr RPAREN
           | variable

    variable: ID
    '''

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type: str):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def program(self) -> AST:
        """program : compound_statement DOT"""
        node = self.compound_statements()
        self.eat(DOT)
        return node

    def compound_statements(self) -> AST:
        """compound_statement: BEGIN statement_list END"""
        self.eat('BEGIN')
        nodes = self.statement_list()
        self.eat('END')
        root = Compound()
        for node in nodes:
            root.childrens.append(node)
        return root

    def statement_list(self) -> list:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        if self.current_token.type is not SEMI:
            return results
        self.eat(SEMI)
        results.extend(self.statement_list())
        return results

    def statement(self) -> AST:
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type is 'BEGIN':
            node = self.compound_statements()
        elif self.current_token.type is ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self) -> AST:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left=left, op=op, right=right)

    def variable(self) -> AST:
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self) -> AST:
        """An empty production"""
        return NoOp()

    def factor(self) -> AST:
        """
        factor: PLUS  factor
              | MINUS factor
              | INTEGER
              | LPAREN expr RPAREN
              | variable
        """
        token = self.current_token
        if token.type is PLUS:
            self.eat(PLUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is MINUS:
            self.eat(MINUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token=token)
        elif token.type is LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type is ID:
            return self.variable()
        else:
            self.error()

    def term(self) -> AST:
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            else:
                self.eat(FLOAT_DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> AST:
        """expr: term((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node


class Visitor(object):
    '''
    Visitor is common base class to visit abstract syntax tree
    each concrete visitor should implement its visit method
    '''

    def visit(self, node: AST):
        if isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, Num):
            return self.visit_num(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unaryop(node)
        elif isinstance(node, Compound):
            return self.visit_compound(node)
        elif isinstance(node, Var):
            return self.visit_var(node)
        elif isinstance(node, Assign):
            return self.visit_assign(node)
        elif isinstance(node, NoOp):
            return self.visit_noop(node)
        else:
            raise Exception("Invalid AST node")

    def visit_binop(self, node: BinOp):
        pass

    def visit_num(self, node: Num):
        pass

    def visit_unaryop(self, node: UnaryOp):
        pass

    def visit_compound(self, node: Compound):
        pass

    def visit_var(self, node: Var):
        pass

    def visit_assign(self, node: Assign):
        pass

    def visit_noop(self, node: NoOp):
        pass


class Interpreter(Visitor):
    '''
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree 
    '''

    def __init__(self, parser: Parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}  # symbol table

    def visit_binop(self, node: BinOp):
        if node.op.type is PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type is MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type is INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type is FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_num(self, node: Num):
        return node.token.value

    def visit_unaryop(self, node: UnaryOp):
        if node.op.type is PLUS:
            return +self.visit(node.factor)
        else:
            return -self.visit(node.factor)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_var(self, node: Var):
        val = self.GLOBAL_SCOPE[node.value]  # get value by variable's name
        if val is not None:
            return val
        raise NameError(repr(node.value))

    def visit_assign(self, node: Assign):
        var_name = node.left.value  # get variable's name
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_noop(self, node: NoOp):
        pass

    def interpret(self) -> int:
        ast = self.parser.parse()
        return self.visit(ast)


def show_help():
    print('simple pascal interpret for version 1.0')


def main():
    if len(sys.argv) is 1:
        show_help()
        return
    text = open(sys.argv[1], 'r').read()
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == "__main__":
    main()
