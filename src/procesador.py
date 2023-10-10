from typing_extensions import Self


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
