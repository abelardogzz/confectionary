import tkinter as tk
import subprocess
import turtle
from time import sleep
from tkinter import scrolledtext



#Program Couter
pc = 0
#Inicio de Espacio de memoria libre y Arreglo de parametros
dirMemLocal = 20000
EspacioMemoriaLocal = 0
DirMemoriaLocalLibre = 0
arrParams = []
InFuncall = False
SumaBaseArr = False
#Program Counter Temp
pcTemps =[]
#Dictionaries
iDic = dict()
fDic = dict()
sDic = dict()
bDic = dict()
quads = list()
#Diccionario para las funciones
ModDic = dict()
LocalMemDic = dict()
#Stack de MemoriaLocal Dormida
MemLocalDormida = []

#Crea Tortuga
t= turtle.Turtle()


#Variable de racion
ration = 1


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
    #print("Cargando PRograma")

    programa = codigo.get("1.0",'end-1c')
    #print(programa)
    arch = open("test.txt","w")
    arch.write(programa)
    arch.close()
    CompilaProg()
    pass

def printLog(t):
    t = str(t) + "\n"
    consola.insert("end",t)
    pass
    
#Llama a yacc para procesar el archivo de ejecucion
def CompilaProg():
    consola.delete("1.0","end")
    command = "hola.bat"
    #Ejecuta el commando que contiene yacc.py y lo deja en stdout local
    program = subprocess.run(command,stdout=subprocess.PIPE)
    resultado = str(program.stdout[0:-2])
    #Analiza si en el resultado se encuentra la aprovacion de lex y yacc y sem
    if "Program Approved" in resultado:
        lblAviso['text'] = "Succesfull build"
        consola.insert("1.0","Succesfull Build")
    else:
        lblAviso['text'] = resultado
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
    global t
    global iDic
    global sDic
    global bDic
    global fDic
    t.shape("turtle")
    t.screen.colormode(255)
    t.up()
    #Limpiado de variables para nueva ejecucion
    pc = 0
    quads.clear()
    iDic.clear()
    fDic.clear()
    bDic.clear()
    sDic.clear()

    #Limpia el contenido de la consola
    consola.delete("1.0","end")

    const = False
    #print("ejecutando programa")
    try:
        arch = open("res.txt","r+")
    except FileNotFoundError:
        consola.insert("1.0","Programa vacio")
        return
    #Agrega el priemr goto
    quad = arch.readline()
        
    quad = ChangeQuad(quad)
    quads.append(quad)

    #Carga los quads de ejecucion
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

    
    
    arch.close()
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
    global InFuncall
    global arrParams
    global EspacioMemoriaLocal
    global SumaBaseArr


    auxCoords = []
    #print("inicia EJECUCION")
    
    quadEnNum = GetOperands(quads[pc])
    #op = quadEnNum[3] - 1
    #Carga las funciones
    #LoadModulos(quadEnNum[3]-1)

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
            #print("IGUALGUAL")
            IgualÍgual(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 6 : #!=
            #print("Diferente")
            IgualDiferente(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 7 : #>
            #print("mayor khe")
            MayorQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 8 : #<
            #print("meno khe")
            MenorQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 9 : #>=
            #print(" mayor Igual khe")
            MayorIgualQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 10: #<=
            #print(" menor Igual khe")
            MenorIgualQue(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 11: #OR
            #print("OR ")
            RelacionOR(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 12: #AND
            #print("AND ")
            RelacionAND(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 25: #Goto
            #print("GotO")
            pc = quadEnNum[3]-1
        elif op == 26: #GotoV
            #print("GotoV")
            GotoV(quadEnNum[1],quadEnNum[3])
        elif op == 27: #GotoF
            #print("GotoF")
            GotoF(quadEnNum[1],quadEnNum[3])
        elif op == 30: #show 
            #print("show")
            Muestra(quadEnNum[1])
        elif op == 31: #Flavour
            #print("flavour")
            Sabroso(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 32: #ration
            #print("Ratio")
            Racion(quadEnNum[1])
        elif op == 33: #DRWCUP
            #print("drwCup")
            DibujaPastel(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 34: #DRWCane
            #print("drwCane")
            if len(auxCoords) == 2:
                DibujaLinea(auxCoords[0],auxCoords[1],quadEnNum[1],quadEnNum[2])
                auxCoords.clear()
            else:
                auxCoords.append(quadEnNum[1])
                auxCoords.append(quadEnNum[2])
        elif op == 35: #DRWChoc
            #print("drwChoc")
            if len(auxCoords) == 2:
                DibujaBarra(auxCoords[0],auxCoords[1],quadEnNum[1],quadEnNum[2])
                auxCoords.clear()
            else:
                auxCoords.append(quadEnNum[1])
                auxCoords.append(quadEnNum[2])            
        elif op == 36: #READ
            print("read")
        elif op == 40: #param
            #print("PARAM")
            CargaParam(quadEnNum[1])
            #arrParams.append(quadEnNum[1])
        elif op == 41: #ERA
            #print("ERA")
            InFuncall = True
            #Checar los pcTemps para ver de donde es la llamada
            CargaERA( quadEnNum[2])

        elif op == 42: #GOSUB
            #print("GOsub")
            CargaParamsYVariables(quadEnNum[2])
        elif op == 43: #ENDPROC
            #print("ENDPROC")
            InFuncall = False
            #pc = pcTemps.pop()
            AcabaLlamadaAFunc()
        elif op == 44: #return
            #print("RETooN")
            InFuncall = False
            AcabaLlamadaAFunc(quadEnNum[3],quadEnNum[1])
        elif op == 50:
            print("VerArr")
            VerificaArr(quadEnNum[1],quadEnNum[2],quadEnNum[3])
        elif op == 51:
            print("SumaBase")
            SumaBase(quadEnNum[1],quadEnNum[2],quadEnNum[3])
            SumaBaseArr = True

        #Aumenta el Program Counter
        pc = pc + 1  

    print("Ejecucion Terminada")
    printLog("Ejecucion Terminada")
    pass

def VerificaArr(dirIndice,dirLB,dirUB):
    global quads
    global pc
    pos = SacaValorDict(dirIndice)
    LB = SacaValorDict(dirLB)
    UB = SacaValorDict(dirUB)

    if pos< LB or pos> UB:
        pc = len(quads)
        printLog("Index out of range")

    pass
def SumaBase(base,dirIndice,dirRes):
    pos = SacaValorDict(dirIndice)
    pos = base + pos
    AgregaValorDict(dirRes,pos) #Agrega la direccion en la temporal de suma
    pass

def CargaParam(p):
    global arrParams
    #val = SacaValorDict(p)
    arrParams.append(SacaValorDict(p))
    pass

#Recibe el tamaño(Cant. Espacio de Memoria) de la funcion e Inicia lo cont
def CargaERA(tam):
    global EspacioMemoriaLocal
    global pcTemps
    global MemLocalDormida
    global LocalMemDic
    global dirMemLocal #20000

    #Establece la cantidad de memoria que va a ocupar la funcion
    EspacioMemoriaLocal = tam


    pass

def AcabaLlamadaAFunc(dirGlobal=None ,dirRet=None):
    global EspacioMemoriaLocal
    global LocalMemDic
    global MemLocalDormida
    global pc

    if dirRet != dirGlobal: #Si ambos son NONE, no hubo return(44)
        val = SacaValorDict(dirRet) #Valor de retorno de una funcion
        #Necesito la DIR GLOBAL DE LA FUNCION
        AgregaValorDict(dirGlobal,val) 

    LocalMemDic.clear()
    pc = pcTemps.pop()
    #Checar si ya es regreso a Ejecucion Principal
    if len(pcTemps) > 0: #Aun queda otra FuncionIncompleta
        LocalMemDic = MemLocalDormida.pop()



    pass

def CargaParamsYVariables(salto):
    global EspacioMemoriaLocal#tamaño
    global arrParams
    global dirMemLocal #20000
    global LocalMemDic
    global MemLocalDormida
    global pcTemps
    global pc

    if len(pcTemps) >0: #Hay un llamada dentro de una funcion
        #Guarda en ARREGLO el DIC de la que se duerme
        aux = LocalMemDic
        MemLocalDormida.append(aux)
        LocalMemDic = {}
        dirMemLocal = 20000
    
    #Carga en MemLocal los parametros en sus direcciones correspondientes
    while EspacioMemoriaLocal >0:
        if len(arrParams) > 0: #Agrega los valores segun se mandaron en los quads
            #print("dCarga Params")
            LocalMemDic[dirMemLocal] =  arrParams.pop()
            dirMemLocal = dirMemLocal + 1
        else:
            #El resto del tamaño se define como vacio
            LocalMemDic[dirMemLocal] = None
            dirMemLocal = dirMemLocal + 1

        EspacioMemoriaLocal = EspacioMemoriaLocal -1

    dirMemLocal = 20000
    #Guarda la direccion de regreso
    pcTemps.append(pc)
    arrParams.clear()
    #Se resta porque despue en IniciaEjecucion se le suma uno
    pc = salto - 1
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
    #Si el valor es verdadero salta
    checa = bDic[checa]
    if checa:
        pc = NewPC - 1
    pass
def GotoF(checa, NewPC):
    global pc
    #Si el valor es falso, salta
    checa = bDic[checa]
    if not checa:
        pc = NewPC - 1
    pass

def Assigna(dirA,dirRes):
    global SumaBaseArr
    if SumaBaseArr:
        dirRes = SacaValorDict(dirRes)
        SumaBaseArr = False

    res = SacaValorDict(dirA)
    AgregaValorDict(dirRes,res)
    print("Assigna----->",res,dirRes)
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
    global SumaBaseArr
    if SumaBaseArr:
        dir = SacaValorDict(dir)
        SumaBaseArr = False

    val = SacaValorDict(dir)
    #print(val)
    printLog(val)
    pass
def Sabroso(dirR,dirG,dirB):
    global t 
    #Recibe los calores y los cambia en las variables globales de turtle
    r = SacaValorDict(dirR)
    g = SacaValorDict(dirG)
    b = SacaValorDict(dirB)
    t.color(r,g,b)

    pass
def Racion(dir):
    global ration
    ration = SacaValorDict(dir)
    pass
def DibujaPastel(dirRad,dirX,dirY):
    global t 
    global ration
    rad = SacaValorDict(dirRad)
    t.setx( SacaValorDict(dirX))
    t.sety( SacaValorDict(dirY))

    t.down()
    t.circle(rad*ration)
    t.up()
    t.home()
    pass
def DibujaLinea(dirX1,dirY1,dirX2,dirY2):
    global t
    global ration
    
    x1 = SacaValorDict(dirX1)
    y1 = SacaValorDict(dirY1)
    x2 = SacaValorDict(dirX2)
    y2 = SacaValorDict(dirY2)

    #Mueve el cursos a donde debe de inicar
    t.goto(x1,y1)
    t.down()
    t.goto(x2*ration,y2*ration)

    t.up()
    t.home()

    pass
def DibujaBarra(dirX1,dirY1,dirX2,dirY2):
    global t
    global ration

    x1 = SacaValorDict(dirX1)
    y1 = SacaValorDict(dirY1)
    x2 = SacaValorDict(dirX2)
    y2 = SacaValorDict(dirY2)


    #Mueve el cursos a donde debe de inicar
    t.goto(x1,y1)
    #Pone el lapiz para escribir
    t.down()
    t.fd(x2*ration)
    t.lt(90)
    t.fd(y2*ration)
    t.lt(90)
    t.fd(x2*ration)
    t.lt(90)
    t.fd(y2*ration)
    t.up()
    t.home()
    pass
def Lee():
    #Pues lee en algo
    pass




#Agrega en un valor en la direccion que se provee como argumentos
#Utilizando los dicionarios, en caso de no estar definido el espacio se creay guarda
def AgregaValorDict(dir,valor):
    global iDic
    global fDic
    global sDic
    global bDic
    global LocalMemDic
    #Checa si es entero
    if dir>= 10000 and dir< 12500  or dir>= 30000 and dir< 32500 or dir>= 40000 and dir< 42500:
        iDic[dir] = int(valor)
    #Checa si es flotante
    if dir>= 12500 and dir< 15000  or dir>= 32500 and dir< 35000 or dir>= 42500 and dir< 45000:
        fDic[dir] = float(valor)
    #Checa si es String
    if dir>= 15000 and dir< 17500  or dir>= 35000 and dir< 37500 or dir>= 45000 and dir< 47500:
        if dir not in sDic.keys():
            valor = valor[1:-1]
        sDic[dir] = valor
    #Checa si es booleano
    if dir>= 17500 and dir< 20000 or dir>= 37500 and dir< 40000 or dir>= 47500 and dir< 50000:
        if type(valor ) is str:
            valor.lower()
        if valor == "yes" or valor :
            bDic[dir] = True
        if valor == "no"  or not valor: 
            bDic[dir] = False

    if dir>= 20000 and dir< 22500 or dir>= 22500 and dir< 25000 or dir>= 25000 and dir< 27500 :
        LocalMemDic[dir] = valor
    elif  dir>= 27500 and dir< 30000:
        if type(valor ) is str:
            valor.lower()
        if valor == "yes" or valor :
            LocalMemDic[dir] = True
        if valor == "no"  or not valor: 
            LocalMemDic[dir] = False


    pass
#Con la direccion Obtiene el valor del diccionario Correspondiente
#En caso de no tener un valor asignado, regresa un valor por defecto y avisa en consola
def SacaValorDict(dir):
    global iDic
    global fDic
    global sDic
    global bDic
    global LocalMemDic
    global pc
    global quads

    #Checa si es entero para regresarlo
    
    if dir>= 10000 and dir< 12500 or dir>= 20000 and dir< 22500 or dir>= 30000 and dir< 32500 or dir>= 40000 and dir< 42500:
        try: 
            return iDic[dir] 
        except KeyError :
            try:
                return LocalMemDic[dir]
            except KeyError:
                print("Warning: Variable no Inicializada")
                printLog("Warning: Variable no Inicializada")
                return 0
    #Checa si es flotante para regresarlo
    if dir>= 12500 and dir< 15000 or dir>= 22500 and dir< 25000 or dir>= 32500 and dir< 35000 or dir>= 42500 and dir< 45000:
        try:
            return fDic[dir] 
        except KeyError:
            try:
                return LocalMemDic[dir]
            except KeyError:
                print("Warning: Variable no Inicializada")
                printLog("Warning: Variable no Inicializada")
                return 0.0
    #Checa si es String para regresarlo
    if dir>= 15000 and dir< 17500 or dir>= 25000 and dir< 27500 or dir>= 35000 and dir< 37500 or dir>= 45000 and dir< 47500:
        try:
            return sDic[dir]
        except KeyError:
            try:
                return LocalMemDic[dir]
            except KeyError:
                print("Warning: Variable no Inicializada")
                printLog("Warning: Variable no Inicializada")
                return ""
    #Checa si es booleano para regresarlo
    if dir>= 17500 and dir< 20000 or dir>= 27500 and dir< 30000 or dir>= 37500 and dir< 40000 or dir>= 47500 and dir< 50000:
        try:
            return bDic[dir]
        except KeyError:
            try:
                return LocalMemDic[dir]
            except KeyError:
                print("Warning: Variable no Inicializada")
                printLog("Warning: Variable no Inicializada")
                return False
 
root = tk.Tk()
#app = App(root)
root.title("Program FOOD")
dialog_frame = tk.Frame(root)
dialog_frame.pack()
#Area de codigo


consola = tk.Text(dialog_frame,height = 5)
consola.pack(side="bottom")
#codigo = tk.Text(dialog_frame)
codigo = tk.scrolledtext.ScrolledText(dialog_frame)
codigo.pack(side="bottom")

tk.Button(dialog_frame,text='Compilar',command = LoadProgram).pack(side="top")
#Carga el programa desde el ultimo que se corrio
arch = open("test.txt","r")
codigo.insert("1.0",arch.read())
arch.close()
#Btn para ejectuar
tk.Button(dialog_frame,text='Ejecutar',command =EjecutarPrograma ).pack(side="top")
tk.Label(dialog_frame,text="Escribe tu codigo abajo").pack(side="top")

lblAviso = tk.Label(dialog_frame,text="Resultados de compilacion")
lblAviso.pack(side="left")
#BTN de cierre
tk.Button(dialog_frame, text="Cerrar", command=quit).pack(side="right")


root.mainloop()
t.screen.mainloop()


