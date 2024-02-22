from config import *
import requests
import json

from functions import *
from helpers import *
from datetime import datetime


class ReaderData:
    def __init__(self) -> None:
        pass

    def ReaderStatus():
       
        res = dict()
        # URL do seu aplicativo Flask
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetTagInfo")
        
        try:
            response = requests.post(url, data={})
            if(response.status_code == 200):
                res['status'] = "success"
                res['message'] = "A leitura está em andamento."
                res["erro"] = 0
                res['retornomsg'] = "O Equipamento está comunicando!"
            else:
                res['status'] = "error"
                res['message'] = "Erro na requisição"
                res["erro"] = 1
                res['retornomsg'] = "Ocorreu um erro na comunicação com equipamento!"
            return res
        
        except requests.exceptions.ConnectionError as e:
            error_message = f"Erro de conexão: Não foi possível estabelecer uma conexão com o servidor. Verifique se o servidor está em execução e acessível. Detalhes: {str(e)}"
            res['status'] = "error"
            res['message'] = error_message
            res["erro"] = 1
            res['retornomsg'] = "Ocorreu um erro na comunicação com equipamento!"
            return res
        except requests.exceptions.HTTPError as e:
            if response.status_code == 405:
                error_message = f"Erro 405: Método não permitido. Verifique se você está usando o método correto para a solicitação. Detalhes: {str(e)}"
                res['status'] = "error"
                res['message'] = error_message
                res["erro"] = 1
                res['retornomsg'] = "Ocorreu um erro na comunicação com equipamento!"
                return res
            elif response.status_code == 500:
                error_message = f"Erro 500: Erro interno do servidor. O servidor encontrou um erro interno e não pode completar a solicitação. Detalhes: {str(e)}"

                res['status'] = "error"
                res['message'] = error_message
                res["erro"] = 1
                res['retornomsg'] = "Ocorreu um erro na comunicação com equipamento!"
                return res
            else:
                error_message = f"Erro HTTP não tratado. Código de status: {response.status_code}. Detalhes: {str(e)}"
            print(error_message)
        except Exception as e:
            error_message = f"Erro inesperado: {str(e)}"
                                
            res['status'] = "error"
            res['message'] = error_message
            res["erro"] = 1
            res['retornomsg'] = "Ocorreu um erro na comunicação com equipamento!"
            return res
    
    def OpenDevice_Reader():
      
        res = dict()
        data = {
            'strComPort': '',  # Substitua pela porta serial desejada
            'Baudrate': 115200  # Substitua pela taxa de baud desejada (correspondente a 115200 no seu código)
        }   
        # URL do seu aplicativo Flask
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenDevice")
        try:
            response = requests.post(url, json=data)
            print(response.text)
        except Exception as e:
            print(e)        

    def Start_Reader(self):
        DeviceParam = self.GetDeviceParam()
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/StartCounting")
        try:
            response = requests.post(url, json=DeviceParam)
            print(response.text)
        except Exception as e:
            print(e)
        # res = dict()
        # # URL do seu aplicativo Flask
        # server = r_json(path=SERVER_CONFIG_FILE_PATH)
        # url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/getPorts")
        # try:
        #     response = requests.post(url, json={})
        #     print(response.text)
        # except Exception as e:
        #     print(e)

    def getPower_Reader():
        
        res = dict()
        # URL do seu aplicativo Flask
        data = {
            'strComPort': '',  # Substitua pela porta serial desejada
            'Baudrate': 115200  # Substitua pela taxa de baud desejada (correspondente a 115200 no seu código)
        }   
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/getPorts")
        try:
            response = requests.post(url, json=data)
            print(response.text)
        except Exception as e:
            print(e)

    def GetPorts_Reader():
        res = dict()
     
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/getPorts")
        try:
            response = requests.post(url, data={})
            print(response.text)
        except Exception as e:
            print(e)

    def GetDeviceParam(self):
        res = dict()
     
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetDevicePara")
        data = {
         "hComm": "1240" #teste
        }
        try:
            response = requests.post(url, json=data)
            return response.text
        except Exception as e:
            print(e)
R = ReaderData()
print(R.Start_Reader())