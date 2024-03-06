from get_data import *


import requests

gwt = GetWebData()
url = "http://192.168.1.115:3000/start_reader/"


data = {
    "nome_equipamento": "PORTAL LEITOR RFID298"
}

response = requests.post(url, json=data)

print(response.text)