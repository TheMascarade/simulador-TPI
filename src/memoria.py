# NOTA
# DiscoAlocar() ya verifica si queda espacio en disco asi en el flujo del simulador solamente tenemos que invocar ese metodo para saber si se puede admitir un proceso o no
# Tambien podemos hacer lo mismo con memoria interna si resulta mas facil

from proceso import *


class Memoria:
    def __init__(self, particiones) -> None:
        self.Particiones: list["Particion"] = particiones
        self.Disco: list["Proceso"] = []

    def Mostrar(self):
        for particion in self.Particiones:
            print("-----------------------------")
            particion.Mostrar
        print("-----------------------------")

    def Alocar(self, proceso: "Proceso"):
        index = 0
        frag = 9999999
        # Nos fijamos si podemos alocar en alguna particion
        if not self.ParticionDisponible(proceso):
            return False
        # Algoritmo best-fit porque ya sabemos que podemos alocar
        for particion in self.Particiones:
            fragParticion = particion.GetFragInterna(proceso)
            if fragParticion >= 0 and fragParticion < frag:
                frag = fragParticion
                index = self.Particiones.index(particion)
        self.Particiones[index].CargarProceso(proceso)
        return True

    def ParticionDisponible(self, proceso: "Proceso"):
        for particion in self.Particiones:
            if not particion.Ocupado and particion.Tam >= proceso.tam:
                return True
        return False

    def DiscoQuedaEspacio(self):
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

    def Desalocar(self, proceso: "Proceso"):
        index = 0
        for particion in self.Particiones:
            if particion.GetProceso == proceso:
                particion.Desalocar()
                break

    def CargarDesdeDisco(self):
        if self.Disco == 0:
            return
        for proc in self.Disco:
            if self.Alocar(proc):
                proc.estado = Estado.Listo


class Particion:
    def __init__(self, id, tam, dir_comienzo, frag_interna):
        self.Id = id
        self.Tam = tam
        self.DirComienzo = dir_comienzo
        self.FragInterna = frag_interna
        self.Proceso: "Proceso" | None
        self.Ocupado = False
        self.Os = False

    def CargarProceso(self, proceso: "Proceso"):
        self.Proceso = proceso
        self.SetOcupado()
        self.SetFragInterna()

    def Desalocar(self):
        self.Proceso = None
        self.SetOcupado()
        self.SetFragInterna()

    def GetFragInterna(self, proceso: "Proceso"):
        return self.Tam - proceso.tam

    def SetFragInterna(self):
        if self.Proceso != None:
            self.FragInterna = self.Tam - self.Proceso.tam
        else:
            self.FragInterna = None

    def GetProceso(self):
        return self.Proceso

    def SetOcupado(self):
        self.Ocupado = not self.Ocupado

    def Mostrar(self):
        id = 0
        if self.Proceso == None:
            id = 0
        else:
            id = self.Proceso.id
        print("Particion:", self.Id)
        print("Proceso:", id)
        print("Tamaño:", self.Tam)
        print("Direccion inicio:", self.DirComienzo)
        print("Fragmentacion interna:", self.FragInterna)
