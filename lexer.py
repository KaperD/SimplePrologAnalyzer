import ply.lex as lex
import sys

tokens = [
    'IDENTIFIER',
    'DOT',
    'CORKSCREW',
    'CUP',
    'CAP',
    'OPEN',
    'CLOSE'
]

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_DOT = r'\.'
t_CORKSCREW = r':-'
t_CUP = r';'
t_CAP = r','
t_OPEN = r'\('
t_CLOSE = r'\)'

t_ignore = ' \t'

def t_newline(t): 
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# if __name__ == "__main__":
#     readFile = open(sys.argv[1], 'r')
#     writeFile = open(sys.argv[1] + '.out', 'w')

#     lexer = lex.lex()

#     lexer.input(readFile.read())

#     while True: 
#         tok = lexer.token() 
#         if not tok: 
#             break
#         writeFile.write(str(tok)[9:-1])
#         writeFile.write('\n')