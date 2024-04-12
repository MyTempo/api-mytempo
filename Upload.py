from API.config.config import *
from API.helpers.functions import *
from API.helpers.helpers import *
from datetime import datetime
from API.models.Database import *
from API.models.SQliteDB import *
# id_prova, id_checkpoint, id_equipamento, numero_atleta, tempo_atleta, calculo, antena, local, entrada, idstaff

class Upload:
    def __init__(self) -> None:
        self.atletas_enviados = []
        self.db = Database(True)
        self.localdb = LocalDatabase(True) 
        self.acumulate_querys = []

    def onlyAthleteNum(self, results):
        for r in results:
            self.atletas_enviados.append(r[0])
        return self.atletas_enviados

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
      
                
    


        