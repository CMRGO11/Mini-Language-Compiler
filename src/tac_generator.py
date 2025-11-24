class TACGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions = []
    # Los temp sirven para las variables temporales donde se guarda la informacion de operaciones binarias

    def new_temp(self):
        # Genera un nuevo nombre de temporal
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    # Las etiquetas indican saltos de linea y cambian el flujo del código
    def new_label(self):
        # Genera una nueva etiqueta
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instruction):
        # Añade una instrucción TAC a la lista
        self.instructions.append(instruction)

    def visit(self, node):
        # Método principal que visita cada tipo de nodo
        # Busca el método del tipo que reciba
        method_name = f'visit_{type(node).__name__}'
        # Ejecuta su método dependiendo del tipo
        method = getattr(self, method_name, self.visit_unknown)
        return method(node)

    def visit_unknown(self, node):
        raise Exception(
            f"Método visit no implementado para {type(node).__name__}")

    # ========== MÉTODOS del AST ==========

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    # Para valores enteros
    def visit_Literal(self, node):
        return node.token.valor
    # Para variables

    def visit_Variable(self, node):
        return node.token.valor

    # Para operaciones binarias
    def visit_BinaryOp(self, node):
        # Visita primero sus nodos hijos
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        temp = self.new_temp()  # obtiene una variable temporal para luego almacenarla
        self.emit(f"{temp} := {left_value} {node.op_token.valor} {right_value}")
        return temp
    # Para asignación x = a + b

    def visit_Assignment(self, node):
        # Checa el target (x)
        target = node.var_token.valor
        # Checa el valor de la asignación (a + b)
        value = self.visit(node.expression)
        self.emit(f"{target} := {value}")
        return target
    # Para ifs

    def visit_IfStatement(self, node):
        # Visita primero la condición
        condition = self.visit(node.condition)
        # Declara label del else, importante para marcar el flujo
        label_else = self.new_label()

        self.emit(f"if {condition} == false goto {label_else}")
        # Visita la condición que se cumple
        self.visit(node.true_branch)

        if node.false_branch:  # Si hay sentencia de else no vacía
            # Declara nuevo label para el salto al final de la condición
            label_end = self.new_label()
            self.emit(f"goto {label_end}")
            self.emit(f"{label_else}:")  # Inicio del bloque else
            self.visit(node.false_branch)
            self.emit(f"{label_end}:")
        else:
            self.emit(f"{label_else}:")

    # Para el while
    def visit_WhileStatement(self, node):
        # Declaración de labels primero para el flujo de información
        label_start = self.new_label()
        label_end = self.new_label()

        self.emit(f"{label_start}:")
        # Procesar la condición
        condition = self.visit(node.condition)
        self.emit(f"if {condition} == false goto {label_end}")
        # Visitar el contenido del while
        self.visit(node.body)
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    # Para los bloques de código extensos (de if y while)
    def visit_Block(self, node):
        # Por cada uno de las lineas de código, se visitan
        for statement in node.statements:
            self.visit(statement)

    # Para el print
    def visit_PrintStatement(self, node):
        value = self.visit(node.expression)
        self.emit(f"print {value}")

    def visit_VarDecl(self, node):
        # Las declaraciones no generan código TAC ejecutable
        self.emit(
            f"# Declaración: {node.tipo_token.valor} {node.var_token.valor}")

    def generate(self, ast):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        self.visit(ast)
        return self.instructions


class GeneradorDeCodigo:
    def __init__(self):
        print("[CodeGen] Iniciado (Generador TAC Real).")
        self.generator = TACGenerator()

    def generar(self, ast_node):
        print("[CodeGen] Generando TAC desde el AST...")
        instructions = self.generator.generate(ast_node)

        # Convertir a string para guardar en archivo
        tac_code = "\n".join(instructions)
        return tac_code
