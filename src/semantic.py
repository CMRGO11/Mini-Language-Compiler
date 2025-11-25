import sys


class AnalizadorSemanticoAST:
    def __init__(self):
        print("[Semántico] Iniciando análisis de tipos y alcances...")
        self.tabla_simbolos = {}  # Guarda {nombre_variable: tipo}

    def _error(self, mensaje):
        print(f"Error Semántico: {mensaje}")
        sys.exit(1)

    def analizar(self, node):
        self.visit(node)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_unknown)
        return method(node)

    def visit_unknown(self, node):
        pass

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        nombre = node.var_token.valor
        tipo = node.tipo_token.valor  # 'int' o 'bool'
        if nombre in self.tabla_simbolos:
            self._error(f"Variable '{nombre}' ya declarada.")
        self.tabla_simbolos[nombre] = tipo

    def visit_Assignment(self, node):
        nombre = node.var_token.valor
        if nombre not in self.tabla_simbolos:
            self._error(f"Variable '{nombre}' no ha sido declarada.")

        tipo_variable = self.tabla_simbolos[nombre]
        tipo_expr = self.visit(node.expression)

        if tipo_variable != tipo_expr:
            self._error(
                f"No se puede asignar '{tipo_expr}' a la variable '{nombre}' de tipo '{tipo_variable}'.")

    def visit_IfStatement(self, node):
        tipo_cond = self.visit(node.condition)
        if tipo_cond != 'bool':
            self._error(
                f"La condición del 'if' debe ser bool, se recibió: {tipo_cond}")
        self.visit(node.true_branch)
        if node.false_branch:
            self.visit(node.false_branch)

    def visit_WhileStatement(self, node):
        tipo_cond = self.visit(node.condition)
        if tipo_cond != 'bool':
            self._error(
                f"La condición del 'while' debe ser bool, se recibió: {tipo_cond}")
        self.visit(node.body)

    def visit_PrintStatement(self, node):
        self.visit(node.expression)

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_BinaryOp(self, node):
        tipo_izq = self.visit(node.left)
        tipo_der = self.visit(node.right)
        op = node.op_token.valor

        if op in ['+', '-', '*', '/']:
            if tipo_izq == 'int' and tipo_der == 'int':
                return 'int'
            self._error(f"Operación aritmética '{op}' requiere enteros.")

        elif op in ['<', '>', '<=', '>=', '==', '!=']:
            if tipo_izq == tipo_der:
                return 'bool'
            self._error(f"Comparación '{op}' requiere tipos iguales.")

        elif op in ['&&', '||']:
            if tipo_izq == 'bool' and tipo_der == 'bool':
                return 'bool'
            self._error(f"Operador lógico '{op}' requiere booleanos.")

        return None

    def visit_Literal(self, node):
        val = node.token.valor
        if val in ['true', 'false']:
            return 'bool'
        return 'int'

    def visit_Variable(self, node):
        nombre = node.token.valor
        if nombre not in self.tabla_simbolos:
            self._error(f"Variable '{nombre}' no declarada.")
        return self.tabla_simbolos[nombre]
