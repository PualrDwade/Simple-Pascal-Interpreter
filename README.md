# Math-Interpreter

## introduce

Math-Interpreter is a simple interpreter to interpret mathematical expression

## design 

this interpreter is build with python and contains 3 parts of Tokenizer, Parser, and Interpreter

**Tokenizer**
```python
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

    def integer(self) -> int:
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char is '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char is '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char is '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char is "/":
                self.advance()
                return Token(DIV, '/')

            if self.current_char is '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char is ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)
```

**Parser**
```python
class Parser(object):
    '''
    Parser parse given tokens to AST
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

    def factor(self) -> AST:
        token = self.current_token
        if token.type is INTEGER:
            self.eat(INTEGER)
            return Num(token=token)
        elif token.type is LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self) -> AST:
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)

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
        return self.expr()
```

**Interpreter**
```python
class Interpreter(Visitor):
    '''
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree 
    '''

    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_binop(self, node: BinOp) -> int:
        if node.op.type is PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type is MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type is DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_num(self, node: Num) -> int:
        return node.token.value

    def interpret(self) -> int:
        ast = self.parser.parse()
        return self.visit(ast)
```

## usage

```python
tokenizer = Tokenizer("4 * (2 - 3)")
parser = Parser(tokenizer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(result)
> -4
```