# NOTA
# DiscoAlocar() ya verifica si queda espacio en disco asi en el flujo del simulador solamente tenemos que invocar ese metodo para saber si se puede admitir un proceso o no
# Tambien podemos hacer lo mismo con memoria interna si resulta mas facil

from proceso import *

class Memoria:
    def __init__(self, particiones) -> None:
        self.Particiones: list[Particion] = particiones
        self.Disco: list[Proceso] = []
        self.procesosAlmacenados=0


    def TratarAlocar(self, proceso: Proceso):
        # True: alocado en memoria
        # False: alocado en disco
        # None: No pudo ser alocado
        index = None
        frag = 9999999
        # Algoritmo best-fit para ver si podemos alocar
        for particion in self.Particiones:
            if particion.Ocupado==True:
                continue
            fragParticion = particion.GetFragInterna(proceso)
            if fragParticion >= 0 and fragParticion < frag:
                frag = fragParticion
                index = self.Particiones.index(particion)

        if index !=None:
            self.Particiones[index].CargarProceso(proceso) 
            return True
        else:
            if len(self.Disco)<2:
                self.Disco.append(proceso)
                return False
        return None

    def EncontrarParticion(self,proceso):
        #devuelve True si esta en memoria
        #devuelve False si esta en Disco
        #Y si no esta devuelve None
        for part in self.Particiones:
            if proceso == part.Proceso:
                return True
        if proceso in self.Disco:
            return False
        raise("no esta asignado el proceso")

    def PasarAMemoria(self,proceso): 
        self.Disco.remove(proceso) 
        index = None
        frag = 9999999
        for particion in self.Particiones:
            fragParticion = particion.GetFragInterna(proceso)
            if fragParticion >= 0 and fragParticion < frag:
                frag = fragParticion
                index = self.Particiones.index(particion)
        procADisco=self.Particiones[index].Proceso
        self.Disco.append(procADisco)
        procADisco.estado=Estado.Suspendido
        self.Particiones[index].CargarProceso(proceso)
        proceso.estado=Estado.Listo
        return procADisco
        

    def ParticionDisponible(self, proceso: Proceso):
        for particion in self.Particiones:
            if not particion.Ocupado and particion.Tam >= proceso.tam:
                return True
        return False

    def DiscoDisponible(self):
        if len(self.Disco) >= 2:
            return False
        return True

    def DiscoAlocar(self, proceso):
        if self.DiscoQuedaEspacio():
            self.Disco.append(proceso)
            return True
        return False

    def DiscoDesalocar(self, proceso):
        self.Disco.remove(proceso)

    def Desalocar(self, proceso: Proceso):
        index = 0
        for particion in self.Particiones:
            if particion.Proceso == proceso:
                particion.Desalocar()
                break
        self.procesosAlmacenados-=1

    def CargarDesdeDisco(self, proceso : Proceso):
        # Se supone que llamamos a este metodo cuando desalocamos de memoria principal porque termino un proceso
        if self.ParticionDisponible(proceso):
            self.DiscoDesalocar(proceso)
            self.TratarAlocar(proceso) # Ya sabemos que se puede meter en memoria
            return True
        return False





class Particion:
    def __init__(self, id, tam, dir_comienzo, frag_interna):
        self.Id = id
        self.Tam = tam
        self.DirComienzo = dir_comienzo
        self.FragInterna = tam
        self.Proceso = None
        self.Ocupado = False
        self.Os = False

    def CargarProceso(self, proceso: Proceso):
        self.Proceso = proceso
        self.Ocupado=True
        self.FragInterna = self.Tam - proceso.tam

    def Desalocar(self):
        self.Proceso = None
        self.Ocupado = False
        self.FragInterna = self.Tam

    def GetFragInterna(self,proceso:Proceso):
        return self.Tam-proceso.tam


