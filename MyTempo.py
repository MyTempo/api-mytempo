from config import *
from functions import *
from helpers import *
from datetime import datetime
import sqlite3

class MyTempo:
    
    def __init__(self) -> None:
        pass

    def getFirstTime(self, tempo_prova):
        conn = sqlite3.connect('equipamentos.db')
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
                                SELECT atleta, MIN(tempo) AS menor_tempo
                                FROM tempos_first
                                WHERE TIME(tempo) >= TIME('{tempo_prova}')
                                GROUP BY atleta;
                               """)
        rows = cursor.fetchall()
        cursor.execute('DROP TABLE tempos_first')
        print("Tabela apagada com sucesso!")
        conn.close()
        for temps in rows:
            self.primeiros_tempos_minerados.append(temps)
        return self.primeiros_tempos_minerados