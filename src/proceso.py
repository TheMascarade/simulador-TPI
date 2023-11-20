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
        self.espera = 0 # Tiempo que pasa en el estado de listo
        self.retorno = 0 # Tiempo que pasa entre estado listo y ejecucion
        self.tiempoTerminado=0

    def DescontarIrrupcion(self):
        self.irrupcion -= 1
    

    def __str__(self) -> str:
        return "id:"+self.id+" tiempo de arribo:"+str(self.arribo)+" tiempo restante:"+str(self.irrupcion)+str(self.tam)