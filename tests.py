from get_data import *


import requests

gwt = GetWebData()
url = "http://192.168.1.115:3000/start_reader"


data = {
    " ": ""
}

response = requests.post(url, json=data)

print(response.text)