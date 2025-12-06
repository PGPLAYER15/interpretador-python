import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

def lexer(text):
    line_num = 1
    line_start = 0

    token_specs = [
        ('NUMBER', r'\d+'),
        ('PRINT',  r'\bprint\b'),

        # operadores booleanos
        ('AND', r'\band\b'),
        ('OR', r'\bor\b'),
        ('NOT', r'\bnot\b'),

        ('ID',     r'[A-Za-z_]\w*'),

        # operadores logicos

        ("EQ", r'=='),
        ("NEQ", r'!='),
        ("LTE", r'<='),
        ("GTE", r'>='),
        ('LT', r'<'),
        ('GT', r'>'),

        #Operaciones aritmeticas y asignacion

        ('ASSIGN', r'='),
        ('PLUS',   r'\+'),
        ('MINUS',  r'-'),
        ('DIV', r'/'),
        ('MULT', r'\*'),

        # Delimitadores

        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('COMMA', r','),
        ('SEMI', r';'),

        ('NEWLINE', r'\n'),
        ('SKIP',   r'[ \t]+'),

    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            yield Token('NUMBER', value)
        elif kind == 'ID':
            yield Token('ID', value)
        elif kind == 'NEWLINE':
            yield Token('NEWLINE', value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value!r}')
        else:
            yield Token(kind, value)