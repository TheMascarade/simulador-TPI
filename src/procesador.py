# Notas:
# Que empiece con __ significa que es privado
from proceso import *

Debug = False


class Procesador:
    def __init__(self, procesos=[]):
        self.__ProcesoActual = None
        self.__ProcesosListos = procesos
        # Porque el enunciado dice q el round robin es de 2, podria ser global la variable pero preferi dejarla aca
        self.__Quantum = 2

    def Mostrar(self):
        pass

    def EnviarAColaDeListos(self, proceso):
        # Tiene que ser menor a 3 porque los listos son
        # solo los cargados en memoria, no los que estan en disco
        if len(self.__ProcesosListos) < 3:
            self.__ProcesosListos.append(proceso)
            self
            return True
        else:
            if Debug == True:
                print("Se esta metiendo mas de 5 procesos")
            return False

    def Ejecutar(self) -> Proceso | None:
        """Descontamos el Quantum y si termina el proceso antes,
        Si termina un proceso lo devolvemos y sino no devolvemos nada"""
        if not self.__ProcesoActual:
            self.AsignarSiguienteProcesoEjecutar()
        self.__ProcesoActual.DescontarIrrupcion()
        self.__Quantum -= 1
        # Proceso terminado
        if self.__ProcesoActual.irrupcion == 0:
            procesoTerminado = self.__ProcesosListos.pop(0)
            self.AsignarSiguienteProcesoEjecutar()
            self.__ResetQuantum()
            return procesoTerminado
        # Fin de tiempo disponible para proceso
        if self.__Quantum == 0:
            self.RotarColaListos()
            self.AsignarSiguienteProcesoEjecutar()
            # Quantum vuelve a ser 2
            self.__ResetQuantum()

    def __ResetQuantum(self):
        self.__Quantum = 2

    def __SetProcesosListos(self, procesos=[]):
        pass

    def GetProcesosListos(self):
        return self.__ProcesosListos

    def SiguienteProcesoAEjecutar(self):
        return self.__ProcesosListos[0]

    def AsignarSiguienteProcesoEjecutar(self):
        self.__ProcesoActual = self.SiguienteProcesoAEjecutar()
        self.__ProcesoActual.estado = Estado.Ejecutando

    def RotarColaListos(self):
        ultimoProceso = self.__ProcesosListos.pop(0)
        ultimoProceso.estado = Estado.Listo
        self.__ProcesosListos.append(ultimoProceso)
