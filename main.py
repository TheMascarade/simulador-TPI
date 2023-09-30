import json


def main():
    cargaTrabajo = json.load(open("json/procesos.json"))
    cargaTrabajo.sort(key=lambda d: d["tiempo_arribo"])


if __name__ == "__main__":
    main()