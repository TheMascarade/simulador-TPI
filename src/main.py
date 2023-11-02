import json
from memoria import *
from procesador import *
from proceso import *


class Simulador:
    def __init__(self, cargaTrabajo: list["Proceso"], particiones: list["Particion"]):
        self.cargaTrabajo = cargaTrabajo
        self.reloj = 0
        self.procesador = Procesador()
        self.memoria = Memoria(particiones)

    def TrabajosPosibles(self):
        procesosAdmisibles = []
        for proceso in self.cargaTrabajo:
            # Enviamos todos los procesos que solicitan memoria en ese instante o que dejamos en estado de nuevo.
            if proceso.arribo <= self.reloj:
                procesosAdmisibles.append(proceso)
        return procesosAdmisibles

    def Mostrar(self):
        self.procesador.Mostrar()
        self.memoria.Mostrar()

    def Correr(self):
        # 1 Ver los procesos entrantes en ese instante
        # 2 Ver si se pueden cargar procesos
        # 3 Ejecutar el proceso `procesador.Ejecutar(proceso)`
        # 4 Ver si el proceso termino o si acabo el quantum
        #    - Si termino ver si podemos cargar otro y desalocarlo
        #    - Si termino el quantum volverlo a colaListos (se encarga procesador)
        while True:
            nuevos = self.TrabajosPosibles()
            # Alocamos todos los procesos que podemos
            for nuevo in nuevos:
                # Tratamos de alocar en memoria interna
                if self.memoria.Alocar(nuevo):
                    # Si se puede enviamos a cola de listos
                    self.procesador.EnviarAColaDeListos(nuevo)
                else:
                    # No queda espacio en memoria entonces probamos con disco
                    self.memoria.DiscoAlocar(nuevo)
            res = self.procesador.Ejecutar()
            if res is Proceso:
                self.memoria.Desalocar(res)
            self.AumentarReloj()

    def AumentarReloj(self):
        self.reloj += 1


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
