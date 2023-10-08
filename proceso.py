class Estado(Enum):
    Nuevo=1
    Listo=2
    Ejecutando=3
    Bloqueado=4
    Terminado=5
    ListoSuspendido=6
    BloqueadoSuspendido=7


class proceso:
    def __init__(self,id,tArribo,tIrrupcion) :
       
       self.estado=Estado.Nuevo
       pass 

    def liberarMemoria(self):
        pass

    def CambiarEstado(self):
        pass