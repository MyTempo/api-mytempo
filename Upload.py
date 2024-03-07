from config import *
from functions import *
from helpers import *
from datetime import datetime
from Database import *

# id_prova, id_checkpoint, id_equipamento, numero_atleta, tempo_atleta, calculo, antena, local, entrada, idstaff

class Upload:
    def __init__(self) -> None:
        self.atletas_enviados = []
        self.db = Database(True)

    def primeirosTempos(self, id_prova, id_check, id_equipamento, atleta, tempo, antena=0, local="", entrada=0, idstaff=9):
        self.db.executeNonQuery(f"INSERT INTO tempos (idprova, idcheck, idequipamento, numero, tempo, calculo, antena, local, entrada, idstaff) VALUES ({id_prova}, {id_check}, {id_equipamento}, {atleta}, {tempo}, {antena}, {local}, {entrada}, {idstaff})")

