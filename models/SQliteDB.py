import sqlite3
from API.config.config import *

class CustomObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class LocalDatabase:
    def __init__(self, messages=False) -> None:
        self.db_file = DB_PATH
        self.messages = messages
        self.results = []
        self.conn_ = False
        self.info = {
            "status": "",
            "connection": "",
            "query": "",
            "affected_rows": "",
            "errors": "",
            "has_changed": ""
        }
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnection()

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            if self.messages:
                print("Conexão estabelecida com sucesso.")
                self.conn_ = True
        except Exception as e:
            if self.messages:
                print("Erro ao conectar ao banco de dados:", e)
                
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

    def executeQuery(self, query, return_as_object=False):
        try:
            self.connect()
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                if return_as_object:
                 
                    result_object = CustomObject(**dict(zip(columns, row)))
                else:
                    result_object = row
                results.append(result_object)
            self.results = results
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


    def OnlyExecute(self, query, return_as_object=False):
        return self.cursor.execute(query).fetchall()


    def closeConnection(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            if self.messages:
                print("Conexão fechada.")
                self.conn_ = False
    def openOnlyExec(self):
        self.conn_ = True
        self.connect()
        self.cursor = self.conn.cursor()
    
    def closeOnlyExec(self):
        self.conn_ = False
        self.conn.commit()
        self.closeConnection()