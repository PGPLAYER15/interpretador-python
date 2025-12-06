import argparse
import sys
import unittest
from parser import (
    parse, Parser, ParseError,
    NumberNode, IdNode, BinOpNode, UnaryOpNode,
    AssignNode, PrintNode, ProgramNode, print_ast
)
from lexer import lexer


class ParserTest(unittest.TestCase):
    """Tests unitarios para el parser"""
    
    # ---------- Tests de expresiones aritméticas ----------
    
    def test_number(self):
        """Parsea un número simple"""
        ast = parse("42;")
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], NumberNode)
        self.assertEqual(ast.statements[0].value, 42)
    
    def test_addition(self):
        """Parsea una suma"""
        ast = parse("1 + 2;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, '+')
        self.assertEqual(stmt.left.value, 1)
        self.assertEqual(stmt.right.value, 2)
    
    def test_subtraction(self):
        """Parsea una resta"""
        ast = parse("5 - 3;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, '-')
    
    def test_multiplication(self):
        """Parsea una multiplicación"""
        ast = parse("4 * 5;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, '*')
    
    def test_division(self):
        """Parsea una división"""
        ast = parse("10 / 2;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, '/')
    
    def test_precedence_mult_add(self):
        """Verifica precedencia: multiplicación antes que suma"""
        # 1 + 2 * 3 debe parsearse como 1 + (2 * 3)
        ast = parse("1 + 2 * 3;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '+')
        self.assertEqual(stmt.left.value, 1)
        self.assertIsInstance(stmt.right, BinOpNode)
        self.assertEqual(stmt.right.op, '*')
    
    def test_parentheses(self):
        """Verifica que los paréntesis cambian la precedencia"""
        # (1 + 2) * 3 debe parsearse con la suma primero
        ast = parse("(1 + 2) * 3;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '*')
        self.assertIsInstance(stmt.left, BinOpNode)
        self.assertEqual(stmt.left.op, '+')
    
    def test_unary_minus(self):
        """Parsea negación unaria"""
        ast = parse("-5;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, UnaryOpNode)
        self.assertEqual(stmt.op, '-')
        self.assertEqual(stmt.operand.value, 5)
    
    # ---------- Tests de expresiones de comparación ----------
    
    def test_comparison_eq(self):
        """Parsea igualdad"""
        ast = parse("x == 5;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, '==')
    
    def test_comparison_neq(self):
        """Parsea desigualdad"""
        ast = parse("x != 5;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '!=')
    
    def test_comparison_lt(self):
        """Parsea menor que"""
        ast = parse("x < 5;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '<')
    
    def test_comparison_gt(self):
        """Parsea mayor que"""
        ast = parse("x > 5;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '>')
    
    def test_comparison_lte(self):
        """Parsea menor o igual"""
        ast = parse("x <= 5;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '<=')
    
    def test_comparison_gte(self):
        """Parsea mayor o igual"""
        ast = parse("x >= 5;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, '>=')
    
    # ---------- Tests de expresiones booleanas ----------
    
    def test_and(self):
        """Parsea operador and"""
        ast = parse("x and y;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, BinOpNode)
        self.assertEqual(stmt.op, 'and')
    
    def test_or(self):
        """Parsea operador or"""
        ast = parse("x or y;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, 'or')
    
    def test_not(self):
        """Parsea operador not"""
        ast = parse("not x;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, UnaryOpNode)
        self.assertEqual(stmt.op, 'not')
    
    def test_boolean_precedence(self):
        """Verifica precedencia: and antes que or"""
        # x or y and z debe parsearse como x or (y and z)
        ast = parse("x or y and z;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, 'or')
        self.assertIsInstance(stmt.right, BinOpNode)
        self.assertEqual(stmt.right.op, 'and')
    
    def test_not_precedence(self):
        """Verifica que not tiene mayor precedencia que and"""
        # not x and y debe parsearse como (not x) and y
        ast = parse("not x and y;")
        stmt = ast.statements[0]
        self.assertEqual(stmt.op, 'and')
        self.assertIsInstance(stmt.left, UnaryOpNode)
        self.assertEqual(stmt.left.op, 'not')
    
    # ---------- Tests de asignaciones ----------
    
    def test_assignment(self):
        """Parsea una asignación simple"""
        ast = parse("x = 42;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, AssignNode)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.value, NumberNode)
        self.assertEqual(stmt.value.value, 42)
    
    def test_assignment_expression(self):
        """Parsea asignación con expresión compleja"""
        ast = parse("result = 1 + 2 * 3;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, AssignNode)
        self.assertEqual(stmt.name, 'result')
        self.assertIsInstance(stmt.value, BinOpNode)
    
    # ---------- Tests de print ----------
    
    def test_print_number(self):
        """Parsea print con número"""
        ast = parse("print(123);")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, PrintNode)
        self.assertIsInstance(stmt.expr, NumberNode)
        self.assertEqual(stmt.expr.value, 123)
    
    def test_print_expression(self):
        """Parsea print con expresión"""
        ast = parse("print(1 + 2);")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.expr, BinOpNode)
    
    def test_print_variable(self):
        """Parsea print con variable"""
        ast = parse("print(x);")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.expr, IdNode)
        self.assertEqual(stmt.expr.name, 'x')
    
    # ---------- Tests de programas completos ----------
    
    def test_multiple_statements(self):
        """Parsea múltiples sentencias"""
        code = """
        x = 10;
        y = 20;
        print(x + y);
        """
        ast = parse(code)
        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[0], AssignNode)
        self.assertIsInstance(ast.statements[1], AssignNode)
        self.assertIsInstance(ast.statements[2], PrintNode)
    
    def test_complex_expression(self):
        """Parsea expresión compleja con múltiples operadores"""
        ast = parse("(a + b) * c >= d and not e;")
        stmt = ast.statements[0]
        # (a + b) * c >= d and not e
        # Debe ser: ((((a + b) * c) >= d) and (not e))
        self.assertEqual(stmt.op, 'and')
    
    # ---------- Tests de errores ----------
    
    def test_missing_semicolon(self):
        """Error: falta punto y coma"""
        with self.assertRaises(ParseError):
            parse("x = 5")
    
    def test_missing_rparen(self):
        """Error: falta paréntesis de cierre"""
        with self.assertRaises(ParseError):
            parse("print(x;")
    
    def test_unexpected_token(self):
        """Error: token inesperado"""
        with self.assertRaises(ParseError):
            parse("+ 5;")


def manual_test():
    """Demo interactivo del parser"""
    print("=" * 60)
    print("Demo del Analizador Sintáctico")
    print("=" * 60)
    
    examples = [
        "42;",
        "1 + 2 * 3;",
        "(1 + 2) * 3;",
        "-5;",
        "x = 10;",
        "print(x + y);",
        "a > b and c < d;",
        "not x or y;",
        """
        x = 10;
        y = 20;
        z = x + y * 2;
        print(z);
        """,
    ]
    
    for code in examples:
        print(f"\n{'─' * 40}")
        print(f"Código: {code.strip()[:50]}{'...' if len(code.strip()) > 50 else ''}")
        print(f"{'─' * 40}")
        try:
            ast = parse(code)
            print_ast(ast)
        except ParseError as e:
            print(f"Error de sintaxis: {e}")
    
    print(f"\n{'=' * 60}")
    print("Parser OK - Todos los ejemplos procesados")
    print("=" * 60)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Run parser tests or manual demo")
    arg_parser.add_argument('--manual', action='store_true', help='Run interactive demo')
    args = arg_parser.parse_args()
    
    if args.manual:
        manual_test()
    else:
        unittest.main(argv=[sys.argv[0]])
