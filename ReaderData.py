from config import *
import requests
import json
import threading
from functions import *
from helpers import *
from datetime import datetime
from readfiles import Intern
import re
from Upload import *
from SQliteDB import *


class ReaderData:
    def __init__(self) -> None:
        self.hComm = ""
        self.tag_thread = False
        self.is_counting = False
        self.deviceParams = {}
        self.session = ""

        #Setting Configurations 
        self.created_at = ""
        self.server = r_json(path=SERVER_CONFIG_FILE_PATH)
        self.upload = Upload()

        self.reader_data = {
                'server_ip': self.server['server_ip'],
                'ip': READER_DEFAULT_IP,
                'port': self.server['equip_port'],
                'timeoutMs': 3000
            }
        self.equipamento = self.server = r_json(path=READER_CONFIG_FILE_PATH)
        self.localDB = LocalDatabase()
        #data 

        self.atletas_num = []
        self.atletas = []
        self.atletas_tempos = []

    def ReaderStatus(self):
       
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
                res['data'] = response.json()
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
            'strComPort': '',  
            'Baudrate': 115200 
        }   
        
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenDevice")
        try:
            response = requests.post(url, json=data)
            print(response.text)
        except Exception as e:
            print(e)       

    
    def getTagInfo(self):
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetTagInfo")
        tag_info = requests.post(url, data={})
        print(tag_info.text)

    def gettingTagInfo(self):
        while True:
            self.getTagInfo()

    def getTagInfoThread(self):
        if(self.is_counting == True):
            get_tag_info_thread = threading.Thread(target=self.gettingTagInfo)
        if self.tag_thread == False:
            get_tag_info_thread.start()
        else:
            get_tag_info_thread.join()
    
    def getFirstTagInfoThread(self):
        FirstTagInfo = threading.Thread(target=self.getCompressedData)
        FirstTagInfo.start()
    

    def getCompressedData(self):
        self.h = Helpers()
        self.h.created_at = TIME_FORMAT_1 
        r_file = Intern()
        most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
        
        with open(most_recent_file_path, 'r') as file:
            lines = file.readlines()
        
        unique_lines = list(dict.fromkeys(lines))
        
        lines_without_letters = [line for line in unique_lines if not re.search('[a-zA-Z]', line)]
    
        with open(most_recent_file_path, 'w') as output_file:
            output_file.writelines(lines_without_letters)

        tempos = {}    

        try:
            r_file = Intern()
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
            
            with open(most_recent_file_path) as arq:
                rows = arq.read().splitlines()

                tempos = {}
                largou = []
                for row in rows:
                    
                    self.session = str(row[0:3])
                    numero_atleta = int(row[23:27])
                    tempo_atleta = str(row[27:])

                    
                    if numero_atleta not in tempos:
                        tempos[numero_atleta] = [tempo_atleta]

                for numero_atleta, lista_tempos in tempos.items():
                    tempos = {
                        "session": self.session, 
                        "atleta": numero_atleta,
                        "primeiro_tempo": lista_tempos[0],
                        "idprova": self.equipamento["idprova"],
                        "id_equipamento": self.equipamento["equipamento"],
                        "id_checkpoint": self.equipamento['idcheck'],
                        "identificacao": self.equipamento['identificacao'],
                        "hora_prova": self.equipamento['hora']
                    }
                    largou.append(tempos)

                w_json(f"{PATH_REF_DATA}/{self.h.generateTagFileName(self.session, tag_type="refined")}", largou)
                return {"message":"Arquivo Refinado com sucesso!"}
        except Exception as e:
            import traceback
            print(f"Erro: {e}")
            traceback.print_exc()

    def onlyAthleteNum(self, results):
        for r in results:
            self.atletas.append(r[0])
        return self.atletas

        

    def uploadPrimeirosTempos(self):
        
        self.atletas = self.onlyAthleteNum(self.localDB.executeQuery(f"SELECT numero_atleta FROM atletas_da_prova WHERE id_prova = {self.equipamento['idprova']}"))

        self.h = Helpers()
        self.h.created_at = TIME_FORMAT_1 
        r_file = Intern()
        most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
        
        with open(most_recent_file_path, 'r') as file:
            lines = file.readlines()
        
        unique_lines = list(dict.fromkeys(lines))
        
        lines_without_letters = [line for line in unique_lines if not re.search('[a-zA-Z]', line)]
    
        with open(most_recent_file_path, 'w') as output_file:
            output_file.writelines(lines_without_letters)

        tempos = {}    

        try:
            r_file = Intern()
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
            
            with open(most_recent_file_path) as arq:
                rows = arq.read().splitlines()

                tempos = {}
                largou = []
                for row in rows:
                    
                    self.session = str(row[0:3])
                    numero_atleta = int(row[23:27])
                    tempo_atleta = str(row[27:])

                    
                    if numero_atleta not in tempos:
                        tempos[numero_atleta] = [tempo_atleta]

                
         
                for numero_atleta, lista_tempos in tempos.items():
                    self.atletas_num.append(numero_atleta)
                    self.atletas_tempos.append(lista_tempos[0])

                set_atletas = set(self.atletas)
                set_atletas_num = set(self.atletas_num)

                common_atletas = set_atletas.intersection(set_atletas_num)

                for atleta in common_atletas:
                    print(atleta)
                    # self.upload.primeirosTempos(self.equipamento["idprova"], self.equipamento['idcheck'], self.equipamento['equipamento'], atleta, )
                                                
                    # tempos = {
                    #     "session": self.session, 
                    #     "atleta": numero_atleta,
                    #     "primeiro_tempo": lista_tempos[0],
                    #     "idprova": self.equipamento["idprova"],
                    #     "id_equipamento": self.equipamento["equipamento"],
                    #     "id_checkpoint": self.equipamento['idcheck'],
                    #     "identificacao": self.equipamento['identificacao'],
                    #     "hora_prova": self.equipamento['hora']
                    # }
                  
               
                # w_json(f"{PATH_REF_DATA}/{self.h.generateTagFileName(self.session, tag_type="refined")}", largou)
                return {"message":"Arquivo Refinado com sucesso!"}
        except Exception as e:
            import traceback
            print(f"Erro: {e}")
            traceback.print_exc()
  


    def Start_Counting(self, deviceParams = {}):
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        startCount = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/StartCounting")
        response = requests.post(startCount, json=deviceParams)
        print(startCount)
        return response

    def Start_Reader(self):
        self.GetPorts_Reader()
        try:
            server = r_json(path=SERVER_CONFIG_FILE_PATH)
            openConnUrl = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenNetConnection")
            requests.post(openConnUrl, data={})
            url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenNetConnection")
            openNetConnection = requests.post(url, json=self.reader_data)

            if openNetConnection.status_code == 200:
                try:
                    res_data = openNetConnection.json()
                    self.deviceParams = res_data

                    r_data = res_data.get("data")
                    self.hComm = r_data.get("hComm")
                    if self.hComm:
                        getDeviceParam = self.GetDeviceParam(hComm=self.hComm)
                        print(getDeviceParam)
                        deviceParams = getDeviceParam.get("data")
                        if(deviceParams.get("res_code") == 1001):
                            self.RetryToConnect_Reader()

                        else:
                            if deviceParams:
                                StartCounting = self.Start_Counting(deviceParams=Helpers.FormatDeviceParams(deviceParams=deviceParams, hComm=self.hComm))
                                if(deviceParams.get("res_code") != 1001):
                                    if StartCounting.status_code == 200:          
                                        self.is_counting = True
                                        self.gettingTagInfo()
                                        return {
                                            'status': 'success',
                                            'message': 'Sucesso ao Iniciar o processamento',
                                            'erro': 0,
                                            'retornomsg': "Leitor iniciado com sucesso",
                                        }
                                    else:
                                        return {
                                            'status': 'error',
                                            'message': 'Falha ao iniciar o processamento',
                                            'erro': 1,
                                            'retornomsg': "Falha ao iniciar o leitor",
                                            "status_code": StartCounting.status_code
                                        }
                             
                except json.JSONDecodeError:
                    print("Error decoding JSON response.")
        except Exception as e:
            print(e)
            

    def Stop_Reader(self):
        if(self.hComm):
            self.stopInventory()
            self.closeDevice()
            
    def RetryToConnect_Reader(self):
        import time
        print("Tentando conectar aguarde um pouco...")
        self.closeDevice()
        time.sleep(5)
        self.Start_Reader()
          

    def getPower_Reader():
        
        res = dict()
      
        data = {
            'strComPort': '',  
            'Baudrate': 115200 
        }   
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/getPorts")
        try:
            response = requests.post(url, json=data)
            print(response.text)
        except Exception as e:
            print(e)

    def GetPorts_Reader(self):
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
        if(self.hComm):
            data = {
                "hComm": self.hComm 
            }
        else:
            data = {
                "hComm": hComm 
            }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(e)
    
    def stopInventory(self):
        res = dict()
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        data = {
                'ip': server['server_ip'],
                'port': server['equip_port'],
                'timeoutMs': 3000
                }
            
        url_openConn = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/OpenNetConnection")
        openNetConnection = requests.post(url_openConn, json=data)
        if openNetConnection.status_code == 200:
            res_data = openNetConnection.json()
            r_data = res_data.get("data")
            self.hComm = r_data.get("hComm")
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/InventoryStop")
        data = {
         "hComm": self.hComm, 
         "timeout": 10000
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(e)

    def closeDevice(self):
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        data = {
            'ip': server['server_ip'],
            'port': server['equip_port'],
            }
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/CloseDevice")
        data = {
         "hComm": self.hComm, 
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(e)    


r = ReaderData()

r.uploadPrimeirosTempos()