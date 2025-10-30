import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

def lexer(text):
    line_num = 1
    line_start = 0

    token_spec = [
        ('NUMBER', r'\d+'),
        ('PRINT',  r'\bprint\b'),
        ('ID',     r'[A-Za-z_]\w*'),

        # operadores booleanos
        ('AND', r'\band\b'),
        ('OR', r'\bor\b'),
        ('NOT', r'\bnot\b'),

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
        ('MULT', r'*'),

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
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)

    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()

        if kind in ('SKIP', 'COMMENT'):
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f'Carácter inesperado: {value}')
        if kind == 'KEYWORD':
            kind = value.upper()  # print -> PRINT

        yield Token(kind, value)