import json


def main():
    colaListos = json.load(open("json/procesos.json"))
    colaListos.sort(key=lambda d: d["tiempo_arribo"])