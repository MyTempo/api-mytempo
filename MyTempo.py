from API.config.config import *
from API.helpers.functions import *
from API.helpers.helpers import *
from API.models.Database import *
from API.models.SQliteDB import *
from API.models.SqlBuilder import *
from system import *
from ReaderData import ReaderData
from datetime import datetime, timedelta
import threading
import os
import re
import time


class MyTempo:
    
    def __init__(self) -> None:
        self.atletas_da_prova = []
        self.query_inserts = []
        self.tempos = {}
        self.session = ""
        self.is_uploading = False


    def setIp(self, ip, port):
        localdb = LocalDatabase()
        sqlb = SQLQueryBuilder()
        if os.path.exists(SERVER_CONFIG_FILE_PATH):
            try:
                if os.path.exists(READER_CONFIG_FILE_PATH):
                    equip = ""
                    try:
                        equip_dados = r_json(READER_CONFIG_FILE_PATH)
                        equip = equip_dados["equipamento"]
                    except Exception:
                        equip = localdb.executeQuery(sqlb.Select("equipamento").From("equip_data").Build())[0][0]
                    if(ip and port):
                        db = Database()
                        update = f"UPDATE `equipamentos_cadastro` SET `ip` = '{ip}:{port}' WHERE `equipamentos_cadastro`.`id` = {equip} "
                        result = db.executeNonQuery(update)
                        if result['status'] == "success":
                            MyTempo.setupReaderData(MyTempo())
                            
                            
                            return "Equipamento iniciado e configurado com sucesso!"
            except FileNotFoundError as e:
                print("Falha ao configurar servidor remoto: -> ", e)

    def save_equip(data):
        localdb = LocalDatabase()
        sqlb = SQLQueryBuilder()
        localdb.openOnlyExec()
        localdb.OnlyExecute(sqlb.Delete("equip_data").Build())
        localdb.OnlyExecute(
            sqlb.
            Insert("equip_data").Set(
            data_prova=data.get("dataprova"), 
            descricao_check=data.get("descricao_check"), 
            equipamento=data.get("equipamento"), 
            fabricante=data.get("fabricante"), 
            hora=data.get("hora"), 
            idcheck=data.get("idcheck"), 
            identificacao=data.get("identificacao"), 
            idprova=data.get("idprova"), 
            last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
            modelo=data.get("modelo"), 
            serie=data.get("serie"),
            status=data.get("status"), 
            tituloprova=data.get("tituloprova"))
            .Build()
            )
        localdb.closeOnlyExec()
    
    def save_server(server):
        localdb = LocalDatabase(True)
        sqlb = SQLQueryBuilder()
        localdb.openOnlyExec()
        print()
        localdb.OnlyExecute(sqlb.Delete("server").Build())
        localdb.OnlyExecute(sqlb.Insert("server").Set(
            server_ip=str(server.get("server_ip")),
            port=str(server.get("port")),
            equip_port=str(server.get("equip_port"))
        ).Build())
        localdb.closeOnlyExec()

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

    def mountAndVerifyIfAthleteDataExists(atleta="", tempo="", antena=0, local="", entrada=0, idstaff=9):
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)
         
                tempo_atleta = f"{datetime.now().date()} {tempo}"
                calculo = sanitizeTimeInput(tempo_atleta)
                query = f"INSERT OR IGNORE INTO tempos (idprova, idcheck, idequipamento, numero, tempo, calculo, antena, local, entrada, idstaff) VALUES ({equipamento['idprova']}, {equipamento['idcheck']}, '{equipamento["equipamento"]}', {atleta}, '{tempo_atleta}', '{calculo}', {antena}, '{local}', {entrada}, {idstaff})"
                return query
            except Exception as e:
                print(f"erro ao montar query: -> {e}")

    def mountAthleteDataCol(col_name, atleta="", tempo="", antena=0, local="", entrada=0, idstaff=9):
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                equipamento = r_json(READER_CONFIG_FILE_PATH)

                tempo_atleta = tempo
                calculo = sanitizeTimeInput(tempo_atleta)
                query = f"INSERT INTO {col_name} (idprova, idcheck, idequipamento, numero, tempo, calculo, antena, local, entrada, idstaff) VALUES ({equipamento['idprova']}, {equipamento['idcheck']}, '{equipamento["equipamento"]}', {atleta}, '{tempo_atleta}', '{calculo}', {antena}, '{local}', {entrada}, {idstaff})"
                return query
            except Exception as e:
                print(f"erro ao montar query: -> {e}")
      
    def GetAthletes(self):
        db = Database()
        localdb = LocalDatabase()
        if os.path.exists(READER_CONFIG_FILE_PATH):
            try:
                localdb.openOnlyExec()
                equipamento = r_json(READER_CONFIG_FILE_PATH)
                results = db.executeQuery(f"SELECT numero, nome, sexo, equipe, percurso FROM atletas WHERE idprova = {equipamento['idprova']}")
                
                for r in results:
                    localdb.OnlyExecute(f"INSERT INTO atletas_da_prova(numero_atleta, id_prova, nome, sexo, equipe, percurso) VALUES ({int(r[0])}, {int(equipamento['idprova'])}, '{r[1]}', '{r[2]}', '{r[3]}', {int(r[4])});")
                localdb.closeOnlyExec()
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

        db = Database()
        qb = SQLQueryBuilder()
        
        percursos = qb.Select("idprova, descricaop, km, horalargada, fimlargada, emlargada, tempochecada, id").From("percurso").Where(f"idprova = {int(idprova)}").Build()
        
        localdb = LocalDatabase()
        localdb.openOnlyExec()
        try:
            for data in db.executeQuery(percursos, return_as_object=True):
                query = f"INSERT INTO percursos (idprova, descricaop, km, horalargada, fimlargada, tempo_em_largada, tempo_chegada, id_percurso) VALUES ({data.idprova}, '{data.descricaop}', '{data.km}', '{data.horalargada}', '{data.fimlargada}', '{data.emlargada}', '{data.tempochecada}', {data.id});"
                localdb.OnlyExecute(query)
        
            localdb.closeOnlyExec() 
        except Exception as e:
            print(e)
            
    def emptyAthletesTable(self):
        LocalDb = LocalDatabase()
        LocalDb.executeNonQuery(f"DELETE FROM atletas_da_prova")       

    def emptyPercursos(self):
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
    

    def writeRefined(data_list):
        from readfiles import Intern
        r_file = Intern()
        try:
            most_recent_file_path = r_file.getMostRecentFileModified(PATH_REF_DATA)

            with open(most_recent_file_path, "w") as arquivo:
                for data in data_list:
                    athlete_num, time = data
                    num_of_zeros = 19 - len(str(athlete_num))
                    complement = "0" * num_of_zeros
                    formatted_data = f"{complement}{athlete_num}{time}\n"
                    arquivo.write(formatted_data)
        except Exception as e: 
            print(e)
            return
    

    def sel_sys_settings_fields(field):
        sqlb = SQLQueryBuilder() 
        localdb = LocalDatabase()
  
        return localdb.executeQuery(sqlb.Select(field).From("system_settings").Build())[0][0]
    
    def set_config_field(field, value):
        sqlb = SQLQueryBuilder() 
        localdb = LocalDatabase()
        fields = {field: value}
        return localdb.executeNonQuery(sqlb.Update("system_settings").Set(**fields).Build())


    def BackgroundProcess(self):

        is_active = MyTempo.sel_sys_settings_fields("bg_process_active")
        while(is_active == 1):
            try:
                MyTempo.processAthleteTimes()    
                print("rodando...")
                time.sleep(5)
            except Exception as e:
                print("ocorreu um erro: -> ", e)
                time.sleep(5)
                self.processAthleteTimes()

    def callBackgroundProcess(self):
        if self.is_uploading == False:
            backgroundProcess = threading.Thread(target=self.BackgroundProcess)
            backgroundProcess.start()
        else:
            backgroundProcess.join()

    def autoBackup():
        localdb = LocalDatabase(True)
        localdb.openOnlyExec()
        localdb.OnlyExecute("""
            INSERT INTO atletas_tempos_backup (numero_atleta, tempo, time_stamp)
            SELECT DISTINCT t.numero_atleta, t.tempo, datetime('now')
            FROM atletas_tempos AS t
            LEFT JOIN atletas_tempos_backup AS b 
                ON b.numero_atleta = t.numero_atleta AND b.tempo = t.tempo
            WHERE b.numero_atleta IS NULL;
        """)
        localdb.closeOnlyExec()
        

    def uploadTempos():
        my = MyTempo()
        localdb = LocalDatabase()
        db = Database()
        sqlb = SQLQueryBuilder()

        atletas_local = localdb.executeQuery(sqlb.Select("*").From("tempos").Build(), return_as_object=True)
        
        sqlb.reset()
        lista_q = []

       # basicamente, verifica se o atleta já foi enviado para o servidor, baseado em uma tabela no db local
        for atletas_l in atletas_local:
            sqlb.reset()
            atletas_ = sqlb.Select("*").From("recover").Where(f"numero = {atletas_l.numero} AND tempo = '{atletas_l.tempo}'").Build()
            lista_q.append(atletas_)

        localdb.openOnlyExec()
        db.openOnlyExec()
        for i, query in enumerate(lista_q):
            res = localdb.OnlyExecute(query)
            if not res:
                db.OnlyExecute(MyTempo.mountAthleteDataCol(col_name="tempos",atleta=atletas_local[i].numero, tempo=atletas_local[i].tempo, local=atletas_local[i].local, entrada=ENTRY_TYPE))
                localdb.OnlyExecute(MyTempo.mountAthleteDataCol(col_name="recover", atleta=atletas_local[i].numero, tempo=atletas_local[i].tempo, local=atletas_local[i].local, entrada=ENTRY_TYPE))
        localdb.closeOnlyExec()
        db.closeOnlyExec()

    def MainProcess() -> None:
        from readfiles import Intern
        
        tempos = {}
        
        if os.path.exists(READER_CONFIG_FILE_PATH):
            equip_dados = r_json(READER_CONFIG_FILE_PATH)
        
        localdb = LocalDatabase()
        qb = SQLQueryBuilder()
        helpers = Helpers()
        helpers.created_at = TIME_FORMAT_1 
        horaLargadaOficial = []
        tempoMinimoChegada = []
        horaLargada_ = []
        tempoChegada = []

        queryPercursos = qb.Select("horalargada, fimlargada, tempo_em_largada, tempo_chegada").From("percursos").Where("horalargada IS NOT NULL AND fimlargada IS NOT NULL").Build()
        percursosTempos = localdb.executeQuery(queryPercursos, return_as_object=True)

        # pega trata o tempo de cada percurso, formatando os tempos e somando os adicionais
        #   |
        #  \/       
        for percursoI in percursosTempos:
            if percursoI and percursoI.horalargada and percursoI.fimlargada:
                tempo_str = percursoI.horalargada
                # chegada_str = percursoI.fimlargada

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
        r_data = ReaderData()
        r_data.getCompressedData()
        with open(most_recent_file_path, 'r') as file:
            lines = file.readlines()
        
        unique_lines = list(dict.fromkeys(lines))
        
        lines_without_letters = [line for line in unique_lines if not re.search('[a-zA-Z]', line)]

        for row in lines_without_letters:
            # session = str(row[0:3])
            numero_atleta = int(row[23:27])
            tempo_atleta = str(row[27:])
            tempos.setdefault(numero_atleta, []).append(tempo_atleta)

        tempos_atletas = {}

        
        for numero_atleta, lista_tempos in tempos.items():
            if len(lista_tempos) > 0:
                print(f"atleta {numero_atleta} ainda não possui tempos válidos em relação aos horarios de largada e chegada!")
          
        
            tempos_atletas.setdefault(numero_atleta, {'largada': [], 'chegada': []})
            
            # iterar com os atletas sobre cada percurso (ficar em observação de como se comporta)
            #  |
            # \/

            for horaLargada, MinEmchegada, horaLargada_ofc in zip(horaLargadaOficial, tempoMinimoChegada, horaLargada_):
                largada_atleta = None
                tempo_chegada = None
                for tempo in lista_tempos:
                    # print(horaLargada, MinEmchegada, horaLargada_ofc)
                        # 16:05:00     16:15:00      16:00:00
                    try:
                        # print(f"{tempo} {horaLargada}")
                        if tempo >= horaLargada_ofc and tempo <= horaLargada:
                            largada_atleta = tempo
                            print(f"largada do atleta no percurso de {horaLargada_ofc}")
                        if tempo >= horaLargada and tempo >= MinEmchegada:
                            print(f"chegada do atleta no percurso de {MinEmchegada}")
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

        # itera sobre cada atleta para saber em qual percurso ele é pertencente

        for atl in res:  
            for atleta_id, atleta_data in tempos_atletas.items():
               
                if atl.numero_atleta == atleta_id:
                    if "largada" not in t_atletas.get(atleta_id, {}):
                        t_atletas[atleta_id] = {"largada": [], "chegada": []}
                    horalargada_datetime = datetime.strptime(atl.horalargada, '%H:%M:%S')
                    larg_total = horalargada_datetime + timedelta(minutes=int(atl.tempo_em_largada))
                    
                    chegada_ = datetime.strptime(atl.fimlargada, '%H:%M:%S')
                    duracao_chegada_total = datetime.strptime(atl.tempo_chegada, '%H:%M:%S') - datetime.min
                    chegada_total = chegada_ + duracao_chegada_total
                    chegada_total = chegada_total.time()

                    for a_key, a_value in atleta_data.items():
                        if a_key == "largada":
                            for larg in a_value:
                         
                                larg_trunc = larg.split('.')[0]  
                                larg_time = datetime.strptime(larg_trunc, '%H:%M:%S').time()
                        
                                if larg_time >= horalargada_datetime.time() and larg_time <= larg_total.time():
                                    
                                    t_atletas[atleta_id]["largada"].append(larg)

                        elif a_key == "chegada":
                            for cheg in a_value:
                                if cheg >= horaLargada and cheg >= str(chegada_total):
                                    t_atletas[atleta_id]["chegada"].append(cheg)
                                    
                 
        tempos_atletas_agrupados = {}

        # agrupa os atletas e separa os tempos por largada e chegada, baseado na lógica de maior e menor tempo né aff

        for atleta_id, tempos in t_atletas.items():
            largada = []
            chegada = []

            if 'largada' in tempos:
                largada = sorted(set(tempos['largada']), key=lambda x: tempos['largada'].index(x))
            if 'chegada' in tempos:
                chegada = sorted(set(tempos['chegada']), key=lambda x: tempos['chegada'].index(x))

            tempos_atletas_agrupados[atleta_id] = {'largada': largada, 'chegada': chegada}

        qb.reset()
        atletas = qb.Select("numero").From("tempos").Where(f"idprova = {equip_dados['idprova']}").Build()
        r_atletas = localdb.executeQuery(atletas, return_as_object=True)

        atletas_existentes = set([atl_in_base.numero for atl_in_base in r_atletas])
        
        localdb.openOnlyExec()
        for ta in tempos_atletas_agrupados.items():
            atleta_id = ta[0]
            tempos_atleta = ta[1]
            
            if atleta_id in atletas_existentes:
                print(f"{atleta_id} já existente na base")
                continue
                
            #itera sobre as listas preparadas e prepara para o processamento
            for tipo_tempo, lista_tempos in tempos_atleta.items():
                
                if tipo_tempo == "largada":

                    if lista_tempos:
                        if(len(lista_tempos) > 0):
                            localdb.OnlyExecute(MyTempo.mountAthleteData(atleta=atleta_id, tempo=lista_tempos[0], local="0", entrada=ENTRY_TYPE))
                elif tipo_tempo == "chegada":
                    if lista_tempos:
                        if(len(lista_tempos) > 0):
                           localdb.OnlyExecute(MyTempo.mountAthleteData(atleta=atleta_id, tempo=lista_tempos[0], local="1", entrada=ENTRY_TYPE))
                        print(atleta_id)


        localdb.closeOnlyExec()                
        # chama o metodo para fazer o upload dos atletas
        # MyTempo.uploadTempos()
    
 
    def processAthleteTimes() -> None:
        
        localdb = LocalDatabase()
        qb = SQLQueryBuilder()
        reader_data = ReaderData()
        reader_data.getCompressedData()
        on_start_athletes = []
        on_end_athletes = []
        end_of_end_point = []

        def insert_athlete(athl_num, timestamp):
            return f"INSERT INTO atletas_tempos (numero_atleta, tempo) VALUES ({athl_num}, '{timestamp}')"
        
        def verify_if_exists(athl_num, local):
            qb.reset()
            return qb.Select("numero, tempo, local").From("tempos").Where(f"numero='{athl_num}'").Where(f"local={local}").Build()
        
        def get_athlete_of_each_percurso_from_start(start_time, end_of_start):
    
            return f"""
            SELECT t.numero_atleta, MAX(t.tempo) AS ultimo_tempo
            FROM atletas_tempos AS t
            JOIN atletas_da_prova AS ap ON ap.numero_atleta = t.numero_atleta
            WHERE t.tempo > "{start_time}" AND t.tempo < "{end_of_start}"
            GROUP BY t.numero_atleta;
            """
        
        def get_athlete_of_each_percurso_from_start_backup(start_time, end_of_start):
    
            return f"""
                SELECT t.numero_atleta, MAX(t.tempo) AS ultimo_tempo
                FROM atletas_tempos_backup AS t
                JOIN atletas_da_prova AS ap ON ap.numero_atleta = t.numero_atleta
                WHERE t.tempo > "{start_time}" AND t.tempo < "{end_of_start}"
                GROUP BY t.numero_atleta;
            """

        
        def get_first_time_of_the_end(end_of_route):
            return f"""
                SELECT t.numero_atleta, MIN(t.tempo) AS primeiro_tempo
                FROM atletas_tempos AS t
                JOIN atletas_da_prova AS ap ON ap.numero_atleta = t.numero_atleta
                WHERE t.tempo > "{end_of_route}"
                GROUP BY t.numero_atleta, ap.percurso;
                """
        
        def get_first_time_of_the_end_backup(end_of_route):
            return f"""
                SELECT t.numero_atleta, MIN(t.tempo) AS primeiro_tempo
                FROM atletas_tempos_backup AS t
                JOIN atletas_da_prova AS ap ON ap.numero_atleta = t.numero_atleta
                WHERE t.tempo > "{end_of_route}"
                GROUP BY t.numero_atleta, ap.percurso;
                """

        def get_invalid_athletes(before_of):
            return f"""
                    SELECT 
                        t.numero_atleta, 
                        MIN(t.tempo) AS primeiro_tempo
                    FROM 
                        atletas_tempos AS t
                    JOIN 
                        atletas_da_prova AS ap ON ap.numero_atleta = t.numero_atleta
                    WHERE 
                        t.tempo < "{before_of}"
                    GROUP BY 
                        t.numero_atleta;
            """

        try:
            localdb.openOnlyExec()
            localdb.OnlyExecute(qb.Delete("atletas_tempos").Build())
            for athl_num, times_list in reader_data.readFiles().items():
                for athl_time in times_list:
                    if(len(athl_time) > 12):
                        continue
                    else:
                        localdb.OnlyExecute(insert_athlete(athl_num, athl_time))
            
            queryPercursos = qb.Select("horalargada, fimlargada, tempo_em_largada, tempo_chegada, id_percurso").From("percursos").Where("horalargada IS NOT NULL AND fimlargada IS NOT NULL").Build()

            percursos = localdb.OnlyExecute(queryPercursos)

            for per in percursos:
                start_time_str = per[0]
                start_time_str = ":".join(map(lambda x: x.rjust(2, "0"), start_time_str.split(":")))
                end_time_str = per[1]
                end_time_str = ":".join(map(lambda x: x.rjust(2, "0"), end_time_str.split(":")))
                additional_time = per[3] 
                start_time = datetime.strptime(start_time_str, '%H:%M:%S')
                end_time = datetime.strptime(end_time_str, '%H:%M:%S')
                
                additional_time_in_hours, additional_time_in_minutes, additional_time_in_seconds = map(int, additional_time.split(':'))

                additional_time_formatted = timedelta(hours=additional_time_in_hours, minutes=additional_time_in_minutes, seconds=additional_time_in_seconds)
        
                end_of_end_point = end_time + additional_time_formatted

                hour_end_of_end_point = end_of_end_point.strftime('%H:%M:%S')
                
                times_start = set(localdb.OnlyExecute(get_athlete_of_each_percurso_from_start_backup(start_time_str, end_time_str)) + localdb.OnlyExecute(get_athlete_of_each_percurso_from_start(start_time_str, end_time_str)))
                converted_times_start = list(times_start)
                on_start_athletes.append(converted_times_start)
        
                times_end = set(localdb.OnlyExecute(get_first_time_of_the_end(hour_end_of_end_point)) + localdb.OnlyExecute(get_first_time_of_the_end_backup(hour_end_of_end_point)))
                converted_times_end = list(times_end)
                on_end_athletes.append(converted_times_end)

            for on_start_athlete in on_start_athletes:
                for on_start_a in on_start_athlete:
                    if(on_start_a[0] is not None or on_start_a[0] != "NULL" and on_start_a[1] is not None):
                    
                        if(len(localdb.OnlyExecute(verify_if_exists(on_start_a[0], "0")))) < 1:
                            localdb.OnlyExecute(MyTempo.mountAndVerifyIfAthleteDataExists(atleta=on_start_a[0], tempo=on_start_a[1], local="0", entrada=ENTRY_TYPE))
    
            
            for on_end_athlete in on_end_athletes:
                for on_end_a in on_end_athlete:
                    if(on_end_a[0] is not None or on_end_a[0] != "NULL" and on_end_a[1] is not None):
                        
                        if(len(localdb.OnlyExecute(verify_if_exists(on_end_a[0], "1")))) < 1:
                            localdb.OnlyExecute(MyTempo.mountAndVerifyIfAthleteDataExists(atleta=on_end_a[0], tempo=on_end_a[1], local="1", entrada=ENTRY_TYPE))
            try:
                conj = on_start_athletes[0] + on_end_athletes[0]
                MyTempo.writeRefined(conj)
            except:
                pass
                
            localdb.closeOnlyExec()
            MyTempo.autoBackup()
        except Exception as e:
            print("erro no processamento dos atletas ->", e)
            try:
                localdb.closeOnlyExec()
            except Exception as e:
                print(e)
            finally:
                MyTempo.processAthleteTimes()

    def emptyRecoverTable(self):
        localdb = LocalDatabase()
        return localdb.executeNonQuery("DELETE FROM recover")
    
    def emptyTemposTable(self):
        localdb = LocalDatabase()
        return localdb.executeNonQuery("DELETE FROM tempos")

    def emptyAthletesTimesTable():
        localdb = LocalDatabase()
        return localdb.executeNonQuery("DELETE FROM atletas_tempos")
    
    def emptyAthletesTimesTableBackup():
        localdb = LocalDatabase()
        return localdb.executeNonQuery("DELETE FROM atletas_tempos_backup")
    
    def setupReaderData(self):        
        localdb = LocalDatabase()
        qb = SQLQueryBuilder()
        localdb.openOnlyExec()
        idprova = ""
        if os.path.exists(READER_CONFIG_FILE_PATH):
            equip_dados = r_json(READER_CONFIG_FILE_PATH)
            idprova = equip_dados['idprova']
        else:
            idprova = localdb.OnlyExecute(qb.Select("idprova").From("equip_data").Build())[0][0]
            

        
        localdb.OnlyExecute(qb.Delete("recover").Build())
        localdb.OnlyExecute(qb.Delete("percursos").Build())
        localdb.OnlyExecute(qb.Delete("tempos").Build())
        localdb.OnlyExecute(qb.Delete("atletas_da_prova").Build())
        localdb.OnlyExecute(qb.Delete("atletas_tempos_backup").Where(f"time_stamp <= datetime('now', '-{localdb.OnlyExecute("SELECT bkp_delete_in_days FROM system_settings")[0][0]} day')").Build())
        localdb.closeOnlyExec()
        self.getPercursos(idprova)
        self.GetAthletes()

    def pendriveGetData():
        try:
            localdb = LocalDatabase()
            sqlb = SQLQueryBuilder()
            system = System()
            file_name = f"MyTempo-Backup-{datetime.now().date()}.txt"
            usb_dir = system.get_usb_path()

            if usb_dir is not None:
                file_path = os.path.join(usb_dir, file_name)
                
                if not os.path.exists(file_path):
                    with open(file_path, "w") as file:
                        for data in localdb.executeQuery(sqlb.Select("DISTINCT numero_atleta, tempo").From("atletas_tempos_backup").Build()):
                            athlete_num, time = data
                            num_of_zeros = 19 - len(str(athlete_num))
                            complement = "0" * num_of_zeros
                            formatted_data = f"{complement}{athlete_num}{time}\n"
                            file.write(formatted_data)
                    print(f"Arquivo '{file_name}' criado com sucesso.")
                else:
                    with open(file_path, "w") as file:
                        for data in localdb.executeQuery(sqlb.Select("DISTINCT numero_atleta, tempo").From("atletas_tempos_backup").Build()):
                            athlete_num, time = data
                            num_of_zeros = 19 - len(str(athlete_num))
                            complement = "0" * num_of_zeros
                            formatted_data = f"{complement}{athlete_num}{time}\n"
                            file.write(formatted_data)
                    print(f"Dados adicionados ao arquivo '{file_name}'.")
            else:
                print("Pendrive não encontrado.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def verifyIfHasPendrive():
        pendrive_status = MyTempo.sel_sys_settings_fields("pendrive_identifier_loop_status")
        if(pendrive_status == 0):
            MyTempo.pendriveGetData()
            return
        
        while pendrive_status == 1:
            MyTempo.pendriveGetData()
            time.sleep(5)
    
    def readerStartup():
        localdb = LocalDatabase()
        sqlb = SQLQueryBuilder()
        localdb.openOnlyExec()

        reader_settings = localdb.OnlyExecute(sqlb.Select("*").From("system_settings").Build())
        if(len(reader_settings) <= 0):
            localdb.OnlyExecute(sqlb.Insert("system_settings").Set(
                pid=0,
                session=0,
                bg_process_active=1,
                bkp_delete_in_days=1,
                reader_is_writting=1,
                pendrive_identifier_loop_status=1
            ).Build())
        localdb.closeOnlyExec()

        
    def stop_process_by_pid(pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"Processo com PID {pid} interrompido com sucesso.")
        except psutil.NoSuchProcess:
            print(f"Não há nenhum processo com PID {pid} em execução.")
        except psutil.AccessDenied:
            print(f"Permissão negada para interromper o processo com PID {pid}.")
# m = MyTempo()

# m.setupReaderData()

# # print(m.)[=[]]
