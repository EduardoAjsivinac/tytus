import sys, os.path
nodo_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\AST\\')
sys.path.append(nodo_dir)

c3d_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\C3D\\')
sys.path.append(c3d_dir)

entorno_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\ENTORNO\\')
sys.path.append(entorno_dir)

from Nodo import Nodo
from Nodo import Nodo
from Entorno import *
from Tipo_Expresion import *
from Tipo import Data_Type
from Tipo import Type
from Label import *
from Temporal import *
from Simbolo import *

class Sentencia_Asignacion(Nodo):

    def __init__(self, nombreNodo, fila = -1, columna = -1, valor = None):
        Nodo.__init__(self,nombreNodo, fila, columna, valor)
    
    def execute(self, enviroment):

        identificador = self.hijos[0]
        expresion = self.hijos[1]
        value = expresion.execute(enviroment)

        nombreVariableAsignar = identificador.valor.lower()
        variableBuscar = enviroment.obtenerSimbolo(nombreVariableAsignar)

        if variableBuscar == None :
            print('Error al buscar variable')
        else :
            
            if variableBuscar.data_type.data_type == expresion.tipo.data_type :
                variableBuscar.valor = value
            else:
                print('Error: No coincide el tipo de dato')


        pass
    
    def compile(self, enviroment):
        
        codigoCompile = ''
        identificador = self.hijos[0]
        expresionExecute = self.hijos[1]
        value = None
        auxiliar = False

        nombreVariableAsignar = identificador.valor.lower()

        if expresionExecute.nombreNodo == 'SENTENCIA_SELECT':
            value = expresionExecute.execute(enviroment)
            print('Se ejecuto la sentencia select')
            print('Tipo result: ',expresionExecute.tipo.data_type)
        else:
            value = expresionExecute.compile(enviroment)
            auxiliar = True
        
        if auxiliar == True :

            codigoCompile += value
            codigoCompile += nombreVariableAsignar + ' = ' + expresionExecute.dir + '\n'
            return codigoCompile
            
        else:

            if expresionExecute.tipo.data_type == Data_Type.listaDatos :
                codigoCompile += nombreVariableAsignar + ' = None\n'
                return codigoCompile
            else :
                codigoCompile += nombreVariableAsignar + ' = ' + str(value) + '\n'
                return codigoCompile
            
                
            pass

    def getText(self):
        pass