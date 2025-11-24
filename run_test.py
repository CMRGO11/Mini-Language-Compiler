
"""
Script simple para ejecutar tests del compilador
"""

import os
import subprocess
import sys


def ejecutar_test(archivo_src, categoria):
    """Ejecuta un test individual y muestra el resultado"""
    print(f"\n{'='*50}")
    print(f"🧪 Ejecutando: {categoria}/{archivo_src}")
    print(f"{'='*50}")

    # Construir rutas
    ruta_src = os.path.join("tests", categoria, archivo_src)
    nombre_base = os.path.splitext(archivo_src)[0]
    ruta_tac = os.path.join("tests", categoria, f"{nombre_base}.tac")

    try:
        # Compilar
        print(f"Compilando {ruta_src}...")
        resultado_compile = subprocess.run([
            "python", "compilador.py", "compile",
            ruta_src, "-o", ruta_tac
        ], capture_output=True, text=True)

        if resultado_compile.returncode != 0:
            print(f"Error compilando:")
            print(resultado_compile.stderr)
            return False

        # Ejecutar
        print(f"Ejecutando {ruta_tac}...")
        resultado_run = subprocess.run([
            "python", "compilador.py", "run", ruta_tac
        ], capture_output=True, text=True)

        if resultado_run.returncode != 0:
            print(f"Error ejecutando:")
            print(resultado_run.stderr)
            return False

        print(f"Test completado: {archivo_src}")
        return True

    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


def main():
    """Ejecuta todos los tests por categoría"""

    # Estructura de tests (mínimo 12 como pide el PDF)
    tests_por_categoria = {
        "basic": [
            "basic1_declarations.src",      # Declaraciones simples
            "basic2_assignments.src",       # Asignaciones
            "basic3_arithmetic.src",         # Operaciones aritméticas
            "basic4_bool_expr.src"         # Expresiones complejas
        ],
        "control_flow": [
            "cf1_if_simple.src",          # If simple
            "cf2_if_else.src",            # If-else
            "cf3_while_simple.src",              # While loop
            "cf4_while_if_nested.src"             # Control flow anidado
        ],
        "semantic_errors": [
            "semerr1_undeclared_var.src",         # Variable no declarada
            "semerr2_type_mismatch.src"         # Error de tipos
        ],
        "integration": [
            "int1_sum_loop.src",          # Programa complejo
            "int2_min_and_bool.src"          # Algoritmo completo
        ]
    }

    print("INICIANDO EJECUCIÓN DE TESTS")
    print("Nota: Esto compila y ejecuta cada test, mostrando la salida en terminal")

    total_tests = 0
    exitosos = 0

    for categoria, tests in tests_por_categoria.items():
        print(f"\n📁 CATEGORÍA: {categoria.upper()}")

        for test in tests:
            total_tests += 1
            if ejecutar_test(test, categoria):
                exitosos += 1

    # Resumen final
    print(f"\n{'='*60}")
    print(f" Resumen:")
    print(f"   Tests ejecutados: {total_tests}")
    print(f"   Tests exitosos:   {exitosos}")
    print(f"   Tests fallidos:   {total_tests - exitosos}")
    print(f"{'='*60}")

    if exitosos == total_tests:
        print("Todos los tests pasaron")
    else:
        print("Algunos tests fallaron")


if __name__ == "__main__":
    main()
