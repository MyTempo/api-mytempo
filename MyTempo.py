from config import *
from functions import *
from helpers import *
from datetime import datetime, timedelta
from Database import *
from SQliteDB import *
from SqlBuilder import *
import os
import re

class MyTempo:
    
    def __init__(self) -> None:
        self.atletas_da_prova = []
        self.query_inserts = []
        self.tempos = {}
        self.session = ""
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
        LocalDb = LocalDatabase(True)
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)
                results = db.executeQuery(f"SELECT numero, nome, sexo, equipe FROM atletas WHERE idprova = {equipamento['idprova']}")
                
                for r in results:
                    LocalDb.executeNonQuery(f"INSERT INTO atletas_da_prova(numero_atleta, id_prova, nome, sexo, equipe) VALUES ({int(r[0])}, {int(equipamento['idprova'])}, '{r[1]}', '{r[2]}', '{r[3]}');")
                
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


    def getPercursos(self, idprova):
        msg = True
        db = Database(msg)
        localdb = LocalDatabase(msg)
        qb = SQLQueryBuilder()
        
        percursos = qb.Select("idprova, descricaop, km, horalargada, fimlargada, emlargada, tempochecada").From("percurso").Where(f"idprova = {int(idprova)}").Build()
        
        for data in db.executeQuery(percursos, return_as_object=True):

            query = f"INSERT INTO percursos (idprova, descricaop, km, horalargada, fimlargada, tempo_em_largada, tempo_chegada) VALUES ({data.idprova}, '{data.descricaop}', '{data.km}', '{data.horalargada}', '{data.fimlargada}', '{data.emlargada}', '{data.tempochecada}');"


            localdb.executeNonQuery(query)

    def emptyAthletesTable(self):
        LocalDb = LocalDatabase()
        LocalDb.executeNonQuery(f"DELETE FROM atletas_da_prova")       

    def emptyGetPercursos(self):
        LocalDb = LocalDatabase()
        LocalDb.executeNonQuery("DELETE FROM percursos")

    
    def primeirosTempos(self, id_prova, id_check, id_equipamento, atleta, tempo, antena=0, local="", entrada=0, idstaff=9):
        tempo_atleta = f"{datetime.now().date()} {tempo}"
        calculo = sanitizeTimeInput(tempo_atleta)
        verify_athlete = f"SELECT numero_atleta FROM atletas_da_prova WHERE id_prova = {id_prova} AND numero_atleta = {atleta}"
        res = self.localdb.executeQuery(verify_athlete)
        if(len(res) > 0):
            pass
        else:
            query = f"INSERT INTO tempos (idprova, idcheck, idequipamento, numero, tempo, calculo, antena, local, entrada, idstaff) VALUES ({id_prova}, {id_check}, '{id_equipamento}', {atleta}, '{tempo_atleta}', '{calculo}', {antena}, '{local}', {entrada}, {idstaff})"
            self.atletas_enviados.append(query)
            offquery = f"INSERT INTO atletas_da_prova(numero_atleta, id_prova) VALUES ('{atleta}', '{id_prova}')"
            offline_return = self.localdb.executeNonQuery(offquery)
             
    def MainProcess(): ## Este metodo será executado repetidas vezes, é necessário constante otimização e melhoria
        from ReaderData import ReaderData
        from readfiles import Intern
        
        tempos = {}

        if os.path.exists(READER_CONFIG_FILE_PATH):
            equip_dados = r_json(READER_CONFIG_FILE_PATH)
        
        localdb = LocalDatabase()
        qb = SQLQueryBuilder()
        reader = ReaderData()
        helpers = Helpers()
        helpers.created_at = TIME_FORMAT_1 
        horaLargadaOficial = []


        queryPercursos = qb.Select("horalargada, fimlargada, tempo_em_largada, tempo_chegada").From("percursos").Build()
     
        percursosTempos = localdb.executeQuery(queryPercursos, return_as_object=True)
        for percursoI in percursosTempos:
            # Verifica se percursoI não está vazio e se o valor de horalargada não é None
            if percursoI and percursoI.horalargada:
                tempo_str = percursoI.horalargada
                
                if percursoI.tempo_em_largada is not None and isinstance(percursoI.tempo_em_largada, str) and percursoI.tempo_em_largada.isdigit():
                    try:
                        minutos_adicionais = int(percursoI.tempo_em_largada)
                        tempo_datetime = datetime.strptime(tempo_str, '%H:%M:%S') + timedelta(minutes=minutos_adicionais)
                        horaLargadaOficial.append(tempo_datetime.strftime('%H:%M:%S'))
                        
                    except ValueError as e:
                        pass
                else:
                    print("Valor inválido para tempo_em_largada.")
            else:
                print("Valor de horalargada ausente ou inválido.")

        r_file = Intern()
        most_recent_file_path = r_file.getMostRecentFileModified(PATH_BRUTE_DATA)
        
        with open(most_recent_file_path, 'r') as file:
            lines = file.readlines()
        
        unique_lines = list(dict.fromkeys(lines))
        
        lines_without_letters = [line for line in unique_lines if not re.search('[a-zA-Z]', line)]
        for row in lines_without_letters:
            session = str(row[0:3])
            numero_atleta = int(row[23:27])
            tempo_atleta = str(row[27:])

            tempos.setdefault(numero_atleta, []).append(tempo_atleta)

        for numero_atleta, lista_tempos in tempos.items():    
            for l in lista_tempos:
                for horaLargada in horaLargadaOficial:
                    if l >= horaLargada:
                        print("inválido")
                    # elif l > TempoMinimoEmChegada:
                        # classificar enviar o tempo


                pass
       
m = MyTempo()
# m.getPercursos(163)
print(MyTempo.MainProcess())