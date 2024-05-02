from main import app
from API.helpers.functions import w_json
from MyTempo import *
from API.config.config import *
from system import Process
import socket
import threading
import asyncio

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


def start_process():
    process = Process(f"{BASE_DIR}\\sistema\\start_sys.py")
    process.start_process()
    
def set_config():
    update_json_value(CONFIG_FILE_PATH, "getting_tag", "active")
    

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
        w_json_if_not_exists(CONFIG_FILE_PATH, SYS_CONFIG)
        
        set_config()
        

        mt = MyTempo()
        asyncio.run(MyTempo.readerStartup())
        asyncio.run(MyTempo.save_server(data))
        asyncio.run(mt.setIp(data["server_ip"], data['port']))
        asyncio.run(MyTempo.hasUploaded())
        api = threading.Thread(target=start_process)
        
        pendrive_checker = threading.Thread(target=MyTempo.verifyIfHasPendrive)
        pendrive_checker.start()
        
        api.start()
        mt.callBackgroundProcess()
  
        app.run(host='0.0.0.0', port=data["port"])
        
    else:
        print("Não foi possível obter o endereço IP do servidor.")


