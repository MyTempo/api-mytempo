from config import *
from functions import *
from helpers import *
from datetime import datetime
from Database import *
from SQliteDB import *
import os
class MyTempo:
    
    def __init__(self) -> None:
        self.atletas_da_prova = []
        self.query_inserts = []
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
                            self.emptyAthletesTable()
                            # self.GetAthletes()
                            return "Equipamento iniciado e configurado com sucesso!"
            except FileNotFoundError as e:
                print("Falha ao configurar servidor remoto: -> ", e)

    def verifyDB(self):
        return os.path.exists(DB_PATH)

    def GetAthletes(self):
        db = Database()
        LocalDb = LocalDatabase()
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)
                results = db.executeQuery(f"SELECT numero FROM atletas WHERE idprova = {equipamento['idprova']}")
                for r in results:
                    LocalDb.executeNonQuery(f"INSERT INTO atletas_da_prova(numero_atleta, id_prova) VALUES ({int(r[0])}, {int(equipamento['idprova'])});")
                
                return {                
                    'status': 'success',
                    'message': 'Tudo certo!',
                    'erro': 0,
                    'retornomsg': 'Atletas Baixados com sucesso!',
                    }
            
            except Exception:
                return {                
                    'status': 'error',
                    'message': 'Ocorreu um erro ao baixar os atletas',
                    'erro': 0,
                    'retornomsg': 'Ocorreu um erro ao baixar os atletas',
                    }

    def emptyAthletesTable(self):
        LocalDb = LocalDatabase(True)
        LocalDb.executeNonQuery(f"DELETE FROM atletas_da_prova")       

    


