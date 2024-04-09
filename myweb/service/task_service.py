from domain.model.task import Task

class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def get_task_list(self):
        data = self.repository.get_task_list()
        return data
    
    def get_task(self, id: int):
        data = self.repository.get_task(id)
        return data
    
    def add_task(self, text: str):
        id = self.repository.insert_task(text)
        return id
    
    def edit_task(self, task: Task):
        self.repository.update_task(task)

    def remove_task(self, id: int):
        data = self.repository.delete_task(id)
        return data

    def process_data(self, data):
        # 在這裡進行資料處理
        processed_data = [row for row in data]
        return processed_data