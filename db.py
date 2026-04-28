import mysql.connector
from mysql.connector import Error
from configdb import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return []

    def execute_insert(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Erro ao executar insert: {e}")
            self.connection.rollback()
            return None

    def execute_many(self, query, params_list):
        try:
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao executar many: {e}")
            self.connection.rollback()
            return False

db = Database()

def get_db_connection():
    return db.connect()
