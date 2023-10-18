import json
from src.procesador import *
from src.memoria import *
from src.proceso import *
#modificar esta variable para mostrar mas o menos valores
Debug=True

def main():
    

    cargaTrabajo: list[dict] = json.load(open("json/procesos.json"))
    cargaTrabajo.sort(key=lambda d: d["tiempo_arribo"]+d["id"])
    cargaTrabajo=[Proceso(x['id'],x["tiempo_arribo"],x["tiempo_irrupcion"],x['tam']) for x in cargaTrabajo]
    tiempoEjecucion: int = 0
    colaListos: list[dict] = []
    memoria=Memoria()
    procesador=Procesador()
    #loop de entrada de procesos

    while cargaTrabajo: #mientras carga de trabajo tenga trabajo
        proceso=cargaTrabajo[0]
        loopIngresoDeProceso()

        procesador.DescontarQuantum()

        tiempoEjecucion+=1

    for proceso in cargaTrabajo:
        tiempoEjecucion += proceso["tiempo_irrupcion"]
    for instante in range(0, tiempoEjecucion):
        # Aca se maneja la administracion de colaListos, asignacion de memoria, salida y demas
        colaListos.extend(buscarProcesosEntrantes(instante, cargaTrabajo))
    
    def loopIngresoDeProceso():
        while (proceso["tiempo_arribo"]<tiempoEjecucion ):
                if procesador.EnviarProcesoColaDeListos(proceso):
                    #memoria.cargar(proceso)
                    cargaTrabajo.pop(0)
                else: #sino puede cargarlo romper el ciclo de enviar a la coal de listos
                    break

def buscarProcesosEntrantes(instante: int, cargaTrabajo: list[dict]):
    entrantes: list[dict] = []
    for proceso in cargaTrabajo:
        if proceso["tiempo_arribo"] == instante:
            entrantes.append(proceso)
        if proceso["tiempo_arribo"] > instante:
            break
    return entrantes


if __name__ == "__main__":
    main()

