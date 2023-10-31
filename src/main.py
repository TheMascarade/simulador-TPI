import json
from memoria import *
from procesador import *
from proceso import *


class Simulador:
    def __init__(self, cargaTrabajo: list["Proceso"], particiones: list["Particion"]):
        self.cargaTrabajo = cargaTrabajo
        self.tiempoEjecucion = 0
        self.procesador = Procesador()
        self.memoria = Memoria(particiones)

    def TrabajosPosibles(self):
        procesosAdmitibles = []
        for proceso in self.cargaTrabajo:
            if proceso.arribo == self.tiempoEjecucion:
                procesosAdmitibles.append(proceso)

        return procesosAdmitibles

    def Mostrar(self):
        self.procesador.Mostrar()
        self.memoria.Mostrar()

    def Correr(self):
        """este seria el loop principal q definimos"""
        while True:
            if respuestaProcesador:
                print("Terminó el proceso", respuestaProcesador.id)
                self.memoria.Desalocar(proceso=respuestaProcesador.id)

            trabajosPosibles = self.TrabajosPosibles()
            # hay algun proceso sin admitir
            if len(trabajosPosibles) > 0:
                proceso = self.cargaTrabajo[0]
                # hay alguna particion disponible y suficiente
                if self.memoria.BuscarParticionDisponible(proceso):
                    self.memoria.Alocar(proceso)
                    self.procesador.EnviarProcesoColaDeListos(proceso)

            procesoAEjecutar = self.procesador.SiguienteProcesoAEjecutar()
            if self.memoria.ProcesoEnMemoria(procesoAEjecutar):
                self.memoria.Swap(procesoAEjecutar)

            respuestaProcesador = self.procesador.DescontarQuantum()

        print("Tardó en ejecutarse ", self.tiempoEjecucion, " unidades de tiempo")

    def set_tiempo_ejecucion(self):
        for proceso in self.cargaTrabajo:
            self.tiempoEjecucion += proceso.tiempo_irrupcion

    def actualizar(self, msg: str):
        ()


def main():
    lista_procesos = json.load(open("json/procesos.json"))
    lista_procesos.sort(key=lambda d: d["tiempo_arribo"])
    cargaTrabajo: list["Proceso"] = []
    for proc in lista_procesos:
        proceso = Proceso(
            proc["id"], proc["tam"], proc["tiempo_arribo"], proc["tiempo_irrupcion"]
        )
        cargaTrabajo.append(proceso)
    lista_particiones = json.load(open("json/particiones.json"))
    particiones = []
    for part in lista_particiones:
        particion = Particion(
            part["id"], part["tam"], part["dir_comienzo"], part["frag_interna"]
        )
        particiones.append(particion)
    sim = Simulador(cargaTrabajo, particiones)
    sim.Correr()


if __name__ == "__main__":
    main()
