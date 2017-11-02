//Cargar quads a arreglo 
String [] quads; 
int i = 0;

IntDict iDic = new IntDict();
FloatDict fDic = new FloatDict();
StringDict sDic = new StringDict();
//Manejo logico mas complejo por solo tener una lista, secuencial
//Tres listas de booleanos (?)
ArrayList<Boolean> bDic = new ArrayList<Boolean>();


int [] ops ; 
int [] op;
int cp = 0;


void setup(){
  quads = loadStrings("quads.txt");
  op = GetOperand(quads[cp]); //Obtiene el primer comando del primer quad
  println(ops);
  //op = ops[0];
  println("Op:"+ op);
  
}

void draw(){
  
   switch(op[0]){
     case 0: //Sum
        println("sum");
        
        //ops = SumaOp(quads[cp]);
        
        break;
     case 1: //res
        break;
     case 2: //Multi
        break;
     case 3: //Div
        break;
     case 4: //asignacion 
        break;
      case 25:
        print("Goto");
        //ops = GetGoto(quads[cp]);
        cp = op[3] -1; //por logica necesita restar uno
        PrintArr(op);
        break;
      case 26: //GotoV
        break;
      case 27: //GotoF
        break;
      case 30: //Show
        break;
      case 31: //Flavor
        break;
      case 32: //Ration
        break;
      case 33: //DrwCup
        break;
      case 34: //DrwCane
        break;
      case 35: //DrwChoc
        break;
      case 40: //Param
        break;
      case 41: //ERA
        break;
      case 42: //GOSUB
        break;
      case 43: //Retorno
        break;
    }
    
  cp += 1;
  println("--->Este es el cp",cp);
  if( cp == quads.length-1){
    print("Termino programa con Exito");
    exit();
  }
  op = GetOperand(quads[cp]);
}

void PrintArr(int[] arr){  int i; print("PRArrI"); for (i =0; i< arr.length;i++){    print(arr[i]," ");  } println("");}
void PrintArr(String[] arr){  int i; print("PRArrS"); for (i =0; i< arr.length;i++){  print(arr[i]);  } println(""); }

void SumaOp(int dirA,int dirB,int posRes){
  print("Entra a sumar en suma");
  //Se obtienen los tipos de los datos
  int a = getDict(dirA);
  int b = getDict(dirB);
  if (a == 0 && b==0){
    int valA = iDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    //putiDictValue(posRes, valA + valB);
    iDic.set(str(posRes),valA + valB);
  }else if(a== 0 && b==1 ){
    int valA = iDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    //putfDictValue(posRes,float(valA) + valB);
    fDic.set(str(posRes),float(valA) + valB);
  }else if(a== 1 && b==0 ){
    float valA = fDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    //putfDictValue(posRes,valA + float(valB));
    fDic.set(str(posRes),valA + float(valB));
  }else if(a== 1 && b==1 ){
    float valA = fDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    //putfDictValue(posRes, valA + valB);
    fDic.set(str(posRes),valA + valB);
  }

}

//Funcion que no se usar, despreciadad
int[] GetGoto(String q){
  String cp = q.replace('[','\b'); cp = cp.replace(']','\b'); cp = cp.trim();
  //println("cp:"+cp);
  String [] ops = split(cp,",");
  int op = getInt(ops[0]); //Operador 1 de quad
  println("GOTOop:"+op);
  int right_op = getInt(ops[1]); //Operador 2 de quad
  int left_op = getInt(ops[2]); //Operador 3 de quad
  int res = getInt(ops[3]); //Operador 4 de quad
  
  int [] operands = {op,right_op,left_op,res};
  return operands;
}

int [] GetOperand(String q){
  String cp = q.replace('[','\b');  cp = cp.replace(']','\b');  cp = cp.trim();
  println("cp:"+cp);
  String [] ops = split(cp,",");
  PrintArr(ops);
  //int op = Integer.parseInt(ops[0]);
  int op = getInt(ops[0]); //Operador 1 de quad
  int right_op = getInt(ops[1]); //Operador 2 de quad
  int left_op = getInt(ops[2]); //Operador 3 de quad
  int res = getInt(ops[3]); //Operador 4 de quad
  //println("GOop:"+op);
  //return op;
  int [] operands = {op,right_op,left_op,res};
  return operands;
}

int getInt(String s){
  int ent;
  try {
    ent = Integer.parseInt(s.trim());
  } catch (NumberFormatException e) {
    //e.printStackTrace();
    println("Esto no es un dirVir "+s);
    ent = -1;
    //exit();
  }
  
 return ent; 
}
//Regresa a que tipo de diccionario pertenece
int getDict(int dir){
    //Clasificar las direcciones para buscar en los diccionarios
  //Checar si esEntera
  if(dir>= 10000 &&dir<12500 ||dir>= 30000 &&dir< 32500 ||dir>= 40000 &&dir< 42500){
    return 0;
  }
  //Checar si es Flotante
  if(dir>= 12500 &&dir< 15000  ||dir>= 32500 &&dir< 35000 ||dir>= 42500 &&dir< 45000 ){
    return 1;
  }
  //Checar si es String
  if(dir>= 15000 &&dir< 17500  ||dir>= 35000 &&dir< 37500 ||dir>= 45000 &&dir< 47500 ){
    return 2;
  }
  //Checar si es Booleana
  //Posible conlficto,  
  if(dir>= 17500 &&dir< 20000  ){
    dir = dir - 17500;
    return 3;
  }else if(dir>= 37500 &&dir< 40000 ){
    dir = dir - 37500;
    return 3;
  }else if(dir>= 47500 &&dir< 50000){
    dir = dir - 47500;
    return 3;
  }
  return -1;
}
/*
int getiDictValue(int dir){
    //Clasificar las direcciones para buscar en los diccionarios
  //Checar si esEntera
  if(dir>= 10000 &&dir<12500 ||dir>= 30000 &&dir< 32500 ||dir>= 40000 &&dir< 42500){
    return iDic.get(str(dir));
  } 
}
void putiDictValue(int dirRes,int val){
  iDic.set(str(dirRes),val);
}
float getfDictValue(int dir){
    //Clasificar las direcciones para buscar en los diccionarios
  //Checar si es Flotante
  if(dir>= 12500 &&dir< 15000  ||dir>= 32500 &&dir< 35000 ||dir>= 42500 &&dir< 45000 ){
    return fDic.get(str(dir));
  }
}
void putfDictValue(int dirRes,float val){
  fDic.set(str(dirRes),val);
}
String getsDictValue(int dir){
    //Clasificar las direcciones para buscar en los diccionarios
  //Checar si es String
  if(dir>= 15000 &&dir< 17500  ||dir>= 35000 &&dir< 37500 ||dir>= 45000 &&dir< 47500 ){
    return sDic.get(str(dir));
  }
}
void putsDictValue(int dirRes,String val){
  sDic.set(str(dirRes),val);
}
Boolean getbDictValue(int dir){
    //Clasificar las direcciones para buscar en los diccionarios
  //Checar si es Booleana
  //Posible conlficto,  
  if(dir>= 17500 &&dir< 20000  ){
    dir = dir - 17500;
    return bDic.get(dir);
  }else if(dir>= 37500 &&dir< 40000 ){
    dir = dir - 37500;
    return bDic.get(dir);
  }else if(dir>= 47500 &&dir< 50000){
    dir = dir - 47500;
    return bDic.get(dir);
  }
}
*/
//Conflictos
void putbDictValue(int dirRes,Boolean val){
  if(dirRes>= 17500 && dirRes< 20000  ){
    //dir = dir - 17500;
    bDic.add(val);
  }else if(dirRes>= 37500 && dirRes< 40000 ){
    //dir = dir - 37500;
    bDic.add(val);
  }else if(dirRes>= 47500 && dirRes< 50000){
    //dir = dir - 47500;
    bDic.add(val);
  }
}

void putDictValue(int dir){

}