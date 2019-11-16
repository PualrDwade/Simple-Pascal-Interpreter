# symbol hold's the programe unit's meta message use for some optimizer
# such as 2 important functional usage:
# 1: To make sure that when we assign a value to a variable the types are correct (type checking)
# 2: To make sure that a variable is declared before it is used


class Symbol(object):
    """Symbol is base class for many kinds of symbols"""

    def __init__(self, name: str, type=None):
        self.name = name
        self.type = type

    def __str__(self):
        return "<{class_name}(name = '{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )

    __repr__ = __str__


class BuildinTypeSymbol(Symbol):
    """BuildinTypeSymbol is buidin symbol which category is BuildinTypeSymbol"""

    def __init__(self, name: str):
        super().__init__(name)


class ProcedureSymbol(Symbol):
    """ProcedureSymbol is symbol of procedure declaration"""

    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else []

    def __repr__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )


class VarSymbol(Symbol):
    """VarSymbol has name and type"""

    def __init__(self, name: str, type: Symbol):
        super().__init__(name, type)

    def __str__(self):
        return "<{class_name}({name}:{type})>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type.name
        )

    __repr__ = __str__


class ScopedSymbolTable(object):
    def __init__(self, scope_name: str, scope_level: int, enclosing_scope=None):
        self.__symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Enclosing scope',
                 self.enclosing_scope.scope_name if self.enclosing_scope else None
                 )
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

    def lookup(self, name: str, current_scope_only=False) -> Symbol:
        print('Lookup: %s. (Scope name: %s)' % (name, self.scope_name))
        symbol = self.__symbols.get(name)
        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

        return None
