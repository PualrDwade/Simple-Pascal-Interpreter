from visitor import Visitor
from parser import Parser
from tokenizer import Token
from tokens import PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type, ProcedureDecl
from semantic_analyzer import SemanticAnalyzer


class Interpreter(Visitor):
    '''
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree 
    '''

    def __init__(self, parser: Parser):
        self.parser = parser
        self.GLOBAL_MEMORY = {}

    def visit_binop(self, node: BinOp):
        if node.op.type is PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type is MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type is INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type is FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_num(self, node: Num):
        return node.token.value

    def visit_unaryop(self, node: UnaryOp):
        if node.op.type is PLUS:
            return +self.visit(node.factor)
        else:
            return -self.visit(node.factor)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_var(self, node: Var):
        val = self.GLOBAL_MEMORY[node.value]  # get value by variable's name
        if val is not None:
            return val
        raise NameError(repr(node.value))

    def visit_assign(self, node: Assign):
        var_name = node.left.value  # get variable's name
        self.GLOBAL_MEMORY[var_name] = self.visit(node.right)

    def visit_noop(self, node: NoOp):
        pass

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_vardecl(self, node: VarDecl):
        pass

    def visit_type(self, node: Type):
        pass

    def visit_procdecl(self, node: ProcedureDecl):
        self.visit_block(node.block)

    def interpret(self) -> int:
        ast = self.parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        # self.visit(ast)
