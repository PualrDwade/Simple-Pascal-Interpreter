from tokens import *
from tokenizer import Tokenizer, Token
from astnodes import *


class Parser(object):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type: str):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def program(self) -> Program:
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(PROGRAM)
        var_node = self.variable()
        programe_name = var_node.value  # value hold the variable's name
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)
        return Program(programe_name, block)

    def block(self) -> Block:
        """block : declarations compound_statement"""
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self) -> [AST]:
        """declarations : VAR (variable_declaration SEMI)+
                        | (PROCEDURE ID SEMI block SEMI)*
                        | empty
        """
        declarations = []

        if self.current_token.type is VAR:
            self.eat(VAR)
            while self.current_token.type is ID:
                declarations.extend(self.variable_declaration())
                self.eat(SEMI)

        while self.current_token.type is PROCEDURE:
            self.eat(PROCEDURE)
            proc_name = self.current_token.value
            self.eat(ID)
            self.eat(SEMI)
            block = self.block()
            proc_decl = ProcedureDecl(proc_name, block)
            declarations.append(proc_decl)
            self.eat(SEMI)

        return declarations

    def variable_declaration(self) -> [VarDecl]:
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type is COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()

        return [VarDecl(var_node, type_node) for var_node in var_nodes]

    def type_spec(self) -> Type:
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        if token.type is INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        return Type(token)

    def compound_statement(self) -> Compound:
        """compound_statement: BEGIN statement_list END"""
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes:
            root.childrens.append(node)
        return root

    def statement_list(self) -> [AST]:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        if self.current_token.type is not SEMI:
            return results
        self.eat(SEMI)
        results.extend(self.statement_list())
        return results

    def statement(self) -> AST:
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type is BEGIN:
            node = self.compound_statement()
        elif self.current_token.type is ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self) -> AST:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left=left, op=op, right=right)

    def variable(self) -> Var:
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self) -> AST:
        """An empty production"""
        return NoOp()

    def factor(self) -> AST:
        """
        factor: PLUS  factor
              | MINUS factor
              | INTEGER_CONST
              | REAL_CONST
              | LPAREN expr RPAREN
              | variable
        """
        token = self.current_token
        if token.type is PLUS:
            self.eat(PLUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is MINUS:
            self.eat(MINUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type is REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type is LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type is ID:
            return self.variable()
        else:
            self.error()

    def term(self) -> AST:
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            else:
                self.eat(FLOAT_DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> AST:
        """expr: term((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
