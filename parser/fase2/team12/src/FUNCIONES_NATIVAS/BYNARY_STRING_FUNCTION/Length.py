import sys, os.path
import math

dir_nodo = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')) + '\\EXPRESION\\EXPRESION\\')
sys.path.append(dir_nodo)

ent_nodo = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')) + '\\ENTORNO\\')
sys.path.append(ent_nodo)

from Expresion import Expresion
from Tipo import Data_Type
from Tipo_Expresion import Type_Expresion

class Function_Length(Expresion):

    def __init__(self, nombreNodo, fila, columna, valor):
        Expresion.__init__(self, nombreNodo, fila, columna, valor)    
    
    def execute(self, enviroment):
        exp = self.hijos[0]
        valueExp = exp.execute(enviroment)

        if exp.tipo.data_type == Data_Type.character :
            
            self.tipo = Type_Expresion(Data_Type.numeric)            
            self.valorExpresion = len(valueExp)
            return self.valorExpresion

        else :

            self.tipo = Type_Expresion(Data_Type.error)
            self.valorExpresion = None
            return self.valorExpresion
    
    def compile(self, enviroment):
        print("Compile")
    
    def getText(self):
        exp = self.hijos[0]
        stringReturn = 'length(' + exp.getText() + ')'
        return stringReturn