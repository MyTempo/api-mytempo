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
                            
                            return "Equipamento iniciado e configurado com sucesso!"
            except FileNotFoundError as e:
                print("Falha ao configurar servidor remoto: -> ", e)

    def verifyDB(self):
        return os.path.exists(DB_PATH)
    
    def mountAthleteData(atleta="", tempo="", antena=0, local="", entrada=0, idstaff=9):
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)
         
                tempo_atleta = f"{datetime.now().date()} {tempo}"
                calculo = sanitizeTimeInput(tempo_atleta)
                query = f"INSERT INTO tempos (idprova, idcheck, idequipamento, numero, tempo, calculo, antena, local, entrada, idstaff) VALUES ({equipamento['idprova']}, {equipamento['idcheck']}, '{equipamento["equipamento"]}', {atleta}, '{tempo_atleta}', '{calculo}', {antena}, '{local}', {entrada}, {idstaff})"
                return query
            except Exception as e:
                print(f"erro ao montar query: -> {e}")
    
                
    def GetAthletes(self):
        db = Database(True)
        LocalDb = LocalDatabase(True)
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)
                results = db.executeQuery(f"SELECT numero, nome, sexo, equipe, percurso FROM atletas WHERE idprova = {equipamento['idprova']}")
                
                for r in results:
                    LocalDb.executeNonQuery(f"INSERT INTO atletas_da_prova(numero_atleta, id_prova, nome, sexo, equipe, percurso) VALUES ({int(r[0])}, {int(equipamento['idprova'])}, '{r[1]}', '{r[2]}', '{r[3]}', {int(r[4])});")
                
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
        qb = SQLQueryBuilder()
        
        percursos = qb.Select("idprova, descricaop, km, horalargada, fimlargada, emlargada, tempochecada, id").From("percurso").Where(f"idprova = {int(idprova)}").Build()
        
        with LocalDatabase(msg) as localdb:
            for data in db.executeQuery(percursos, return_as_object=True):
                query = f"INSERT INTO percursos (idprova, descricaop, km, horalargada, fimlargada, tempo_em_largada, tempo_chegada, id_percurso) VALUES ({data.idprova}, '{data.descricaop}', '{data.km}', '{data.horalargada}', '{data.fimlargada}', '{data.emlargada}', '{data.tempochecada}', {data.id});"
                localdb.executeNonQuery(query)

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
            self.localdb.executeNonQuery(offquery)
             
    def MainProcess() -> None:
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
        tempoMinimoChegada = []
        horaLargada_ = []
        tempoChegada = []
        
        queryPercursos = qb.Select("horalargada, fimlargada, tempo_em_largada, tempo_chegada").From("percursos").Where("horalargada IS NOT NULL AND fimlargada IS NOT NULL").Build()
        percursosTempos = localdb.executeQuery(queryPercursos, return_as_object=True)

        for percursoI in percursosTempos:
            if percursoI and percursoI.horalargada and percursoI.fimlargada:
                tempo_str = percursoI.horalargada
                chegada_str = percursoI.fimlargada
            
                if percursoI.tempo_em_largada is not None and isinstance(percursoI.tempo_em_largada, str) and percursoI.tempo_em_largada.isdigit():
                    try:
                        if percursoI.fimlargada is not None and isinstance(percursoI.fimlargada, str):
                            chegada_datetime = datetime.strptime(percursoI.fimlargada, '%H:%M:%S')
                            duracao_chegada = datetime.strptime(percursoI.tempo_chegada, '%H:%M:%S') - datetime.min
                            chegada_formatada = chegada_datetime + duracao_chegada
                            tempoMinimoChegada.append(chegada_formatada.strftime('%H:%M:%S'))

                            if percursoI.tempo_chegada is not None and isinstance(percursoI.tempo_chegada, str):
                                tempoChegada.append(percursoI.tempo_chegada)
                    except ValueError as e:
                        pass
                    try:
                        minutos_adicionais = int(percursoI.tempo_em_largada)
                        tempo_datetime = datetime.strptime(tempo_str, '%H:%M:%S') + timedelta(minutes=minutos_adicionais)
                        horaLargada_.append(tempo_str)
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

        tempos_atletas = {}
    
        for numero_atleta, lista_tempos in tempos.items():
                    
            tempos_atletas.setdefault(numero_atleta, {'largada': [], 'chegada': []})

            for horaLargada, MinEmchegada, horaLargada_ofc in zip(horaLargadaOficial, tempoMinimoChegada, horaLargada_):
                largada_atleta = None
                tempo_chegada = None

                for tempo in lista_tempos:
                    try:
                        if tempo >= horaLargada_ofc and tempo <= horaLargada:
                            largada_atleta = tempo
                        if tempo >= horaLargada and tempo >= MinEmchegada:
                            tempo_chegada = tempo
                    except ValueError:
                        print(f"O tempo {tempo} não está no formato correto e será ignorado.")

                if largada_atleta is not None:
                    tempos_atletas[numero_atleta]['largada'].append(largada_atleta)
                if tempo_chegada is not None:
                    tempos_atletas[numero_atleta]['chegada'].append(tempo_chegada)
        
        qb.reset()
        atletas_percurso = qb.Select("DISTINCT atletas_da_prova.*, percursos.*").From("atletas_da_prova").Join("percursos", "atletas_da_prova.percurso = percursos.id_percurso").Where(f"idprova = {equip_dados['idprova']}").Where("horalargada IS NOT NULL AND fimlargada IS NOT NULL").Build()

        res = localdb.executeQuery(atletas_percurso, return_as_object=True)
       
        t_atletas = {}

        for atl in res:
            for atleta_id, atleta_data in tempos_atletas.items():
                if atl.numero_atleta == atleta_id:
                    if "largada" not in t_atletas.get(atleta_id, {}):
                        t_atletas[atleta_id] = {"largada": [], "chegada": []}
                   
                    horalargada_datetime = datetime.strptime(atl.horalargada, '%H:%M:%S')
                    larg_total = horalargada_datetime + timedelta(minutes=int(atl.tempo_em_largada))

                    print(atl.horalargada)
                    print(larg_total.time())
                    for a_key, a_value in atleta_data.items():
                        if a_key == "largada":
                            for larg in a_value:
                                larg_time = datetime.strptime(larg, '%H:%M:%S.%f').time()
                                if larg_time >= horalargada_datetime.time() and larg_time <= larg_total.time():
                                    t_atletas[atleta_id]["largada"].append(larg_time)

                        elif a_key == "chegada":
                            for cheg in a_value:
                                if cheg >= horaLargada and cheg >= MinEmchegada:
                                    t_atletas[atleta_id]["chegada"].append(cheg)

                        
        for tempos_l in t_atletas.items():
            print(tempos_l)
            # print(tempos_l[1].items())


m = MyTempo()

# m.emptyGetPercursos()
# m.getPercursos(163)
print(MyTempo.MainProcess())
# print(m.GetAthletes())
