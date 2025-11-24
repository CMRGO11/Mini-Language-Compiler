# ================== 1. ANALIZADOR LÉXICO (FINAL) ==================

import re


class AnalizadorLexico:
    def __init__(self):
        self.palabras_reservadas = {
            'int': 'TIPO_INT', 'bool': 'TIPO_BOOL', 'if': 'IF',
            'else': 'ELSE', 'while': 'WHILE', 'print': 'PRINT',
            'true': 'TRUE', 'false': 'FALSE'
        }

        self.mapa_tokens = {
            '&&': 'OP_AND', '||': 'OP_OR',
            '==': 'OP_REL', '!=': 'OP_REL', '<=': 'OP_REL', '>=': 'OP_REL',
            '<': 'OP_REL', '>': 'OP_REL',
            '!': 'OP_NOT',
            '+': 'OP_ARIT', '-': 'OP_ARIT', '*': 'OP_ARIT', '/': 'OP_ARIT',
            '=': 'ASIGN',
            ';': 'PUNTOCOMA', ',': 'COMA',
            '(': 'LPAREN', ')': 'RPAREN',
            '{': 'LBRACE', '}': 'RBRACE'
        }

        # Grupos de no captura (?:...) aplicados para evitar problemas de índice
        rules = [
            (r'\s+', None),
            (r'//.*', None),
            (r'(?:==|<=|>=|!=|&&|\|\|)', 'OPERADOR_MULTI'),
            (r'\b(?:int|bool|if|else|while|print|true|false)\b', 'KEYWORD'),
            (r'\b[0-9]+\b', 'NUMERO_ENTERO'),
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'ID'),
            (r'[=<>\+\-\*/!;,(){}]', 'OPERADOR_SIMPLE')
        ]

        self.patron_token = re.compile(
            '|'.join(f'({rule})' for rule, _ in rules))
        self.tipos_token = [tipo for _, tipo in rules]

    def tokenizar(self, codigo):
        tokens = []
        linea = 1

        for match in self.patron_token.finditer(codigo):
            tipo = None
            valor = match.group(0)

            # ********** CORRECCIÓN DEL ÍNDICE APLICADA (i + 1) **********
            for i, tipo_sub in enumerate(self.tipos_token):
                if match.group(i + 1):  # <-- CAMBIO CLAVE
                    tipo = tipo_sub
                    break
            # ************************************************************

            if tipo is None:
                if '\n' in valor:
                    linea += valor.count('\n')
                continue

            tipo_token = None
            if tipo == 'KEYWORD':
                tipo_token = self.palabras_reservadas.get(valor)
            elif tipo == 'ID':
                tipo_token = 'ID'
            elif tipo == 'NUMERO_ENTERO':
                tipo_token = 'LITERAL_ENTERO'
            elif tipo == 'OPERADOR_MULTI' or tipo == 'OPERADOR_SIMPLE':
                tipo_token = self.mapa_tokens.get(valor)

            if tipo_token is None:
                print(
                    f"Advertencia Léxica en línea {linea}: Token no reconocido '{valor}' (tipo {tipo}) ignorado.")
                continue

            tokens.append(Token(tipo_token, valor, linea))

        tokens.append(Token('EOF', 'EOF', linea))
        return tokens


class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"
