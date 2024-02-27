import mysql.connector
from config import *

class Database:
    def __init__(self, messages=False) -> None:

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
        

    def executeQuery(self, query):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.cursor.execute(query)
                self.results = self.cursor.fetchall()
                self.info['affected_rows'] = self.cursor.rowcount
                self.info['query'] = query
                self.info['connection'] = str(self.conn)
                self.info['status'] = "success"
                self.info['errors'] = None
                self.info['has_changed'] = "not"
                if self.messages == True:
                    print(self.info)
                return self.results

            else:
                self.info['affected_rows'] = self.cursor.rowcount
                self.info['query'] = query
                self.info['connection'] = str(self.conn)
                self.info['status'] = "error"
                self.info['errors'] = "Connection not active"

                if self.messages:
                    print(self.info)
                    
                return None

        except Exception as e:
            if self.messages:
                self.info['status'] = "error"
                self.info['errors'] = str(e)
                print(self.info)
            return None


    def executeNonQuery(self, query):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.cursor.execute(query)
                self.info['affected_rows'] = self.cursor.rowcount
                self.info['query'] = query
                self.info['connection'] = str(self.conn)
                self.info['status'] = "success"
                self.info['errors'] = None
                self.info['has_changed'] = "yes"
                self.conn.commit()
                return self.info
                if self.messages == True:
                    print(self.info)


            else:
                self.info['affected_rows'] = self.cursor.rowcount
                self.info['query'] = query
                self.info['connection'] = str(self.conn)
                self.info['status'] = "error"
                self.info['errors'] = "Connection not active"

                if self.messages:
                    print(self.info)
                    
                return None

        except Exception as e:
            if self.messages:
                self.info['status'] = "error"
                self.info['errors'] = str(e)
                print(self.info)
            return None
        


    def closeConnection(self):
        if self.conn.is_connected():
            self.conn.close()

