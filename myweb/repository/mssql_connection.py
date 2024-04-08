import pymssql

class MSSQLConnection:
    def __init__(self, server: str, database: str, user: str, password: str):
        self.conn = pymssql.connect(server=server, database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()