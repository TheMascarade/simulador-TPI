from enum import Enum


class Estado(Enum):
    Nuevo = 0
    Listo = 1
    Ejecutando = 2
    Suspendido = 3
    Terminado = 4

class Proceso:
    def __init__(self, id, tam, tArribo, tIrrupcion):
        self.id = id
        self.arribo = tArribo
        self.irrupcion = tIrrupcion
        self.tam = tam
        self.estado = Estado.Nuevo

    def DescontarIrrupcion(self):
        self.irrupcion -= 1
    

    def __str__(self) -> str:
        return str(self.id)+str(self.arribo)+str(self.irrupcion)+str(self.tam)+str(self.estado.value)