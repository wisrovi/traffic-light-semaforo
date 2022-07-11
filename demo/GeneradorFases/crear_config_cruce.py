import json
   

def create_controladora(name, mac, opuesto:str="", espejo:str="", principal:bool=False) -> dict:
    controladora = {
        "name" : name,
        "mac" : mac,
        "config": {
            "opuesto": opuesto,
            "espejo": espejo,
            "principal": principal
        }
    }
    return controladora
   

data_save = list()
data_save.append(  create_controladora("maestra", "0013A20041041B1E", opuesto="", espejo="", principal=True)  )
data_save.append(  create_controladora("slave 1 (afuera)", "0013A20040B15FED", opuesto="", espejo="0013A20041041B1E", principal=False)  )
data_save.append(  create_controladora("slave 2 (sala)", "0013A20040E276CF", opuesto="0013A20041041B1E", espejo="", principal=False)  )


with open("config_cruce.json", "w") as outfile:
    json.dump(data_save, outfile)



import sys
sys.exit()
data_save = {
    "times": {
        "red": 30,
        "red-yellow": 5,
        "yellow": 5,
        "green": 60
    },
    "secure": {
        "green": 5
    }
}

with open("config.json", "w") as outfile:
    json.dump(data_save, outfile)