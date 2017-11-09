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
    arch = open("prog.txt","w")
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
def ComienzaProg():
    t= turtle.Turtle()
    #global t
    t.shape("classic")
    t.circle(80)
    t.screen.mainloop()
    pass

def ChangeQuad(q):
    q = q[1:-1] #Quita los brackets
    q = q.split(",")
    print("quady",q)
    q[0] = q[0].strip()
    q[1] = q[1].strip()
    q[2] = q[2].strip()
    q[3] = q[3].strip()
    return q

def EjecutarPrograma():
    const = False
    print("ejecutando programa")
    arch = open("res.txt","r")
    quad = arch.readline()

    while(quad != "%%"):
        quad = ChangeQuad(quad)
        quads.append(quad)
        quad = arch.readline()
    while( quad != ''):
        print(quad)
        quad = arch.readline()
        quad = ChangeQuad(quad)

    arch.close()
    print(quads)
    pass

#Agrega en un valor en la direccion que se provee como argumentos
def AgregaValorDict(dir,valor):
    #Checa si es entero
    if dir>= 10000 and dir< 12500 or dir>= 20000 and dir< 22500 or dir>= 30000 and dir< 32500 or dir>= 40000 and dir< 42500:
        iDic[dir] = valor
    #Checa si es flotante
    if dir>= 12500 and dir< 15000 or dir>= 22500 and dir< 25000 or dir>= 32500 and dir< 35000 or dir>= 42500 and dir< 45000:
        iDic[dir] = valor
    #Checa si es String
    if dir>= 15000 and dir< 17500 or dir>= 25000 and dir< 27500 or dir>= 35000 and dir< 37500 or dir>= 45000 and dir< 47500:
        iDic[dir] = valor
    #Checa si es booleano
    if dir>= 17500 and dir< 20000 or dir>= 27500 and dir< 30000 or dir>= 37500 and dir< 40000 or dir>= 47500 and dir< 50000:
        iDic[dir] = valor

    pass

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

#Btn para ejectuar
tk.Button(dialog_frame,text='Ejecutar',command =EjecutarPrograma ).pack(side="top")
#BTN de cierre
tk.Button(dialog_frame, text="Cerrar", command=quit).pack(side="right")
root.mainloop()