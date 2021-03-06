from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, Program, \
    Block, VarDecl, ProcedureDecl, ProcedureCall, Boolean, Condition, Then, Else, FunctionDecl, FunctionCall, WhileLoop, \
    Continue, Break
from callstack import CallStack, Frame, FrameType
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from tokens import TokenType
from visitor import Visitor
from errors import RuntimeError, ErrorCode, ContinueError, BreakError


class Interpreter(Visitor):
    """
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree
    """

    def __init__(self, parser: Parser):
        self.parser = parser
        self.analyzer = SemanticAnalyzer()
        self.callstack = CallStack()

    def error(self, error_code: ErrorCode, token):
        raise RuntimeError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def log(self, msg):
        print(msg)

    def visit_binop(self, node: BinOp):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        # todo type checker
        if node.op.type is TokenType.PLUS:
            return left_val + right_val
        elif node.op.type is TokenType.MINUS:
            return left_val - right_val
        elif node.op.type is TokenType.MUL:
            return left_val * right_val
        elif node.op.type is TokenType.INTEGER_DIV:
            return left_val // right_val
        elif node.op.type is TokenType.FLOAT_DIV:
            return left_val / right_val
        elif node.op.type is TokenType.MOD:
            return left_val % right_val
        elif node.op.type is TokenType.AND:
            return left_val and right_val
        elif node.op.type is TokenType.OR:
            return left_val or right_val
        elif node.op.type is TokenType.EQUALS:
            return left_val == right_val
        elif node.op.type is TokenType.NOT_EQUALS:
            return left_val != right_val
        elif node.op.type is TokenType.GREATER:
            return left_val > right_val
        elif node.op.type is TokenType.GREATER_EQUALS:
            return left_val >= right_val
        elif node.op.type is TokenType.LESS:
            return left_val < right_val
        elif node.op.type is TokenType.LESS_EQUALS:
            return left_val <= right_val

    def visit_num(self, node: Num):
        return node.value

    def visit_boolean(self, node: Boolean):
        return node.value

    def visit_unaryop(self, node: UnaryOp):
        if node.op.type is TokenType.PLUS:
            return +self.visit(node.factor)
        if node.op.type is TokenType.MINUS:
            return -self.visit(node.factor)
        if node.op.type is TokenType.NOT:
            return not self.visit(node.factor)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_var(self, node: Var):
        current_frame: Frame = self.callstack.peek()
        # get value by variable's name
        val = current_frame.get_value(node.name)
        return val

    def visit_assign(self, node: Assign):
        var_name = node.left.name  # get variable's name
        var_value = self.visit(node.right)
        current_frame: Frame = self.callstack.peek()
        if current_frame.type is FrameType.FUNCTION and current_frame.name == var_name:
            current_frame.return_val = var_value
        else:
            current_frame.set_value(var_name, var_value)

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
        var_name = node.var_node.name
        current_frame: Frame = self.callstack.peek()
        current_frame.define(var_name)

    def visit_procdecl(self, node: ProcedureDecl):
        proc_name = node.token.value
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
            current_frame.define(formal_param.var_node.name)
            current_frame.set_value(formal_param.var_node.name, actual_param_value)

        self.visit(proc_node.block)
        self.log(str(self.callstack))

        self.callstack.pop()
        self.log(f'LEAVE: PROCEDURE {proc_name}')

    def visit_funcdecl(self, node: FunctionDecl):
        func_name = node.token.value
        current_frame: Frame = self.callstack.peek()
        current_frame.define(func_name)
        current_frame.set_value(func_name, node)

    def visit_funccall(self, node: FunctionCall):
        current_frame = self.callstack.peek()
        func_name = node.func_name
        func_node: FunctionDecl = current_frame.get_value(func_name)

        self.log(f'ENTER: FUNCTION {func_name}')
        func_frame = Frame(name=func_name, type=FrameType.FUNCTION)
        self.callstack.push(func_frame)
        current_frame: Frame = self.callstack.peek()

        # get actual params values to formal params
        actual_param_values = [self.visit(actual_param)
                               for actual_param in node.actual_params]

        for (formal_param, actual_param_value) in zip(func_node.params, actual_param_values):
            current_frame.define(formal_param.var_node.name)
            current_frame.set_value(formal_param.var_node.name, actual_param_value)

        self.visit(func_node.block)
        self.log(str(self.callstack))
        self.log(f'LEAVE: FUNCTION {func_name}')

        return_val = current_frame.return_val
        self.callstack.pop()
        if return_val is None:
            self.error(error_code=ErrorCode.MISSING_RETURN, token=node.token)
        return return_val

    def visit_condition(self, node: Condition):
        if self.visit(node.condition_node):
            self.visit(node.then_node)
        elif node.else_node is not None:
            self.visit(node.else_node)

    def visit_then(self, node: Then):
        self.visit(node.child)

    def visit_else(self, node: Else):
        self.visit(node.child)

    def visit_while(self, node: WhileLoop):
        while self.visit(node.conditon_node) is True:
            try:
                self.visit(node.body_node)
            except ContinueError:
                continue
            except BreakError:
                break

    def visit_continue(self, node: Continue):
        raise ContinueError()

    def visit_break(self, node: Break):
        raise BreakError()

    def interpret(self):
        ast = self.parser.parse()
        self.analyzer.visit(ast)
        self.visit(ast)
