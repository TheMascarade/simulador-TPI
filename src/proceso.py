from enum import Enum


class Estado(Enum):
    NoAdmitido = 0
    Nuevo = 1
    Listo = 2
    Ejecutando = 3
    Bloqueado = 4
    Terminado = 5
    ListoSuspendido = 6
    BloqueadoSuspendido = 7


class Proceso:
    def __init__(self, id, tam, tArribo, tIrrupcion):
        self.id = id
        self.arribo = tArribo
        self.irrupcion = tIrrupcion
        self.tam = tam
        self.estado = Estado.NoAdmitido

    def DescontarIrrupcion(self):
        self.irrupcion -= 1
