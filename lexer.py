import ply.lex as lex

# Tokens
tokens = (
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LT', 'LE', 'EQ', 'GT', 'GE', 'NE',
    'IF', 'ELSE', 'FOR', 'WHILE', 'PRINT', 
    'SEMICOLON', 'COMMA', 'TYPE'
)

# Palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'print': 'PRINT',
    'int': 'TYPE',
    'float': 'TYPE',
    'bool': 'TYPE',
    'string': 'TYPE'
}


t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_LT = r'<'
t_LE = r'<='
t_EQ = r'=='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='

def reset_lineno(lexer):
    """Reinicia el contador de líneas a 1."""
    lexer.lineno = 1



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') 
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1] 
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'


def find_line(input_text, token_pos):
    """Encuentra el número de línea basado en los saltos de línea del texto."""
    lines = input_text[:token_pos].splitlines()
    return len(lines) 


def t_error(t):
    line_number = find_line(t.lexer.lexdata, t.lexpos)
    error_message = f"Error léxico: Caracter no reconocido '{t.value[0]}' en la línea {line_number}."
    raise SyntaxError(error_message)


lexer = lex.lex()
