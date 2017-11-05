//Cargar quads a arreglo 
String [] quads; 
int i = 0;
int dirConsts=0; //Direccion donde empiezan constantes
int iGlobal=0;
float fGlobal=0.0;
String sGlobal="";
Boolean bGlobal = true;

IntDict iDic = new IntDict();
FloatDict fDic = new FloatDict();
StringDict sDic = new StringDict();

//Manejo logico mas complejo por solo tener una lista, secuencial
//Cuatro listas de booleanos (?)
ArrayList<Boolean> bDicGlobal = new ArrayList<Boolean>();
ArrayList<Boolean> bDicLocal = new ArrayList<Boolean>();
ArrayList<Boolean> bDicTemp = new ArrayList<Boolean>();
ArrayList<Boolean> bDicConst = new ArrayList<Boolean>();


int [] ops ; //Arreglo de enteros extra
int [] op; //Arreglo que maneja el cuadruplo en numeros enteros
int cp = 0;


void setup(){
  quads = loadStrings("quads.txt");
  op = GetOperand(quads[cp]); //Obtiene el primer comando del primer quad
  //println(op);
  //op = ops[0];
  dirConsts = findIndex(quads,"%%"); //Encuentra el comienzo de las constantes
  println("Op:", op);
  
  loadConst(dirConsts); //Carga las constantes a memoria
  
}

void draw(){
  
   switch(op[0]){
     case 0: //Sum
        println("sum");
        SumaOp(op[1],op[2],op[3]);
        //exit(); //For test
        break;
     case 1: //res
        //println("res");
        RestaOp(op[1],op[2],op[3]);
        break;
     case 2: //Multi
        //println("Multi");
        MultiOp(op[1],op[2],op[3]);
        break;
     case 3: //Div
        //println("Div");
        DivOp(op[1],op[2],op[3]);
        break;
     case 4: //asignacion 
        println("Assi");
        AssignOp(op[1],op[3]);
        break;
      case 25:
        print("Goto");
        //ops = GetGoto(quads[cp]);
        cp = op[3] -1; //por logica necesita restar uno
        //PrintArr(op);
        break;
      case 26: //GotoV-
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
      case 44: //VerArr
        VerificaArr(op[1],op[2],op[3]);
        break;
    }
    
  cp += 1;
  //println("--->Este es el cp",cp);
  if( cp == dirConsts){
    println("Termino programa con Exito");
    println(iDic);
    println(fDic);
    println(sDic);
    exit();
  }else{
    op = GetOperand(quads[cp]);
  }
}

void PrintArr(int[] arr){  int i; print("PRArrI"); for (i =0; i< arr.length;i++){    print(arr[i]," ");  } println("");}
void PrintArr(String[] arr){  int i; print("PRArrS"); for (i =0; i< arr.length;i++){  print(arr[i]);  } println(""); }

//Obtiene las direcciones de los valores que va a sumar, los mapea, los suma y agrega al dicc
void SumaOp(int dirA,int dirB,int posRes){
  print("Entra a sumar en suma");
  //Se obtienen los tipos de los datos
  int a = getDict(dirA); //Obtiene el diccionario al que pertenece la direccion
  int b = getDict(dirB);
  if (a == 0 && b==0){
    int valA = iDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    iGlobal = valA + valB;
    putDictValue(posRes);
    println("ESte es el resultado de summa-->",iGlobal);
  }else if(a== 0 && b==1 ){
    int valA = iDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA + valB;
    putDictValue(posRes);
    println("ESte es el resultado de summa-->",fGlobal);
  }else if(a== 1 && b==0 ){
    float valA = fDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    fGlobal = valA + valB;
    putDictValue(posRes);
    println("ESte es el resultado de summa-->",fGlobal);
  }else if(a== 1 && b==1 ){
    float valA = fDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA + valB;
    putDictValue(posRes);
    println("ESte es el resultado de summa-->",fGlobal);
  }
}
//Obtiene las direcciones de los valores que va a resta, los mapea, los resta y agrega al dicc
void RestaOp(int dirA,int dirB,int posRes){
  print("Entra a restar en resta");
  //Se obtienen los tipos de los datos
  int a = getDict(dirA);//Obtiene el diccionario al que pertenece la direccion
  int b = getDict(dirB);
  if (a == 0 && b==0){
    int valA = iDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    iGlobal = valA - valB;
    putDictValue(posRes);
    //putiDictValue(posRes, valA + valB);
    //iDic.set(str(posRes),valA + valB);
  }else if(a== 0 && b==1 ){
    int valA = iDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA - valB;
    putDictValue(posRes);
    //putfDictValue(posRes,float(valA) + valB);
    //fDic.set(str(posRes),float(valA) + valB);
  }else if(a== 1 && b==0 ){
    float valA = fDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    fGlobal = valA - valB;
    putDictValue(posRes);
    //putfDictValue(posRes,valA + float(valB));
    //fDic.set(str(posRes),valA + float(valB));
  }else if(a== 1 && b==1 ){
    float valA = fDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA - valB;
    putDictValue(posRes);
    //putfDictValue(posRes, valA + valB);
    //fDic.set(str(posRes),valA + valB);
  }
}
//Obtiene las direcciones de los valores que va a multiplicar, los mapea, los multiplica y agrega al dicc
void MultiOp(int dirA,int dirB,int posRes){
  print("Entra a Multiplicar en Multi");
  //Se obtienen los tipos de los datos
  int a = getDict(dirA);//Obtiene el diccionario al que pertenece la direccion
  int b = getDict(dirB);
  if (a == 0 && b==0){
    int valA = iDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    iGlobal = valA * valB;
    putDictValue(posRes);
    //putiDictValue(posRes, valA + valB);
    //iDic.set(str(posRes),valA + valB);
  }else if(a== 0 && b==1 ){
    int valA = iDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA * valB;
    putDictValue(posRes);
    //putfDictValue(posRes,float(valA) + valB);
    //fDic.set(str(posRes),float(valA) + valB);
  }else if(a== 1 && b==0 ){
    float valA = fDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    fGlobal = valA * valB;
    putDictValue(posRes);
    //putfDictValue(posRes,valA + float(valB));
    //fDic.set(str(posRes),valA + float(valB));
  }else if(a== 1 && b==1 ){
    float valA = fDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA * valB;
    putDictValue(posRes);
    //putfDictValue(posRes, valA + valB);
    //fDic.set(str(posRes),valA + valB);
  }
}
//Obtiene las direcciones de los valores que va a dividir, los mapea, los divide y agrega al dicc
void DivOp(int dirA,int dirB,int posRes){
  print("Entra a dividir en divide");
  //Se obtienen los tipos de los datos
  int a = getDict(dirA);//Obtiene el diccionario al que pertenece la direccion
  int b = getDict(dirB);
  if (a == 0 && b==0){
    int valA = iDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    iGlobal = valA / valB;
    putDictValue(posRes);
    //putiDictValue(posRes, valA + valB);
    //iDic.set(str(posRes),valA + valB);
  }else if(a== 0 && b==1 ){
    int valA = iDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = float(valA) / valB;
    putDictValue(posRes);
    //putfDictValue(posRes,float(valA) + valB);
    //fDic.set(str(posRes),float(valA) + valB);
  }else if(a== 1 && b==0 ){
    float valA = fDic.get(str(dirA));
    int valB = iDic.get(str(dirB));
    fGlobal = valA / float(valB);
    putDictValue(posRes);
    //putfDictValue(posRes,valA + float(valB));
    //fDic.set(str(posRes),valA + float(valB));
  }else if(a== 1 && b==1 ){
    float valA = fDic.get(str(dirA));
    float valB = fDic.get(str(dirB));
    fGlobal = valA / valB;
    putDictValue(posRes);
    //putfDictValue(posRes, valA + valB);
    //fDic.set(str(posRes),valA + valB);
  }
}

int [] GetOperand(String q){
  String cp = q.replace('[','\b');  cp = cp.replace(']','\b');  cp = cp.trim();
  //println("cp:"+cp);
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

//Transofrma un string en int, regresando -1 si no es string transformable
int getInt(String s){
  int ent;
  try {
    ent = Integer.parseInt(s.trim());
  } catch (NumberFormatException e) {
    //e.printStackTrace();
    //println("->Esto no es un dirVir "+s);
    ent = -1;
    //exit();
  }
  
 return ent; 
}
float getFloat(String s){
  float flo;
  try {
    flo = Float.parseFloat(s.trim());
  } catch (NumberFormatException e) {
    //e.printStackTrace();
    //println("->Esto no es un dirVir "+s);
    flo = -1.0;
    //exit();
  }
  
 return flo; 
}

//Regresa a que tipo de diccionario pertenece, aka regresa el tipo de dato
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
    return 3;
  }else if(dir>= 37500 &&dir< 40000 ){
    return 3;
  }else if(dir>= 47500 &&dir< 50000){
    return 3;
  }
  return -1;
}

//Agrega un valor en la direccion correspondiente
void putDictValue(int dir){
  //Agrega los valores en los diccionarios segun las direcciones de ubicacion
  if (dir>= 10000 &&dir<12500){ //Entera Global
    iDic.set(str(dir),iGlobal);
  }else if(dir>= 12500 &&dir< 15000){ //Flotante Global
    fDic.set(str(dir),fGlobal);
  }else if(dir>= 15000 &&dir< 17500){ //String Global
    sDic.set(str(dir),sGlobal);
  }else if(dir>= 17500 &&dir< 20000){ //Booleanas Globales_ Base: 17500
    dir = dir - 17500;
    bDicGlobal.add(bGlobal);
  }else if(dir>= 30000 &&dir< 32500){ //Entera Temporales
    iDic.set(str(dir),iGlobal);
  }else if(dir>= 32500 &&dir< 35000){ //Flotantes Temporales
    fDic.set(str(dir),fGlobal);
  }else if(dir>= 35000 &&dir< 37500){ //Strings Temporales
    sDic.set(str(dir),sGlobal);
  }else if(dir>= 37500 &&dir< 40000){ // Booleanas Temporales Base: 37500
    dir = dir - 37500;
    bDicTemp.add(bGlobal);
  }else if(dir>= 40000 &&dir< 42500){ //Enteras Constantes
    iDic.set(str(dir),iGlobal);
  }else if(dir>= 42500 &&dir< 45000){ //Flotantes Constantes
    fDic.set(str(dir),fGlobal);
  }else if(dir>= 45000 &&dir< 47500){ //Strings Constantes
    sDic.set(str(dir),sGlobal);
  }else if(dir>= 47500 &&dir< 50000){ //Booleanas Constantes Base: 47500
    dir = dir - 47500;
    bDicConst.add(bGlobal);
  }else{ //Booleanas Constantes
    println("MEMORY OVERFLOW");
    exit();
  }
}

int findIndex(String [] arr,String x){
  int index ;
  for (index =0;index<arr.length;index++){
    if(arr[index].equals(x)){
      return index;
    }
  }
  return -1;
}

/**
*AssignOp
* Consultando las direcciones de memoria para sacar el contenido
* C
* @param  int dirVal : Direccion del valor a asignar
* @param  int dirAssign : Direccion del valor que toma la asignacion
*/
void AssignOp(int dirVal,int dirAssign){
  //Clasificar las direcciones para buscar en los diccionarios y asignar
  if (dirVal>= 10000 && dirVal<12500){ //Entera Global
    iGlobal = iDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 12500 &&dirVal< 15000){ //Flotante Global
    fGlobal = fDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 15000 &&dirVal< 17500){ //String Global
    sGlobal = sDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 17500 &&dirVal< 20000){ //Booleanas Globales_ Base: 17500
    //Buscar el indice del valor
    dirVal = dirVal - 17500;
    bGlobal = bDicGlobal.get(dirVal);
    putDictValue(dirAssign); //*******DHECAR LA FUNCION ADD

  }else if(dirVal>= 30000 &&dirVal< 32500){ //Entera Temporales
    iGlobal = iDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 32500 &&dirVal< 35000){ //Flotantes Temporales
    fGlobal = fDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 35000 &&dirVal< 37500){ //Strings Temporales
    sGlobal = sDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 37500 &&dirVal< 40000){ // Booleanas Temporales Base: 37500
    dirVal = dirVal - 37500;
    bGlobal = bDicTemp.get(dirVal);
    putDictValue(dirAssign);
    //bDicTemp.add(bGlobal);
  }else if(dirVal>= 40000 &&dirVal< 42500){ //Enteras Constantes
    iGlobal = iDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 42500 &&dirVal< 45000){ //Flotantes Constantes
    fGlobal = fDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 45000 &&dirVal< 47500){ //Strings Constantes
    sGlobal = sDic.get(str(dirVal));
    putDictValue(dirAssign);
  }else if(dirVal>= 47500 &&dirVal< 50000){ //Booleanas Constantes Base: 47500
    dirVal = dirVal - 47500;
    bGlobal = bDicConst.get(dirVal);
    putDictValue(dirAssign);
    //bDicConst.add(bGlobal);
  }else{ //Booleanas Constantes
    println("MEMORY OVERFLOW");
    exit();
  }
}

void loadConst(int p){
  int i,dir;
  print("ENTRO A LOAD CONST ");
  //println(p);
  String cp ;
  String aux;
  int tipo;
  for (i =p+1; i<quads.length;i++){
    cp = quads[i].replace('[','\b');  cp = cp.replace(']','\b');  cp = cp.trim();
   // println("const Eval:"+cp);
    String [] ops = split(cp,",");
    //Segun la direccion de memoria, puedo saber que tipo es y como parsearlo
    dir = getInt(ops[1]);
    tipo = getDict(dir);
    if (tipo == 0){ //es int
      iGlobal = getInt(ops[0]);
     // print("Const Entero: "); println(iGlobal);
      putDictValue(dir); //Meter al diccionario
    } else if( tipo == 1){ //float
      fGlobal = getFloat(ops[0]);
      //print("Const float: "); println(fGlobal);
      putDictValue(dir); //Meter al diccionario
    } else if( tipo == 2){
      sGlobal = ops[0].trim();
      //print("Const String: "); println(sGlobal);
      putDictValue(dir); //Meter al diccionario
    } else if (tipo == 3){ //Booleano
      aux = ops[0].trim();
      if (aux.equals("yes")){
         bGlobal = true; 
      } else{
        bGlobal = false; 
      }
      //print("contstante Bool: "); println(bGlobal);
      putDictValue(dir); //Meter al diccionario
    }


  }
  //exit(); //For test purpose
}

void VerificaArr(int index, int LimI, int LimS){
  try{
  index = iDic.get(str(index));
  } catch(IllegalArgumentException e){
    println("Null Pointer Exception");
    print(e);
    exit();
  }
  LimI = iDic.get(str(LimI));
  LimS = iDic.get(str(LimS));
 if(index < LimI || index >LimS){
   println("Index out of bounds");
   exit();
   
 }
}