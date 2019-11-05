# Tokens for Tokenizer analysis result
from enum import Enum


class TokenType(Enum):
    # single-character token types
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    DOT = '.'
    COLON = ':'
    COMMA = ','
    # block of reserved words
    PROGRAM = 'PROGRAM'  # marks the beginning of the block
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    INTEGER_DIV = '//'
    VAR = 'VAR'
    PROCEDURE = 'PROCEDURE'
    BEGIN = 'BEGIN'
    END = 'END'      # marks the end of the block
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
         'DIV': <TokenType.INTEGER_DIV: 'DIV'>,
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
