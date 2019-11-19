# Tokens for Tokenizer analysis result
from enum import Enum


class TokenType(Enum):
    # single character tokens
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    DOT = '.'
    COLON = ':'
    COMMA = ','

    # arithmetic operators
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    INTEGER_DIV = '//'
    MOD = '%'

    # relational operators
    EQUALS = '='
    NOT_EQUALS = '<>'
    LESS = '<'
    LESS_EQUALS = '<='
    GREATER = '>'
    GREATER_EQUALS = '>='

    # block of reserved words
    PROGRAM = 'PROGRAM'  # marks the beginning of the block
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    REAL = 'REAL'
    VAR = 'VAR'
    PROCEDURE = 'PROCEDURE'
    FUNCTION = 'FUNCTION'
    WHILE = 'WHILE'
    CONTINUE = 'CONTINUE'
    BREAK = 'BREAK'
    DO = 'DO'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    BEGIN = 'BEGIN'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    END = 'END'  # marks the end of the block

    # misc
    ID = 'ID'
    INTEGER_CONST = 'INTEGER_CONST'
    REAL_CONST = 'REAL_CONST'
    ASSIGN = ':='
    EOF = 'EOF'


def build_reserved_keywords():
    """Build a dictionary of reserved keywords.

    The function relies on the fact that in the TokenType
    enumeration the beginning of the block of reserved keywords is
    marked with PROGRAM and the end of the block is marked with
    the END keyword.

    Result:
        {'PROGRAM': <TokenType.PROGRAM: 'PROGRAM'>,
         'INTEGER': <TokenType.INTEGER: 'INTEGER'>,
         'REAL': <TokenType.REAL: 'REAL'>,
         'VAR': <TokenType.VAR: 'VAR'>,
         'PROCEDURE': <TokenType.PROCEDURE: 'PROCEDURE'>,
         'BEGIN': <TokenType.BEGIN: 'BEGIN'>,
         'END': <TokenType.END: 'END'>}
    """
    # enumerations support iteration, in definition order
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.PROGRAM)
    end_index = tt_list.index(TokenType.END)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in tt_list[start_index:end_index + 1]
    }
    return reserved_keywords


RESERVED_KEYWORDS = build_reserved_keywords()
