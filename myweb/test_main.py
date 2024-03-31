import pytest
import json
from dataclasses import dataclass, asdict
from unittest.mock import Mock
from main import app, cache
from domain.model.task import Task
from domain.model.task_result import TaskResult

# 備註:需要初始設定可預先載入的function
# @pytest.fixture(scope="session", autouse=True)
# def setup():

# 備註: 若要隔離DB或外部依賴可以用Mock(return_value={mock_value})

def test_list_tasks():
    # arrange
    mock_task = TaskResult(result=[
        Task(id=1, text="買早餐", status=0),
        Task(id=2, text="買午餐", status=1)
    ])
    cache.set("task", mock_task)

    # act
    with app.test_client() as client:
        response = client.get("/tasks")

    # # assert
    assert response.status_code == 200

    data = json.loads(json.loads(response.get_data(as_text=True)))
    assert len(data["result"]) == 2
    assert data["result"][0]["id"] == 1
    assert data["result"][0]["text"] == "買早餐"
    assert data["result"][0]["status"] == 0
    assert data["result"][1]["id"] == 2
    assert data["result"][1]["text"] == "買午餐"
    assert data["result"][1]["status"] == 1

def test_create_task_success():
    # arrange
    mock_task = TaskResult(result=[
        Task(id=1, text="買早餐", status=1),
        Task(id=2, text="買午餐", status=1)
    ])
    cache.set("task", mock_task)

    request_json = {"text": "買晚餐"}

    # act
    with app.test_client() as client:
        response = client.post("/task", json=request_json)

    # assert
    assert response.status_code == 201

    task = json.loads(json.loads(response.get_data(as_text=True)))
    assert task["text"] == "買晚餐"
    assert task["status"] == 0
    assert task["id"] == 3

def test_create_task_missing_text():
    # arrange
    request_json = {"content": "買飲料"} #缺少text

    # act
    with app.test_client() as client:
        response = client.post("/task", json=request_json)

    # assert
    assert response.status_code == 400

    error_message = json.loads(response.get_data(as_text=True))
    assert error_message["error"] == "欄位 text 須必填"

def test_update_task_success():
    #arrange
    mock_task = TaskResult(result=[
        Task(id=1, text="買早餐", status=0),
        Task(id=2, text="買午餐", status=1)
    ])
    cache.set("task", mock_task)

    request_json = {
        "id": 1,
        "text": "買早餐 完成",
        "status": 1
    }

    # act
    with app.test_client() as client:
        response = client.put("/task", json=request_json)

    # assert
    assert response.status_code == 200

    data = json.loads(json.loads(response.get_data(as_text=True)))
    assert data["id"] == 1
    assert data["text"] == "買早餐 完成"
    assert data["status"] == 1

def test_update_task_missing_id():
    # arrange
    request_json = {
        "text": "缺少id", #缺少id
        "status": 0
    }

    # act
    with app.test_client() as client:
        response = client.put("/task", json=request_json)

    # assert
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert "error" in data
    assert data["error"] == "欄位 id 須必填"

def test_update_task_invalid_status():
    # arrange
    request_json = {
        "id": 2,
        "text": "錯誤的status",
        "status": 2  #錯誤的status
    }

    # act
    with app.test_client() as client:
        response = client.put("/task", json=request_json)

    # assert
    assert response.status_code == 400

    data = json.loads(response.get_data(as_text=True))
    assert "error" in data
    assert data["error"] == "欄位 status 須必填"

def test_delete_task():
    # arrange
    mock_task = TaskResult(result=[
        Task(id=1, text="買早餐", status=0),
        Task(id=2, text="買午餐", status=0),
        Task(id=3, text="買晚餐", status=0)
    ])
    cache.set("task", mock_task)

    # act
    with app.test_client() as client:
        response = client.delete("/task/2")

    # assert
    assert response.status_code == 200

