import sqlite3
from config import *

class LocalDatabase:
    def __init__(self, messages=False) -> None:
        self.db_file = DB_PATH
        self.messages = messages
        self.results = []
        self.info = {
            "status": "",
            "connection": "",
            "query": "",
            "affected_rows": "",
            "errors": "",
            "has_changed": ""
        }
        print(DB_PATH)
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.info['status'] = "success"
            self.info['connection'] = str(self.conn)
            if self.messages:
                print("Conexão estabelecida com sucesso.")
        except Exception as e:
            self.info['status'] = "error"
            self.info['errors'] = str(e)
            if self.messages:
                print("Erro ao conectar ao banco de dados:", e)

    def executeQuery(self, query):
        try:
            self.connect()
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            self.results = self.cursor.fetchall()
            self.info['affected_rows'] = len(self.results)
            self.info['query'] = query
            self.info['status'] = "success"
            if self.messages:
                print("Query executada com sucesso.")
            return self.results
        except Exception as e:
            self.info['status'] = "error"
            self.info['errors'] = str(e)
            if self.messages:
                print("Erro ao executar a consulta:", e)
            return None
        finally:
            self.closeConnection()

    def executeNonQuery(self, query):
        try:
            self.connect()
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            self.info['affected_rows'] = self.cursor.rowcount
            self.info['query'] = query
            self.info['status'] = "success"
            self.conn.commit()
            self.info['has_changed'] = "yes"
            if self.messages:
                print("Operação de alteração executada com sucesso.")
            return self.info
        except Exception as e:
            self.info['status'] = "error"
            self.info['errors'] = str(e)
            if self.messages:
                print("Erro ao executar operação de alteração:", e)
            return None
        finally:
            self.closeConnection()

    def closeConnection(self):
        if self.conn:
            self.conn.close()
            if self.messages:
                print("Conexão fechada.")
