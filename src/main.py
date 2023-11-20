import json
import csv
from memoria import *
from proceso import *

from prettytable import PrettyTable 


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
        self.procesosTerminados = []
        self.procesosOrden=[]

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
        while len(self.procesosNuevos)>0 and self.memoria.procesosAlmacenados<5:
            pudoAlocar = self.memoria.TratarAlocar(self.procesosNuevos[0])
            if pudoAlocar == True:
                proc = self.procesosNuevos.pop(0)
                self.procesosEnMemoria.append(proc)
                self.procesosOrden.append(proc)
                self.memoria.procesosAlmacenados+=1
                proc.estado = Estado.Listo
            elif pudoAlocar == False:
                proc = self.procesosNuevos.pop(0)
                self.procesosEnDisco.append(proc)
                self.procesosOrden.append(proc)
                self.memoria.procesosAlmacenados+=1
                proc.estado = Estado.Suspendido
            else:
                # si no se pudo ubicar pues queda en estado Nuevo hasta que se pueda ubicar
                break

        while  True:
            # Seleccionamos proceso a ejecutar
            
            # Ejecucion del proceso
            self.reloj += 1 
            # Cargamos en procesosNuevos todos los que entran en los instantes sucesivos desde cargaTrabajo
            while (
                len(self.cargaTrabajo) > 0 and 
                self.cargaTrabajo[0].arribo == self.reloj
            ):
                nuevo=self.cargaTrabajo.pop(0)
                self.procesosNuevos.append(nuevo)  
                print("se agrega a la cola de nuevos el proceso ", nuevo.id)
                if len(self.cargaTrabajo) == 0:
                    break

            # Nos fijamos nivel de multiprogramacion y alocamos si es posible los que ingresaron en ese instante
            if self.memoria.procesosAlmacenados < 5:
                while len(self.procesosNuevos)>0 and self.memoria.procesosAlmacenados<5:
                    pudoAlocar = self.memoria.TratarAlocar(self.procesosNuevos[0])
                    if pudoAlocar == True:
                        proc = self.procesosNuevos.pop(0)
                        self.procesosEnMemoria.append(proc)
                        self.procesosOrden.append(proc)
                        self.memoria.procesosAlmacenados+=1
                        proc.estado = Estado.Listo
                        print("se admitio el proceso ",proc.id,"a memoria")
                    elif pudoAlocar == False:
                        proc = self.procesosNuevos.pop(0)
                        self.procesosEnDisco.append(proc)
                        self.procesosOrden.append(proc)
                        self.memoria.procesosAlmacenados+=1
                        proc.estado = Estado.Suspendido
                        print("se admitio el proceso ",proc.id,"a disco")
                    else:
                        # si no se pudo ubicar pues queda en estado Nuevo hasta que se pueda ubicar
                        break
            
            print("----------------------------------------------------------------------------")
            input("apriete una tecla para continuar ejecucion")

            if self.procesoAEjecutar==None and len(self.procesosOrden)>0:
                self.procesoAEjecutar = self.procesosOrden.pop(0)
                estaEnMemoria = self.memoria.EncontrarParticion(self.procesoAEjecutar)
                if estaEnMemoria == True:
                    self.procesoAEjecutar.estado = Estado.Listo
                elif estaEnMemoria == False:
                    self.procesoAEjecutar.estado = Estado.Suspendido
                else:
                    raise ("el proceso no esta cargado")
                
            if len(self.procesosOrden) != 0:
                    for proc in self.procesosOrden:
                        proc.espera += 1
                        proc.retorno += 1
            if self.procesoAEjecutar !=None:
                self.procesoAEjecutar.irrupcion -= 1
                self.procesoAEjecutar.retorno += 1
                self.quantum -= 1
                self.MostrarMensaje()
                print("\nEJECUCION:")
                print("se ejecuta el proceso ",self.procesoAEjecutar.id)
            else:
                print("reloj:", self.reloj)
                print("no hay procesos nuevos en este momento")
                continue
            
            # Tratamos proceso terminado
            if self.procesoAEjecutar.irrupcion == 0:
                terminado = self.procesoAEjecutar
                self.memoria.Desalocar(terminado) 
                if terminado in self.procesosEnDisco:
                    self.procesosEnDisco.remove(terminado)
                if terminado in self.procesosEnMemoria:
                    self.procesosEnMemoria.remove(terminado)
                if terminado in self.procesosOrden:
                    self.procesosOrden.remove(terminado)
                terminado.tiempoTerminado=self.reloj
                print("termino el proceso ",terminado.id)
                # Ahora tratamos de cargar un proceso en disco o nuevo
                for suspendido in self.procesosEnDisco:
                    if self.memoria.CargarDesdeDisco(suspendido):
                        self.procesosEnMemoria.append(suspendido)
                        self.procesosEnDisco.remove(suspendido)
                        print("se mueve a memoria el proceso ",suspendido.id)
                        suspendido.estado = Estado.Listo
                        break
                    else:
                        # Admitimos uno nuevo si no podemos cargar desde disco
                        # Si msg == None seguimos probando con los demas nuevos
                        for nuevo in self.procesosNuevos:
                            msg = self.memoria.TratarAlocar(nuevo)
                            if msg == True:
                                print("se mueve el proceso ",nuevo.id," a memoria")
                                self.procesosEnMemoria.append(nuevo)
                                self.procesosOrden.append(nuevo)
                                self.procesosNuevos.remove(nuevo)
                                self.memoria.procesosAlmacenados+=1
                                nuevo.estado = Estado.Listo
                                break
                            if msg == False:
                                print("se mueve el proceso ",nuevo.id," a disco")
                                self.procesosEnDisco.append(nuevo)
                                self.procesosOrden.append(nuevo)
                                self.procesosNuevos.remove(nuevo)
                                self.memoria.procesosAlmacenados+=1
                                nuevo.estado = Estado.Suspendido
                                break
                self.procesosTerminados.append(terminado)
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
                print("termino el quantum para el proceso",self.procesoAEjecutar.id)
                self.procesosOrden.append(self.procesoAEjecutar)
                self.procesoAEjecutar = self.procesosOrden.pop(0) 
                print("empieza a ejecutarse el proceso",self.procesoAEjecutar.id)
                # Esto no se puede hacer porque en fin de quantum no se descargan procesos
                # self.memoria.CargarDesdeDisco(self.procesoAEjecutar)
                self.quantum = 2

            # si el proceso esta en disco, traelo a memoria
            if self.procesoAEjecutar.estado == Estado.Suspendido:
                print("se trae de disco el proceso ",self.procesoAEjecutar.id)
                self.procesosEnDisco.remove(self.procesoAEjecutar)
                procesoViejo=self.memoria.PasarAMemoria(self.procesoAEjecutar)
                if procesoViejo !=None:
                    self.procesosEnMemoria.remove(procesoViejo)
                    self.procesosEnDisco.append(procesoViejo)
                self.procesosEnMemoria.append(self.procesoAEjecutar)
                self.procesoAEjecutar.estado = Estado.Ejecutando

            if self.procesoAEjecutar.estado==Estado.Listo:
                self.procesoAEjecutar.estado =Estado.Ejecutando

            if (
                self.procesoAEjecutar.estado != Estado.Listo
                and self.procesoAEjecutar.estado != Estado.Ejecutando
            ):
                print("quiere ejecutarse algo q no esta listo")
            


    def MostrarMensaje(self):
        print("ESTADO:")
        print("reloj: ",self.reloj)
        print("quantum: ",self.quantum)
        print("particiones:")
        frag=0
        t=PrettyTable(["id particion","id proceso","fragmentacion/tamano","direccion de comienzo"])
        for x in self.memoria.Particiones:
            if x.Proceso!=None:
                t.add_row([x.Id,x.Proceso.id,str(x.FragInterna)+"/"+str(x.Tam),x.DirComienzo])
            else:
                t.add_row([x.Id,"-",str(x.FragInterna)+"/"+str(x.Tam),x.DirComienzo])
            frag+=x.FragInterna
        print(t)  
        print("fragmentacion total:",frag)      

        if len(self.memoria.Disco)>0:
            print("procesos almacenados en disco")
            for x in self.memoria.Disco:
                print(x)
        else:
            print("no hay procesos en disco")

        if len(self.procesosNuevos)>0:
            print("lista de nuevos procesos:")
            for x in self.procesosNuevos:
                print(x.id,end=" ") 
            print()

    def InformeEstadistico(self):
        ent=input("apriete S para ver el informe estadistico, apriete cualquier otra letra para terminar")
        totalTiempo=0
        for x in self.procesosTerminados:
            x:Proceso
            print("Proceso ",x.id)
            tiempoRecorrido=x.tiempoTerminado-x.arribo
            print("\tinicio en:",x.arribo," termino en:",x.tiempoTerminado," tiempo en espera:",x.espera,"tiempo de ejecucion:",tiempoRecorrido)
            totalTiempo+=tiempoRecorrido 
        print("el tiempo desde inicio a fin fue de la carga de trabajo fue de",self.reloj)
        print("el tiempo total de ejecucion fue",totalTiempo)
        print("el tiempo promedio de ejecucion de cada proceso fue de",totalTiempo/len(self.procesosTerminados))


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
                Proceso( row[0] , int(row[1]), int(row[2]), int(row[3]))
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
    sim.InformeEstadistico()

    


if __name__ == "__main__":
    main()
