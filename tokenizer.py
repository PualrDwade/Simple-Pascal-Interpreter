from tokens import *


class Token(object):
    '''
    Token is base unit for gamma
    '''

    def __init__(self, type: str, value: str):
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
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
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
