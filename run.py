from flask import Flask, request, jsonify
from flask_cors import CORS
from main import app
from functions import w_json
from MyTempo import *
from config import *
import socket


def get_local_ip_addr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Erro ao obter o endereço IP: {e}")
        return None

def create_base_directories():
   for d in DIRETORIOS_BASE_LISTA:
       verify_and_create(d)

if __name__ == '__main__':
    create_base_directories()
    ip_servidor = get_local_ip_addr()
    if ip_servidor:
        data = {
            "server_ip": ip_servidor,
            "port": SERVER_PORT,
            "equip_port": EQUIP_PORT
        }
        w_json(f"{PATH_READER_DATA}/server.json", data)
        mt = MyTempo()
        mt.setIp(data["server_ip"], data['port'])
        
        app.run(host='0.0.0.0', port=data["port"])
        
    else:
        print("Não foi possível obter o endereço IP do servidor.")


