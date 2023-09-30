import json


def main():
    cargaTrabajo = json.load(open("json/procesos.json"))
    cargaTrabajo.sort(key=lambda d: d["tiempo_arribo"])
    tiempoEjecucion: int = 0
    colaListos: list[dict]
    for proceso in cargaTrabajo:
        tiempoEjecucion += proceso["tiempo_irrupcion"]
    for i in range(0, tiempoEjecucion):
        # Aca se maneja la administracion de colaListos, asignacion de memoria, salida y demas



if __name__ == "__main__":
    main()