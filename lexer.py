import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

def lexer(text):
    token_spec = [
        ('NUMBER', r'\d+'),
        ('PRINT',  r'print'),
        ('ID',     r'[A-Za-z_]\w*'),
        ('ASSIGN', r'='),
        ('PLUS',   r'\+'),
        ('MINUS',  r'-'),
        ('NEWLINE', r'\n'),
        ('SKIP',   r'[ \t]+'),
        ('DIV',r'/'),
        ('MULT',r'*'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        yield Token(kind, value)