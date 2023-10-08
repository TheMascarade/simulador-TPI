import json


class Memoria:
    def __init__(self) -> None:
        particiones: list['Particion']
    

class Particion:
    def __init__(self, id, tam, dir_comienzo, frag_interna):
        self.id = id
        self.tam = tam
        self.dir_comienzo = dir_comienzo
        self.frag_interna = frag_interna
        self.observadores: list = []
        self.proceso: 'Proceso'
    def cargar_proceso(self, proceso: 'Proceso'):
        self.proceso = proceso
    def get_proceso(self):
        return self.proceso


class SistemaOperativo:
    def __init__(self, carga_trabajo: list['Proceso']):
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


class Procesador:
    def __init__(self) -> None:
        self.observadores: list = []
        self.proceso: 'Proceso'
        self.clock = 0
    def ejecutar(self, proceso: 'Proceso'):
        self.proceso = proceso
    def correr(self, tiempo_limite:int):
        for self.clock in range(0, tiempo_limite):
            if self.proceso.tiempo_irrupcion == 0:
                self.notificar("Fin proceso")
            self.proceso.tiempo_irrupcion -= 1
    def agregar(self, observador):
        self.observadores.append(observador)
    def remover(self, observador):
        self.observadores.remove(observador)
    def notificar(self, msg: str):
        for observador in self.observadores:
            observador.actualizar(msg)


class Proceso:
    def __init__(self, id: int, tam: int, arribo: int, irrupcion: int) -> None:
        self.id: int = id
        self.tam: int = tam
        self.tiempo_arribo: int = arribo
        self.tiempo_irrupcion: int = irrupcion
        

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
    sim = SistemaOperativo(carga_trabajo)

if __name__ == "__main__":
    main()
