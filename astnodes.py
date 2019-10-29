from tokenizer import Token


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, factor: AST):
        self.token = self.op = op
        self.factor = factor


class Num(AST):
    def __init__(self, token: Token):
        self.token = token


class Compound(AST):
    def __init__(self):
        self.childrens = []  # use list to combine many compound


class Var(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value  # self.value holds the variable's name


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right


class Type(AST):
    def __init__(self, token: Token):
        self.token = token
        self.type = token.value


class VarDecl(AST):
    def __init__(self, var_node: Var, type_node: Type):
        self.var_node = var_node
        self.type_node = type_node


class Block(AST):
    def __init__(self, declarations: [VarDecl], compound_statement: Compound):
        self.declarations = declarations
        self.compound_statement = compound_statement


class Program(AST):
    def __init__(self, name, block: Block):
        self.name = name
        self.block = block


class NoOp(AST):
    pass


class ProcedureDecl(AST):
    def __init__(self, proc_name: str, block: Block):
        self.proc_name = proc_name
        self.block = block
