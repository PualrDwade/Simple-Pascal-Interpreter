from visitor import Visitor
from symbol_table import SymbolTable, VarSymbol
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type


class SymbolTableBuilder(Visitor):
    '''
    SymbolTableBuilder inherit from Visitor and it's work is
    build program's symbol table by given AST parsed by Parser
    '''

    def __init__(self):
        self.__symbol_table = SymbolTable()

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_binop(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)

    def visit_unaryop(self, node: UnaryOp):
        self.visit(node.factor)

    def visit_vardecl(self, node: VarDecl):
        type_name = node.type_node.type
        type_symbol = self.__symbol_table.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        # define variable's symbol
        self.__symbol_table.define(var_symbol)

    def visit_assign(self, node: Assign):
        # judge if variable is not declared
        var_name = node.left.value
        var_symbol = self.__symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        self.visit(node.right)

    def visit_var(self, node: Var):
        # judge if variable is not declared
        var_name = node.value
        var_symbol = self.__symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
