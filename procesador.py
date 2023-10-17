#Notas:
#Que empiece con __ significa que es privado


class procesador:
    def __init__(self,memoria,procesos=[]):
        self.__QuantumProcesoActual=0
        self.__Memoria=memoria
        self.__ProcesosListos=procesos
        #Porque el enunciado dice q el round robin es de 2, podria ser global la variable pero preferi dejarla aca
        self.__QuantumRR=2


    def EnviarProcesoColaDeListos(self,proceso):
        if len(self.__ProcesosListos)<5:
            self.__ProcesosListos.add(proceso)
        else:
            raise Exception("No se pueden admitir mas de 5 proceso")

    def DescontarQuantum(self):
        '''Descontamos el Quantum y si termina el proceso antes, 
        Si termina un proceso lo devolvemos y sino no devolvemos nada'''
        self.__QuantumProcesoActual+=1
        tiempoRes=self.__ProcesosListos[0].DescontarQuantum()
        if (tiempoRes==0):
            self.AsignarSiguienteProcesoEjecutar()
            procesoTerminado=self.__ProcesosListos.pop(0)
            return procesoTerminado
        if(self.__QuantumProcesoActual>=self.__QuantumRR):
            self.AsignarSiguienteProcesoEjecutar()
            return None
    

    def __SetProcesosListos(self,procesos=[]):
        pass

    def GetProcesosListos(self):
        return self.__ProcesosListos

    
    def AsignarSiguienteProcesoEjecutar(self):
        self.__QuantumProcesoActual=0 
        ultimoProceso=self.__ProcesosListos.pop(0)
        #ultimoProceso.liberarMemoria()
        self.__ProcesosListos.append(ultimoProceso)