from API.config.config import *
from API.models.SqlBuilder import *
from API.models.SQliteDB import *
import requests
from flask import jsonify
import subprocess
import psutil
import json
import psutil
import time
import os
import shutil


class System:

    def __init__(self) -> None:
        pass 

    def detect_usb(self):
        drives = psutil.disk_partitions()
        for drive in drives:
            if 'removable' in drive.opts:
                return True
        return False

    def get_usb_path(self):
        drives = psutil.disk_partitions()
        for drive in drives:
            if 'removable' in drive.opts:
                return drive.mountpoint

    def copy_files(self, source_directory):
        usb_dir = self.get_usb_path()
        if usb_dir is not None:
            print(f"Pendrive detected at {usb_dir}")
            source_files = os.listdir(source_directory)
            destination_files = os.listdir(usb_dir)
            for file in source_files:
                source_path = os.path.join(source_directory, file)
                destination_path = os.path.join(usb_dir, file)
                if file not in destination_files:
                    shutil.copy(source_path, destination_path)
                    print(f"File '{file}' copied to the pendrive.")
    
    def get_file():
        ...
    
    def start_pendrive_detector(self):
        while True:
            self.copy_files()
            time.sleep(5)
    
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


    def checkInternet_connection():
        try:
            response = requests.get('https://google.com', timeout=5)
            if response.status_code == 200:
                res = {
                    'status': 'success',
                    'message': 'Conectado à Internet',
                    'erro': 0,
                    'retornomsg': 'O equipamento está conectado á internet'
                }
                return res
            else:
                res = {
                    'status': 'error',
                    'message': 'Sem conexão com a Internet',
                    'erro': 1,
                    'retornomsg': 'O equipamento não está conectado á internet'
                }
                return res
        except requests.ConnectionError:
                res = {
                    'status': 'error',
                    'message': 'Ocorreu um erro na verificação',
                    'erro': 1,
                    'retornomsg': 'O equipamento não está conectado á internet'
                }
                return res

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
        sqlb = SQLQueryBuilder()
        localdb = LocalDatabase()
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(self.process_path, shell=True)
            print(f"Processo iniciado com sucesso. No PID {self.process.pid}")
            localdb.executeNonQuery(f"UPDATE system_settings SET pid = {self.process.pid}")

            return self.process.pid
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

