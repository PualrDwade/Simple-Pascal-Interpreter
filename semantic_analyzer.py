from visitor import Visitor
from symbol_table import ScopedSymbolTable, VarSymbol
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type


class SemanticAnalyzer(Visitor):
    '''
    SemanticAnalyzer inherit from Visitor and it's work is
    build program's symbol table by given AST parsed by Parser
    '''

    def __init__(self):
        self.__scope = ScopedSymbolTable(scope_name='global', scope_level=1)

    def scope(self) -> ScopedSymbolTable:
        return self.__scope

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_binop(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_vardecl(self, node: VarDecl):
        type_name = node.type.type
        type_symbol = self.__scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var.value
        # duplicate define check
        if self.__scope.lookup(var_name) is not None:
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        var_symbol = VarSymbol(var_name, type_symbol)
        self.__scope.define(var_symbol)

    def visit_assign(self, node: Assign):
        # right-hand side
        self.visit(node.right)
        # left-hand side
        self.visit(node.left)

    def visit_var(self, node: Var):
        # judge if variable is not declared
        var_name = node.value
        var_symbol = self.__scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )
