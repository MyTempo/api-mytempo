from API.config.config import *
import requests
import json
import threading
from API.helpers.functions import *
from API.helpers.helpers import *
from readfiles import Intern
import re
from Upload import *
from API.models.SQliteDB import *
import time
import traceback


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
        self.is_sending = False
        self.tempos = {}
        self.primeiros_tempos_minerados = []
    def ReaderStatus(self):
       
        res = dict()
        # URL do seu aplicativo Flask
        server = r_json(path=SERVER_CONFIG_FILE_PATH)
        getting_tag = r_json(path=CONFIG_FILE_PATH)
        url = Helpers.mount_url("http", f"{server['server_ip']}:{READER_SERVER_PORT}", "/GetTagInfo")
        if(getting_tag.get("getting_tag") == "active"):
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
        else:
            res['status'] = "success"
            res['message'] = "A leitura está em desativada."
            res["erro"] = 0
            res['retornomsg'] = "O Equipamento não está ativa!"
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
            try:
                getting_tag = r_json(path=CONFIG_FILE_PATH)
                if getting_tag.get("getting_tag") == "active":
                    self.getTagInfo()
            except Exception as e: # tentar novamente
                print(f"Erro ao decodificar JSON: {e}")
                time.sleep(1)  

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
        try:
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
            
            with open(most_recent_file_path, 'r') as file:
                lines = file.readlines()
            
            unique_lines = list(dict.fromkeys(lines))
            
            lines_without_letters = [line for line in unique_lines if not re.search('[a-zA-Z]', line)]
        
            with open(most_recent_file_path, 'w') as output_file:
                output_file.writelines(lines_without_letters)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: -> {e}")

            
    def getFirstOfAthlete(self):
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
                    print(tempos)
                    tempos = {
                        "session": self.session, 
                        "atleta": numero_atleta,
                        "primeiro_tempo": lista_tempos,
                        "idprova": self.equipamento["idprova"],
                        "id_equipamento": self.equipamento["equipamento"],
                        "id_checkpoint": self.equipamento['idcheck'],
                        "identificacao": self.equipamento['identificacao'],
                        "hora_prova": self.equipamento['hora']
                    }
                    largou.append(tempos)

                
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
                  
                    print(f"{numero_atleta} tempo: {lista_tempos}")
                       
                    
                # db = Database()
                # db.conn = mysql.connector.connect(
                # host=db.host,
                # user=db.user,
                # password=db.password,
                # database=db.database
                # )

                # if db.conn.is_connected():
                #     cursor = db.conn.cursor()

                #     for q in self.upload.atletas_enviados: 
                #         cursor.execute(q)

                #     cursor.close()
                #     db.conn.commit()
                #     db.conn.close()
                # return {"message": "sucesso!"}
        except Exception as e:
            import traceback
            print(f"Erro: {e}")
            traceback.print_exc()

    def background_check(self):
        while True:
            if self.is_sending:
                time.sleep(5)

            if self.is_sending == False:
                break

    def StartSendLoop(self):
        bg_thread = threading.Thread(target=self.background_check)
        bg_thread.daemon = True  
        bg_thread.start()

        while True:
            if self.is_sending:
                send_thread = threading.Thread(target=self.uploadPrimeirosTempos)
                send_thread.start()
                send_thread.join() 
            else:
                pass
            time.sleep(5)
    def toggleEnvio(self, estado):
        self.is_sending = estado 

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

    def readFiles(self):
        try:
            r_file = Intern()
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
            
            with open(most_recent_file_path) as arq:

                rows = arq.read().splitlines()
         
                for row in rows:
                    try:
                        if len(row) < DEFAULT_TAG_LEN:
                            self.session = str(row[0:3])
                            numero_atleta = int(row[8:19])
                            tempo_atleta = str(row[19:31])
                        elif len(row) == DEFAULT_TAG_LEN:
                            self.session = str(row[0:3])
                            numero_atleta = int(row[23:27])
                            tempo_atleta = str(row[27:])
                    except ValueError as e:
                        print("Erro ao ler o arquivo: valor inválido encontrado ->", e)
                        continue
                    
                    self.tempos.setdefault(numero_atleta, []).append(tempo_atleta)

        except FileNotFoundError:
            print("Arquivo não encontrado")
        except ValueError:
                traceback.print_exc() 
                print("Erro ao ler o arquivo: valor inválido encontrado")

        self.tempos = self.tempos
        return self.tempos

    def getLastTime(self):
        # pega o ultimo tempo de cada atleta 0
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            query = """ CREATE TABLE IF NOT EXISTS tempos_first (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        atleta TEXT,
                        tempo TEXT
                    );"""
            cursor.execute(query)
            print('Tabela criada com sucesso!')

            lista = []
            tempos = self.readFiles()
            print(tempos)
            for numero_atleta, lista_tempos in tempos.items():
                for tempo in lista_tempos:
                    cursor.execute("INSERT INTO tempos_first (atleta, tempo) VALUES (?, ?)",
                                    (numero_atleta, tempo))

            query = cursor.execute(f"""
                                SELECT atleta, tempo
                                FROM (
                                        SELECT atleta, tempo,
                                            ROW_NUMBER() OVER (PARTITION BY atleta ORDER BY tempo DESC) AS row_num
                                        FROM tempos_first
                                    ) ranked
                                    WHERE row_num = 1;

                                """)
            rows = cursor.fetchall()
            cursor.execute('DROP TABLE tempos_first')
            conn.close()
            for temps in rows:
                self.ultimos_tempos_minerados.append(temps)

            return self.ultimos_tempos_minerados
        except conn as e:
            print("Erro ")

    def getFirstTime(self, tempo_prova):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = """ CREATE TABLE IF NOT EXISTS tempos_first (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    atleta TEXT,
                    tempo TEXT
                );"""
        cursor.execute(query)

        lista = []
        tempos = self.readFiles()
        print(tempos)
        for numero_atleta, lista_tempos in tempos.items():
            for tempo in lista_tempos:
                cursor.execute("INSERT INTO tempos_first (atleta, tempo) VALUES (?, ?)",
                                (numero_atleta, tempo))

        query = cursor.execute(f"""
                                SELECT atleta, MIN(tempo) AS menor_tempo
                                FROM tempos_first
                                WHERE TIME(tempo) >= TIME('{tempo_prova}')
                                GROUP BY atleta;
                               """)
        rows = cursor.fetchall()
        cursor.execute('DROP TABLE tempos_first')
        conn.close()
        for temps in rows:
            self.primeiros_tempos_minerados.append(temps)
        # print('  atleta   |   tempos')

        # for t in self.primeiros_tempos_minerados:
        #     print(t)
        print(self.primeiros_tempos_minerados)
    
        return self.primeiros_tempos_minerados
        
    def getCompressedDataAll(self):
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

        try:
            r_file = Intern()
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
            
            with open(most_recent_file_path) as arq:

                rows = arq.read().splitlines()

         
                for row in rows:
              
                    self.session = str(row[0:3])
                    numero_atleta = int(row[23:27])
                    tempo_atleta = str(row[27:])

                    self.tempos.setdefault(numero_atleta, []).append(tempo_atleta)

        except FileNotFoundError:
            print("Arquivo não encontrado")
        except ValueError:
                print("Erro ao ler o arquivo: valor inválido encontrado")

        self.tempos = self.tempos
        return self.tempos
    



    # 0000-0000-0078-9000-0000-0543:1714486413306677:1 
    def handleRequest(content):
        if content != None or content != "":
            data_parts = content.split(":")
            tag_code = data_parts[0]
            tag_timestamp = data_parts[1]
            # antenna_id = data_parts[2];
            timestamp = convert_time_from_microseconds(tag_timestamp)
            print(timestamp)
            tag = tag_code.replace('-', "")
            return tag + timestamp

class TagFile:
    def __init__(self) -> None:
        self.fileName = self.generateTagFileName("brute")
        self.filePath = os.path.join(PATH_BRUTE_DATA, self.fileName)

    def generateTagFileName(self, type_t):
       
        if(type_t == "brute"):
            file_name = f'MyTempo-Bruto-Sess-{Helpers.generateRandomNum_int(3)} T-{TIME_FORMAT_2}.txt'
        elif(type_t == "refined"):
            file_name = f'MyTempo-Ref-Sess-{Helpers.generateRandomNum_int(3)} T-{TIME_FORMAT_2}.txt'
        else:
            file_name = type_t
        print(file_name)
        return file_name
    

    def makeFile(self):
        try:
            with open(self.filePath, 'r') as arquivo:
                print(f'O arquivo "{self.filePath}" já existe.')
                return
        except FileNotFoundError:
           
            with open(self.filePath, 'w') as arquivo:
                print(f'O arquivo "{self.filePath}" foi criado.')

    # uncomplete            
    def saveOnFile(self, tag_info, type_f="brute"):
        if os.path.exists(self.filePath):
            with open(self.filePath, "a") as file:
                for tag in tag_info: 
                    file.write(tag)
                    file.write("\n")

    def saveThisOnFile(self, tag_info):
        if os.path.exists(self.filePath):
            with open(self.filePath, "a") as file:
                file.write(tag_info)
                file.write("\n")
                file.close()
        else:
            print("Caminho: ", self.filePath, " não existe")



