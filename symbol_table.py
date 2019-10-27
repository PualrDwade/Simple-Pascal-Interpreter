# symbol hold's the programe unit's meta message use for some optimizer
# such as 2 important functional usage:
# 1: To make sure that when we assign a value to a variable the types are correct (type checking)
# 2: To make sure that a variable is declared before it is used


class Symbol(object):
    """Symbol is base class for many kinds of symbols"""

    def __init__(self, name: str, type=None):
        self.name = name
        self.type = type


class BuildinTypeSymbol(Symbol):
    """BuildinTypeSymbol is buidin symbol which category is BuildinTypeSymbol"""

    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class VarSymbol(Symbol):
    """VarSymbol has name and type"""

    def __init__(self, name: str, type):
        super().__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__
