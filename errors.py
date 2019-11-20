from enum import Enum


class BreakError(Exception):
    pass


class ContinueError(Exception):
    pass


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'
    DUPLICATE_PROC_DECL = 'Duplicate procedure found'
    UNEXPECTED_PROC_ARGUMENTS_NUMBER = 'Unexpected procedure arguments number'
    MISSING_RETURN = 'Function missing return value'
    BREAK_OUTSIDE_LOOP = 'Break outside loop'
    CONTINUE_OUTSIDE_LOOP = 'Continue outside loop'


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        super().__init__(message)
        self.error_code = error_code
        self.token = token
        # add exception class name before the message
        self.message = f'{self.__class__.__name__}: {message}'


class LexerError(Error):
    pass


class SyntaxError(Error):
    pass


class SemanticError(Error):
    pass


class RuntimeError(Error):
    pass
