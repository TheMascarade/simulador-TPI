import json
import csv
from memoria import *
from proceso import *



class Simulador:
    def __init__(self, cargaTrabajo: list[Proceso], particiones: list[Particion]):
        self.cargaTrabajo = cargaTrabajo
        self.reloj = 0
        self.quantum = 2
        self.memoria = Memoria(particiones)
        self.procesoAEjecutar = None
        self.procesosNuevos = []
        self.procesosEnDisco = []
        self.procesosEnMemoria = []
        self.procesosOrden = []
        self.procesosTerminados = []

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

        # cargamos todos los procesos de la carga de trabajo a la lista de nuevos en instante 0
        while self.cargaTrabajo[0].arribo == self.reloj:
            self.procesosNuevos.append(self.cargaTrabajo.pop(0))
            if len(self.cargaTrabajo) == 0:
                break
        while len(self.procesosNuevos):
            pudoAlocar = self.memoria.TratarAlocar(self.procesosNuevos[0])
            if pudoAlocar == True:
                proc = self.procesosNuevos.pop(0)
                self.procesosEnMemoria.append(proc)
                self.procesosOrden.append(proc)
                proc.estado = Estado.Listo

            elif pudoAlocar == False:
                proc = self.procesosNuevos.pop(0)
                self.procesosEnDisco.append(proc)
                self.procesosOrden.append(proc)
                proc.estado = Estado.Suspendido
            else:
                # si no se pudo ubicar pues queda en estado Nuevo hasta que se pueda ubicar
                break

        while True:
            # Seleccionamos proceso a ejecutar
            

            # Ejecucion del proceso
            self.reloj += 1
            # Cambiamos de proceso a ejecutar

            # Cargamos en procesosNuevos todos los que entran en los instantes sucesivos desde cargaTrabajo
            while (
                len(self.cargaTrabajo) > 0 and 
                self.cargaTrabajo[0].arribo == self.reloj
            ):
                self.procesosNuevos.append(self.cargaTrabajo.pop(0))
                if len(self.cargaTrabajo) == 0:
                    break

            # Nos fijamos nivel de multiprogramacion y alocamos si es posible los que ingresaron en ese instante
            if self.memoria.procesosAlmacenados < 5:
                while len(self.procesosNuevos):
                    pudoAlocar = self.memoria.TratarAlocar(self.procesosNuevos[0])
                    if pudoAlocar == True:
                        proc = self.procesosNuevos.pop(0)
                        self.procesosEnMemoria.append(proc)
                        self.procesosOrden.append(proc)
                        proc.estado = Estado.Listo

                    elif pudoAlocar == False:
                        proc = self.procesosNuevos.pop(0)
                        self.procesosEnDisco.append(proc)
                        self.procesosOrden.append(proc)
                        proc.estado = Estado.Suspendido
                    else:
                        # si no se pudo ubicar pues queda en estado Nuevo hasta que se pueda ubicar
                        break
            
            if self.procesoAEjecutar==None and len(self.procesosOrden)>0:
                self.procesoAEjecutar = self.procesosOrden.pop(0)
                estaEnMemoria = self.memoria.EncontrarParticion(self.procesoAEjecutar)
                if estaEnMemoria == True:
                    self.procesoAEjecutar.estado = Estado.Listo
                elif estaEnMemoria == False:
                    self.procesoAEjecutar.estado = Estado.Suspendido
                else:
                    raise ("el proceso no esta cargado")

            if self.procesoAEjecutar !=None:
                self.procesoAEjecutar.irrupcion -= 1
                self.quantum -= 1
            else:
                continue

            self.MostrarMensaje()


            # Tratamos proceso terminado
            if self.procesoAEjecutar.irrupcion == 0:
                terminado = self.procesoAEjecutar
                self.memoria.Desalocar(terminado)
                # Ahora tratamos de cargar un proceso en disco o nuevo
                for suspendido in self.procesosEnDisco:
                    if self.memoria.CargarDesdeDisco(suspendido):
                        self.procesosEnMemoria.append(suspendido)
                        self.procesosEnDisco.remove(suspendido)
                        suspendido.estado = Estado.Listo
                        break
                    else:
                        # Admitimos uno nuevo si no podemos cargar desde disco
                        # Si msg == None seguimos probando con los demas nuevos
                        for nuevo in self.procesosNuevos:
                            msg = self.memoria.TratarAlocar(nuevo)
                            if msg==True:
                                self.procesosEnMemoria.append(nuevo)
                                self.procesosOrden.append(nuevo)
                                self.procesosNuevos.remove(nuevo)
                                nuevo.estado = Estado.Listo
                                break
                            if msg == False:
                                self.procesosEnDisco.append(nuevo)
                                self.procesosOrden.append(nuevo)
                                self.procesosNuevos.remove(nuevo)
                                nuevo.estado = Estado.Suspendido
                                break
                self.procesosTerminados.append(terminado)
                if terminado in self.procesosEnDisco:
                    self.procesosEnDisco.remove(terminado)
                if terminado in self.procesosEnMemoria:
                    self.procesosEnMemoria.remove(terminado)
                if terminado in self.procesosOrden:
                    self.procesosOrden.remove(terminado)
                self.procesoAEjecutar = None
                self.quantum = 2
                # asignar el siguiente proceso de alguna forma
                # Arriba ya nos encargamos de cargar en memoria
                # y actualizar procesosOrden

                #si termino la carga de trabajo y no queda nada en nuevo ni para ejecutarse, termina el loop
                if len(self.cargaTrabajo)==0 and len(self.procesosOrden)==0 and len(self.procesosNuevos)==0:
                    print("termino")
                    break
                if len(self.procesosOrden)!=0:
                    self.procesoAEjecutar = self.procesosOrden.pop(0)
                else:
                    continue
      

            # Tratamos fin de quantum
            elif self.quantum == 0:
                self.procesoAEjecutar.estado = Estado.Listo
                self.procesosOrden.append(self.procesoAEjecutar)
                self.procesoAEjecutar = self.procesosOrden.pop(0)
                # Esto no se puede hacer porque en fin de quantum no se descargan procesos
                # self.memoria.CargarDesdeDisco(self.procesoAEjecutar)
                self.quantum = 2

            # si el proceso esta en disco, traelo a memoria
            if self.procesoAEjecutar.estado == Estado.Suspendido:
                self.procesosEnDisco.remove(self.procesoAEjecutar)
                procesoViejo=self.memoria.PasarAMemoria(self.procesoAEjecutar)
                if procesoViejo !=None:
                    self.procesosEnMemoria.remove(procesoViejo)
                    self.procesosEnDisco.append(procesoViejo)
                self.procesosEnMemoria.append(self.procesoAEjecutar)
                self.procesoAEjecutar.estado = Estado.Ejecutando

            if self.procesoAEjecutar.estado==Estado.Listo:
                self.procesoAEjecutar.estado==Estado.Ejecutando

            if (
                self.procesoAEjecutar.estado != Estado.Listo
                and self.procesoAEjecutar.estado != Estado.Ejecutando
            ):
                print("quiere ejecutarse algo q no esta listo")

    def MostrarMensaje(self):

        print("reloj",self.reloj)
        print("quantum",self.quantum)
        print("particiones")
        for x in self.memoria.Particiones:
            if x.Proceso!=None:
                print("|{}|{}/{}|{}|".format(x.Proceso.id,x.FragInterna,x.Tam,x.DirComienzo))
            else:
                print("|{}|{}/{}|{}|".format("--",x.FragInterna,x.Tam,x.DirComienzo))


        if len(self.memoria.Disco)>0:
            print("procesos almacenados en disco")
            for x in self.memoria.Disco:
                print(x)
        else:
            print("no hay procesos en disco")

        print("\n")


def main():
    # leer carga de trabajo
    lista_procesos = []
    with open("./data/procesos.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        header = next(csv_reader)
        for row in csv_reader:
            if int(row[1]) > 250:
                raise ("no se puede cargar programas que pidan mas de 250 kb")
            lista_procesos.append(
                Proceso(int(row[0]), int(row[1]), int(row[2]), int(row[3]))
            )

    lista_procesos.sort(key=lambda d: d.arribo)
    # leer particiones
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
