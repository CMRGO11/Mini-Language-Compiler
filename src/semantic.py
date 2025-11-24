# src/semantic.py
from .parser import Program  # Importación relativa


class AnalizadorSemanticoAST:
    def __init__(self):
        print("[STUB Semántico] Iniciado (Modo AST).")
        self.tabla_simbolos = {}

    def analizar(self, ast_node):
        if not isinstance(ast_node, Program):
            print(
                f"[STUB Semántico] Error: Se esperaba un nodo 'Program', se recibió {type(ast_node)}")
            return
        print("[STUB Semántico] 'Analizando' el nodo raíz del AST (Program)...")
        print("[STUB Semántico] Análisis simulado completado (sin errores).")
