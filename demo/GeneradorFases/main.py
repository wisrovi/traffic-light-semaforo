from collections import Counter
import json
from traceback import print_tb
from termcolor import colored

class Print_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def yellow(self, text, fin:bool=False) -> None:
        return self.WARNING + text + self.ENDC
    def green(self, text):
        return self.OKGREEN + text + self.ENDC
    def red(self, text):
        return self.FAIL + text + self.ENDC
    def blue(self, text):
        return self.OKBLUE + text + self.ENDC
    def subline(self, text):
        return self.UNDERLINE + text + self.ENDC


MOLDE = None
with open("template.json", "r") as file:
    data = file.read()
    MOLDE = json.loads(data)

config_cruce= None
with open("config_cruce.json", "r") as file:
    data = file.read()
    config_cruce = json.loads(data)

config= None
with open("config.json", "r") as file:
    data = file.read()
    config = json.loads(data)



pc = Print_color()


def graph_time(linea_tiempo):
    grafico = list()
    for t in linea_tiempo:
        if t == "R":
            grafico.append(  colored("R", "red")  )
        elif t == "RY":
            grafico.append(  pc.subline(colored("RY", "blue"))  )
        elif t == "Y":
            grafico.append(  colored("Y", "yellow")  )
        elif t == "G":
            grafico.append(  colored("G", "green")  )
        else:       
            grafico.append(  colored("-", "red")  )
                

    for g in grafico:
        print(g, end=" ")
    print()


def find_vector_time(times):
    linea_tiempo_return = list()
    for i, t in enumerate(times):
        if t[0] == "R":  # RED
            for j in range(t[1]):
                linea_tiempo_return.append("R")
        if t[0] == "G":  # GREEN
            for j in range(t[1]):
                linea_tiempo_return.append("G")
        if t[0] == "Y":  # YELLOW
            for j in range(t[1]):
                linea_tiempo_return.append("Y")
        
    return linea_tiempo_return


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


def hallar_opuesto(time):
    # https://www.youtube.com/watch?v=rs2GpmjRTf0
    nuevo_opuesto = [0 for _ in time]
    startR, stopR, last = None, None, None
    for i, now in enumerate(time):
        if now == "G" or  now == "Y":
            nuevo_opuesto[i] = "R"
        if now == "R":
            if startR is None:
                startR = i
        if last == "R" and now != "R":
            if stopR is None:
                stopR = i
        last = now
    
    if startR is not None and stopR is not None:
        for i, id in enumerate(range(startR, stopR , 1)):
            fin = config['times']['yellow']
            if i < stopR-fin:
                if i >= config['secure']['red']*2:
                    nuevo_opuesto[id] = "G"
                else:                    
                    nuevo_opuesto[id] = "R"
            else:
                nuevo_opuesto[id] = "Y"

    if len(nuevo_opuesto) >= config['secure']['red']:
        for _ in range(config['secure']['red']):
            nuevo_opuesto.append(nuevo_opuesto.pop(0))
    
    return nuevo_opuesto





data = list()
backup_tiempos = dict()
for i, controladora in enumerate(config_cruce):
    nuevo = MOLDE.copy()
    nuevo['mac'] = controladora['mac']
    nuevo['id'] = i+1
    nuevo['name'] = controladora['name']
    nuevo['config'] = controladora['config']
    if controladora['config']['principal']:
        nuevo['tiempos'] = [ 
            ("R", config['times']['red']), 
            ("G", config['times']['green']), 
            ("Y", config['times']['yellow'])
            ]
        nuevo['conteo'] = config['times']['red'] + config['times']['yellow'] + config['times']['green']
    else:
        nuevo['tiempos'] = [ 
            ("R", 0), 
            ("G", 0), 
            ("Y", 0)
            ]
        nuevo['conteo'] = 0
    backup_tiempos[nuevo['mac']] = nuevo['tiempos']
    data.append(nuevo)





for d in data:
    if not d['config']['principal']:
        if len(d['config']['espejo']) > 0:
            d['tiempos'] = backup_tiempos[d['config']['espejo']]
        else:
            if len(d['config']['opuesto']) > 0:
                linea_tiempo = find_vector_time(backup_tiempos[d['config']['opuesto']])  
                nuevo_opuesto = hallar_opuesto(linea_tiempo)
                opuesto = calcular_tiempos_de_vector(nuevo_opuesto)

                backup_tiempos[d['mac']] = opuesto

                d['tiempos'] = opuesto




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

for i, d in enumerate(data):
    linea_tiempo = find_vector_time(d['tiempos'])   
    graph_time(linea_tiempo) 

print(data)
    





#print(data)

import sys
sys.exit()




"""
        Iniciando generador del semaforo con los tiempos estipulados
"""




class Print_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def print_yellow(self, text, fin:bool=False) -> None:
        print(self.WARNING + text + self.ENDC, end=" ")
    def print_green(self, text):
        print(self.OKGREEN + text + self.ENDC, end=" ")
    def print_red(self, text):
        print(self.FAIL + text + self.ENDC, end=" ")
    def print_blue(self, text):
        print(self.OKBLUE + text + self.ENDC, end=" ")

pc = Print_color()

ROJO = 0
AMARILLO = 1
VERDE = 2
CORTE = 3



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
SEMAFOROS_NECESARIOS = 4



data = list()
for i in range(SEMAFOROS_NECESARIOS):
    nuevo = MOLDE.copy()
    nuevo['id'] = i + 1
    nuevo['name'] = "MAC_XBEE_" + str(i + 1)
    data.append(nuevo)

for d in data:
    print()
    print(d.get("name") + ":", end=" ")
    tiempos = list()
    for i, t in enumerate(d.get("tiempos")):
        if i == ROJO:
            for _ in range(t):
                tiempos.append("R")
        if i == AMARILLO:
            for _ in range(t):
                tiempos.append("A")
        if i == VERDE:  
            for _ in range(t):
                tiempos.append("V")        
        if i == CORTE:
            for _ in range(t):
                tiempos.append(tiempos.pop(0))

    for t in tiempos:
        if t == "R":
            pc.print_red(t)
        if t == "A":
            pc.print_yellow(t)
        if t == "V":
            pc.print_green(t)
    print()






from termcolor import colored
print(colored("Queso", "red"), colored("salsa", "green"), colored("pan", "yellow"))


