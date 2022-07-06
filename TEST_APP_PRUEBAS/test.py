data = {"comtype":"xbee","port":"COM4","baudrate":"115200","parity":"none",
"mac":"0013A200417E95E0",
"frametype":"controladora","infoframe":{"iddestino":"01",
"frame":"devices"
}}


import requests
r = requests.post("http://localhost:7000/comunicacion", json=data)
print(r.json().get('data'))