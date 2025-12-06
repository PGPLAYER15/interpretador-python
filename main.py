

import argparse
import sys
from lexer import lexer
from parser import parse, print_ast
from interpreter import interpret, repl


def run_file(filename: str):
    """Ejecuta un archivo de código fuente"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        interp = interpret(code)
        return True
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_code(code: str):
    """Ejecuta código directamente"""
    try:
        interp = interpret(code)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def show_tokens(code: str):
    """Muestra los tokens del código"""
    print("=" * 40)
    print("Tokens:")
    print("=" * 40)
    tokens = list(lexer(code))
    for i, tok in enumerate(tokens):
        print(f"  {i+1:3}. {tok.type:10} : {tok.value!r}")
    print(f"\nTotal: {len(tokens)} tokens")


def show_ast(code: str):
    """Muestra el AST del código"""
    print("=" * 40)
    print("AST (Árbol de Sintaxis Abstracta):")
    print("=" * 40)
    try:
        ast = parse(code)
        print_ast(ast)
    except Exception as e:
        print(f"Error de sintaxis: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Interpretador de Lenguaje Simple",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                       # Iniciar REPL
  python main.py programa.txt          # Ejecutar archivo
  python main.py -c "x = 5; print(x);" # Ejecutar código
  python main.py --tokens "1 + 2;"     # Ver tokens
  python main.py --ast "1 + 2 * 3;"    # Ver AST
        """
    )
    
    parser.add_argument(
        'archivo',
        nargs='?',
        help='Archivo a ejecutar'
    )
    
    parser.add_argument(
        '-c', '--code',
        help='Ejecutar código directamente'
    )
    
    parser.add_argument(
        '--tokens',
        metavar='CODE',
        help='Mostrar tokens del código'
    )
    
    parser.add_argument(
        '--ast',
        metavar='CODE',
        help='Mostrar AST del código'
    )
    
    args = parser.parse_args()
    
    # Mostrar tokens
    if args.tokens:
        show_tokens(args.tokens)
        return
    
    # Mostrar AST
    if args.ast:
        show_ast(args.ast)
        return
    
    # Ejecutar código directamente
    if args.code:
        success = run_code(args.code)
        sys.exit(0 if success else 1)
    
    # Ejecutar archivo
    if args.archivo:
        success = run_file(args.archivo)
        sys.exit(0 if success else 1)
    
    # REPL interactivo
    repl()


if __name__ == "__main__":
    main()
