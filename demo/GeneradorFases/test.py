from libraries.CruceSemaforo import CruceSemaforo
import json

config = None
with open("config.json", "r") as file:
    data = file.read()
    config = json.loads(data)

config_cruce = None
with open("config_cruce.json", "r") as file:
    data = file.read()
    config_cruce = json.loads(data)

cS = CruceSemaforo(config, config_cruce)
cS.graficar_grafo(True)
