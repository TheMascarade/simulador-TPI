# TPI - operativos

## Diagrama de estados

![](https://hackmd.io/_uploads/SkCQqOx-6.png)


### Nuevo: 

Los procesos son creados y entran a una cola de espera para ser asignados una posicion en memoria.

Si hay espacio pasan a **Listos**, de lo contrario pasan a **Listos/suspendido**.

### Listo:

El programa y datos del proceso esta cargado en memoria y **el PCB esta en la cola de listos** esperando para ser ejecutado.

Cuando el temporizador interrumpe la ejecucion (por el quantum) el PCB vuelve al final de la cola de listos. La memoria se desocupa solamente cuando uno de los procesos termina de ejecutarse.

### Listo/Suspendido:

El programa y datos estan almacenados en disco, no se que pasa con el PCB pero tiene que estar generado para poder ser cargado a cola de listos.

Una idea es tener una cola de suspendidos ordenada por tiempo de arribo desde la que vamos a ir cargando a la cola de listos cuando el proceso pase a memoria principal.

Los procesos irian a esta cola cuando no queda espacio en memoria para cargarlos y saldrian cuando uno de ellos se termine de ejecutar.


### Ejecutando:

El activador realizo el cambio de contexto en el procesador y se estan ejecutando las instrucciones. 

Interrumpimos la ejecucion cuando:

- `reloj == quantum`
- `proceso.tiempo_irrupcion == 0`

Implica descontar el tiempo de irrupcion del proceso en cada batido de reloj.


### Salida:

`proceso.tiempo_irrupcion` == 0. El proceso se termino de ejecutar.

## Implementacion

La idea es usar un [patron de observador](https://refactoring.guru/design-patterns/observer/python/example) en donde el simulador y memoria esperan el evento del procesador (ya sea interrupcion por quantum o terminacion de proceso) y lanzan la logica dedicada a la asignacion de memoria y carga de procesos de la lista de suspendidos.

El procesador tiene una lista de observadores en donde va a estar la instancia de simulador y/o memoria (a definir, capaz puede ser el sim el que maneje todo). Cuando ocurre que un proceso termina (`proceso.tiempo_irrupcion == 0`) o que se tiene que interrumpir por el quantum ejecutamos `self.notificar()` desde `procesador` para que cada uno de los observadores haga lo que tiene que hacer.

En la practica el simulador inicia, carga todo lo que puede en memoria y en disco y carga un proceso a ejectuar en el procesador (ya tendriamos las instancias de procesador, memoria y sim).

Ejecutamos `procesador.correr(tiempo_limite:int)` y cuando un proceso se interrumpe, en el caso de hacer `Simulador` la clase maestra, desde su instancia vamos a ver si podemos asignar un nuevo proceso a memoria y eliminar el proceso saliente o si tenemos que reingresar el proceso a `cola_listos`.
