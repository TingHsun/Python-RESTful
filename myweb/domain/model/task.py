from dataclasses import dataclass

# 任務類別
@dataclass
class Task:
    id: int
    text: str
    status: bool

    # # 建構式
    # def __init__(self, id: int, text: str, status: int):
    #     self.id = id  # 編號屬性
    #     self.text = text  # 內容屬性
    #     self.status = status  # 狀態屬性


