from astnodes import AST, BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, \
    Program, Block, VarDecl, Type, ProcedureDecl, ProcedureCall, Condition, Then, Else, Boolean, FunctionCall, \
    FunctionDecl, WhileLoop, Continue, Break


class Visitor(object):
    """
    Visitor is common base class to visit abstract syntax tree
    each concrete visitor should implement its visit method
    """

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
        elif isinstance(node, ProcedureDecl):
            return self.visit_procdecl(node)
        elif isinstance(node, ProcedureCall):
            return self.visit_proccall(node)
        elif isinstance(node, FunctionDecl):
            return self.visit_funcdecl(node)
        elif isinstance(node, FunctionCall):
            return self.visit_funccall(node)
        elif isinstance(node, Condition):
            return self.visit_condition(node)
        elif isinstance(node, Then):
            return self.visit_then(node)
        elif isinstance(node, Else):
            return self.visit_else(node)
        elif isinstance(node, WhileLoop):
            return self.visit_while(node)
        elif isinstance(node, Continue):
            return self.visit_continue(node)
        elif isinstance(node, Break):
            return self.visit_break(node)
        else:
            raise Exception("Invalid AST node: %s" % node)

    def visit_binop(self, node: BinOp):
        pass

    def visit_num(self, node: Num):
        pass

    def visit_boolean(self, node: Boolean):
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

    def visit_procdecl(self, node: ProcedureDecl):
        pass

    def visit_proccall(self, node: ProcedureCall):
        pass

    def visit_funcdecl(self, node: FunctionDecl):
        pass

    def visit_funccall(self, node: FunctionCall):
        pass

    def visit_condition(self, node: Condition):
        pass

    def visit_then(self, node: Then):
        pass

    def visit_else(self, node: Else):
        pass

    def visit_while(self, node: WhileLoop):
        pass

    def visit_continue(self, node: Continue):
        pass

    def visit_break(self, node: Break):
        pass
