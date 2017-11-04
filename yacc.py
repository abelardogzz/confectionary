import ply.yacc as yacc
import lex
import cubo_semantico as CuboSem
from lex import tokens


DEBUG = True

#12:30p.m.
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


#Códigos de operación = 
##  +, -, *, /, =, ==, !=, >, <, =>, =<, ||, &&, /13
##  A partir de 25:
# 25-Goto
# 26-GotoV
# 27-GotoF
# 30-SHOW
# 31-FLAVOR
# 32-RATION
# 33-drCup
# 34-drCane
# 35-drChoc
# 35-READ
# 40-PARAM
# 41-ERA
# 42-GOSUB
# 43-RETORNO



#DiModules structure
# ! <- opcional
#key[nombre, returnValue,!numeroDeParametros, lista de tipos de los parametros, cantidad de variables totales contando parametros, keys de las variables que eventualmente serán direcciones de memoria, numero del cuadruplo en donde empieza]

#MemStacks
#GLOBAL
"""
Gi = 10000
Gf = 12500
Gs = 15000
Gb = 17500
#LOCAL
Li = 20000
Lf = 22500
Ls = 25000
Lb = 27500
#TEMP
Ti = 30000
Tf = 32500
Ts = 35000
Tb = 37500
#CONST
Ci = 40000
Cf = 42500
Cs = 45000
Cb = 47500"""
VirtualMem = ([10000,12500,15000,17500],[20000,22500,25000,27500], [30000,32500,35000,37500], [40000,42500,45000,47500])
localContext = "global"

#DictionarioVariables
DiVars = dict()
DiModules = dict()
DiConst = dict()
DiTemp = dict()
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
globalk = ""

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
    '''programdef : PROGRAM ID ":" seen_program_start globals main'''
    print("Program Approved!");
    printDic1(DiConst)
    printDic1(DiVars)
    printDic1(DiModules)
    printDic1(DiTemp)
    print("pilaO = ",PilaO)
    print("TypeStack = ",TypeStack)
    print("POper = ",POper)
    print("Quads = ")
    printDic(quads)
    pass

def p_seen_program_start(p):
  '''seen_program_start :'''
  global quads
  quad = [25,"","","_____" ] 
  quads = quads + [quad]
  pass

def p_main(p):
    '''main : CNFCTNR seen_CNFCTNR "(" ")" blocks'''
    pass
    

def p_seen_CNFCTNR(p):
    '''seen_CNFCTNR :'''
    global context
    global quads
    context = "confectionary"
    quads[0][3]= len(quads)
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
    print("No hay baile con el señor")
  else:
    returnTo = JumpStack.pop()
    result = PilaO.pop()
    quad = [26,result,"",returnTo ]
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
        print("No hay baile con el señor")
    else:
        result = PilaO.pop()
        quad = [27,result,"","_____" ]
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
    #Este goto lo cambie- originalmente estaba así, ["GOTO", ret,"","____"], ahora esta así ["GOTO","","",ret]
    quad = [25,"","",ret]
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
    '''recipedef : RCP brecipeaux "{" var seen_all_recipe_vars statement  RETURN "(" recipereturn ")" ";" "}" ";" seen_endproc
  | RCP VOID ID seen_recipe_name "(" brecipe seen_parameters ")" "{" var seen_all_recipe_vars statement  "}" ";" seen_endproc
  | empty'''

    #print("recipe");
    pass

def p_seen_endproc(p):
  '''seen_endproc :'''
  global quads
  quad = [43,"","",""]
  quads = quads + [quad]
  pass

def p_brecipeaux(p):
  '''brecipeaux : type ID seen_recipe_name "(" brecipe seen_parameters ")"'''  
  #print("brecipeaux");
  pass

def p_seen_all_recipe_vars(p):
  '''seen_all_recipe_vars :'''
  global incrementalNumberFun
  global context
  global quads
  var_keys = []
  auxCont = 0
  #print(" p[-4] -",  p[-4])
  for k, v in DiVars.items():
    if context in v:
      #print("!!!!!!!!!!!!-",k)
      var_keys = var_keys + [k]
      auxCont = auxCont + 1

  index = str(incrementalNumberFun-1)
  DiModules["FunId-"+index] = DiModules["FunId-"+index] + [auxCont] + [var_keys] + [len(quads)]
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
  parameters_types = list(reversed(parameters_types))
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
  global context

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
          memPos = AVAIL(context, typeNumber, 0, 0)
          print("ME REGRESO LA MEMORIA> ", memPos)
          DiVars[aux]=[p[2],0,typeNumber, context, memPos]
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
          memPos = AVAIL(context, typeNumber, 0, 0)
          print("ME REGRESO LA MEMORIA> ", memPos)
          DiVars[aux]=[p[3],0,typeNumber, context, memPos]
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
  '''recipereturn : exp'''
  global TypeStack
  global incrementalNumberFun
  returnValueType = TypeStack[-1]
  index = str(incrementalNumberFun-1)
  ModuleReturnType = DiModules["FunId-"+index][1]
  if returnValueType != ModuleReturnType:
    print("Return type mismtach in function ", DiModules["FunId-"+index][0])
    exit(0)
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
    global DiTemp

    result = PilaO.pop()
    result_type = TypeStack.pop()
    if result_type == 0 or result_type == 1:
        aux = "t" + str(availTemp)
        availTemp = availTemp + 1
        memPos = AVAIL(context,result_type,1,0)
        print("ME REGRESO LA MEMORIA> ", memPos)
        DiTemp[aux] = memPos
        quad = generate_Quad(32,result,"--",memPos)
        #quad = ["ration",result,"--",dir]
        quads = quads + [quad]
    else:
        print("Type Mis-Match NO HAY BAILE CON EL SEÑOR")
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
    global DiTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        aux = "t" + str(availTemp)
        availTemp = availTemp + 1
        memPos = AVAIL(context,left_type,1,0)
        DiTemp[aux] = memPos
        print("ME REGRESO LA MEMORIA> ", memPos)
        #quad = [ "flavor", left_operand, "--", result]
        quad = generate_Quad(31, left_operand, "--", memPos)

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
    '''vars : VAR type ID ";" var  
    | empty'''
    #'''vars : VAR TIPO ID "=" VAL ";" '''
    #print("vars",p[2],p[3]);
    x = type_to_programType(p[5])
    #print ("x ! -" , x)
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


      memPos = AVAIL(context, typeNumber, 0,0)
      #print("MEMPOS -> ", memPos)
      DiVars[aux]=[p[3],typeNumber, context, memPos]
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
    ''' igrid : VAR INT "[" CTEINT seen_cte "]" "[" CTEINT seen_cte "]" seen_grid ID ";"'''
    global context
    global incrementalNumber
    global VirtualMem

    if(p[4] <= 0 or p[8] <= 0):
      print("Invalid index for int[] array")
      exit()    

    if context != "global" and context !="confectionary":
      memIndex = 1
    else:
      memIndex = 0

    addToDict = True

    for k, v in DiVars.items():
        if p[12] == v or isinstance(v, list) and p[12] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[12])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        memPos = AVAIL(context,0,0,0)

        matSize = p[4] * p[8] 
        lim_sup_dim_1 = p[4]-1
        lim_sup_dim_2 = p[8]-1
       
        incrementalNumber = incrementalNumber + 1
        DiVars[aux]=[p[12],"",0, context, memPos, [0,lim_sup_dim_1], [0, lim_sup_dim_2]]
        separateArrayMem(context,matSize-1,0)


    #print("INT-GRIDDY")
    pass


def p_bigrid(p):
    ''' bigrid : CTEINT seen_cte
          | CTEINT seen_cte bigridaux 
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
    ''' bigridaux : "," CTEINT seen_cte bigridaux 
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
    ''' fgrid : VAR FLOAT "[" CTEINT seen_cte "]" "[" CTEINT seen_cte "]" seen_grid ID ";"'''
    global context
    global incrementalNumber
    addToDict = True

    if(p[4] <= 0 or p[8] <= 0):
      print("Invalid index for int[] array")
      exit() 

    for k, v in DiVars.items():
        if p[12] == v or isinstance(v, list) and p[12] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[12])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        #DiVars[aux]=[p[11],p[14],8, context]
        incrementalNumber = incrementalNumber + 1

        memPos = AVAIL(context,1,0,0)

        matSize = p[4] * p[8] 
        lim_sup_dim_1 = p[4]-1
        lim_sup_dim_2 = p[8]-1
       
        DiVars[aux]=[p[12],"",1, context, memPos, [0,lim_sup_dim_1], [0, lim_sup_dim_2]]
        separateArrayMem(context,matSize-1,1)


    #print("FLOAT-GRIDDY")
    pass

def p_bfgrid(p):
    ''' bfgrid : CTEFLOAT seen_cte
                    | CTEFLOAT seen_cte bfgridaux 
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
    ''' bfgridaux : "," CTEFLOAT seen_cte bfgridaux 
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
    ''' sgrid : VAR STRING "[" CTEINT seen_cte "]" "[" CTEINT seen_cte "]" seen_grid ID ";"'''
    global context
    global incrementalNumber
    addToDict = True

    if(p[4] <= 0 or p[8] <= 0):
      print("Invalid index for int[] array")
      exit() 

    for k, v in DiVars.items():
        if p[12] == v or isinstance(v, list) and p[12] in v:
            varContext = DiVars[k][3]
            if varContext == context:
                addToDict = False 
                repeated_var_error(p[12])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        #DiVars[aux]=[p[11],p[14],9, context]
        incrementalNumber = incrementalNumber + 1


        memPos = AVAIL(context,2,0,0)

        matSize = p[4] * p[8] 
        lim_sup_dim_1 = p[4]-1
        lim_sup_dim_2 = p[8]-1
       
        DiVars[aux]=[p[12],"",2, context, memPos, [0,lim_sup_dim_1], [0, lim_sup_dim_2]]
        separateArrayMem(context,matSize-1,2)



    #print("STRING-GRIDDY")
    pass

def p_bsgrid(p):
    ''' bsgrid : CTESTRING seen_cte
    | CTESTRING seen_cte bsgridaux 
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
    ''' bsgridaux : "," CTESTRING seen_cte bsgridaux 
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
    ''' ishelf : VAR INT "[" CTEINT seen_cte "]" ID seen_shelf ";" '''

    global context
    global incrementalNumber
    addToDict = True

    if(p[4] <= 0):
      print("Invalid index for int[] array: ", p[7])
      exit()

    for k, v in DiVars.items():
          if p[7] == v or isinstance(v, list) and p[7] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[7])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        memPos = AVAIL(context,0,0,0)
        lim_sup = p[4]-1
        DiVars[aux]=[p[7],"",0, context, memPos, [0,p[4]-1]]
        incrementalNumber = incrementalNumber + 1
        separateArrayMem(context,lim_sup,0)
        

    
    #print("INT-shelf")
    pass


def p_seen_ishelf(p):
    '''seen_shelf :'''
    global arrayContent 
    arrayContent = []
    pass

def p_bishelf(p):
    ''' bishelf : CTEINT seen_cte
              | CTEINT seen_cte bishelfaux
            | empty '''
    global arrayContent
    if p[1] != "empty":
        if len(p) == 1:
            arrayContent = [p[1]] + arrayContent
        elif len(p) > 1:
            arrayContent = [p[1]] +  arrayContent
        else: 
          p[0] = arrayContent;
    else:
        p[0] = "empty";

    #print("BINT-SHELF")
    pass

def p_bishelfaux(p):
    ''' bishelfaux : "," CTEINT seen_cte bishelfaux
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
    ''' fshelf : VAR FLOAT "[" CTEINT seen_cte "]" ID seen_shelf ";"'''
    global context
    global incrementalNumber
    addToDict = True

    if(p[4] <= 0):
      print("Invalid index for int[] array: ", p[7])
      exit()

    for k, v in DiVars.items():
          if p[7] == v or isinstance(v, list) and p[7] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[7])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        memPos = AVAIL(context,1,0,0)
        lim_sup = p[4]-1
        DiVars[aux]=[p[7],"",1, context, memPos,[0,p[4]-1]]
        incrementalNumber = incrementalNumber + 1
        separateArrayMem(context,lim_sup,1)
    #print("FLOAT-shelf")
    pass
def p_bfshelf(p):
    ''' bfshelf : CTEFLOAT seen_cte
                      | CTEFLOAT seen_cte bfshelfaux
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
    ''' bfshelfaux : "," CTEFLOAT seen_cte bfshelfaux
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
    ''' sshelf : VAR STRING "[" CTEINT seen_cte "]" ID seen_shelf ";"'''
    global context
    global incrementalNumber
    addToDict = True

    if(p[4] <= 0):
      print("Invalid index for int[] array: ", p[7])
      exit()

    for k, v in DiVars.items():
          if p[7] == v or isinstance(v, list) and p[7] in v:
              varContext = DiVars[k][3]
              if varContext == context:
                  addToDict = False 
                  repeated_var_error(p[7])

    if addToDict == True:
        aux = GlobalID + str(incrementalNumber)
        memPos = AVAIL(context,2,0,0)
        lim_sup = p[4]-1
        DiVars[aux]=[p[7],"",2, context, memPos,[0,p[4]-1]]
        incrementalNumber = incrementalNumber + 1
        separateArrayMem(context,lim_sup,2)
    #print("STRING-shelf")
    pass
def p_bsshelf(p):
    ''' bsshelf : CTESTRING seen_cte
                      | CTESTRING seen_cte bsshelfaux
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
    ''' bsshelfaux : "," CTESTRING seen_cte bsshelfaux
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
    global DiTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        aux = "t" + str(availTemp)
        availTemp = availTemp + 1
        memPos = AVAIL(context, left_type, 1, 0)
        print("ME REGRESO LA MEMORIA> ", memPos)
        DiTemp[aux] = memPos
        quad = generate_Quad(33, left_operand, "--", memPos)
        #quad = [ "drCup", left_operand, "--", result]
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
    global DiTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        aux = "t" + str(availTemp)
        availTemp = availTemp + 1
        memPos = AVAIL(context, left_type,1,0)
        print("ME REGRESO LA MEMORIA> ", memPos)
        DiTemp[aux] = memPos
        #quad = [ "drCane", left_operand, "--", result]
        quad = generate_Quad(34, left_operand, "--", memPos)
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
    global DiTemp

    left_operand = PilaO.pop()
    left_type = TypeStack.pop()

    if left_type == 0 or left_type == 1 :
        aux = "t" + str(availTemp)
        availTemp = availTemp + 1
        memPos = AVAIL(context, left_type, 1, 0)
        print("ME REGRESO LA MEMORIA> ", memPos)
        DiTemp[aux] = memPos
        #quad = [ "drChoc", left_operand, "--", memPos]
        quad = generate_Quad(35, left_operand, "--", memPos)
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
    quad = [36,"","",""]
    quads = quads + [quad]
    pass

def p_funccall(p):
    ''' funccall : ID "(" seen_funcall_id bfunccall ")" ";" seen_funcall_end'''
    print("ended funccall"); 
    pass

def p_seen_funcall_end(p):
  '''seen_funcall_end :'''
  global quads
  global globalk
  quad = [42, DiModules[globalk][0], DiModules[globalk][6], "" ]
  quads = quads + [quad]
  pass

def p_seen_funcall_id(p):
  '''seen_funcall_id :'''
  global quads
  thisk = ""
  existingFunction = False
  for k, v in DiModules.items():
    if p[-2] == v or isinstance(v, list) and p[-2] in v:
      thisk = k
      print("La función ",thisk, " si existe!")
      existingFunction = True
      
  #print("Seen fun call")
  if not existingFunction:
    print("Non-existing function: ", p[-2])
    exit(0)
  if existingFunction:
    #quad = ["era", DiModules[k][0],DiModules[k][4],""]
    quad = [41, DiModules[thisk][0],DiModules[thisk][4],""]
    quads = quads + [quad]
  p[0] = thisk
  global globalk
  globalk=thisk
  global auxCont
  auxCont = 0
  pass

def p_bfunccall(p):
    ''' bfunccall : exp seen_exp_in_params
  | exp seen_exp_in_params bfunccallaux
  | empty '''

    #print("bfunccall"); 
    pass

def p_bfunccallaux(p):
    ''' bfunccallaux : "," exp seen_exp_in_params bfunccallaux
  | empty '''
    #print("bfunccallaux"); 
    pass

def p_seen_exp_in_params(p):
  '''seen_exp_in_params :'''
  global globalk
  global auxCont
  global PilaO
  global TypeStack
  global quads
  numberOfParams = DiModules[globalk][2]
  if numberOfParams == 0 or (numberOfParams-1) < auxCont:
    print("The number of parameters is incorrect")
    exit(0)
  else:
    moduleParamType = DiModules[globalk][3][auxCont]
    #print("param type - ", paramType)
    localParamType = TypeStack.pop()
    argument = PilaO.pop()
    if moduleParamType != localParamType:
      print("Type mismatch in parameter ", auxCont + 1, " in function ", DiModules[globalk][0])
      exit(0)
    else:
      quad = generate_Quad(40,argument,"","param"+str(auxCont))
      #quad = ["PARAM",argument,"","param"+str(auxCont)]
      quads = quads + [quad]
      auxCont +=1
  pass

def p_assignment(p):
    '''assignment : ID  "=" seen_pn_ass_id exp ";" seen_pn_assign
    | ID "=" seen_pn_ass_id funccall seen_pn_assign
    | ID "[" seen_pn_ass_id_arr exp "]" seen_access_array "=" exp ";" seen_pn_assign_array'''
    #| ID "[" seen_pn_ass_id_arr exp "]" seen_access_array "=" funccall seen_pn_assign_array'''   
    #Esto de arriba falta!
    #print("assignment")
    pass


def p_seen_access_array(p):
  '''seen_access_array :'''
  global PilaO
  global TypeStack
  global DiVars
  global quads
  result = PilaO.pop()
  result_type = TypeStack.pop()
  key = p[-3]
  if result_type != 0:
    print("Array index must be int!")
    exit(0)
  upperLimit = DiVars[key][5][1]

  if result>upperLimit:
    print("Array index out of bounds!")
    exit(0)

  quad = generate_Quad("VerArr",result,0,upperLimit)
  quads = quads + [quad]
  print("upperLimit->", upperLimit)
  print("This is the key! -> ", key)

  p[0] = result

  #if

  pass


def p_seen_pn_ass_id_arr(p):
  '''seen_pn_ass_id_arr :'''
  idName = str(p[-2]).replace(" ", "")

  global context
  key = ""
  addToPilaO = False
  for k, v in DiVars.items():
      if idName == v or isinstance(v, list) and idName in v:
          addToPilaO = True
          varContext = DiVars[k][3]
          if varContext == context or varContext == "global":
              #print("addtoila  -",addToPilaO)
              global PilaO
              PilaO =  PilaO + [idName]
              global TypeStack
              TypeStack =  TypeStack + [DiVars[k][2]] 
              global POper
              key = k
              POper =  POper + ["="]
              break  

  if addToPilaO == False:
      missing_variable(idName)
  p[0] = key
  pass

#def p_seen_ok(p):
#    '''seen_ok :'''
#    print("si vi el funccall")
#    pass

def p_seen_pn_ass_id(p):
    '''seen_pn_ass_id :'''
    #print("id es : " + str(p[-1]))
    idName = str(p[-2]).replace(" ", "")

    global context
    
    addToPilaO = False
    for k, v in DiVars.items():
        if idName == v or isinstance(v, list) and idName in v:
            addToPilaO = True
            #print("khakha+",addToPilaO)
            varContext = DiVars[k][3]
            if varContext == context or varContext == "global":
                #print("addtoila  -",addToPilaO)
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

def p_seen_pn_assign_array(p):
    '''seen_pn_assign_array : '''
    if len(POper) != 0:
      if POper[-1] == '=':

          left_operand = PilaO.pop()
          #print("LEFT_OPERAND->",left_operand)
          left_Type = TypeStack.pop()
          result = PilaO.pop()
          #print("RESULT->",result)
          result_Type = TypeStack.pop()
          operator = POper.pop()
          operator = 4

          if result_Type != left_Type:
            result_Type = 99

          #result_Type = CuboSem.CuboSemantico[left_Type][result_Type][operator]
          global quads
          if result_Type != 99:
              #quad = [operator, left_operand , ""  , result ]
              #result = 
              print("Lo que envio en ass->", operator, left_operand, "", result)
              quad = generate_Quad(operator, left_operand, "", result)
              quad[3] = quad[3] + p[-4]
              print("El nuevo quad !*->", quad)
              quads = quads + [quad]
          else:
              print("Mi hija no baila con el señor")
              exit(0)
    pass

def p_seen_pn_assign(p):
    '''seen_pn_assign : '''
    print("p[-1]-",p[-1]);
    print("Entre a pn_assign")
    if len(POper) != 0:
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
              #quad = [operator, left_operand , ""  , result ]
              print("Lo que envio en ass->", operator, left_operand, "", result)
              quad = generate_Quad(operator, left_operand, "", result)
              print("El nuevo quad ->", quad)
              quads = quads + [quad]
          else:
              print("Mi hija no baila con el señor")
              exit(0)
    pass

#def p_bassignment(p):
#    '''bassignment : exp
#  | funccall'''
#    print("ended bassignment")
#    pass


def p_write(p):
    '''write :     SHOW "(" exp seen_pn_show bwrite ")" ";" '''
    #print("write");
    pass

def p_seen_pn_show(p):
    '''seen_pn_show : '''
    global availTemp
    global quads
    global DiTemp
    #Se tiene que hacer un pop para sacar lo que se obtiene, porque estan el pilaO
    #Se puede usar el type para futuro uso del print
    #siendo exp entiende el (+) como suma, no como mas argumentos
    global TypeStack
    global PilaO
    left_operand = PilaO.pop()
    left_Type = TypeStack.pop()
    #print("DATOSssss",left_operand,left_Type)
    aux = "t" + str(availTemp)
    availTemp = availTemp + 1
    memPos = AVAIL(context,left_Type,1,0)
    print("ME REGRESO LA MEMORIA> ", memPos)
    DiTemp[aux] = memPos
    #print("SHOW LEFT OP ->", left_operand)
    quad = generate_Quad(30,left_operand,"--",memPos)

    #quad = ["show",left_operand,"--",memPos]
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
      pass

def p_seen_pn_sim(p):
    '''seen_pn_sim :'''
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
            global DiTemp
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()
            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                aux = "t"+str(availTemp)
                availTemp = availTemp + 1
                memPos = AVAIL(context, resultType,1,0)
                print("ME REGRESO LA MEMORIA> ", memPos)
                DiTemp[aux] = memPos
                quad = generate_Quad(operator, left_operand , right_operand , memPos)
                #quad = [operator, left_operand , right_operand , result ]
                quads = quads + [quad]
                PilaO = PilaO + [memPos]
                TypeStack = TypeStack + [resultType]
                #print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SEÑOR")
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
            global DiTemp
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()
            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                aux = "t"+str(availTemp)
                availTemp = availTemp + 1
                memPos = AVAIL(context, resultType, 1,0)
                print("ME REGRESO LA MEMORIA> ", memPos)
                DiTemp[aux] = memPos
                quad = generate_Quad(operator, left_operand , right_operand , memPos)
                #quad = [operator, left_operand , right_operand , memPos ]
                quads = quads + [quad]
                PilaO = PilaO + [memPos]
                TypeStack = TypeStack + [resultType]
                #print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SEÑOR")
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
            global DiTemp
            right_operand = PilaO.pop()
            right_Type = TypeStack.pop()
            left_operand = PilaO.pop()
            left_Type = TypeStack.pop()
            operator = POper.pop()


            resultType = CuboSem.CuboSemantico[left_Type][right_Type][operator]
            if resultType != 99:
                aux = "t"+str(availTemp)
                availTemp = availTemp + 1
                memPos = AVAIL(context, resultType, 1,0)
                print("ME REGRESO LA MEMORIA> ", memPos)
                DiTemp[aux] = memPos
                quad = generate_Quad(operator, left_operand , right_operand , memPos)
                #quad = [operator, left_operand , right_operand , result ]
                quads = quads + [quad]
                PilaO = PilaO + [memPos]
                TypeStack = TypeStack + [resultType]
                #print("Quad! - ", operator ," ", left_operand , " ", right_operand , " " , "t1"  )
            else:
                print("MI HIJA NO BAILA CON EL SEÑOR")
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
    print ("RESULT->",result)
    quad = [27, result, "--", "____" ]
    quads = quads + [quad]
    JumpStack = JumpStack + [len(quads) - 1]
    #print("´´´´",len(quads))
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
    aux = "t"+str(availTemp)
    availTemp = availTemp + 1
    memPos = AVAIL(context, resultType, 1,0)
    print("ME REGRESO LA MEMORIA> ", memPos)
    DiTemp[aux] = memPos
    quad = generate_Quad(operator, left_operand , right_operand , memPos)
    #quad = [operator, left_operand , right_operand , aux ]
    quads = quads + [quad]
    PilaO = PilaO + [memPos]
    TypeStack = TypeStack + [resultType]
  else:
    print("MI HIJA NO BAILA CON EL SEÑOR")
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

  quad = [25,"--","--", "____" ]
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

    #print("recibi esto : ",p[-1])
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
                #print("popoiu +" , addToPilaO)
                #print("deberia meterlo a la pila")
                varContext = DiVars[k][3]
                if varContext == context or varContext == "global":
                    #print("deberia meterlo a la pila")
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
               | CTEFLOAT seen_cte
        | ctebool seen_cte
        | CTESTRING seen_cte''' 
    p[0] = p[1] #print("CTEVAR ",p[1])
    pass

def p_idbody(p): 
    '''idbody : "(" exp idbodyaux ")"
        | empty'''
    print ("saw id body->", p[-1])
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
    cteType = type_to_programType(cteToPass)
    cteType = type_to_typeNumber(cteType)
    global DiConst
    global incrementalNumberConst
    global GlobalConst
    #print ("seen cte!")
    addToDict = True
    for k, v in DiConst.items():
      if cteToPass == v or isinstance(v, list) and cteToPass in v:
        addToDict = False

    if addToDict:
      memPos = AVAIL("",cteType,0,1)
      print("ME REGRESO LA MEMORIA> ", memPos)
      aux = GlobalConst + str(incrementalNumberConst)
      incrementalNumberConst = incrementalNumberConst + 1
      DiConst[aux]=[cteToPass,memPos]
            

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
    print("Syntax error",p.value,p.lineno)
    exit(0)
    pass

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
    #print("typeString : ", var)
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


#memPos = AVAIL(context, typeNumber, tempFlag, constFlag)
def AVAIL(context, varType , tempFlag,constFlag):
  global VirtualMem
  global localContext

  if varType >= 4 and varType <7:
    varType = varType-4 
  elif varType >= 7:
    varType = varType-7

  if constFlag != 0:
    memSpace = VirtualMem[3][varType]
    VirtualMem[3][varType] = VirtualMem[3][varType] + 1
  else:
    if tempFlag != 0:
      memSpace = VirtualMem[2][varType]
      print("MEMTOGIVE> ",memSpace)
      VirtualMem[2][varType] = VirtualMem[2][varType] + 1
    else:
      if context != "global" and context != "confectionary":
        if localContext != context:
          VirtualMem[1][0] = 20000
          VirtualMem[1][1] = 22500
          VirtualMem[1][2] = 25000
          VirtualMem[1][3] = 27500
        localContext = context
        memSpace = VirtualMem[1][varType]
        VirtualMem[1][varType] = VirtualMem[1][varType] + 1
      else:
        memSpace = VirtualMem[0][varType]
        VirtualMem[0][varType] = VirtualMem[0][varType] + 1
  return memSpace


def generate_Quad(operator, left_op, right_op, result):

  #if type(left_op) != str:
  global DiConst
  global incrementalNumberConst
  global GlobalConst

  left_op = quadParamChecker(left_op)
  right_op = quadParamChecker(right_op)

  if type(result) != str:
    result = quadParamChecker(result)
  else:
    if "param" not in result:
      print("ALV")
      result = quadParamChecker(result)
  quad = [operator, left_op, right_op, result]
  return quad

def quadParamChecker(itemToCheck):
  global DiConst
  global DiVars
  global incrementalNumberConst
  global incrementalNumber
  global GlobalConst
  cteType = type(itemToCheck)
  cteType = type_to_typeNumber(cteType)
  if type(itemToCheck) != str: #osea q es constante o temporal
    #print("ITEMTOCHECK> ", itemToCheck)
    if itemToCheck >= 30000 and itemToCheck < 40000:
      #print("ITEMTOCHECK> ", itemToCheck,"im a temp so not a constant")
      key = 0
      isIndeedATemp = False
      for k, v in DiTemp.items():
        if itemToCheck == v or isinstance(v, list) and itemToCheck in v:
           key = k
           isIndeedATemp = True

      if not isIndeedATemp:
        print("ITEMTOCHECK> ", itemToCheck,"i'm not a temp! so a constant")
        addToDict = True
        key = 0
        for k, v in DiConst.items():
          if itemToCheck == v or isinstance(v, list) and itemToCheck in v:
            #print("mi key es -> ", k)
            addToDict = False
            key = k

        if addToDict:
          memPos = AVAIL("",cteType,0,1)
          print("ME REGRESO LA MEMORIA> ", memPos)
          aux = GlobalConst + str(incrementalNumberConst)
          incrementalNumberConst = incrementalNumberConst + 1
          DiConst[aux]=[itemToCheck,memPos]
          key = aux
          itemToCheck = DiConst[key][1]

          
    else:
      addToDict = True
      key = 0
      for k, v in DiConst.items():
        if itemToCheck == v or isinstance(v, list) and itemToCheck in v:
          #print("mi key es -> ", k)
          addToDict = False
          key = k

      if addToDict:
        memPos = AVAIL("",cteType,0,1)
        print("ME REGRESO LA MEMORIA> ", memPos)
        aux = GlobalConst + str(incrementalNumberConst)
        incrementalNumberConst = incrementalNumberConst + 1
        DiConst[aux]=[itemToCheck,memPos]
        key = aux

      itemToCheck = DiConst[key][1]

  elif itemToCheck != "--" and itemToCheck != "":
    #print("ITEMTOCHECK ->", itemToCheck)
    key = 0
    consOrVar = ""
    isInDic = False
    for k, v in DiVars.items():
      if itemToCheck == v or isinstance(v, list) and itemToCheck in v:
        #print("mi key es -> ", k)
        isInDic = True
        consOrVar = "var"
        key = k   

    if not isInDic:
      for k, v in DiConst.items():
        if itemToCheck == v or isinstance(v, list) and itemToCheck in v:
          #print("mi key es -> ", k)
          consOrVar = "cons"
          isInDic = True
          key = k 

    if consOrVar == "var":
      itemToCheck = DiVars[key][4]
    elif consOrVar == "cons":
      itemToCheck = DiConst[key][1]
    else: 
      print("Var ", itemToCheck, " is not defined! Please define it!")
      exit(0)


      
    #itemToCheck = DiVars[key][3]
  #print("yo soy -> ", itemToCheck)
  return itemToCheck


def separateArrayMem(context,lim_sup,arrType):
  for x in range(0, lim_sup):
    AVAIL(context,arrType,0,0)



import ply.yacc as yacc
parser = yacc.yacc()
#yacc.yacc()
file = open("test.txt", "r")
yacc.parse(file.read())
