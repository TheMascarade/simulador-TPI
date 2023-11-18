import json
import csv
from memoria import *
from procesador import *
from proceso import *


class Simulador:
    def __init__(self, cargaTrabajo: list[Proceso], particiones: list[Particion]):
        self.cargaTrabajo = cargaTrabajo
        self.reloj = 0 
        self.memoria = Memoria(particiones)
        self.procesosNuevos=[]
        self.procesoAEjecutar=None
        self.procesosEnDisco=[]
        self.procesosEnMemoria=[]

    def TrabajosPosibles(self) -> list[Proceso]:
        procesosAdmisibles = []
        for proceso in self.cargaTrabajo:
            # Enviamos todos los procesos que solicitan memoria en ese instante o que dejamos en estado de nuevo.
            if proceso.arribo <= self.reloj:
                procesosAdmisibles.append(proceso)
        return procesosAdmisibles


    def Correr(self):
        # 1 Ver los procesos entrantes en ese instante
        # 2 Ver si se pueden cargar procesos
        # 3 Ejecutar el proceso `procesador.Ejecutar(proceso)`
        # 4 Ver si el proceso termino o si acabo el quantum
        #    - Si termino ver si podemos cargar otro y desalocarlo
        #    - Si termino el quantum volverlo a colaListos (se encarga procesador)


        while self.cargaTrabajo[0].arribo==self.reloj:
            self.procesosNuevos.append(self.cargaTrabajo.pop(0))
            if len(self.cargaTrabajo)==0:
                break


        while True:
            while len(self.cargaTrabajo)>0 and self.cargaTrabajo[0].arribo==self.reloj:
                self.procesosNuevos.append(self.cargaTrabajo.pop(0))
                if len(self.cargaTrabajo)==0:
                    break
                    
            if self.memoria.procesosAlmacenados<5:
                while len(self.procesosNuevos):
                    pudoAlocar=self.memoria.TratarAlocar(self.procesosNuevos[0])
                    if pudoAlocar==True:
                        proc=self.procesosNuevos.pop(0)
                        self.procesador.EnviarACola(proc,Estado.Listo)
                    elif pudoAlocar==False:
                        proc=self.procesosNuevos.pop(0)
                        self.procesador.EnviarACola(proc,Estado.Suspendido)
                    else:
                        #si no se pudo ubicar pues queda en estado Nuevo hasta que se pueda ubicar
                        #averiguar como romper doble loop
                        break
            test=self.procesador.ProcesosListos
            res = self.procesador.Ejecutar()
            self.reloj += 1
            if res is not None:
                if res[0]=='fin':
                    self.memoria.Desalocar(res)
                #nos fijamos si el siguiente proceso a ejecutar esta en memoria
                sigProc= self.procesador.SiguienteProcesoAEjecutar()
                if self.memoria.EncontrarParticion(sigProc)==True:
                    self.memoria.PasarAMemoria(sigProc,self.procesador.__ProcesosListos)
                
                


    def MostrarMensaje(self,resultado):
        pass



def main():
    #leer carga de trabajo
    lista_procesos=[]
    with open('data\procesos.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        line_count=0
        header=next(csv_reader)
        for row in csv_reader:
            if int(row[1])>250:
                raise("no se puede cargar programas que pidan mas de 250 kb")
            lista_procesos.append(Proceso(int(row[0]),int(row[1]),int(row[2]),int(row[3])))
    
    lista_procesos.sort(key=lambda d: d.arribo)
    #leer particiones
    lista_particiones = json.load(open("data/particiones.json"))
    particiones = []
    for part in lista_particiones:
        particion = Particion(
            part["id"], part["tam"], part["dir_comienzo"], part["frag_interna"]
        )
        particiones.append(particion)
    
    sim = Simulador(lista_procesos, particiones)
    sim.Correr()


if __name__ == "__main__":
    main()




