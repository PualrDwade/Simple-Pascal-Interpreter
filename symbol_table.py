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


class ProcedureSymbol(Symbol):
    """ProcedureSymbol is symbol of procedure declaration"""

    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )


class VarSymbol(Symbol):
    """VarSymbol has name and type"""

    def __init__(self, name: str, type):
        super().__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class ScopedSymbolTable(object):
    def __init__(self, scope_name: str, scope_level: int):
        self.__symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.__init_buildins()

    def __init_buildins(self):
        # initialize the built-in types when the symbol table instance is created.
        self.define(BuildinTypeSymbol('INTEGER'))
        self.define(BuildinTypeSymbol('REAL'))

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.__symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr = __str__

    def define(self, symbol: Symbol):
        print('Define: %s' % symbol)
        self.__symbols[symbol.name] = symbol

    def lookup(self, name) -> Symbol:
        print('Lookup: %s' % name)
        symbol = self.__symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol
