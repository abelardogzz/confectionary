//Cargar quads a arreglo 
String [] quads; 
int i = 0;

IntDict iDic = new IntDict();
FloatDict fDic = new FloatDict();
StringDict sDic = new StringDict();
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

void SumaOp(int[] q){
  print("Arre en suma");
  PrintArr(q);
  //return operands;
}

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