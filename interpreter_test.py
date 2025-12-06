import argparse
import sys
import unittest
from io import StringIO
from interpreter import interpret, run, Interpreter, RuntimeError
from parser import parse
class InterpreterTest(unittest.TestCase):
    """Tests unitarios para el intérprete"""
    
    # ---------- Tests de expresiones aritméticas ----------
    
    def test_number(self):
        """Evalúa un número"""
        result = run("42;")
        self.assertEqual(result, 42)
    
    def test_addition(self):
        """Evalúa una suma"""
        result = run("1 + 2;")
        self.assertEqual(result, 3)
    
    def test_subtraction(self):
        """Evalúa una resta"""
        result = run("10 - 4;")
        self.assertEqual(result, 6)
    
    def test_multiplication(self):
        """Evalúa una multiplicación"""
        result = run("6 * 7;")
        self.assertEqual(result, 42)
    
    def test_division(self):
        """Evalúa una división entera"""
        result = run("15 / 4;")
        self.assertEqual(result, 3)  # División entera
    
    def test_complex_arithmetic(self):
        """Evalúa expresión aritmética compleja"""
        result = run("2 + 3 * 4;")  # 2 + 12 = 14
        self.assertEqual(result, 14)
    
    def test_parentheses(self):
        """Evalúa expresión con paréntesis"""
        result = run("(2 + 3) * 4;")  # 5 * 4 = 20
        self.assertEqual(result, 20)
    
    def test_unary_minus(self):
        """Evalúa negación unaria"""
        result = run("-5;")
        self.assertEqual(result, -5)
    
    def test_double_negation(self):
        """Evalúa doble negación"""
        result = run("--5;")
        self.assertEqual(result, 5)
    
    def test_division_by_zero(self):
        """Error: división por cero"""
        with self.assertRaises(RuntimeError):
            run("10 / 0;")
    
    # ---------- Tests de comparaciones ----------
    
    def test_equal_true(self):
        """Evalúa igualdad verdadera"""
        result = run("5 == 5;")
        self.assertEqual(result, True)
    
    def test_equal_false(self):
        """Evalúa igualdad falsa"""
        result = run("5 == 6;")
        self.assertEqual(result, False)
    
    def test_not_equal(self):
        """Evalúa desigualdad"""
        result = run("5 != 6;")
        self.assertEqual(result, True)
    
    def test_less_than(self):
        """Evalúa menor que"""
        result = run("3 < 5;")
        self.assertEqual(result, True)
    
    def test_greater_than(self):
        """Evalúa mayor que"""
        result = run("10 > 5;")
        self.assertEqual(result, True)
    
    def test_less_equal(self):
        """Evalúa menor o igual"""
        result = run("5 <= 5;")
        self.assertEqual(result, True)
    
    def test_greater_equal(self):
        """Evalúa mayor o igual"""
        result = run("6 >= 5;")
        self.assertEqual(result, True)
    
    # ---------- Tests de operaciones booleanas ----------
    
    def test_and_true(self):
        """Evalúa and verdadero"""
        result = run("1 and 2;")
        self.assertEqual(result, 2)
    
    def test_and_false(self):
        """Evalúa and falso"""
        result = run("0 and 2;")
        self.assertEqual(result, 0)
    def test_or_true(self):
        """Evalúa or - primer valor verdadero"""
        result = run("1 or 2;")
        self.assertEqual(result, 1)
    
    def test_or_false(self):
        """Evalúa or - ningún valor verdadero"""
        result = run("0 or 0;")
        self.assertEqual(result, 0)
    
    def test_not_true(self):
        """Evalúa not de valor verdadero"""
        result = run("not 1;")
        self.assertEqual(result, False)
    
    def test_not_false(self):
        """Evalúa not de valor falso"""
        result = run("not 0;")
        self.assertEqual(result, True)
    
    def test_complex_boolean(self):
        """Evalúa expresión booleana compleja"""
        result = run("1 > 0 and 2 < 3;")
        self.assertEqual(result, True)
    
    # ---------- Tests de variables ----------
    
    def test_assignment(self):
        """Prueba asignación de variable"""
        interp = interpret("x = 42;")
        self.assertEqual(interp.env['x'], 42)
    
    def test_variable_use(self):
        """Prueba uso de variable"""
        interp = interpret("x = 10; y = x + 5;")
        self.assertEqual(interp.env['x'], 10)
        self.assertEqual(interp.env['y'], 15)
    
    def test_variable_reassignment(self):
        """Prueba reasignación de variable"""
        interp = interpret("x = 10; x = 20;")
        self.assertEqual(interp.env['x'], 20)
    
    def test_undefined_variable(self):
        """Error: variable no definida"""
        with self.assertRaises(RuntimeError):
            run("x + 5;")
    
    def test_initial_env(self):
        """Prueba entorno inicial"""
        interp = interpret("y = x + 10;", env={'x': 5})
        self.assertEqual(interp.env['y'], 15)
    
    # ---------- Tests de print ----------
    
    def test_print_number(self):
        """Prueba print de número"""
        interp = interpret("print(42);")
        self.assertEqual(interp.output, [42])
    
    def test_print_expression(self):
        """Prueba print de expresión"""
        interp = interpret("print(1 + 2 * 3);")
        self.assertEqual(interp.output, [7])
    
    def test_print_variable(self):
        """Prueba print de variable"""
        interp = interpret("x = 100; print(x);")
        self.assertEqual(interp.output, [100])
    
    def test_multiple_prints(self):
        """Prueba múltiples prints"""
        interp = interpret("print(1); print(2); print(3);")
        self.assertEqual(interp.output, [1, 2, 3])
    
    # ---------- Tests de programas completos ----------
    
    def test_fibonacci_style(self):
        """Programa estilo Fibonacci (sin loops)"""
        code = """
        a = 0;
        b = 1;
        c = a + b;
        d = b + c;
        e = c + d;
        print(e);
        """
        interp = interpret(code)
        # a=0, b=1, c=1, d=2, e=3
        self.assertEqual(interp.output, [3])
    
    def test_complex_program(self):
        """Programa con varias operaciones"""
        code = """
        x = 10;
        y = 20;
        suma = x + y;
        producto = x * y;
        mayor = x > y;
        print(suma);
        print(producto);
        print(mayor);
        """
        interp = interpret(code)
        self.assertEqual(interp.output, [30, 200, False])
    
    def test_conditional_expression(self):
        """Expresión condicional con and/or"""
        code = """
        x = 5;
        resultado = x > 0 and x < 10;
        print(resultado);
        """
        interp = interpret(code)
        self.assertEqual(interp.output, [True])


def manual_test():
    """Demo interactivo del intérprete"""
    print("=" * 60)
    print("Demo del Intérprete")
    print("=" * 60)
    
    examples = [
        ("Aritmética básica", "2 + 3 * 4;"),
        ("Paréntesis", "(2 + 3) * 4;"),
        ("Negación", "-5 + 10;"),
        ("Comparación", "10 > 5;"),
        ("Operadores booleanos", "1 and 0 or 1;"),
        ("Variables", "x = 10; y = 20; x + y;"),
        ("Print", "x = 42; print(x);"),
        ("Programa completo", """
            a = 5;
            b = 10;
            c = a + b;
            print(c);
            d = c > 10;
            print(d);
        """),
    ]
    
    for name, code in examples:
        print(f"\n{'─' * 40}")
        print(f"📝 {name}")
        print(f"   Código: {code.strip()[:40]}{'...' if len(code.strip()) > 40 else ''}")
        print(f"{'─' * 40}")
        
        try:
            interp = interpret(code)
            if interp.output:
                print(f"   Salida: {interp.output}")
            print(f"   Variables: {interp.env}")
        except Exception as e:
            print(f"    Error: {e}")
    
    print(f"\n{'=' * 60}")
    print(" Intérprete OK - Todos los ejemplos ejecutados")
    print("=" * 60)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Run interpreter tests or manual demo")
    arg_parser.add_argument('--manual', action='store_true', help='Run interactive demo')
    args = arg_parser.parse_args()
    
    if args.manual:
        manual_test()
    else:
        unittest.main(argv=[sys.argv[0]])
