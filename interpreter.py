from typing import Any, Dict
from parser import (
    parse, ProgramNode, NumberNode, IdNode, BinOpNode,
    UnaryOpNode, AssignNode, PrintNode
)


# ==================== ERRORES ====================

class RuntimeError(Exception):
    pass


# ==================== INTÉRPRETE ====================

class Interpreter:
    
    
    def __init__(self):
        self.env: Dict[str, Any] = {}  # Entorno de variables
        self.output: list = []  # Captura la salida de print para testing
    
    def run(self, node) -> Any:
        """Punto de entrada: ejecuta un nodo AST"""
        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name, None)
        
        if method is None:
            raise RuntimeError(f"No se puede evaluar el nodo: {type(node).__name__}")
        
        return method(node)
    
    # ---------- Evaluadores por tipo de nodo ----------
    
    def eval_ProgramNode(self, node: ProgramNode) -> Any:
        """Evalúa todas las sentencias del programa"""
        result = None
        for stmt in node.statements:
            result = self.run(stmt)
        return result
    
    def eval_NumberNode(self, node: NumberNode) -> int:
        """Evalúa un literal numérico"""
        return node.value
    
    def eval_IdNode(self, node: IdNode) -> Any:
        """Evalúa un identificador (variable)"""
        if node.name not in self.env:
            raise RuntimeError(f"Variable no definida: '{node.name}'")
        return self.env[node.name]
    
    def eval_BinOpNode(self, node: BinOpNode) -> Any:
        """Evalúa una operación binaria"""
        left = self.run(node.left)
        
        if node.op == 'and':
            if not left:
                return left
            return self.run(node.right)
        
        if node.op == 'or':
            if left:
                return left
            return self.run(node.right)
        
        right = self.run(node.right)
        
        # Operadores aritméticos
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                raise RuntimeError("División por cero")
            return left // right  # División entera
        
        # Operadores de comparación
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        
        else:
            raise RuntimeError(f"Operador desconocido: '{node.op}'")
    
    def eval_UnaryOpNode(self, node: UnaryOpNode) -> Any:
        """Evalúa una operación unaria"""
        operand = self.run(node.operand)
        
        if node.op == '-':
            return -operand
        elif node.op == 'not':
            return not operand
        else:
            raise RuntimeError(f"Operador unario desconocido: '{node.op}'")
    
    def eval_AssignNode(self, node: AssignNode) -> Any:
        """Evalúa una asignación"""
        value = self.run(node.value)
        self.env[node.name] = value
        return value
    
    def eval_PrintNode(self, node: PrintNode) -> None:
        """Evalúa una sentencia print"""
        value = self.run(node.expr)
        print(value)
        self.output.append(value)  # Captura para testing
        return None


# ==================== FUNCIONES DE CONVENIENCIA ====================

def interpret(text: str, env: Dict[str, Any] = None) -> Interpreter:
    """
    Función de conveniencia: lexer + parser + interpreter en un solo paso.
    
    Args:
        text: Código fuente a interpretar
        env: Entorno inicial opcional con variables predefinidas
    
    Returns:
        El intérprete después de ejecutar (contiene env y output)
    """
    ast = parse(text)
    interpreter = Interpreter()
    if env:
        interpreter.env.update(env)
    interpreter.run(ast)
    return interpreter


def run(text: str) -> Any:
    """
    Ejecuta código y retorna el último valor evaluado.
    
    Args:
        text: Código fuente a ejecutar
    
    Returns:
        El resultado de la última expresión evaluada
    """
    ast = parse(text)
    interpreter = Interpreter()
    return interpreter.run(ast)


# ==================== REPL ====================

def repl():
    """
    Read-Eval-Print Loop interactivo.
    
    Permite ejecutar código línea por línea de forma interactiva.
    """
    print("=" * 60)
    print("Intérprete Interactivo")
    print("Escribe código para ejecutar. Escribe 'salir' para terminar.")
    print("=" * 60)
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input(">>> ")
            
            if line.strip().lower() in ('salir', 'exit', 'quit'):
                print("¡Adiós!")
                break
            
            if not line.strip():
                continue
            
            # Agregar punto y coma si no lo tiene
            if not line.strip().endswith(';'):
                line = line + ';'
            
            ast = parse(line)
            result = interpreter.run(ast)
            
            # Mostrar resultado si no es None y no es un print
            if result is not None:
                print(f"=> {result}")
        
        except KeyboardInterrupt:
            print("\n¡Adiós!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    repl()
