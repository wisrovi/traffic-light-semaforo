import json
from libraries.CruceSemaforo import CruceSemaforo, plt

"""
Probando instancias
"""
# https://towardsdatascience.com/graph-visualisation-basics-with-python-part-ii-directed-graph-with-networkx-5c1cd5564daa
config = None
with open("config.json", "r") as file:
    data = file.read()
    config = json.loads(data)

config_cruce = None
with open("config_cruce.json", "r") as file:
    data = file.read()
    config_cruce = json.loads(data)

cS = CruceSemaforo(config, config_cruce)
cS.graficar_grafo(False)
cS.process_cruce(True)
fases = cS.generar_fases()
cS.graficar_fases(True)

for mac, fas in fases.items():
    print(mac, fas)


""" 
# https://www.ascii-art-generator.org/es.html
# https://www.w3schools.com/REACT/DEFAULT.ASP
# https://towardsdatascience.com/graph-visualisation-basics-with-python-part-ii-directed-graph-with-networkx-5c1cd5564daa
# https://matplotlib.org/stable/gallery/text_labels_and_annotations/mathtext_asarray.html
                   TIPO 1

     __________             __________
    |          |     |     |          |
    |          |  |  |  |  |          |
    |          |  V  |  V  |          |
    |__________| | | | | | |__________|
        -->   =                -->   
        -->   =                -->
     ----------             ----------
        -->   =                -->
        -->   =                -->
     __________             __________
    |          |     |     |          |
    |          |  |  |  |  |          |
    |          |  V  |  V  |          |
    |__________|     |     |__________|

"""
