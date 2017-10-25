import ply.yacc as yacc
import lex
import cubo_semantico as CuboSem
from lex import tokens


DEBUG = True


#from enum import Enum
#class Types(Enum):
#    INT = 0
#    FLOAT = 1
#    STRING = 2
#    BOOL = 3
#    INT[] = 4
#   FLOAT[] = 5
#   STRING[] = 6
#   INT[][] = 7
#   FLOAT[][] = 8
#   STRING[][] = 9
#    VOID = 10
#    ERROR = 99


#DiModules structure
# ! <- opcional
#key[nombre, returnValue,!numeroDeParametros, lista de tipos de los parametros, cantidad de variables totales contando parametros, keys de las variables que eventualmente ser�n direcciones de memoria]



#DictionarioVariables
DiVars = dict()
DiModules = dict()
DiConst = dict()
incrementalNumber = 0;
incrementalNumberFun = 0;
incrementalNumberConst = 0;
availTemp = 0;
auxCont = 0;
GlobalID = "varId-";
GlobalConst = "Const-"
context = "global"
arrayContent = list()
matrixContent = list()

#Stacks
#POper - operandos
POper = list()
#PilaO
PilaO = list()
#JumpStack
JumpStack = list()
#TypeStack 
TypeStack = list()

#QUADLIST
quads = list()



def printDic1(p):
    for x in p:
        print(x,p[x])
def printDic(p):
    z=0
    for z,x in enumerate(p):
        print( z, x )


# GRAMMAR
#program : PROGRAM ID ":" globals main
def p_programdef(p):
    '''programdef : PROGRAM ID ":" globals main'''
    print("Program Approved!");
    printDic1(DiVars)
    printDic1(DiModules)
    print("pilaO = ",PilaO)
    print("TypeStack = ",TypeStack)
    print("POper = ",POper)
    print("Quads = ")
    printDic(quads)
    pass

def p_main(p):
    '''main : CNFCTNR seen_CNFCTNR "(" ")" blocks'''
    pass
    

def p_seen_CNFCTNR(p):
    '''seen_CNFCTNR :'''
    global context
    context = "confectionary"
    #print("context: " + context)
    pass

def p_repeatdef(p):
    '''repeatdef : REPEAT seen_repeat "(" expression seen_exp_repeat ")" "{" statement "}" ";" seen_repeat_end'''
    #print("main");
    pass

def p_make_repeat(p):
    '''make_repeat : MAKE seen_repeat "{" statement "}" REPEAT "(" expression seen_exp_repeat_make ")" ";"'''
    #print("main");
    pass

def p_seen_exp_repeat_make(p):
	'''seen_exp_repeat_make :'''
	global PilaO
	global POper
	global quads
	global JumpStack
	print(TypeStack)
	result_Type = TypeStack.pop()

	if result_Type != 3:
		print("No hay baile con el se�or")
	else:
		returnTo = JumpStack.pop()
		result = PilaO.pop()
		quad = ["GotoV",result,"",returnTo ]
		quads = quads + [quad]
	pass

def p_seen_repeat(p):
    '''seen_repeat : '''
    global JumpStack
    global quads
    JumpStack = JumpStack + [len(quads)]
    pass

def p_seen_exp_repeat(p):
    '''seen_exp_repeat : '''
    global PilaO
    global POper
    global quads
    global JumpStack
    print(TypeStack)
    result_Type = TypeStack.pop()

    if result_Type != 3:
        print("No hay baile con el se�or")
    else:
        result = PilaO.pop()
        quad = ["GotoF",result,"","_____" ]
        quads = quads + [quad]
        JumpStack = JumpStack + [len(quads)-1]

    pass

def p_seen_repeat_end(p):
    '''seen_repeat_end :'''
    global PilaO
    global POper
    global quads
    global JumpStack
    end = JumpStack.pop()
    ret = JumpStack.pop()
    quad = ["GOTO", ret,"","____"]
    quads = quads + [quad]
    FILL(end,len(quads))

    pass

#def p_addsubs(p):
#  '''addsubs : "+"
#  | "-" '''
  #print("addsubs");
#  pass 

def p_globals(p):
    '''globals : var recipedef globals
    | empty '''
    #print( "GLOBALS")
    pass

def p_recipedef(p):
    '''recipedef : RCP brecipeaux "{" var statement seen_all_recipe_vars RETURN "(" recipereturn ")" ";" "}"
  | RCP VOID ID seen_recipe_name "(" brecipe seen_parameters ")" "{" var statement seen_all_recipe_vars "}" '''

    #print("recipe");
    pass

def p_brecipeaux(p):
  '''brecipeaux : type ID seen_recipe_name "(" brecipe seen_parameters ")"'''  
  #print("brecipeaux");
  pass

def p_seen_all_recipe_vars(p):
  '''seen_all_recipe_vars :'''
  global incrementalNumberFun
  global context
  var_keys = []
  auxCont = 0
  #print(" p[-4] -",  p[-4])
  for k, v in DiVars.items():
    if context in v:
      #print("!!!!!!!!!!!!-",k)
      var_keys = var_keys + [k]
      auxCont = auxCont + 1
  index = str(incrementalNumberFun-1)
  DiModules["FunId-"+index] = DiModules["FunId-"+index] + [auxCont] + [var_keys]
  pass

def p_seen_parameters(p):
  '''seen_parameters :'''
  global incrementalNumberFun
  parameters_types = []
  auxCont = 0
  #print(" p[-4] -",  p[-4])
  for k, v in DiVars.items():
    if p[-4] in v:
      #print("!!!!!!!!!!!!-",k)
      parameters_types = parameters_types + [DiVars[k][2]]
      auxCont = auxCont + 1
  index = str(incrementalNumberFun-1)
  DiModules["FunId-"+index] = DiModules["FunId-"+index] + [auxCont] + [parameters_types]
  pass

def p_seen_recipe_name(p):
    '''seen_recipe_name :'''
    global context
    context = p[-1]

    #DANGERZONE
    global incrementalNumberFun
    global auxCont #PARAMCOUNTER

    addToDict = True
    for k, v in DiModules.items():
      if p[-1] == v or isinstance(v, list) and p[-1] in v:
        funName = DiModules[k][0]
        if funName == p[-1]:
            addToDict = False 
            repeated_fun_error(p[-1])

    if addToDict:
      aux = "FunId-" + str(incrementalNumberFun)
      typeNumber = type_to_typeNumber(p[-2])
      DiModules[aux]=[p[-1],typeNumber]
      incrementalNumberFun = incrementalNumberFun + 1

    #ENDDANGERZONE



    #print("recipe context: "+ context)
    pass

def p_brecipe(p):
  '''brecipe : empty
  | type ID bbrecipe'''
  global context
  global incrementalNumber
  if p[1] != "empty": 

      addToDict = True
      for k, v in DiVars.items():
          if p[3] == v or isinstance(v, list) and p[3] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[3])

      if addToDict == True:
          aux = GlobalID + str(incrementalNumber)
          typeNumber = type_to_typeNumber(p[1])
          DiVars[aux]=[p[2],0,typeNumber, context]
          incrementalNumber = incrementalNumber + 1
  #print("brecipe");
  pass

def p_bbrecipe(p):
  '''bbrecipe : empty
  | "," type ID bbrecipe
  | "," type_array ID bbrecipe
  | "," type_matrix ID bbrecipe'''
  global context
  global incrementalNumber
  if p[1] != "empty":

      addToDict = True
      for k, v in DiVars.items():
          if p[3] == v or isinstance(v, list) and p[3] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[3])

      if addToDict == True:
          aux = GlobalID + str(incrementalNumber)
          typeNumber = type_to_typeNumber(p[2])
          DiVars[aux]=[p[3],0,typeNumber, context]
          incrementalNumber = incrementalNumber + 1
  #print("bbrecipe");
  pass


def p_type_array(p):
    '''type_array : type "[" "]" '''
    p[0] = p[1] + "[]"
    pass

def p_type_matrix(p):
    '''type_matrix : type "[" "]" "[" "]" '''
    p[0] = p[1] + "[][]"
    pass


def p_recipereturn(p):
  '''recipereturn : ctevar
  | ID'''
  #print("recipereturn");
  pass

def p_blocks(p):
    '''blocks : "{" var statement "}" '''
    #print("    -----    blocks");
    pass    


def p_statement(p):
    '''statement : ration statement
  | flavor statement
  | funccall statement
  | drawing statement
  | read statement
  | write statement
  | assignment statement 
    | condition statement
    | repeatdef statement
    | make_repeat statement 
    | empty '''
    #print("statment")
    pass

#-----------------------------#
#------Special Functions------#
def p_ration(p):
    '''ration : RATION "(" exp seen_pn_ratio ")" ";" '''
    #print("Ration");
    pass

def p_seen_pn_ratio(p):
    '''seen_pn_ratio : '''
    global PilaO
    global TypeStack
    global availTemp
    global quads

    result = PilaO.pop()
    result_type = TypeStack.pop()
    if result_type == 0 or result_type == 1:
        dir = "t" + str(availTemp)
        availTemp = availTemp + 1
        quad = ["ration",result,"--",dir]
        quads = quads + [quad]
    else:
        print("Type Mis-Match NO HAY BAILE CON EL SE�OR")
        exit(0)
    pass

def p_flavor(p):
    '''flavor : FLVR "(" exp "," seen_pn_flavor exp "," seen_pn_flavor exp seen_pn_flavor ")" ";" '''
    #print("flavor");
    pass

def p_seen_pn_flavor(p):
    '''seen_pn_flavor : '''
    global TypeStack
    global POper
    global PilaO
    global quads
    global availTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        result = "t" + str(availTemp)
        availTemp = availTemp + 1
        quad = [ "flavor", left_operand, "--", result]
        quads = quads + [quad]
    else:
        print("---Type mis-match, no hay baile flavor")
        exit(0)
    pass

def p_var(p):
    '''var : vars 
  | shelf
  | grid
  | empty '''
    #print("var");
    pass

def p_vars(p):
    '''vars : VAR type ID "=" ctevar ";" var  
    | empty'''
    #'''vars : VAR TIPO ID "=" VAL ";" '''
    #print("vars",p[2],p[3]);
    x = type_to_programType(p[5])
    print ("x ! -" , x)
    if p[2] != x:
        print("Type mismatch! in ", p[5])
        exit(0)
    global context
    global incrementalNumber

 
    addToDict = True
    for k, v in DiVars.items():
          if p[3] == v or isinstance(v, list) and p[3] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[3])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        typeNumber = type_to_typeNumber(p[2])
        DiVars[aux]=[p[3],p[5],typeNumber, context]
        incrementalNumber = incrementalNumber + 1
    
    pass

def p_grid(p):
    ''' grid :  igrid var
                      | fgrid var
            | sgrid var '''
    #print("p_grid")
    pass
#------------INT GRID--------------------
def p_igrid(p):
    ''' igrid : INT "[" CTEINT "]" "[" CTEINT "]" seen_grid ID "=" "{" bigrid "}" ";"'''
    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
        if p[9] == v or isinstance(v, list) and p[9] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[9])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[9],p[12],7, context]
        incrementalNumber = incrementalNumber + 1
    #print("INT-GRIDDY")
    pass


def p_bigrid(p):
    ''' bigrid : CTEINT 
          | CTEINT bigridaux 
        | empty '''
    global matrixContent
    if p[1] != "empty":
        if len(p) == 1:
            matrixContent = [p[1]] + matrixContent
        elif len(p) > 1:
            matrixContent = [p[1]] +  matrixContent
        else:
            print("what?")
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    #print("Bigrid")
    pass

def p_bigridaux(p):
    ''' bigridaux : "," CTEINT bigridaux 
                          | empty  '''
    global matrixContent
    if p[1] != "empty":
        matrixContent = [p[2]]+ matrixContent
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    pass
    #print("Bigridaux")
    pass

def p_seen_grid(p):
    '''seen_grid :'''
    global matrixContent 
    matrixContent = []
    pass

#------------FLOAT GRID--------------------
def p_fgrid(p):
    ''' fgrid : FLOAT "[" CTEINT "]" "[" CTEINT "]" seen_grid ID "=" "{" bfgrid "}" ";"'''
    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
        if p[9] == v or isinstance(v, list) and p[9] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[9])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[9],p[12],8, context]
        incrementalNumber = incrementalNumber + 1
    #print("FLOAT-GRIDDY")
    pass

def p_bfgrid(p):
    ''' bfgrid : CTEFLOAT 
                    | CTEFLOAT bfgridaux 
          | empty '''
    global matrixContent
    if p[1] != "empty":
        if len(p) == 1:
            matrixContent = [p[1]] + matrixContent
        elif len(p) > 1:
            matrixContent = [p[1]] +  matrixContent
        else:
            print("what?")
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    #print("Bfgrid")
    pass


def p_bfgridaux(p):
    ''' bfgridaux : "," CTEFLOAT bfgridaux 
    | empty  '''
    global matrixContent
    if p[1] != "empty":
        matrixContent = [p[2]]+ matrixContent
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    pass
    #print("Bfgridaux")
    pass
#------------STRING GRID--------------------
def p_sgrid(p):
    ''' sgrid : STRING "[" CTEINT "]" "[" CTEINT "]" seen_grid ID "=" "{" bsgrid "}" ";"'''
    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
        if p[9] == v or isinstance(v, list) and p[9] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[9])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[9],p[12],9, context]
        incrementalNumber = incrementalNumber + 1
    #print("STRING-GRIDDY")
    pass

def p_bsgrid(p):
    ''' bsgrid : CTESTRING 
    | CTESTRING bsgridaux 
    | empty '''
    global matrixContent
    if p[1] != "empty":
        if len(p) == 1:
            matrixContent = [p[1]] + matrixContent
        elif len(p) > 1:
            matrixContent = [p[1]] +  matrixContent
        else:
            print("what?")
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    #print("Bsgrid")
    pass

def p_bsgridaux(p):
    ''' bsgridaux : "," CTESTRING bsgridaux 
    | empty  '''
    global matrixContent
    if p[1] != "empty":
        matrixContent = [p[2]]+ matrixContent
        p[0] = matrixContent;
    else:
        p[0] = "empty";
    pass
    #print("Bsgridaux")
    pass

#SHELF DEF
def p_shelf(p):
    ''' shelf :  ishelf var
                      | fshelf var
            | sshelf var '''
    #print("shelf")
    pass

#------------INT SHELF-----------
def p_ishelf(p):
    ''' ishelf : INT "[" CTEINT "]" ID seen_shelf "=" "{" bishelf "}" ";" '''

    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
          if p[5] == v or isinstance(v, list) and p[5] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[5])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[5],p[9],4, context]
        incrementalNumber = incrementalNumber + 1
    
    #print("INT-shelf")
    pass

def p_seen_ishelf(p):
    '''seen_shelf :'''
    global arrayContent 
    arrayContent = []
    pass

def p_bishelf(p):
    ''' bishelf : CTEINT 
              | CTEINT bishelfaux
            | empty '''
    global arrayContent
    if p[1] != "empty":
        if len(p) == 1:
            arrayContent = [p[1]] + arrayContent
        elif len(p) > 1:
            arrayContent = [p[1]] +  arrayContent
        else:
            print("what?")
        p[0] = arrayContent;
    else:
        p[0] = "empty";

    #print("BINT-SHELF")
    pass

def p_bishelfaux(p):
    ''' bishelfaux : "," CTEINT bishelfaux
        | empty '''
    
    global arrayContent
    if p[1] != "empty":
        arrayContent = [p[2]]+ arrayContent
        p[0] = arrayContent;
    else:
        p[0] = "empty";
    pass
    
            


#------------FLOAT SHELF-----------
def p_fshelf(p):
    ''' fshelf : FLOAT "[" CTEINT "]" ID seen_shelf "=" "{" bfshelf "}" ";"'''
    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
          if p[5] == v or isinstance(v, list) and p[5] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[5])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[5],p[9],5, context]
        incrementalNumber = incrementalNumber + 1
    #print("FLOAT-shelf")
    pass
def p_bfshelf(p):
    ''' bfshelf : CTEFLOAT 
                      | CTEFLOAT bfshelfaux
            | empty '''
    global arrayContent
    if p[1] != "empty":
        if len(p) == 1:
            arrayContent = [p[1]] + arrayContent
        elif len(p) > 1:
            arrayContent = [p[1]] +  arrayContent
        else:
            print("what?")
        p[0] = arrayContent;
    else:
        p[0] = "empty";
    #print("BFLOAt-SHELF")
    pass
def p_bfshelfaux(p):
    ''' bfshelfaux : "," CTEFLOAT bfshelfaux
                        | empty '''
    #print("AUX-BFLOAT-SHELF")
    global arrayContent
    if p[1] != "empty":
        arrayContent = [p[2]]+ arrayContent
        p[0] = arrayContent;
    else:
        p[0] = "empty";
    pass
#------------STRING SHELF-----------
def p_sshelf(p):
    ''' sshelf : STRING "[" CTEINT "]" ID seen_shelf "=" "{" bsshelf "}" ";"'''
    global context
    global incrementalNumber
    addToDict = True

    for k, v in DiVars.items():
          if p[5] == v or isinstance(v, list) and p[5] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[5])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        DiVars[aux]=[p[5],p[9],6, context]
        incrementalNumber = incrementalNumber + 1
    #print("STRING-shelf")
    pass
def p_bsshelf(p):
    ''' bsshelf : CTESTRING 
                      | CTESTRING bsshelfaux
            | empty '''
    global arrayContent
    if p[1] != "empty":
        if len(p) == 1:
            arrayContent = [p[1]] + arrayContent
        elif len(p) > 1:
            arrayContent = [p[1]] +  arrayContent
        else:
            print("what?")
        p[0] = arrayContent;
    else:
        p[0] = "empty";
    #print("BSTRING-SHELF")
    pass
def p_bsshelfaux(p):
    ''' bsshelfaux : "," CTESTRING bsshelfaux
                        | empty '''
    global arrayContent
    if p[1] != "empty":
        arrayContent = [p[2]]+ arrayContent
        p[0] = arrayContent;
    else:
        p[0] = "empty";
    #print("AUX-BSTRING-SHELF")
    pass
#------------SHELFS END-----------

def p_type(p):
    '''type : INT
  | FLOAT
  | STRING
  | BOOL '''
    p[0] = p[1] #print("p1 = " + p[1]);
    pass

def p_drawing(p):
    '''drawing : DRWCPCK drawcupcake 
    | DRWCN drawcane
    | DRWCHBR drawchocobar ''' 
    #print("drawing");
    pass

def p_drawcupcake(p):
    '''drawcupcake : "(" exp "," seen_pn_drCU exp "," seen_pn_drCU exp seen_pn_drCU ")" ";" '''
    print("drawcupcake");
    pass

def p_seen_pn_drCU(p):
    '''seen_pn_drCU : '''
    global TypeStack
    global POper
    global PilaO
    global quads
    global availTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        result = "t" + str(availTemp)
        availTemp = availTemp + 1
        quad = [ "drCup", left_operand, "--", result]
        quads = quads + [quad]
    else:
        print("---Type mis-match, no hay baile Cupcake")
        exit(0)
    pass

def p_drawcane(p):
    '''drawcane : "(" exp "," seen_pn_drCA exp "," seen_pn_drCA exp "," seen_pn_drCA exp seen_pn_drCA ")" ";" '''
    #print("drawcane");
    pass
def p_seen_pn_drCA(p):
    '''seen_pn_drCA : '''
    global TypeStack
    global POper
    global PilaO
    global quads
    global availTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        result = "t" + str(availTemp)
        availTemp = availTemp + 1
        quad = [ "drCane", left_operand, "--", result]
        quads = quads + [quad]
    else:
        print("Type mis match, no hay baile en Cane")
    pass

def p_drawchocobar(p):
    '''drawchocobar : "(" exp "," seen_pn_drCH exp "," seen_pn_drCH exp "," seen_pn_drCH exp seen_pn_drCH ")" ";" '''
    #print("drawchocobar");
    pass
def p_seen_pn_drCH(p):
    '''seen_pn_drCH : '''
    global TypeStack
    global POper
    global PilaO
    global quads
    global availTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        result = "t" + str(availTemp)
        availTemp = availTemp + 1
        quad = [ "drChoc", left_operand, "--", result]
        quads = quads + [quad]
    else:
        print("Type mis match, no hay baile en chocolate")
    pass

def p_read(p):
    '''read : READ "(" seen_pn_read ")" ";" '''
    #print("Read");
    pass

def p_seen_pn_read(p):
    '''seen_pn_read :'''
    global quads
    quad = ["read","","",""]
    quads = quads + [quad]
    pass

def p_funccall(p):
    ''' funccall : ID "(" bfunccall ")" ";" '''
    #print("funccall"); 
    pass

def p_bfunccall(p):
    ''' bfunccall : exp 
  | exp bfunccallaux
  | empty '''
    #print("bfunccall"); 
    pass

def p_bfunccallaux(p):
    ''' bfunccallaux : "," exp bfunccallaux
  | empty '''
    #print("bfunccallaux"); 
    pass


def p_assignment(p):
    '''assignment : ID  "=" seen_pn_ass_id bassignment ";" seen_pn_assign'''
    #print("assignment")
    pass

def p_seen_pn_ass_id(p):
    '''seen_pn_ass_id :'''
    print("id es : " + str(p[-1]))
    idName = str(p[-2]).replace(" ", "")

    global context
    
    addToPilaO = False
    for k, v in DiVars.items():
        if idName == v or isinstance(v, list) and idName in v:
            addToPilaO = True
            print("khakha+",addToPilaO)
            varContext = DiVars[k][3]
            if varContext == context or varContext == "global":
                print("el primero lugar donde deberia meterlo a la pila")
                print("addtoila  -",addToPilaO)
                global PilaO
                PilaO =  PilaO + [idName]
                global TypeStack
                TypeStack =  TypeStack + [DiVars[k][2]] 
                global POper
                POper =  POper + ["="]
                break  

    if addToPilaO == False:
        missing_variable(idName)

    #global PilaO
    #PilaO = [idName] + PilaO
    pass

def p_seen_pn_assign(p):
    '''seen_pn_assign : '''
    if POper[-1] == '=':

        left_operand = PilaO.pop()
        left_Type = TypeStack.pop()
        result = PilaO.pop()
        result_Type = TypeStack.pop()
        operator = POper.pop()
        operator = 4
        result_Type = CuboSem.CuboSemantico[left_Type][result_Type][operator]
        global quads
        if result_Type != 99:
            quad = [operator, left_operand , ""  , result ]
            quads = quads + [quad]
        else:
            print("Mi hija no baila con el se�or")
            exit(0)
    pass

def p_bassignment(p):
    '''bassignment : exp
  | funccall'''
    #print("bassignment")
    pass


def p_write(p):
    '''write :     SHOW "(" exp seen_pn_show bwrite ")" ";" '''
    #print("write");
    pass

def p_seen_pn_show(p):
    '''seen_pn_show : '''
    global availTemp
    global quads

    #Se tiene que hacer un pop para sacar lo que se obtiene, porque estan el pilaO
    #Se puede usar el type para futuro uso del print
    #siendo exp entiende el (+) como suma, no como mas argumentos
    global TypeStack
    global PilaO
    left_operand = PilaO.pop()
    left_Type = TypeStack.pop()
    print("DATOSssss",left_operand,left_Type)
    dir = "t" + str(availTemp)
    availTemp = availTemp + 1
    quad = ["show",left_operand,"--",dir]
    quads = quads + [quad]
    pass
#Con coma, pues jala bien
def p_bwrite(p):
    '''bwrite : "," exp seen_pn_show bwrite
  | empty '''
    #print("bwrite")
    pass


def p_expression(p):
    '''expression : exp bx'''
    #print("EXPRESSION")
    pass

def p_bx(p):
      '''bx : sim seen_pn_sim exp seen_pn_exp
            | empty'''
      #print("---------------------wea",p[1])
      pass

def p_seen_pn_sim(p):
    '''seen_pn_sim :'''
    print("wea")
    global POper
    simi = p[-1]
    if simi == "<":
        POper = POper + [8]
    elif simi == ">":
        POper = POper + [7]
    elif simi == ">=":
        POper = POper + [9]
    elif simi == "<=":
        POper = POper + [10]
    elif simi == "==":
        POper = POper + [5]
    elif simi == "!=":
        POper = POper + [6]

    pass

def p_seen_pn_exp(p):
    '''seen_pn_exp :'''
    global POper
    if     len(POper) != 0:
        if POper[-1] == 5 or POper[-1] == 6 or POper[-1] == 7 or POper[-1] == 8 or POper[-1] == 9 or POper[-1] == 10 or POper[-1] == 11 or POper[-1] == 12:
            global PilaO
            global TypeStack
            global availTemp
            global quads
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()
            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                result = "t"+str(availTemp)
                availTemp = availTemp + 1
                quad = [operator, left_operand , right_operand , result ]
                quads = quads + [quad]
                PilaO = PilaO + [result]
                TypeStack = TypeStack + [resultType]
                print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SE�OR")
                exit()
    pass

def p_sim(p):
      ''' sim : GET
      | LET
      | "<"
      | ">"
      | EQUAL
      | DIFF '''
      p[0] = p[1]
      pass


def p_exp(p):
    '''exp : term seen_pn_term
           | term seen_pn_term bexp '''
    #print("EXP")
    pass

def p_seen_pn_term(p):
    '''seen_pn_term :'''
    #print("Poper top-",POper[-1])
    if len(POper) != 0:
        if POper[-1] == 0 or POper[-1] == 1:
            global PilaO
            global TypeStack
            global availTemp
            global quads
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()
            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                result = "t"+str(availTemp)
                availTemp = availTemp + 1
                quad = [operator, left_operand , right_operand , result ]
                quads = quads + [quad]
                PilaO = PilaO + [result]
                TypeStack = TypeStack + [resultType]
                print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SE�OR")
                exit()
    pass


def p_bexp(p):
    '''bexp : "+" seen_pn_plus_minus exp 
            | "-" seen_pn_plus_minus exp '''
    #print("add operations to exp")
    pass

def p_seen_pn_plus_minus(p):
    '''seen_pn_plus_minus :'''
    global POper
    if p[-1] == '+':
        operandToAdd = 0
    elif p[-1] == '-':
        operandToAdd = 1
    POper = POper + [operandToAdd]
    pass

def p_term(p):
    '''term : factor seen_pn_factor 
    | factor seen_pn_factor bterm '''
    #print("TERM")
    pass

def p_seen_pn_factor(p):
    '''seen_pn_factor :'''
    if len(POper) != 0:
        if POper[-1] == 2 or POper[-1] == 3 and len(POper) != 0:
            global PilaO
            global TypeStack
            global availTemp
            global quads
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()
            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                result = "t"+str(availTemp)
                availTemp = availTemp + 1
                quad = [operator, left_operand , right_operand , result ]
                quads = quads + [quad]
                PilaO = PilaO + [result]
                TypeStack = TypeStack + [resultType]
                print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SE�OR")
                exit()
    pass

def p_bterm(p):
    '''bterm : "*" seen_pn_times_div term 
             | "/" seen_pn_times_div term'''
    #print("Add an op")
    pass

def p_seen_pn_times_div(p):
    '''seen_pn_times_div :'''
    global POper
    if p[-1] == '*':
        operandToAdd = 2
    elif p[-1] == '/':
        operandToAdd = 3
    POper = POper + [operandToAdd]
    pass

def p_condition(p):
    '''condition : IF "("  expression condssymbols seen_exp_in_if ")" "{" statement bif "}" bcond ";" seen_end_if''' 
    #| IF "(" expression ")" "{" statement "}" ELSE "{" statement "}"  ";"'''
    #print("condition")
    pass

def p_seen_end_if(p):
	'''seen_end_if :'''
	global quads
	end = JumpStack.pop()
	FILL(end,len(quads))
	pass

def p_seen_exp_in_if(p):
	'''seen_exp_in_if :'''
	global TypeStack
	global PilaO
	global availTemp
	global quads
	global JumpStack
	exp_type = TypeStack.pop()
	if exp_type != 3:
		print("Type mismatch!")
		exit(0)
	else:
		result = PilaO.pop()
		quad = ["GotoF", result, "--", "____" ]
		quads = quads + [quad]
		JumpStack = JumpStack + [len(quads) - 1]
		print("����",len(quads))
	pass

def p_condssymbols(p):
    '''condssymbols : empty
  | AND expression seen_more_than_one_expression condssymbols
  | OR expression seen_more_than_one_expression condssymbols'''
    #print("condssymbols");
    pass

def p_seen_more_than_one_expression(p):
	'''seen_more_than_one_expression :'''
	global TypeStack
	global PilaO
	global availTemp
	global quads
	global JumpStack
	#DANGERZONE
	right_Type = TypeStack.pop()
	right_operand = PilaO.pop()
	left_Type = TypeStack.pop()
	left_operand = PilaO.pop()
	operator = 0
	print("MI HIJA" , p[-2])
	if p[-2] == "&&":
		operator = 12
	elif p[-2] == "||":
		operator = 11

	resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
	if resultType != 99:
		result = "t"+str(availTemp)
		availTemp = availTemp + 1
		quad = [operator, left_operand , right_operand , result ]
		quads = quads + [quad]
		PilaO = PilaO + [result]
		TypeStack = TypeStack + [resultType]
	else:
		print("MI HIJA NO BAILA CON EL SE�OR")
		exit()

	#ENDDANGERZONE
	pass

def p_bif(p):
    '''bif : statement
    | empty'''
    #print("bif");
    pass

def p_bcond(p):
    '''bcond : ELSE seen_else "{" statement bif '}'
    | empty'''
    #print("bif");
    pass

def p_seen_else(p):
	'''seen_else :'''
	global TypeStack
	global PilaO
	global availTemp
	global quads
	global JumpStack

	quad = ["Goto","--","--", "____" ]
	quads = quads + [quad]
	false = JumpStack.pop()
	JumpStack = JumpStack + [len(quads) - 1]
	FILL(false,len(quads))
	pass



def p_factor(p):
    '''factor : "(" seen_LP expression ")" seen_RP
    | bfactor ctevar seen_pn_add_ctevar'''
    #print("FACTOR")
    pass

def p_seen_pn_add_ctevar(p):
    '''seen_pn_add_ctevar :'''
    operand = p[-1]
    global PilaO 
    global TypeStack

    print("recibi esto : ",p[-1])
    if type(operand) is int:
        PilaO = PilaO + [operand]
        TypeStack =  TypeStack + [0]
    elif type(operand) is float:
        PilaO = PilaO + [operand]
        TypeStack =  TypeStack + [1]
    elif operand[0] == "\"":
        PilaO = PilaO + [operand]
        TypeStack =  TypeStack + [2]
    elif type(operand) is bool:
        PilaO = PilaO + [operand]
        TypeStack =  TypeStack + [3]
    else:
        idName = str(p[-1]).replace(" ", "")

        global context
        addToPilaO = False
        for k, v in DiVars.items():
            if idName == v or isinstance(v, list) and idName in v:
                addToPilaO = True
                print("popoiu +" , addToPilaO)
                print("deberia meterlo a la pila")
                varContext = DiVars[k][3]
                if varContext == context or varContext == "global":
                    print("deberia meterlo a la pila")
                    PilaO =  PilaO + [idName]
                    
                    TypeStack =  TypeStack + [DiVars[k][2]] 
                     

        if addToPilaO == False:
            missing_variable(idName)

    pass
    
def p_seen_LP(p):
    '''seen_LP :'''
    global POper
    POper = POper + ["("]
    print("--------Se METE fondo falso")
    pass
def p_seen_RP(p):
    '''seen_RP :'''
    global POper
    POper.pop()
    print("--------Se SACA fondo falso")
    pass

def p_bfactor(p): 
    '''bfactor : "-"
    | empty'''
    pass

def p_ctevar(p):
    '''ctevar : ID idbody 
               | CTEINT seen_cte
               | CTEFLOAT
        | ctebool
        | CTESTRING''' 
    p[0] = p[1] #print("CTEVAR ",p[1])
    pass

def p_idbody(p): 
    '''idbody : "[" exp "]"
        | "(" exp idbodyaux ")"
        | empty'''
    pass

def p_idbodyaux(p): 
    '''idbodyaux : "," exp idbodyaux
        | empty'''
    pass

    
def p_ctebool(p):
    '''ctebool : YES
              | NO'''
    p[0] = p[1]
    pass

def p_seen_cte(p):
    '''seen_cte :'''
    cteToPass = p[-1]
    #cteAdder(cteToPass)
    pass

#def cteAdder(cteToPass):
#    continue
    #print("Me pasaron la constante - " + str(cteToPass))


def p_empty(p):
    'empty : '
    p[0] = "empty"
    #print("empty")
    pass

def p_error(p):
    print("Syntax error")

def repeated_var_error(var_name):
    print("Variable " + var_name + " is repeated!")
    #exit()

def repeated_fun_error(fun_name):
    print("Funcion "+ fun_name+ " is repeated!")
    #exit()

def missing_variable(var_name):
    print(var_name+ " is not defined!")
    exit()

def type_to_typeNumber(typeString):
    typeNumber = -1
    #print("typeString : "+typeString)
    if typeString == "int":
        typeNumber = 0
    elif typeString == "float":
        typeNumber = 1
    elif typeString == "string":
        typeNumber = 2
    elif typeString == "bool":
        typeNumber = 3
    elif typeString == "int[]":
        typeNumber = 4
    elif typeString == "float[]":
        typeNumber = 5
    elif typeString == "string[]":
        typeNumber = 6
    elif typeString == "void":
        typeNumber = 9
    return typeNumber

def type_to_programType(var):
    print("typeString : ", var)
    if type(var) is int:
        var = "int"
    elif var == "yes" or var == "no":
        var = "bool"
    elif type(var) is float:
        var = "float"
    elif type(var) is str:
        var = "string"
    
    return var

def FILL(quadNumber,jump):
	global quads
	quads[quadNumber][3] = jump

def AVAIL(type):
  if type == 0:
    return 0

	

import ply.yacc as yacc
parser = yacc.yacc()
#yacc.yacc()
file = open("test.txt", "r")
yacc.parse(file.read())
