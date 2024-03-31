from dataclasses import dataclass
from typing import List
from domain.model.task import Task

# 任務結果類別
@dataclass
class TaskResult:
    result: List[Task]

    # # 建構式
    # def __init__(self, result):
    #     self.result = result  # 任務結果