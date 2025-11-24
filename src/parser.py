import sys
# ================== 2. CLASES AST ==================


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


class VarDecl(Statement):
    def __init__(self, tipo_token, var_token):
        self.tipo_token = tipo_token
        self.var_token = var_token


class Assignment(Statement):
    def __init__(self, var_token, expression):
        self.var_token = var_token
        self.expression = expression


class IfStatement(Statement):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class Block(Statement):
    def __init__(self, statements):
        self.statements = statements


class BinaryOp(Expression):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right


class UnaryOp(Expression):
    def __init__(self, op_token, right):
        self.op_token = op_token
        self.right = right


class Literal(Expression):
    def __init__(self, token):
        self.token = token


class Variable(Expression):
    def __init__(self, token):
        self.token = token


# ================== 3. ANALIZADOR SINTÁCTICO ==================

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_actual = self.tokens[self.pos]

    def _error(self, mensaje):
        print(
            f"Error Sintáctico en línea {self.token_actual.linea}: {mensaje}. Se encontró: {self.token_actual.tipo}")
        sys.exit(1)  # Termina el programa

    def _avanzar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_actual = self.tokens[self.pos]

    def _consumir(self, tipo_esperado):
        if self.token_actual.tipo == tipo_esperado:
            self._avanzar()
        else:
            self._error(f"Se esperaba '{tipo_esperado}'")

    def parse(self):
        statements = []
        while self.token_actual.tipo != 'EOF':
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.token_actual.tipo in ('TIPO_INT', 'TIPO_BOOL'):
            return self.parse_var_declaration()
        elif self.token_actual.tipo == 'IF':
            return self.parse_if_statement()
        elif self.token_actual.tipo == 'WHILE':
            return self.parse_while_statement()
        elif self.token_actual.tipo == 'PRINT':
            return self.parse_print_statement()
        elif self.token_actual.tipo == 'ID':
            return self.parse_assignment_statement()
        elif self.token_actual.tipo == 'LBRACE':
            return self.parse_block()
        else:
            self._error("Declaración no válida")

    def parse_block(self):
        statements = []
        self._consumir('LBRACE')
        while self.token_actual.tipo != 'RBRACE' and self.token_actual.tipo != 'EOF':
            statements.append(self.parse_statement())
        self._consumir('RBRACE')
        return Block(statements)

    def parse_var_declaration(self):
        tipo_token = self.token_actual
        self._avanzar()
        var_token = self.token_actual
        self._consumir('ID')
        self._consumir('PUNTOCOMA')
        return VarDecl(tipo_token, var_token)

    def parse_assignment_statement(self):
        var_token = self.token_actual
        self._consumir('ID')
        self._consumir('ASIGN')
        expr = self.parse_expression()
        self._consumir('PUNTOCOMA')
        return Assignment(var_token, expr)

    def parse_if_statement(self):
        self._consumir('IF')
        self._consumir('LPAREN')
        condicion = self.parse_expression()
        self._consumir('RPAREN')
        true_branch = self.parse_statement()

        false_branch = None
        if self.token_actual.tipo == 'ELSE':
            self._avanzar()
            false_branch = self.parse_statement()

        return IfStatement(condicion, true_branch, false_branch)

    def parse_while_statement(self):
        self._consumir('WHILE')
        self._consumir('LPAREN')
        condicion = self.parse_expression()
        self._consumir('RPAREN')
        body = self.parse_statement()
        return WhileStatement(condicion, body)

    def parse_print_statement(self):
        self._consumir('PRINT')
        self._consumir('LPAREN')
        expr = self.parse_expression()
        self._consumir('RPAREN')
        self._consumir('PUNTOCOMA')
        return PrintStatement(expr)

    def parse_expression(self):
        nodo = self.parse_primary_expression()
        while self.token_actual.tipo in ('OP_ARIT', 'OP_REL', 'OP_AND', 'OP_OR'):
            op_token = self.token_actual
            self._avanzar()
            right = self.parse_primary_expression()
            nodo = BinaryOp(left=nodo, op_token=op_token, right=right)
        return nodo

    def parse_primary_expression(self):
        token = self.token_actual
        if token.tipo == 'LITERAL_ENTERO':
            self._avanzar()
            return Literal(token)
        elif token.tipo in ('TRUE', 'FALSE'):
            self._avanzar()
            return Literal(token)
        elif token.tipo == 'ID':
            self._avanzar()
            return Variable(token)
        elif token.tipo == 'LPAREN':
            self._avanzar()
            nodo = self.parse_expression()
            self._consumir('RPAREN')
            return nodo
        else:
            self._error(
                "Expresión primaria no válida (se esperaba número, ID, 'true'/'false' o '(')")
