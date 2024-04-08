from repository.mssql_connection import MSSQLConnection

class TaskRepository:
    def __init__(self, sqlconn: MSSQLConnection):
        self.sqlconn = sqlconn

    def get_task_list(self):
        data = self.sqlconn.execute_query("SELECT * FROM [dbo].[Task] WITH(NOLOCK)")
        
        # 傳入參數語法，取代%s
        # cursor.execute(querystr, "Parameter")

        return data