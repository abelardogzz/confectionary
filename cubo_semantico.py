from enum import Enum
class Types(Enum):
	I = 0 #INT
	F = 1 #Float
	S = 2 #String
	Sum = 0
	Minus = 1
	Times = 2
	Div = 3
	ERR = 999


CuboSemantico = [
  #INT
    #  +, -, *, /, =, ==, !=, >, <, =>, =<, ||, &&, /13
    [[ 0, 0, 0, 0, 1,  3,  3, 3, 3,  3,  3,  3,  3], #INT
     [ 1, 1, 1, 1, 1,  3,  3, 3, 3,  3,  3,  3,  3], #FLOAT
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], # STRING
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99] ], #BOOL  
  #FLOAT
    #  +, -, *, /, =, ==, !=, >, <, =>, =<, ||, &&, /13
    [[ 1, 1, 1, 1, 1,  3,  3, 3, 3,  3,  3, 99, 99], #INT
     [ 1, 1, 1, 1, 1,  3,  3, 3, 3,  3,  3,  3,  3], #FLOAT
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], # STRING
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99]],#Bool
  #String             #Comparacion de longitud
    #  +, -, *, /, =, ==, !=, >, <, =>, =<, ||, &&, /13
    [[99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], #INT
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], #FLOAT
     [ 2, 2,99,99, 2,  3,  3, 3, 3,  3,  3, 99, 99], # STRING
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99]], #Bool
  #Bool
    #  +, -, *, /, =, ==, !=, >, <, =>, =<, ||, &&, /13
    #  0, 1, 2, 3, 4,  5,  6, 7, 8,  9, 10, 11, 12, /13
    [[99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], #INT 
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], #FLOAY
     [99,99,99,99,99, 99, 99,99,99, 99, 99, 99, 99], #String
     [99,99,99,99,99,  3,  3,99,99, 99, 99,  3,  3]] #Bool
]


#print(CuboSemantico)
#CuboSemantico[Operador][OpIzq][OpDer]
#suma
#print("int + int", CuboSemantico[0][0][0]) 
#print("int + float", CuboSemantico[0][1][0]) 
#print("int + string", CuboSemantico[0][2][0]) 
#print("float + bool", CuboSemantico[0][3][0]) 
#print("float + bool", CuboSemantico[1][3][0]) 

#bool
#print("Bool == bool", CuboSemantico[3][3][5])
#print("Bool != bool", CuboSemantico[3][3][6])
#print("Bool || bool", CuboSemantico[3][3][11])
#print("Bool && bool", CuboSemantico[3][3][12])




