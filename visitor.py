from tokenizer import Token
from astnodes import *


class Visitor(object):
    '''
    Visitor is common base class to visit abstract syntax tree
    each concrete visitor should implement its visit method
    '''

    def visit(self, node: AST):
        if isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, Num):
            return self.visit_num(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unaryop(node)
        elif isinstance(node, Compound):
            return self.visit_compound(node)
        elif isinstance(node, Var):
            return self.visit_var(node)
        elif isinstance(node, Assign):
            return self.visit_assign(node)
        elif isinstance(node, NoOp):
            return self.visit_noop(node)
        elif isinstance(node, Program):
            return self.visit_program(node)
        elif isinstance(node, Block):
            return self.visit_block(node)
        elif isinstance(node, VarDecl):
            return self.visit_vardecl(node)
        elif isinstance(node, Type):
            return self.visit_type(node)
        else:
            raise Exception("Invalid AST node")

    def visit_binop(self, node: BinOp):
        pass

    def visit_num(self, node: Num):
        pass

    def visit_unaryop(self, node: UnaryOp):
        pass

    def visit_compound(self, node: Compound):
        pass

    def visit_var(self, node: Var):
        pass

    def visit_assign(self, node: Assign):
        pass

    def visit_noop(self, node: NoOp):
        pass

    def visit_program(self, node: Program):
        pass

    def visit_block(self, node: Block):
        pass

    def visit_vardecl(self, node: VarDecl):
        pass

    def visit_type(self, node: Type):
        pass
