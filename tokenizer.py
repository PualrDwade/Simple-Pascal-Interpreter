from errors import LexerError
from tokens import TokenType, RESERVED_KEYWORDS


class Token(object):
    def __init__(self, type: TokenType, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        """String representation of the class instance.

        Example:
            >>> Token(TokenType.INTEGER, 7, lineno=5, column=10)
            Token(TokenType.INTEGER, 7, position=5:10)
        """
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )

    def __repr__(self):
        return self.__str__()


class Tokenizer(object):
    """
    Tokenizer analysis given text and parse it to tokens
    it also names Lexer
    """

    def __init__(self, text: str):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        # token line number and column number
        self.lineno = 1
        self.column = 1

    def error(self):
        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
            lexeme=self.current_char,
            lineno=self.lineno,
            column=self.column,
        )
        raise LexerError(message=s)

    def skip_comment(self):
        while self.current_char is not '}':
            if self.pos == len(self.text) - 1:
                raise Exception('Unclosed comment')
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

        # Create a new token with current line and column number
        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)

        value = ''
        while self.current_char is not None and self.current_char.isalnum():
            value += self.current_char
            self.advance()

        token_type = RESERVED_KEYWORDS.get(value.upper())
        if token_type is None:
            token.type = TokenType.ID
            token.value = value
        else:
            # reserved keyword
            token.type = token_type
            token.value = value.upper()

        return token

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        if self.current_char is '\n':
            self.lineno += 1
            self.column = 0
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char is '.':
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(
                type=TokenType.REAL_CONST,
                value=float(result),
                lineno=self.lineno,
                column=self.column
            )
        else:
            return Token(
                type=TokenType.INTEGER_CONST,
                value=int(result),
                lineno=self.lineno,
                column=self.column
            )

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

            if self.current_char is '/' and self.peek() is '/':
                self.advance()
                self.advance()
                return Token(
                    type=TokenType.INTEGER_DIV,
                    value='//',
                    lineno=self.lineno,
                    column=self.column
                )

            if self.current_char.isalpha() or self.current_char is '_':
                return self.identify()

            if self.current_char is ':' and self.peek() is '=':
                self.advance()
                self.advance()
                return Token(
                    type=TokenType.ASSIGN,
                    value=':=',
                    lineno=self.lineno,
                    column=self.column
                )

            if self.current_char is '<' and self.peek() is '>':
                self.advance()
                self.advance()
                return Token(
                    type=TokenType.NOT_EQUALS,
                    value='<>',
                    lineno=self.lineno,
                    column=self.column
                )

            if self.current_char is '<' and self.peek() is '=':
                self.advance()
                self.advance()
                return Token(
                    type=TokenType.LESS_EQUALS,
                    value='<=',
                    lineno=self.lineno,
                    column=self.column
                )

            if self.current_char is '>' and self.peek() is '=':
                self.advance()
                self.advance()
                return Token(
                    type=TokenType.GREATER_EQUALS,
                    value='>=',
                    lineno=self.lineno,
                    column=self.column
                )

            # single-character token
            try:
                # get enum member by value, e.g.
                # TokenType(';') --> TokenType.SEMI
                token_type = TokenType(self.current_char)
            except ValueError:
                # no enum member with value equal to self.current_char
                self.error()
            else:
                # create a token with a single-character lexeme as its value
                token = Token(
                    type=token_type,
                    value=token_type.value,  # e.g. ';', '.', etc
                    lineno=self.lineno,
                    column=self.column,
                )
                self.advance()
                return token

        return Token(TokenType.EOF, None)
