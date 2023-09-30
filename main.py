import json


def main():
    colaListos = json.load(open("json/procesos.json"))
    colaListos.sort(key=lambda d: d["tiempo_arribo"])


if __name__ == "__main__":
    main()