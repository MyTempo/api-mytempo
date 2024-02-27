from config import *
from functions import *
from helpers import *
from datetime import datetime
from Database import *
import os
class MyTempo:
    
    def __init__(self) -> None:
        pass

    def setIp(self, ip, port):
        if os.path.exists(SERVER_CONFIG_FILE_PATH):
            try:
                if os.path.exists(READER_CONFIG_FILE_PATH):
                    equip_dados = r_json(READER_CONFIG_FILE_PATH)
                    if(ip and port):
                        db = Database()
                        update = f"UPDATE `equipamentos_cadastro` SET `ip` = '{ip}:{port}' WHERE `equipamentos_cadastro`.`id` = {equip_dados["equipamento"]} "
                        result = db.executeNonQuery(update)
                        if result['status'] == "success":
                            return "Equipamento iniciado e configurado com sucesso!"
            except FileNotFoundError as e:
                print("Falha ao configurar servidor remoto: -> ", e)
        
    