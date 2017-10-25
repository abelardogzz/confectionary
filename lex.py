
#-----------
# lex.py 
# ----------

import ply.lex as lex

# Palabras reservadas
reserved = {
    'if' : 'IF',
    'else': 'ELSE',
    'recipe': 'RCP',
    'repeat': 'REPEAT',
    'program': 'PROGRAM',
    'show': 'SHOW',
    'read': 'READ',
    'var' : 'VAR',
  	'drawCupcake': 'DRWCPCK',
    'drawCane': 'DRWCN',
    'drawChocoBar': 'DRWCHBR',
    'ration': 'RATION',
  	'flavor': 'FLVR',
    'confectionary': 'CNFCTNR',
    'return': 'RETURN',
    'void': 'VOID',
    #TYPES
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'string' : 'STRING',
    'yes': 'YES',
    'no': 'NO',
    'make':'MAKE',
    #'shelf': 'ARRAY',
    #'grid': 'MATRIX',
}

# Tokens 
tokens = ['ID', 'CTEINT', 'CTEFLOAT', 'CTESTRING', 'GET','LET', 'EQUAL', 'DIFF', 'AND', 'OR',] + list(reserved.values())

#One digit symbols
literals = ['*', '/', '+', '-', '>', '<', '=', '.', ',', ':', ';', '(', ')', '{', '}', '[', ']']


#Multi-Digit symbols
#t_MENORMAYOR = "<>"
t_GET = ">="
t_LET = "<="
t_EQUAL = "=="
t_DIFF = "!="
t_AND = "&&"
t_OR = "\|\|"

#REGEXs
def t_ID(t):
    r'[a-zA-Z].[a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID') 
    return t

def t_CTEFLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEINT(t):
    r'[0-9]+|-[0-9]+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'[\"a-zA-Z0-9| |!]+\"'
    t.type = reserved.get(t.value, 'CTESTRING')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore tabs or spaces
t_ignore  = ' \t'

#Error handling
def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Lexing
lex.lex()

if __name__ == '__main__':
    lex.runmain()

