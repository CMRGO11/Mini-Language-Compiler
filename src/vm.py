class MaquinaTAC:
    def __init__(self):
        print("[MaquinaTAC] VM Inicializada.")
        self.mem = {}  # Memoria de variables y temporales
        self.labels = {}  # Mapa de etiquetas a número de línea

    def _get_val(self, operando):
        if operando.isdigit():
            return int(operando)
        elif operando == 'true':
            return True
        elif operando == 'false':
            return False
        return self.mem.get(operando, 0)

    def preprocesar_etiquetas(self, lineas):
        """Busca donde están las etiquetas para los saltos"""
        self.labels.clear()
        instrucciones_limpias = []
        indice = 0
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue

            if linea.endswith(':'):  # Es una etiqueta
                label_name = linea[:-1]
                self.labels[label_name] = indice
            else:
                instrucciones_limpias.append(linea)
                indice += 1
        return instrucciones_limpias

    def ejecutar(self, codigo_tac_string):
        lineas_crudas = codigo_tac_string.split('\n')
        instrucciones = self.preprocesar_etiquetas(lineas_crudas)
        pc = 0  # Program Counter

        print(
            f"\n--- [Ejecución Real] Iniciando ({len(instrucciones)} instrucciones) ---")

        while pc < len(instrucciones):
            inst = instrucciones[pc]
            partes = inst.split()

            # 1. Saltos (GOTO)
            if partes[0] == 'goto':
                etiqueta = partes[1]
                pc = self.labels[etiqueta]
                continue

            # 2. IF (if t1 == false goto L2)
            elif partes[0] == 'if':
                cond_val = self._get_val(partes[1])
                target_val = False
                label = partes[5]
                if cond_val == target_val:
                    pc = self.labels[label]
                    continue

            # 3. PRINT
            elif partes[0] == 'print':
                val = self._get_val(partes[1])
                print(f"OUTPUT >> {val}")

            # 4. Asignaciones y Operaciones
            elif len(partes) >= 3 and partes[1] == ':=':
                destino = partes[0]

                if len(partes) == 3:  # x := 5
                    self.mem[destino] = self._get_val(partes[2])

                elif len(partes) == 5:  # t1 := a + b
                    op1 = self._get_val(partes[2])
                    operador = partes[3]
                    op2 = self._get_val(partes[4])

                    res = 0
                    if operador == '+':
                        res = op1 + op2
                    elif operador == '-':
                        res = op1 - op2
                    elif operador == '*':
                        res = op1 * op2
                    elif operador == '/':
                        res = int(op1 / op2)
                    elif operador == '<':
                        res = op1 < op2
                    elif operador == '>':
                        res = op1 > op2
                    elif operador == '==':
                        res = (op1 == op2)
                    elif operador == '!=':
                        res = (op1 != op2)
                    elif operador == '&&':
                        res = (op1 and op2)
                    elif operador == '||':
                        res = (op1 or op2)

                    self.mem[destino] = res

            pc += 1
        print("--- [Ejecución Real] Finalizada ---")
