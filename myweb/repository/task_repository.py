from domain.model.task import Task
from repository.mssql_connection import MSSQLConnection

class TaskRepository:
    def __init__(self, sqlconn: MSSQLConnection):
        self.sqlconn = sqlconn

    def get_task_list(self):
        data = self.sqlconn.execute_query("SELECT * FROM [dbo].[Task] WITH(NOLOCK)")
        return data
    
    def get_task(self, id: int):
        data = self.sqlconn.execute_query_first("SELECT * FROM [dbo].[Task] WITH(NOLOCK) WHERE id = %s", id)
        return data
    
    def insert_task(self, text: str):
        id = self.sqlconn.execute_insert("INSERT INTO [dbo].[Task] (text, status) VALUES(%s, 0); SELECT SCOPE_IDENTITY() AS ID;", text)
        return id

    def update_task(self, task: Task):
        self.sqlconn.execute_update("UPDATE [dbo].[Task] SET text = %s, status = %s WHERE id = %s", (task.text, task.status, task.id))

    def delete_task(self, id: int):
        self.sqlconn.execute_delete("DELETE FROM [dbo].[Task] WHERE id = %s", id)