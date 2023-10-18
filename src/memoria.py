from dataclasses import dataclass
from proceso import *

@dataclass
class Particion:
    id: int
    tam: int
    dirComienzo: int
    fragmentacionInterna: int
    ocupado: bool = False
    proceso: Proceso = None

    def calcularFragmentacionActual(self) -> int:
        return self.tam-self.proceso.tam
    def calcularFragmentacion(self,proceso) -> int:
        return self.tam-proceso.tam


    def Mostrar(self):
        print(self.id,", ",self.tam,", ",self.dirComienzo)
        if self.ocupado:
            print("proceso: ",self.proceso.id," frag :",self.calcularFragmentacionActual())
        else:
            print("Sin proceso")


class Memoria:
    def __init__(self,particiones:list()):
        self.particiones = particiones 
        self.noCargados=[None,None]

    def Alocar(self,proceso:Proceso):
        fragmentacionMax=999999
        idParticion=None
        for i in len(self.particiones):
            if (not self.particiones[i].ocupado):
                fragmentacion=self.particiones[i].calcularFragmentacion(proceso)
            if fragmentacion < fragmentacionMax and fragmentacion>0:
                idParticion=i
                
        if idParticion:
            self.particiones[i].proceso=proceso
            self.particiones[i].ocupado=True
            
    def Desalocar(self,proceso):
        for i in len(self.particiones):
            if proceso==self.particiones[i].proceso:
                self.particiones[i].proceso=None
                self.particiones[i].ocupado=False

    def BuscarParticionDisponible(self,proceso:Proceso):
        for particion in self.particiones:
            if (not particion.ocupado) and (particion.tam <= proceso.tam):
                return True
        return False


    def Mostrar(self):
        print("particiones")
        for x in self.particiones:
            x.Mostrar()
