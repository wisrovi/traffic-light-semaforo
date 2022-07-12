import json
import sys
import matplotlib.pyplot as plt
import networkx as nx
from libraries.Print_color import colored, Print_color

pc = Print_color()


class CruceSemaforo():
    semaforos = dict()

    def __init__(self):
        self.MOLDE = None
        with open("template.json", "r") as file:
            data = file.read()
            self.MOLDE = json.loads(data)

        self.config_cruce = None
        with open("config_cruce.json", "r") as file:
            data = file.read()
            self.config_cruce = json.loads(data)

        self.config = None
        with open("config.json", "r") as file:
            data = file.read()
            self.config = json.loads(data)

        self.tiempo_verde = self.config['times']['green']
        self.tiempo_amarillo = self.config['times']['yellow']
        self.tiempo_seguro = self.config['secure']['red']

        self.__valid_cruce()
        self.__valid_tiempo_base()

    def get_config_files(self):
        return self.MOLDE, self.config_cruce, self.config

    def __hallar_opuestos_pendientes(self):
        opuesto_mas_amplio = 0
        lista_opuestos_mas_amplio = list()
        for i, controladora in enumerate(self.config_cruce):
            opuestos = controladora['config']['opuesto']
            if opuesto_mas_amplio < len(opuestos):
                if controladora['mac'] not in self.semaforos:
                    opuesto_mas_amplio = len(opuestos)
                    lista_opuestos_mas_amplio = [controladora['mac']] + opuestos
        opuesto_mas_amplio += 1

        return lista_opuestos_mas_amplio

    def __valid_tiempo_base(self):
        for _ in range(len(self.config_cruce)):
            lista_opuestos_mas_amplio = self.__hallar_opuestos_pendientes()
            opuesto_mas_amplio = len(lista_opuestos_mas_amplio)

            if opuesto_mas_amplio > 0:
                self.__crear_opuestos(lista_opuestos_mas_amplio)
            self.__crear_espejos()

        for i, controladora in enumerate(self.config_cruce):
            # print(k, self.calcular_tiempos_de_vector(v))
            v = self.semaforos.get(controladora['mac'])
            print(controladora['mac'], end=": ")
            if v is not None:
                self.graph_time(v)

    def __crear_espejos(self):
        for i, controladora in enumerate(self.config_cruce):
            espejo = controladora['config']['espejo']
            mac = controladora['mac']
            if mac not in self.semaforos:
                if espejo in self.semaforos:
                    self.semaforos[mac] = self.semaforos[espejo]

    def __crear_opuestos(self, lista):
        reduccion_verde = int(self.tiempo_verde * 0.3)
        tiempo_verde = self.tiempo_verde - reduccion_verde
        base = list()
        for _ in lista:
            for _ in range(self.tiempo_seguro):
                base.append("R")
            for _ in range(tiempo_verde):
                base.append("G")
            for _ in range(reduccion_verde):
                base.append("P")
            for _ in range(self.tiempo_amarillo):
                base.append("Y")

        corte = self.tiempo_seguro + tiempo_verde + reduccion_verde + self.tiempo_amarillo
        self.semaforos = dict()
        for i, mac in enumerate(lista):
            temporal = list()
            for j, d in enumerate(base):
                if j >= corte * (i) and j <= corte * (i + 1):
                    temporal.append(d)
                else:
                    temporal.append("R")
            self.semaforos[mac] = temporal

    def __valid_cruce(self):
        """
            Validar que exista a una categoria:
            - principal: solo puede haber uno
            - espejo: reflejo de otro semaforo
            - opuesto: es una lista de los semaforos opuestos
        """
        conteo_principales = 0
        for i, controladora in enumerate(self.config_cruce):
            es_principal = controladora['config']['principal']
            espejos = len(controladora['config']['espejo'])
            opuestos = len(controladora['config']['opuesto'])
            if espejos == 0 and opuestos == 0 and not es_principal:
                print(
                    f"Error la mac {controladora['mac']} no tiene una configuracion, no es principal, tiene espejo u opuestos")
                sys.exit()
            if es_principal:
                conteo_principales += 1

        if conteo_principales != 1:
            print(f"Debe haber UN principal, en el momento hay {conteo_principales} principales")
            sys.exit()

    @staticmethod
    def graph_time(linea_tiempo):
        grafico = list()
        for t in linea_tiempo:
            if t == "R":
                grafico.append(colored("R", "red"))
            elif t == "S":
                grafico.append(pc.subline(colored("S", "red")))
            elif t == "Y":
                grafico.append(colored("Y", "yellow"))
            elif t == "G":
                grafico.append(colored("G", "green"))
            elif t == "P":
                grafico.append(pc.subline(colored("G", "green")))
            else:
                grafico.append(colored("-", "red"))

        for g in grafico:
            print(g, end=" ")
        print()

    @staticmethod
    def calcular_tiempos_de_vector(tiempos):
        last = tiempos[0]
        conteo = 0
        data = list()
        if bool(tiempos):
            for now in tiempos:
                if now != last:
                    data_save = (last, conteo)
                    data.append(data_save)
                    conteo = 1
                else:
                    conteo += 1
                last = now
            data_save = (last, conteo)
            data.append(data_save)

            return data

    @staticmethod
    def hallar_opuesto_1a1(time):
        # https://www.youtube.com/watch?v=rs2GpmjRTf0
        nuevo_opuesto = [0 for _ in time]
        startR, stopR, last = None, None, None
        for i, now in enumerate(time):
            if now == "G" or now == "Y":
                nuevo_opuesto[i] = "R"
            if now == "R":
                if startR is None:
                    startR = i
            if last == "R" and now != "R":
                if stopR is None:
                    stopR = i
            last = now

        if startR is not None and stopR is not None:
            for i, id in enumerate(range(startR, stopR, 1)):
                fin = config['times']['yellow']
                if i < stopR - fin:
                    if i >= config['secure']['red'] * 2:
                        nuevo_opuesto[id] = "G"
                    else:
                        nuevo_opuesto[id] = "R"
                else:
                    nuevo_opuesto[id] = "Y"

        if len(nuevo_opuesto) >= config['secure']['red']:
            for _ in range(config['secure']['red']):
                nuevo_opuesto.append(nuevo_opuesto.pop(0))

        return nuevo_opuesto


"""
Probando instancias
"""


data = {
    "A": {
        "o": ["B", "C"],
        "e": "",
    },
    "B": {
        "o": [],
        "e": "D"
    },
    "C": {
        "o": [],
        "e": "D"
    },
    "D": {
        "o": [],
        "e": "A"
    }
}


nodos = [i for i in range(len(data))]
sizes = [1000 for _ in nodos] + [1000]
labels = dict()
for i, v in enumerate(data):
    labels[i] = v
colors = ["skyblue" for _ in labels]
edge_colors = list()
conexiones = list()
for i, v in enumerate(data):
    o = data[v]["o"]
    e = data[v]["e"]
    if len(o) > 0:
        for keyA in o:
            for j, keyB in enumerate(data):
                if keyA == keyB:
                    conexiones.append((i, j))
                    edge_colors.append("red")
                    break
    else:
        if len(e) > 0:
            for j, keyB in enumerate(data):
                if e == keyB:
                    conexiones.append((i, j))
                    break
            edge_colors.append("blue")


"""
    Crendo el grafo para graficar
"""

G = nx.DiGraph()
G.add_nodes_from(nodos)
G.add_edges_from(conexiones)


nx.draw_networkx(G, labels=labels, arrows=True,
                 node_shape="s",
                 node_color=colors,
                 edge_color=edge_colors,  # color of the edges
                 edgecolors="gray")  # edges of the box of node

plt.title("Comunicacion Semaforo.")
plt.legend(loc="upper left")
plt.gca().legend(('espejo', 'opuesto'))
plt.savefig("grafo semaforo.jpeg", dpi=300)
plt.show()


sys.exit()



cS = CruceSemaforo()
MOLDE, config_cruce, config = cS.get_config_files()

""" 
# https://www.ascii-art-generator.org/es.html
# https://www.w3schools.com/REACT/DEFAULT.ASP


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

"""
        Iniciando generador del semaforo con los tiempos estipulados
"""

"""                TIPO 1

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
