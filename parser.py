from dataclasses import dataclass
from typing import List, Any, Optional
from lexer import lexer, Token


# ==================== NODOS AST ====================

@dataclass
class NumberNode:
    value: int


@dataclass
class IdNode:
    name: str


@dataclass
class BinOpNode:
    left: Any
    op: str
    right: Any


@dataclass  
class UnaryOpNode:
    op: str
    operand: Any


@dataclass
class AssignNode:
    name: str
    value: Any


@dataclass
class PrintNode:
    expr: Any


@dataclass
class ProgramNode:
    statements: List[Any]


# ==================== ERRORES ====================

class ParseError(Exception):
    pass


# ==================== PARSER ====================

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    # ---------- Utilidades ----------
    
    def current_token(self) -> Optional[Token]:
        """Retorna el token actual sin consumirlo"""
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'NEWLINE':
            self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def peek(self, token_type: str) -> bool:
        """Verifica si el token actual es del tipo especificado"""
        token = self.current_token()
        return token is not None and token.type == token_type
    
    def consume(self, token_type: str) -> Token:
        """Consume el token actual si coincide con el tipo esperado"""
        token = self.current_token()
        if token is None:
            raise ParseError(f"Se esperaba '{token_type}', pero se llegó al final del archivo")
        if token.type != token_type:
            raise ParseError(f"Se esperaba '{token_type}', pero se encontró '{token.type}' ({token.value!r})")
        self.pos += 1
        return token
    
    def match(self, *token_types: str) -> Optional[Token]:
        """Consume y retorna el token si coincide con alguno de los tipos, None si no"""
        token = self.current_token()
        if token is not None and token.type in token_types:
            self.pos += 1
            return token
        return None
    
    # ---------- Reglas de la gramática ----------
    
    def parse(self) -> ProgramNode:
        """Punto de entrada: parsea todo el programa"""
        statements = []
        while self.current_token() is not None:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return ProgramNode(statements)
    
    def parse_statement(self) -> Any:
        """Parsea una sentencia: asignación, print, o expresión"""
        token = self.current_token()
        
        if token is None:
            return None
        
        # Sentencia print
        if token.type == 'PRINT':
            return self.parse_print()
        
        # Asignación: ID = expr ;
        if token.type == 'ID':
            # Mirar adelante para ver si es asignación
            if self.pos + 1 < len(self.tokens):
                next_tok = self.tokens[self.pos + 1]
                if next_tok.type == 'ASSIGN':
                    return self.parse_assignment()
        
        # Expresión como sentencia
        return self.parse_expression_statement()
    
    def parse_print(self) -> PrintNode:
        """Parsea: print '(' expresion ')' ';'"""
        self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMI')
        return PrintNode(expr)
    
    def parse_assignment(self) -> AssignNode:
        """Parsea: ID '=' expresion ';'"""
        name_token = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return AssignNode(name_token.value, expr)
    
    def parse_expression_statement(self) -> Any:
        """Parsea: expresion ';'"""
        expr = self.parse_expression()
        self.consume('SEMI')
        return expr
    
    def parse_expression(self) -> Any:
        """Parsea una expresión (punto de entrada)"""
        return self.parse_or()
    
    def parse_or(self) -> Any:
        """Parsea: and_expr ('or' and_expr)*"""
        left = self.parse_and()
        while self.match('OR'):
            right = self.parse_and()
            left = BinOpNode(left, 'or', right)
        return left
    
    def parse_and(self) -> Any:
        """Parsea: not_expr ('and' not_expr)*"""
        left = self.parse_not()
        while self.match('AND'):
            right = self.parse_not()
            left = BinOpNode(left, 'and', right)
        return left
    
    def parse_not(self) -> Any:
        """Parsea: 'not' not_expr | comparacion"""
        if self.match('NOT'):
            operand = self.parse_not()
            return UnaryOpNode('not', operand)
        return self.parse_comparison()
    
    def parse_comparison(self) -> Any:
        """Parsea: suma (('==' | '!=' | '<' | '>' | '<=' | '>=') suma)?"""
        left = self.parse_sum()
        op = self.match('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE')
        if op:
            right = self.parse_sum()
            # Mapear tipos de token a operadores legibles
            op_map = {
                'EQ': '==', 'NEQ': '!=',
                'LT': '<', 'GT': '>',
                'LTE': '<=', 'GTE': '>='
            }
            return BinOpNode(left, op_map[op.type], right)
        return left
    
    def parse_sum(self) -> Any:
        """Parsea: termino (('+' | '-') termino)*"""
        left = self.parse_term()
        while True:
            op = self.match('PLUS', 'MINUS')
            if op:
                right = self.parse_term()
                op_str = '+' if op.type == 'PLUS' else '-'
                left = BinOpNode(left, op_str, right)
            else:
                break
        return left
    
    def parse_term(self) -> Any:
        """Parsea: factor (('*' | '/') factor)*"""
        left = self.parse_factor()
        while True:
            op = self.match('MULT', 'DIV')
            if op:
                right = self.parse_factor()
                op_str = '*' if op.type == 'MULT' else '/'
                left = BinOpNode(left, op_str, right)
            else:
                break
        return left
    
    def parse_factor(self) -> Any:
        """Parsea: NUMBER | ID | '(' expresion ')' | '-' factor"""
        token = self.current_token()
        
        if token is None:
            raise ParseError("Se esperaba una expresión, pero se llegó al final del archivo")
        
        # Número
        if token.type == 'NUMBER':
            self.pos += 1
            return NumberNode(int(token.value))
        
        # Identificador
        if token.type == 'ID':
            self.pos += 1
            return IdNode(token.value)
        
        # Expresión entre paréntesis
        if token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        
        # Negación unaria
        if token.type == 'MINUS':
            self.consume('MINUS')
            operand = self.parse_factor()
            return UnaryOpNode('-', operand)
        
        raise ParseError(f"Token inesperado: {token.type} ({token.value!r})")


# ==================== FUNCIONES AUXILIARES ====================

def parse(text: str) -> ProgramNode:
    """Función de conveniencia: lexer + parser en un solo paso"""
    tokens = list(lexer(text))
    parser = Parser(tokens)
    return parser.parse()


def print_ast(node, indent=0):
    """Imprime el AST de forma legible (para debug)"""
    prefix = "  " * indent
    
    if isinstance(node, ProgramNode):
        print(f"{prefix}Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, NumberNode):
        print(f"{prefix}Number({node.value})")
    elif isinstance(node, IdNode):
        print(f"{prefix}Id({node.name})")
    elif isinstance(node, BinOpNode):
        print(f"{prefix}BinOp({node.op}):")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, UnaryOpNode):
        print(f"{prefix}UnaryOp({node.op}):")
        print_ast(node.operand, indent + 1)
    elif isinstance(node, AssignNode):
        print(f"{prefix}Assign({node.name}):")
        print_ast(node.value, indent + 1)
    elif isinstance(node, PrintNode):
        print(f"{prefix}Print:")
        print_ast(node.expr, indent + 1)
    else:
        print(f"{prefix}Unknown: {node}")


if __name__ == "__main__":
    print("=" * 60)
    print("Analizador Sintáctico - Árbol de Sintaxis Abstracta (AST)")
    print("=" * 60)
    
    ejemplos = [
        "42;",
        "1 + 2 * 3;",
        "(1 + 2) * 3;",
        "x = 10;",
        "print(x + y);",
        "a > b and c < d;",
        "not x or y;",
    ]
    
    for codigo in ejemplos:
        print(f"\n{'─' * 40}")
        print(f"Código: {codigo}")
        print(f"{'─' * 40}")
        try:
            ast = parse(codigo)
            print_ast(ast)
        except ParseError as e:
            print(f"Error: {e}")
