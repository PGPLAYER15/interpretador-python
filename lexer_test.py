import argparse
import sys
import unittest
from lexer import lexer

class LexerTest(unittest.TestCase):
    def test_token_types_and_values(self):
        sample = (
            "print and or not == != <= >= < > = + - * / ( ) { } , ;\n"
            "123 abc\n"
        )
        toks = list(lexer(sample))
        actual_types = [t.type for t in toks]

        expected_types = [
            'PRINT','AND','OR','NOT',
            'EQ','NEQ','LTE','GTE','LT','GT',
            'ASSIGN','PLUS','MINUS','MULT','DIV',
            'LPAREN','RPAREN','LBRACE','RBRACE','COMMA','SEMI',
            'NEWLINE','NUMBER','ID','NEWLINE'
        ]

        self.assertEqual(
            actual_types, expected_types,
            f"Unexpected token types.\nExpected: {expected_types}\nActual:   {actual_types}"
        )

        values = {t.type: t.value for t in toks}
        self.assertIn('NUMBER', values)
        self.assertIn('ID', values)
        self.assertEqual(values['NUMBER'], '123')
        self.assertEqual(values['ID'], 'abc')

def manual_test():
    text = "print(123);\nfoo = 42 and not 0;"
    tokens = list(lexer(text))
    for t in tokens:
        print(f"{t.type}: {t.value!r}")

    assert tokens and tokens[0].type == "PRINT", "Lexer no devolvió PRINT como primer token"
    print("Lexer OK")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run lexer tests or manual token dump")
    parser.add_argument('--manual', action='store_true', help='Print tokens and run a quick manual check')
    args = parser.parse_args()

    if args.manual:
        manual_test()
    else:
        unittest.main(argv=[sys.argv[0]])
