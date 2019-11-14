from callstack import CallStack, Frame, FrameType
from semantic_analyzer import SemanticAnalyzer
from visitor import Visitor
from parser import Parser
from tokenizer import Token
from tokens import TokenType
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type, ProcedureDecl, ProcedureCall


class Interpreter(Visitor):
    '''
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree 
    '''

    def __init__(self, parser: Parser):
        self.parser = parser
        self.analyzer = SemanticAnalyzer()
        self.callstack = CallStack()

    def log(self, msg):
        print(msg)

    def visit_binop(self, node: BinOp):
        if node.op.type is TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type is TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type is TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type is TokenType.FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_num(self, node: Num):
        return node.token.value

    def visit_unaryop(self, node: UnaryOp):
        if node.op.type is TokenType.PLUS:
            return +self.visit(node.factor)
        else:
            return -self.visit(node.factor)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_var(self, node: Var):
        current_frame = self.callstack.peek()
        val = current_frame[node.value]  # get value by variable's name
        return val

    def visit_assign(self, node: Assign):
        var_name = node.left.value  # get variable's name
        current_frame = self.callstack.peek()
        current_frame[var_name] = self.visit(node.right)

    def visit_noop(self, node: NoOp):
        pass

    def visit_program(self, node: Program):
        program_name = node.name

        self.log(f'ENTER: PROGRAM {program_name}')

        frame = Frame(name=program_name,
                      type=FrameType.PROGRAM,
                      nesting_level=1)

        self.callstack.push(frame)

        self.log(str(self.callstack))

        self.visit(node.block)

        self.log(f'LEAVE: PROGRAM {program_name}')

        self.log(str(self.callstack))

        self.callstack.pop()

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_vardecl(self, node: VarDecl):
        pass

    def visit_type(self, node: Type):
        pass

    def visit_procdecl(self, node: ProcedureDecl):
        # self.visit_block(node.block)
        pass

    def visit_proccall(self, node: ProcedureCall):
        proc_name = node.proc_name
        self.log(f'call procedure: {proc_name}')
        # todo call proccall

    def interpret(self) -> int:
        ast = self.parser.parse()
        self.analyzer.visit(ast)
        self.visit(ast)
