from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, \
    Block, VarDecl, ProcedureDecl, ProcedureCall
from callstack import CallStack, Frame, FrameType
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from tokens import TokenType
from visitor import Visitor


class Interpreter(Visitor):
    """
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree
    """

    def __init__(self, parser: Parser):
        self.parser = parser
        self.analyzer = SemanticAnalyzer()
        self.callstack = CallStack()

    @staticmethod
    def log(msg):
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
        current_frame: Frame = self.callstack.peek()
        # get value by variable's name
        val = current_frame.get_value(node.value)
        return val

    def visit_assign(self, node: Assign):
        var_name = node.left.value  # get variable's name
        var_value = self.visit(node.right)
        current_frame: Frame = self.callstack.peek()
        current_frame.set_value(var_name, var_value)

    def visit_noop(self, node: NoOp):
        pass

    def visit_program(self, node: Program):
        program_name = node.name

        self.log(f'ENTER: PROGRAM {program_name}')

        frame = Frame(name=program_name, type=FrameType.PROGRAM)

        self.callstack.push(frame)
        self.visit(node.block)

        self.log(str(self.callstack))

        self.callstack.pop()
        self.log(f'LEAVE: PROGRAM {program_name}')

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_vardecl(self, node: VarDecl):
        var_name = node.var_node.value
        current_frame: Frame = self.callstack.peek()
        current_frame.define(var_name)

    def visit_procdecl(self, node: ProcedureDecl):
        proc_name = node.proc_token.value
        current_frame: Frame = self.callstack.peek()
        current_frame.define(proc_name)
        current_frame.set_value(proc_name, node)

    def visit_proccall(self, node: ProcedureCall):
        proc_name = node.proc_name
        current_frame = self.callstack.peek()
        proc_node: ProcedureDecl = current_frame.get_value(proc_name)

        self.log(f'ENTER: PROCEDURE {proc_name}')

        # get actual params values
        actual_param_values = [self.visit(actual_param)
                               for actual_param in node.actual_params]

        proc_frame = Frame(name=proc_name, type=FrameType.PROCEDURE)

        self.callstack.push(proc_frame)
        current_frame: Frame = self.callstack.peek()

        # map actual params to formal params
        for (formal_param, actual_param_value) in zip(proc_node.params, actual_param_values):
            current_frame.define(formal_param.var.value)
            current_frame.set_value(formal_param.var.value, actual_param_value)

        self.visit(proc_node.block)
        self.log(str(self.callstack))

        self.callstack.pop()
        self.log(f'LEAVE: PROCEDURE {proc_name}')

    def interpret(self):
        ast = self.parser.parse()
        self.analyzer.visit(ast)
        self.visit(ast)
