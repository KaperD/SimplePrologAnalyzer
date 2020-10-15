from parsec import *
import sys
import threading
import argparse

# Prolog = Module TypesDef Relations

# Module = module Identifier . | epsilon

# TypesDef  = TypeDef . | TypeDef . TypesDef
# TypeDef   = type Identifier Type
# Type = AtomOrVarType | BracketsType
# AtomOrVarType = Atom | Var | Atom -> Type | Var -> Type
# BracketsType = (Type) | (Type) -> Type

# Relations = Relation . | Relation . Relations
# Relation = Atom :- Expression | Atom

# Expression = Cap ; Expression | Cap

# Cap = Atom , Cap | (Expression) , Cap | Atom | (Expression)

# Atom = Identifier AtomSuffix | Identifier
# AtomSuffix = Elem | Elem AtomSuffix
# Elem = List | Var | Identifier | (Atom) | (Elem)

# List = [] | [ListBody] | [ListElem '|' Var]
# ListBody = ListElem , ListBody | ListElem
# ListElem = Atom | Var | List

# Identifier = [a-z_][a-zA-Z_0-9]* but not 'module' or 'type'
# Var = [A-Z][a-zA-Z_0-9]*


# ----------------------Utility----------------------

@generate
def Empty():
    yield string('')
    return None

@generate
def EOF():
    yield eof()
    return None
    
spaces = regex(r'\s*', re.MULTILINE)

# ----------------------Terminals----------------------

@generate
def Var():
    var = yield spaces >> regex(r'[A-Z][a-zA-Z_0-9]*') << spaces
    return f'Var {var}'

@generate
def Identifier():
    id = yield spaces >> regex(r'(?!type\b|module\b)[a-z_][a-zA-Z_0-9]*') << spaces
    return id

@generate
def Dot():
    yield spaces >> string('.') << spaces
    return None

# ----------------------Module----------------------

@generate
def Module():
    yield spaces >> regex(r'module\b') << spaces # regex, а не string, потому что string прочитае первые буквы, даже если слово moduJJJ, а мне это не нужно
    name = yield Identifier
    yield Dot
    return f'Module = {name}'

# ----------------------Types----------------------

@generate
def AtomOrVarType(): # тип начинается с атома или переменной
    atom = yield Atom ^ Var
    arrow = yield spaces >> string('->') << spaces ^ Empty
    if arrow:
        type = yield Type
        return f'Type ({atom}) ({type})'
    return atom

@generate
def BracketsType(): # начинается со скобок
    yield spaces >> string('(') << spaces
    type = yield Type
    yield spaces >> string(')') << spaces
    arrow = yield spaces >> string('->') << spaces ^ Empty
    if arrow:
        type2 = yield Type
        return f'Type ({type}) ({type2})'
    return type

@generate
def Type():
    type = yield AtomOrVarType ^ BracketsType
    return type

@generate
def TypeDef():
    yield spaces >> regex(r'type\b') << spaces # если есть слово type, то мы точно хотим корректный тип
    typeName = yield Identifier
    type = yield Type
    return f'Typedef {typeName} = {type}'
    

@generate
def TypesDef():
    type = yield TypeDef
    yield Dot
    otherTypes = yield spaces >> TypesDef | Empty
    if otherTypes:
        return f'{type}\n{otherTypes}'
    return type

# ----------------------Relations----------------------

@generate
def AtomCap():
    atom = yield spaces >> Atom << spaces
    comma = yield string(',') | Empty
    if comma:
        cap = yield spaces >> Cap << spaces
        return f'"," ({atom}) ({cap})'
    return atom

@generate
def BracketsCap():
    yield spaces >> string('(') << spaces
    expression = yield Expression
    yield spaces >> string(')') << spaces
    comma = yield string(',') | Empty
    if comma:
        cap = yield spaces >> Cap << spaces
        return f'"," ({expression}) ({cap})'
    return expression

@generate
def Cap():
    cap = yield AtomCap | BracketsCap
    return cap

@generate
def Expression():
    cap = yield spaces >> Cap << spaces
    column = yield string(';') | Empty
    if column:
        expression = yield Expression
        return f'";" ({cap}) ({expression})'
    return cap

@generate
def Relation():
    atom = yield spaces >> Atom << spaces
    operator = yield string(':-') | Empty
    if operator:
        expression = yield Expression
        return f'Relation = ":-" ({atom}) ({expression})'
    return "Relation = " + atom

@generate
def Relations():
    relation = yield Relation
    yield Dot
    otherRelations = yield EOF ^ Relations
    if otherRelations:
        return f'{relation}\n{otherRelations}'
    return relation

# ----------------------List----------------------

@generate
def ListElem():
    elem = yield Atom ^ Var ^ List
    return elem

@generate
def ElementsList():
    comma = yield spaces >> string(',') << spaces | ListEnd
    if comma:
        elem = yield ListElem
        tail = yield ElementsList
        if tail:
            return f'{elem}, {tail}'
        return f'{elem}'
    return None

@generate
def HeadTailList():
    yield spaces >> string('|') << spaces
    tail = yield Var
    yield ListEnd
    return f'| {tail}'

@generate
def ListEnd():
    yield spaces >> string(']') << spaces
    return None

@generate
def List():
    yield spaces >> string('[') << spaces
    elem = yield ListEnd ^ ListElem
    if elem:
        listBody = yield  HeadTailList | ElementsList
        if listBody:
            return f'List [{elem} {listBody}]'
        return f'List [{elem}]'
    return 'EmptyList'

# ----------------------Atom----------------------

@generate
def BracketsAtom():
    yield spaces >> string('(') << spaces
    atom = yield Atom
    yield spaces >> string(')') << spaces
    return f'{atom}'

@generate
def BracketsElem():
    yield spaces >> string('(') << spaces
    elem = yield Elem
    yield spaces >> string(')') << spaces
    return f'{elem}'

@generate
def Elem():
    elem = yield List | Var | Identifier | BracketsAtom ^ BracketsElem
    return elem

@generate
def AtomSuffix():
    elem = yield spaces >> Elem << spaces
    suf = yield AtomSuffix | Empty
    if suf:
        return elem + ' ' + suf
    return elem
        
@generate
def Atom():
    id = yield Identifier
    suf = yield AtomSuffix | Empty
    if suf:
        return f'Atom ({id} {suf})'
    return f'Atom {id}'

# ----------------------Prolog----------------------

@generate
def Prolog(): 
    yield spaces
    module = yield Module | Empty
    types = yield TypesDef | Empty
    relations = yield Relations | EOF
    result = ''
    if module:
        result += module + '\n'
    if types:
        result += types + '\n'
    if relations:
        result += relations
    return result

class ParseResult:
    def __init__(self, str, b):
        self.str = str
        self.success = b
    def __bool__(self):
        return self.success
    def __str__(self):
        return self.str

def parseText(text, parser):
    try:
        return ParseResult(parser.parse(text), True)
    except ParseError as ex:
        message = 'Syntax error:\n' + str(ex) + '\n'
        line, position = ex.loc_info(text, ex.index)
        message += text.split('\n')[line] + '\n'
        message += '-' * position + '^'
        # print(message)
        return ParseResult(message, False)


def main():
    args = argparse.ArgumentParser(description='Parse Prolog.')
    args.add_argument('--atom', action='store_const', const=Atom, dest = 'parser')
    args.add_argument('--typeexpr', action='store_const', const=Type, dest = 'parser')
    args.add_argument('--type', action='store_const', const=TypeDef, dest = 'parser')
    args.add_argument('--module', action='store_const', const=Module, dest = 'parser')
    args.add_argument('--relation', action='store_const', const=Relation, dest = 'parser')
    args.add_argument('--list', action='store_const', const=List, dest = 'parser')
    args.add_argument('--prog', action='store_const', const=Prolog, dest = 'parser')
    args.add_argument('file', type=str)

    r = args.parse_args()


    readFile = open(r.file, 'r')
    writeFile = open(r.file + '.out', 'w')

    parser = Prolog
    if r.parser:
        parser = r.parser

    result = parseText(readFile.read(), parser) 

    if result:
        writeFile.write(str(result))
        writeFile.write('\n')
    else:
        print(str(result))
    

    writeFile.close()
    readFile.close()

if __name__ == "__main__":
    main()
    # sys.setrecursionlimit(100000)
    # threading.stack_size(0x2000000)
    # t = threading.Thread(target=main)
    # t.start()
    # t.join()
