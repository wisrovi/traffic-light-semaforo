import json
import sys
from typing import Dict, Any

import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from libraries.Print_color import colored, Print_color

pc = Print_color()


class CruceSemaforo(object):
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

    def process_cruce(self, show: bool = False):
        self.__valid_cruce()
        self.__valid_tiempo_base(show)

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

    def __valid_tiempo_base(self, show: bool = False):
        for _ in range(len(self.config_cruce)):
            lista_opuestos_mas_amplio = self.__hallar_opuestos_pendientes()
            opuesto_mas_amplio = len(lista_opuestos_mas_amplio)

            if opuesto_mas_amplio > 0:
                self.__crear_opuestos(lista_opuestos_mas_amplio)
            self.__crear_espejos()

        #for _ in range(len(self.config_cruce)):
        faltas = self.__correccion_final()
        self.exitoso = True
        if faltas > 0:
            print("[ERROR]: hubo un problema al obedecer todas las condiciones del cruce")
            self.exitoso = False

        if show:
            texto = str()
            for i, controladora in enumerate(self.config_cruce):
                # print(k, self.calcular_tiempos_de_vector(v))
                v = self.semaforos.get(controladora['mac'])
                if v is not None:
                    grafico = self.graph_time(v)
                    texto += f"{controladora['mac']}: "
                    for g in grafico:
                        texto += f"{g} "
                    texto += f" [{controladora['name']}]"
                    texto += f"\n"
            print(texto)

    def __crear_espejos(self):
        for i, controladora in enumerate(self.config_cruce):
            espejo = controladora['config']['espejo']
            mac = controladora['mac']
            if mac not in self.semaforos:
                if espejo in self.semaforos:
                    self.semaforos[mac] = self.semaforos[espejo]

    def __crear_opuestos(self, lista):
        reduccion_verde = int(self.tiempo_verde * self.config['secure']['parpadeo_verde'])
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
        if len(self.semaforos) == 0:
            self.semaforos = dict()
        for i, mac in enumerate(lista):
            temporal = list()
            for j, d in enumerate(base):
                if corte * i <= j <= corte * (i + 1):
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
                    f"Error la mac {controladora['mac']} no tiene una configuracion, no es principal, tiene espejo u "
                    f"opuestos")
                return
            if es_principal:
                conteo_principales += 1

        if conteo_principales != 1:
            print(f"Debe haber UN principal, en el momento hay {conteo_principales} principales")
            return

    def __correccion_final(self):
        self.maximo = max([len(semaf) for mac, semaf in self.semaforos.items()])
        for mac, semaf in self.semaforos.items():
            if len(semaf) < self.maximo:
                for _ in range(self.maximo-len(semaf)):
                    semaf.append("R")

        faltas = 0
        for i, v in enumerate(self.config_cruce):
            o = self.config_cruce[i]['config']["opuesto"]
            e = self.config_cruce[i]['config']["espejo"]
            actual = self.config_cruce[i]['mac']
            if len(o) > 0:
                # tiene opuestos
                for opuesto in o:
                    A = self.semaforos[actual]
                    B = self.semaforos[opuesto]
                    compare = A == B
                    compare = not compare
                    if not compare:
                        faltas += 1
                    #print("Opuesto:", actual, opuesto, compare)

            if len(e) > 0:
                # tiene iguales
                A = self.semaforos[actual]
                B = self.semaforos[e]
                compare = A == B
                if not compare:
                    faltas += 1
                #print("Igual:", actual, e, compare)

        if faltas == 0:
            for mac, vector in self.semaforos.items():
                es_compartido = None
                for j, d in enumerate(self.config_cruce):
                    if mac == d['mac']:
                        es_compartido = self.config_cruce[j]['config'].get("compartido")
                        if len(es_compartido) == 0:
                            es_compartido = None
                        break
                if es_compartido is not None:
                    conteo = 0
                    vector = self.semaforos[mac].copy()
                    partir = int(self.tiempo_verde * self.config['secure']['partir_verde'])
                    for k, t in enumerate(vector):
                        if t == "G":
                            if conteo < partir:
                                vector[k] = "C"
                                conteo += 1
                            else:
                                break
                    self.semaforos[mac] = vector

        return faltas

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
            elif t == "C":
                grafico.append(pc.subline(colored("R", "red")))
            elif t == "G":
                grafico.append(colored("G", "green"))
            elif t == "P":
                grafico.append(pc.subline(colored("G", "green")))
            else:
                grafico.append(colored("-", "red"))

        return grafico

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

    def graficar_grafo(self, show: bool = False):
        # https://towardsdatascience.com/graph-visualisation-basics-with-python-part-ii-directed-graph-with-networkx-5c1cd5564daa
        # https://www.programcreek.com/python/example/89568/networkx.draw_networkx_edge_labels

        nodos = [i for i in range(len(self.config_cruce))]
        labels: Dict[int, Any] = dict()
        colors = list()
        for i, v in enumerate(self.config_cruce):
            labels[i] = v['name']
            if v['config']['principal']:
                colors.append("mistyrose")
            else:
                colors.append("skyblue")
        edge_colors = list()
        conexiones = list()
        edge_labels = dict()
        for i, v in enumerate(self.config_cruce):
            o = self.config_cruce[i]['config']["opuesto"]
            e = self.config_cruce[i]['config']["espejo"]
            if len(o) > 0:
                for keyA in o:
                    for j, keyB in enumerate(self.config_cruce):
                        if keyA == keyB['mac']:
                            conexiones.append((i, j))
                            edge_colors.append("red")
                            edge_labels[(i, j)] = "O"
                            break
            if len(e) > 0:
                for j, keyB in enumerate(self.config_cruce):
                    if e == keyB['mac']:
                        conexiones.append((i, j))
                        edge_labels[(i, j)] = "M"
                        break
                edge_colors.append("blue")


        """Graficar"""
        G = nx.DiGraph()
        G.add_nodes_from(nodos)
        G.add_edges_from(conexiones)

        pos = nx.spring_layout(G)
        nx.draw_networkx(G, labels=labels,
                         arrows=True,
                         pos=pos,
                         node_shape="s",
                         node_color=colors,
                         edge_color=edge_colors,  # color of the edges
                         edgecolors="gray")  # edges of the box of node

        nx.draw_networkx_edge_labels(G,
                                     pos,
                                     font_size=10,
                                     edge_labels=edge_labels,
                                     font_color='black')
        plt.title("Funcionamiento Semaforo")
        plt.xlabel("O = opposite - M = mirror")
        plt.ylabel("Iteraccion entre controladoras")
        plt.savefig("grafo semaforo.jpeg", dpi=300)
        if show:
            plt.show()

    def generar_fases(self):
        coleccion_fases = dict()
        tiempos = dict()
        for mac, v in self.semaforos.items():
            coleccion_fases[mac] = list()
            tiempos[mac] = list()

        conteo = 0
        for i in range(self.maximo):
            corte = False
            for mac, v in self.semaforos.items():
                if mac in tiempos:
                    if len(tiempos[mac]) == 0:
                        tiempos[mac] += [v[i]]
                    else:
                        if tiempos[mac][-1] != v[i]:
                            tiempos[mac] += [v[i]]
                            corte = True
                        else:
                            tiempos[mac] += [v[i]]
                else:
                    tiempos[mac] = [ v[i] ]
            if corte:
                menor = self.maximo
                for mac, v in self.semaforos.items():
                    if menor > len(tiempos[mac]):
                        menor = len(tiempos[mac])
                menor -= 1
                for mac, v in self.semaforos.items():
                    this_size = len(tiempos[mac])
                    coleccion_fases[mac].append(tuple(tiempos[mac][:menor]))
                    if menor < this_size:
                        tiempos[mac] = tiempos[mac][menor:]
                    else:
                        tiempos[mac] = list()
                    conteo = i

        for mac, v in self.semaforos.items():
            coleccion_fases[mac].append(tuple(v[conteo:]))

        fases = dict()
        for mac, v in coleccion_fases.items():
            acumulado_este_controlador = list()
            for f in v:
                acumulado_este_controlador.append(self.calcular_tiempos_de_vector(list(f))[0])
            fases[mac] = acumulado_este_controlador

        return fases







"""
Probando instancias
"""
# https://towardsdatascience.com/graph-visualisation-basics-with-python-part-ii-directed-graph-with-networkx-5c1cd5564daa
cS = CruceSemaforo()
cS.graficar_grafo(True)
cS.process_cruce(True)
fases = cS.generar_fases()

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
