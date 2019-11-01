from visitor import Visitor
from symbol_table import ScopedSymbolTable, VarSymbol, ProcedureSymbol
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type, ProcedureDecl


class SemanticAnalyzer(Visitor):
    '''
    SemanticAnalyzer inherit from Visitor and it's work is
    build program's symbol table by given AST parsed by Parser
    '''

    def __init__(self):
        self.current_scope = None

    def scope(self) -> ScopedSymbolTable:
        return self.current_scope

    def visit_program(self, node: Program):
        # add global scoped symbol table
        print('enter scope: global')
        global_scope = ScopedSymbolTable(scope_name='global', scope_level=1)
        self.current_scope = global_scope
        self.visit(node.block)
        print(global_scope)
        print('leave scope: global')

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
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var.value
        # duplicate define check
        if self.current_scope.lookup(var_name) is not None:
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)

    def visit_assign(self, node: Assign):
        # right-hand side
        self.visit(node.right)
        # left-hand side
        self.visit(node.left)

    def visit_var(self, node: Var):
        # judge if variable is not declared
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_procdecl(self, node: ProcedureDecl):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        # then we shoud enter new scope
        print('enter scope: %s' % proc_name)
        # new scope include var declaration and formal params
        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name, scope_level=2)
        self.current_scope = procedure_scope
        # intert params into the procedure scope
        for param in node.params:
            param_name = param.var.value
            param_type = self.current_scope.lookup(param.type.type)
            # build var symbol and append to proc_symbol
            var_symbol = VarSymbol(name=param_name, type=param_type)
            proc_symbol.params.append(var_symbol)
            # define symbol into current scope
            self.current_scope.define(var_symbol)

        self.visit(node.block)
        print(procedure_scope)
        print('leave scope: %s' % proc_name)
