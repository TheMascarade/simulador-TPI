from proceso import Proceso

# NOTA
# DiscoAlocar() ya verifica si queda espacio en disco asi en el flujo del simulador solamente tenemos que invocar ese metodo para saber si se puede admitir un proceso o no
# Tambien podemos hacer lo mismo con memoria interna si resulta mas facil

class Memoria:
    def __init__(self, particiones) -> None:
        self.Particiones: list['Particion'] = particiones
        self.Disco: list['Proceso'] = []
    def Alocar(self, proceso: 'Proceso'):
        index = 0
        frag = 9999999
        for particion in self.Particiones:
            frag_particion = particion.GetFragInterna(proceso)
            if frag_particion >= 0 and frag_particion < frag:
                frag = frag_particion
                index = self.Particiones.index(particion)
        if frag != 9999999:
            self.Particiones[index].CargarProceso(proceso)
    def BuscarParticionDisponible(self, proceso: 'Proceso'):
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
    def Desalocar(self, proceso: 'Proceso'):
        index = 0
        for particion in self.Particiones:
            if particion.GetProceso == proceso:
                particion.Desalocar()
                break

class Particion:
    def __init__(self, id, tam, dir_comienzo, frag_interna):
        self.Id = id
        self.Tam = tam
        self.DirComienzo = dir_comienzo
        self.FragInterna = frag_interna
        self.Proceso: 'Proceso' | None
        self.Ocupado = False
        self.Os = False
    def CargarProceso(self, proceso: 'Proceso'):
        self.Proceso = proceso
        self.SetOcupado()
        self.SetFragInterna()
    def Desalocar(self):
        self.Proceso = None
        self.SetOcupado()
        self.SetFragInterna()
    def GetFragInterna(self, proceso: 'Proceso'):
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