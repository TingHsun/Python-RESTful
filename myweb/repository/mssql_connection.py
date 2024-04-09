import pymssql

class MSSQLConnection:
    def __init__(self, server: str, database: str, user: str, password: str):
        self.conn = pymssql.connect(server=server, database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def execute_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def execute_query_first(self, sql, data):
        self.cursor.execute(sql, data)
        return self.cursor.fetchone()

    def execute_insert(self, sql, data):
        self.cursor.execute(sql, data)
        inserted_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return inserted_id
    
    def execute_update(self, sql, data):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def execute_delete(self, sql, data):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()