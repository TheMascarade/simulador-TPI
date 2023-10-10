import json
from memoria import *
from procesador import *

class SistemaOperativo:
    def __init__(self, carga_trabajo: list['Proceso'], particiones: list['Particion']):
        self.carga_trabajo = carga_trabajo
        self.tiempo_ejecucion: int
        self.QUANTUM = 2
        self.procesador = Procesador()
        self.memoria = Memoria()
    def correr(self):
        self.set_tiempo_ejecucion()
    def set_tiempo_ejecucion(self):
        for proceso in self.carga_trabajo:
            self.tiempo_ejecucion += proceso.tiempo_irrupcion
    def actualizar(self, msg:str):
        ()


def main():
    lista_procesos = json.load(open("json/procesos.json"))
    lista_procesos.sort(key=lambda d: d["tiempo_arribo"])
    carga_trabajo: list['Proceso'] = []
    for proc in lista_procesos:
        proceso = Proceso(
            proc["id"],            
            proc["tam"],
            proc["tiempo_arribo"],
            proc["tiempo_irrupcion"]
        )
        carga_trabajo.append(proceso)
    lista_particiones = json.load(open("json/particiones.json"))
    particiones = []
    for part in lista_particiones:
        particion = Particion(
            part["id"],
            part["tam"],
            part["dir_comienzo"],
            part["frag_interna"]
        )
        particiones.append(particion)
    sim = SistemaOperativo(carga_trabajo, particiones)

if __name__ == "__main__":
    main()
