from astnodes import AST, BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, \
    Param, VarDecl, Type, ProcedureDecl, ProcedureCall, Boolean
from errors import ParserError, ErrorCode
from tokenizer import Tokenizer
from tokens import TokenType
from typing import List


class Parser(object):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type: TokenType):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def program(self) -> Program:
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        programe_name = var_node.name  # value hold the variable's name
        self.eat(TokenType.SEMI)
        block = self.block()
        self.eat(TokenType.DOT)
        return Program(programe_name, block)

    def block(self) -> Block:
        """block : declarations compound_statement"""
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self) -> List[AST]:
        """
        declarations : (VAR (variable_declaration SEMI)+)? procedure_declaration*
        """
        declarations = []

        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI)

        while self.current_token.type == TokenType.PROCEDURE:
            proc_decl = self.procedure_declaration()
            declarations.append(proc_decl)

        return declarations

    def procedure_declaration(self) -> ProcedureDecl:
        """procedure_declaration :
            PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI
        """
        self.eat(TokenType.PROCEDURE)
        proc_token = self.current_token
        self.eat(TokenType.ID)
        params = []

        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            params = self.formal_parameter_list()
            self.eat(TokenType.RPAREN)

        self.eat(TokenType.SEMI)
        block_node = self.block()
        proc_decl = ProcedureDecl(proc_token, params, block_node)
        self.eat(TokenType.SEMI)
        return proc_decl

    def formal_parameter_list(self) -> List[Param]:
        """ formal_parameter_list : formal_parameters
                              | formal_parameters SEMI formal_parameter_list
        """
        if not self.current_token.type is TokenType.ID:
            return []

        params = self.formal_parameters()
        while self.current_token.type is TokenType.SEMI:
            self.eat(TokenType.SEMI)
            params.extend(self.formal_parameters())

        return params

    def formal_parameters(self) -> List[Param]:
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        return [Param(var_node=var_node, type_node=type_node) for var_node in var_nodes]

    def variable_declaration(self) -> List[VarDecl]:
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()

        return [VarDecl(var_node=var_node, type_node=type_node) for var_node in var_nodes]

    def type_spec(self) -> Type:
        """type_spec : INTEGER
                     | REAL
                     | BOOLEAN
        """
        token = self.current_token
        if token.type in (TokenType.INTEGER, TokenType.REAL, TokenType.BOOLEAN):
            self.eat(token.type)
            return Type(token)
        self.error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

    def compound_statement(self) -> Compound:
        """compound_statement: BEGIN statement_list END"""
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)
        root = Compound()
        for node in nodes:
            root.childrens.append(node)
        return root

    def statement_list(self) -> List[AST]:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        if self.current_token.type is not TokenType.SEMI:
            return results
        self.eat(TokenType.SEMI)
        results.extend(self.statement_list())
        return results

    def statement(self) -> AST:
        """
        statement : compound_statement
                  | proccall_statement
                  | if_else_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type is TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type is TokenType.ID and self.tokenizer.current_char is '(':
            node = self.proccall_statement()
        elif self.current_token.type is TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def if_else_statement(self) -> AST:
        """
        if_else_statement : if condition_statement then statement_list (else statement_list) ?
        """
        pass

    def condition_statement(self) -> AST:
        """
        condition_statement : expr (EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL) expr
        """

    def assignment_statement(self) -> AST:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        op = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left=left, op=op, right=right)

    def proccall_statement(self) -> ProcedureCall:
        """proccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN"""
        procc_token = self.current_token
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        if self.current_token.type is TokenType.RPAREN:
            self.eat(TokenType.RPAREN)
            return ProcedureCall(procc_token.value, [], procc_token)
        else:
            actual_params = [self.expr()]
            while self.current_token.type is TokenType.COMMA:
                self.eat(TokenType.COMMA)
                actual_params.append(self.expr())

            self.eat(TokenType.RPAREN)
            return ProcedureCall(procc_token.value, actual_params, procc_token)

    def variable(self) -> Var:
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self) -> AST:
        """An empty production"""
        return NoOp()

    def first_priority(self) -> AST:
        """
        factor: PLUS  factor
              | MINUS factor
              | NOT factor
              | INTEGER_CONST
              | REAL_CONST
              | TRUE
              | FALSE
              | LPAREN expr RPAREN
              | variable
        """
        token = self.current_token
        if token.type is TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)

        elif token.type is TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)

        elif token.type is TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(token)

        elif token.type is TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(token)

        elif token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        else:
            return self.variable()

    def second_priority(self) -> AST:
        """term : factor ((MUL | DIV | MOD) factor)*"""
        left = self.first_priority()
        result = left
        while self.current_token.type in (TokenType.MUL,
                                          TokenType.INTEGER_DIV,
                                          TokenType.FLOAT_DIV,
                                          TokenType.MOD):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.first_priority())

        return result

    def third_priority(self) -> AST:
        """simple_expr: term((PLUS | MINUS) term)*"""
        left = self.second_priority()
        result = left

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.second_priority())

        return result

    def fourth_priority(self) -> AST:
        """
        GREATER| GREATER_EQUALS| LESS| LESS_EQUALS
        """
        left = self.third_priority()
        result = left

        while self.current_token.type in (TokenType.GREATER,
                                          TokenType.GREATER_EQUALS,
                                          TokenType.LESS,
                                          TokenType.LESS_EQUALS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.third_priority())

        return result

    def fifth_priority(self) -> AST:
        """
        EQUALS|NOT_EQUALS
        """
        left = self.fourth_priority()
        result = left

        while self.current_token.type in (TokenType.EQUALS, TokenType.NOT_EQUALS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.fourth_priority())

        return result

    def sixth_priority(self) -> AST:
        """
        AND
        """
        left = self.fifth_priority()
        result = left

        while self.current_token.type is TokenType.AND:
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.fifth_priority())

        return result

    def seventh_priority(self) -> AST:
        """
        OR
        """
        left = self.sixth_priority()
        result = left

        while self.current_token.type is TokenType.OR:
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.sixth_priority())

        return result

    def expr(self) -> AST:
        return self.seventh_priority()

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
