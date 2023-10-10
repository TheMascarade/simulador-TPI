from procesador import Proceso
import sys


class Memoria:
    def __init__(self, particiones) -> None:
        self.particiones: list['Particion'] = particiones
        self.observadores: list = []
    def cargar_proceso(self, proceso: 'Proceso'):
        index = 0
        frag = sys.maxsize
        for particion in self.particiones:
            if not particion.ocupado:
                frag_particion = particion.get_frag_interna(proceso)
                if frag_particion >= 0 and frag_particion < frag:
                    frag = frag_particion
                    index = self.particiones.index(particion)
        if frag != sys.maxsize:
            self.particiones[index].cargar_proceso(proceso)
            self.notificar("cargado")
        else:
            self.notificar("no cargado")
    def elim_proceso(self, proceso: 'Proceso'):
        index = 0
        for particion in self.particiones:
            if particion.get_proceso == proceso:
                particion.elim_proceso()
                self.notificar("proceso eliminado")
                break
    def agregar(self, observador):
        self.observadores.append(observador)
    def remover(self, observador):
        self.observadores.remove(observador)
    def notificar(self, msg: str):
        for observador in self.observadores:
            observador.notificar(msg)

class Particion:
    def __init__(self, id, tam, dir_comienzo, frag_interna):
        self.id = id
        self.tam = tam
        self.dir_comienzo = dir_comienzo
        self.frag_interna = frag_interna
        self.proceso: 'Proceso'
        self.ocupado = False
        self.os = False
    def cargar_proceso(self, proceso: 'Proceso'):
        self.proceso = proceso
        self.set_frag_interna()
        self.set_ocupado()
    def elim_proceso(self):
        self.proceso = Proceso(0, 0, 0, 0)
        self.set_ocupado()
        self.set_frag_interna(0)
    def get_frag_interna(self, proceso: 'Proceso'):
        return self.tam - proceso.tam
    def set_frag_interna(self, frag = None):
        if frag is None:
            self.frag_interna = self.tam - self.proceso.tam
        else:
            self.frag_interna = frag
    def get_proceso(self):
        return self.proceso
    def set_ocupado(self):
        self.ocupado = not self.ocupado
