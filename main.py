import json


def main():
    cargaTrabajo: list[dict] = json.load(open("json/procesos.json"))
    cargaTrabajo.sort(key=lambda d: d["tiempo_arribo"])
    tiempoEjecucion: int = 0
    colaListos: list[dict] = []
    for proceso in cargaTrabajo:
        tiempoEjecucion += proceso["tiempo_irrupcion"]
    for instante in range(0, tiempoEjecucion):
        # Aca se maneja la administracion de colaListos, asignacion de memoria, salida y demas
        colaListos.extend(buscarProcesosEntrantes(instante, cargaTrabajo))


def buscarProcesosEntrantes(instante: int, cargaTrabajo: list[dict]) -> list[dict]:
    entrantes: list[dict] = []
    for proceso in cargaTrabajo:
        if proceso["tiempo_arribo"] == instante:
            entrantes.append(proceso)
        if proceso["tiempo_arribo"] > instante:
            break
    return entrantes


if __name__ == "__main__":
    main()
