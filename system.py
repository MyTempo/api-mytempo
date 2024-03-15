from config import *
import requests
from flask import jsonify
import subprocess
import psutil
import json

class System:

    def __init__(self) -> None:
        pass 
    
    def checkInternet():
        try:
            response = requests.get('https://google.com', timeout=5)
            if response.status_code == 200:
                res = {
                    'status': 'success',
                    'message': 'Conectado à Internet',
                    'erro': 0,
                    'retornomsg': 'O equipamento está conectado á internet'
                }
                return jsonify(res)
            else:
                res = {
                    'status': 'error',
                    'message': 'Sem conexão com a Internet',
                    'erro': 1,
                    'retornomsg': 'O equipamento não está conectado á internet'
                }
                return jsonify(res)
        except requests.ConnectionError:
                res = {
                    'status': 'error',
                    'message': 'Ocorreu um erro na verificação',
                    'erro': 1,
                    'retornomsg': 'O equipamento não está conectado á internet'
                }
                return jsonify(res)

    def getEquipInfo(self):
        try:
            with open(READER_CONFIG_FILE_PATH, 'r') as arquivo:
                equip_data = json.load(arquivo)
                equip_data['status_e'] = 'success'
                equip_data_json = json.dumps(equip_data)

                return equip_data_json
        except Exception:
            res = {
                    'status': 'error',
                    'message': 'Ocorreu um erro na verificação',
                    'erro': 1,
                    'retornomsg': 'O equipamento não está conectado á internet',
                    'modelo': ""
                }
        print(res)
        return jsonify(res)


class Process:
    def __init__(self, process_path):
        self.process_path = process_path
        self.process = None

    def start_process(self):
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(self.process_path, shell=True)
            print("Processo iniciado com sucesso.")
        else:
            print("O processo já está em execução.")

            
    
    def stop_process(self):
        if self.process and self.process.poll() is None:
            pid = self.process.pid
            p = psutil.Process(pid)
            p.terminate()
            print("Processo interrompido com sucesso.")
        else:
            print("Não há nenhum processo em execução para interromper.")