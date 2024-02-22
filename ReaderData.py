from config import *
import requests
import json
import threading
from functions import *
from helpers import *
from datetime import datetime


class ReaderData:
    def __init__(self) -> None:
        self.hComm = ""
        self.tag_thread = False
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

    def Stop_Reader(self):
        if(self.hComm):
            print(self.hComm)
    
    def getTagInfo(self):
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetTagInfo")
        tag_info = requests.post(url, data={})
        print(tag_info.text)

    def gettingTagInfo(self):
        while True:
            self.getTagInfo()

    def getTagInfoThread(self):
        get_tag_info_thread = threading.Thread(target=self.gettingTagInfo)
        if self.tag_thread == False:
            get_tag_info_thread.start()
        else:
            get_tag_info_thread.join()
        
    def Start_Reader(self):
        try:
            server = r_json(path=SERVER_CONFIG_FILE_PATH)
            data = {
                'ip': server['server_ip'],
                'port': server['equip_port'],
                'timeoutMs': 3000
            }
            url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenNetConnection")
            openNetConnection = requests.post(url, json=data)

            if openNetConnection.status_code == 200:
                try:
                    res_data = openNetConnection.json()
                    r_data = res_data.get("data")
                    self.hComm = r_data.get("hComm")
                    if self.hComm:
                        getDeviceParam = self.GetDeviceParam(hComm=self.hComm)
                        deviceParams = getDeviceParam.get("data")
                        print(deviceParams)
                        print("aqui passou")
                        if deviceParams:
                            startCount = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/StartCounting")
                            response = requests.post(startCount, json=deviceParams)
                            print(response.text)
                            if response.status_code == 200:
                                print(response.text)
                                self.gettingTagInfo()
                            else:
                                print(f"Failed to start counting. Status code: {response.status_code}")
                except json.JSONDecodeError:
                    print("Error decoding JSON response.")
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

    def GetDeviceParam(self, hComm=""):
        res = dict()
     
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetDevicePara")
        data = {
         "hComm": hComm #teste
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(e)
    
    def stopInventory(self, hComm=""):
        res = dict()
     
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/InventoryStop")
        data = {
         "hComm": hComm #teste
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(e)
R = ReaderData()
print(R.Start_Reader())
