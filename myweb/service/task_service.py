class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def get_task_list(self):
        data = self.repository.get_task_list()
        return data

    def process_data(self, data):
        # 在這裡進行資料處理
        processed_data = [row for row in data]
        return processed_data