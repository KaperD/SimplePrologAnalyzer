from lexer import tokens
from lexer import lexer
import ply.yacc as yacc
import sys

# Prolog = Relation . Prolog | empty
# Relation = Atom :- Expression | Atom
# Expression = Cap ; Expression | Cap
# Cap = Atom , Cap | (Expression) , Cap | Atom | (Expression)
# Atom = Identifier AtomSuffix | Identifier
# AtomSuffix = Atom | CloseAtom | CloseAtom AtomSuffix
# CloseAtom = (Atom) | (CloseAtom)
# Identifier = [a-zA-Z_][a-zA-Z_0-9]*

class Node:
    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{self.type} ({str(self.left)}) ({str(self.right)})'

def p_prolog(p):
    '''prolog : 
              | relation DOT prolog'''
    if len(p) > 1:
        p[0] = Node("'.'", p[1], p[3])
    else:
        p[0] = ''

def p_relation(p):
    '''relation : atom CORKSCREW expression
                | atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("':-'", p[1], p[3])

def p_expression(p):
    '''expression : cap CUP expression 
                  | cap'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("';'", p[1], p[3])

def p_cap(p):
    '''cap : atom CAP cap 
           | closeExpr CAP cap 
           | atom 
           | closeExpr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("','", p[1], p[3])

def p_closeExpr(p):
    'closeExpr : OPEN expression CLOSE'
    p[0] = p[2]

def p_atom(p):
    '''atom : IDENTIFIER
            | IDENTIFIER atomSuffix'''
    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]
    else:
        p[0] = p[1]

def p_atomSuffix(p):
    '''atomSuffix : atom
                  | closeAtom
                  | closeAtom atomSuffix'''
    if len(p) == 3:
        p[0] = p[1] + ' ' + p[2]
    else:
        p[0] = p[1]

def p_closeAtom_simple(p):
    'closeAtom : OPEN atom CLOSE'
    p[0] = '{' + p[2] + '}'

def p_closeAtom_recursive(p):
    'closeAtom : OPEN closeAtom CLOSE'
    p[0] = p[2]

def find_column(input, token): # взята с сайта ply
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1

errorMessage = ''

def p_error(p): 
    if p:
        column = find_column(lexer.lexdata, p)
        global errorMessage
        errorMessage += f'Line {p.lineno}, column {column}: Syntax error\n'
        errorMessage += lexer.lexdata.split('\n')[p.lineno - 1] + '\n'
        errorMessage += '-' * (column - 1) + '^\n'
    else:
        errorMessage += 'Syntax error: unexpected EOF\n'
    global success
    success = False
    while parser.token():
        pass

parser = yacc.yacc()
success = True

def parseText(text):
    global success
    success = True
    result = parser.parse(text) 
    if success:
        return result
    else:
        return None

if __name__ == '__main__':
    readFile = open(sys.argv[1], 'r')
    writeFile = open(sys.argv[1] + '.out', 'w')

    result = parseText(readFile.read()) 

    if result:
        # print(str(result))
        writeFile.write(str(result))
        writeFile.write('\n')
    else:
        print(errorMessage, end='')

    writeFile.close()
    readFile.close()