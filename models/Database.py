import mysql.connector
from API.config.config import *


class CustomObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Database:
    def __init__(self, messages=False):
        self.host = MYTEMPO_MYSQL_CONFIG["host"]
        self.user = MYTEMPO_MYSQL_CONFIG["user"]
        self.password = MYTEMPO_MYSQL_CONFIG["password"]
        self.database = MYTEMPO_MYSQL_CONFIG["database"]
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

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnection()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
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
            self.cursor = self.conn.cursor(dictionary=True) if return_as_object else self.conn.cursor()
            self.cursor.execute(query)
            self.results = [CustomObject(**row) for row in self.cursor.fetchall()] if return_as_object else self.cursor.fetchall()
            self.info['affected_rows'] = self.cursor.rowcount
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
        if self.conn.is_connected():
            self.conn.close()
            if self.messages:
                print("Conexão fechada.")

    def OnlyExecute(self, query):
        self.cursor.execute(query)


    def openOnlyExec(self):
        self.connect()
        self.cursor = self.conn.cursor()

    def closeOnlyExec(self):
        self.conn.commit()
        self.closeConnection()
        if self.messages:
            print("Conexão fechada.")