import tkinter as tk
import subprocess
import turtle



#Program Couter
pc = 0
#Dictionaries
iDic = dict()
fDic = dict()
sDic = dict()
bDic = dict()
quads = list()
#Diccionario para las funciones
ModDic = dict()

#Crea Tortuga
t= turtle.Turtle()


def printDict(d):
    for x in d:
        print(x)
    pass
txt = ""
if __name__ == '__main__':
    print("Start")


def click_ok():
    print("Presiona OK")
    pass

def LoadProgram():
    #global codigo
    #txt = self.codigo
    print("Cargando PRograma")
    programa = codigo.get("1.0",'end-1c')
    print(programa)
    arch = open("test.txt","w")
    arch.write(programa)
    arch.close()
    CompilaProg()
    pass
    
#Llama a yacc para procesar el archivo de ejecucion
def CompilaProg():
    command = "hola.bat"
    program = subprocess.run(command,stdout=subprocess.PIPE)
    print( program.stdout)
    #print(text)
    pass

#Comeinza el proceso de interfaz Tortuga
def CargaInterfaz():
    #t= turtle.Turtle()
    global t
    t.shape("turtle")
    t.circle(80)
    t.screen.mainloop()
    pass

#Recibe un quad en string y regresa una lista con los elementos del quad
def ChangeQuad(q):
    q = q[1:-2] #Quita los brackets
    q = q.split(",")
    #print("quady",q)
    q[0] = q[0].strip()
    q[1] = q[1].strip()
    q[2] = q[2].strip()
    q[3] = q[3].strip()
    return q

#Recibe un quad CONSTANTE y lo carga en la memoria con su valor
def LoadConst(q):
    q = q[1:-2] #Quita los brackets
    q = q.split(",")
    #print("quady",q)
    q[0] = q[0].strip()
    q[1] = q[1].strip()
    AgregaValorDict(int(q[1]),q[0])
    pass

def EjecutarPrograma():
    global quads
    global pc
    pc = 0
    quads.clear()

    const = False
    print("ejecutando programa")
    arch = open("res.txt","r")
    #Agrega el priemr goto
    quad = arch.readline()
    quad = ChangeQuad(quad)
    quads.append(quad)

    #Carga los quads de Modulos y ejecucion
    while(True):
        quad = arch.readline()
        if quad == "%%\n":
            break
        quad = ChangeQuad(quad)
        quads.append(quad)
        #print(quad)
    
        #Carga las constantes
    quad = arch.readline()
    while( quad != ''):
        LoadConst(quad)
        quad = arch.readline()
        #print(quad)
    
    
    arch.close()
    #print(quads)
    print("ACABE DE CARGAR")
    #Despues de cargar todos los quads y sus constantes continua el programa
    IniciaEjecucion()
    pass

def GetOperands(q):
    op = getInt(q[0])
    right_op = getInt(q[1])
    left_op = getInt(q[2])
    res = getInt(q[3])
    return [op,right_op,left_op,res]

def getInt(i):
    try:
        i = int(i)
    except ValueError:
        i = -1
    return i

def IniciaEjecucion():
    global pc
    global quads
    print("inicia EJECUCION")
    

    while( pc < len(quads)):

        quadEnNum = GetOperands(quads[pc])
        op = quadEnNum[0]
        #print(quadEnNum)

        #Switch para opciones
        if op == 0 : #+
            #print("Operación")
            Suma(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 1: #-
            #print("Resta")
            Resta(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 2: #*
            #print("multi")
            Multiplica(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 3: #/
            #print("divi")
            Divide(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 4: #=
            #print("assign")
            Assigna(quadEnNum[1],quadEnNum[3])
        elif op == 5: #==
            print("IGUALGUAL")
            IgualÍgual(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 6 : #!=
            print("Diferente")
            IgualDiferente(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 7 : #>
            print("mayor khe")
            MayorQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 8 : #<
            print("meno khe")
            MenorQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 9 : #>=
            print(" mayor Igual khe")
            MayorIgualQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 10: #<=
            print(" menor Igual khe")
            MenorIgualQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 11: #OR
            print("OR ")
            RelacionOR(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 12: #AND
            print("AND ")
            RelacionAND(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 25: #Goto
            print("GotO")
            pc = quadEnNum[3]-1
        elif op == 26: #GotoV
            print("GotoV")
            GotoV(quadEnNum[1],quadEnNum[3])
        elif op == 27: #GotoF
            print("GotoF")
            GotoF(quadEnNum[1],quadEnNum[3])
        elif op == 30: #
            print("show")
            Muestra(quadEnNum[1])
        elif op == 31:
            print("flavour")
            
        elif op == 32:
            print("Ratio")
            
        elif op == 33:
            print("drwCup")
            
        elif op == 34:
            print("drwCane")
            
        elif op == 35:
            print("drwChoc")
            
        elif op == 36:
            print("read")
            

        
        #Aumenta el Program Counter
        pc = pc + 1

    print("Se acabo EL PROGRAMA WUUU")
    pass
def Suma(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    #print("SI LOS SUMA",a+b)
    AgregaValorDict(dirRes,a+b)
    pass
def Resta(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    #print("SI LOS REsta",a-b)
    AgregaValorDict(dirRes,a-b)
    pass
def Multiplica(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    #print("SI LOS Multi",a*b)
    AgregaValorDict(dirRes,a*b)
    pass
def Divide(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    #print("SI LOS Divide",a/b)
    AgregaValorDict(dirRes,a/b)
    pass

def GotoV(checa,NewPC):
    global pc
    checa = bDic[checa]
    if checa:
        pc = NewPC - 1
    pass
def GotoF(checa, NewPC):
    global pc
    checa = bDic[checa]
    if not checa:
        pc = NewPC - 1
    pass

def Assigna(dirA,dirRes):
    res = SacaValorDict(dirA)
    AgregaValorDict(dirRes,res)
    print("Assigna----->",res)
    pass
def IgualÍgual(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a==b)
    pass
def IgualDiferente(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a!=b)
    pass
def MayorQue(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a>b)
    pass
def MenorQue(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a<b)
    pass
def MayorIgualQue(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a>=b)
    pass
def MenorIgualQue(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a<=b)
    pass
def RelacionOR(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a or b)
    pass
def RelacionAND(dirA,dirB,dirRes):
    a = SacaValorDict(dirA)
    b = SacaValorDict(dirB)
    AgregaValorDict(dirRes,a and b)
    pass

def Muestra(dir):
    val = SacaValorDict(dir)
    print(val)
    pass
def Sabroso(dirR,dirG,dirB):

    pass
def Racion(dir):
    pass
def DibujaPastel(dirRad,dirX,dirY):
    pass
def DibujaLinea(dirX1,dirY1,dirX2,dirY2):

    pass
def DibujaBarra(dirX1,dirY1,dirX2,dirY2):
    pass
def Lee():
    #Pues lee en algo
    pass



#Agrega en un valor en la direccion que se provee como argumentos
def AgregaValorDict(dir,valor):
    global iDic
    global fDic
    global sDic
    global bDic
    #Checa si es entero
    if dir>= 10000 and dir< 12500 or dir>= 20000 and dir< 22500 or dir>= 30000 and dir< 32500 or dir>= 40000 and dir< 42500:
        iDic[dir] = int(valor)
    #Checa si es flotante
    if dir>= 12500 and dir< 15000 or dir>= 22500 and dir< 25000 or dir>= 32500 and dir< 35000 or dir>= 42500 and dir< 45000:
        fDic[dir] = float(valor)
    #Checa si es String
    if dir>= 15000 and dir< 17500 or dir>= 25000 and dir< 27500 or dir>= 35000 and dir< 37500 or dir>= 45000 and dir< 47500:
        valor = valor[2:-2]
        sDic[dir] = valor
    #Checa si es booleano
    if dir>= 17500 and dir< 20000 or dir>= 27500 and dir< 30000 or dir>= 37500 and dir< 40000 or dir>= 47500 and dir< 50000:
        if type(valor ) is str:
            valor.lower()
        if valor == "yes" or valor :
            bDic[dir] = True
        if valor == "no"  or not valor: 
            bDic[dir] = False
    pass
def SacaValorDict(dir):
    global iDic
    global fDic
    global sDic
    global bDic
    #Checa si es entero para regresarlo
    
    if dir>= 10000 and dir< 12500 or dir>= 20000 and dir< 22500 or dir>= 30000 and dir< 32500 or dir>= 40000 and dir< 42500:
        try: 
            return iDic[dir] 
        except KeyError :
            print("Warning: Variable no Inicializada")
            return 0
    #Checa si es flotante para regresarlo
    if dir>= 12500 and dir< 15000 or dir>= 22500 and dir< 25000 or dir>= 32500 and dir< 35000 or dir>= 42500 and dir< 45000:
        try:
            return fDic[dir] 
        except KeyError:
            print("Warning: Variable no Inicializada")
            return 0.0
    #Checa si es String para regresarlo
    if dir>= 15000 and dir< 17500 or dir>= 25000 and dir< 27500 or dir>= 35000 and dir< 37500 or dir>= 45000 and dir< 47500:
        try:
            return sDic[dir]
        except KeyError:
            print("Warning: Variable no Inicializada")
            return ""
    #Checa si es booleano para regresarlo
    if dir>= 17500 and dir< 20000 or dir>= 27500 and dir< 30000 or dir>= 37500 and dir< 40000 or dir>= 47500 and dir< 50000:
        try:
            return bDic[dir]
        except KeyError:
            print("Warning: Variable no Inicializada")
            return False
 
root = tk.Tk()
#app = App(root)
root.title("Program FOOD")
dialog_frame = tk.Frame(root)
dialog_frame.pack()
#Area de codigo
tk.Label(dialog_frame,text="Escribe tu codigo abajo").pack(side="top")
codigo = tk.Text(dialog_frame)
codigo.pack(side="bottom")
tk.Button(dialog_frame,text='Compilar',command = LoadProgram).pack(side="top")
#Carga el programa desde el ultimo que se corrio
arch = open("test.txt","r")
codigo.insert("1.0",arch.read())
arch.close()
#Btn para ejectuar
tk.Button(dialog_frame,text='Ejecutar',command =EjecutarPrograma ).pack(side="top")
#BTN de cierre
tk.Button(dialog_frame, text="Cerrar", command=quit).pack(side="right")
root.mainloop()