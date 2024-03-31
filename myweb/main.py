import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from dataclasses import asdict
from domain.model.task import Task
from domain.model.task_result import TaskResult

config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)

cache.set('task', TaskResult(result=[])) #假設cache key = "task"當成db table

@app.route("/")
@app.route("/<name>")
def index(name=None):
    if name == None:
        return "Hello, Max!"
    return "Hello," + name

# get task list api
@app.route("/tasks", methods=['GET'])
def list_tasks():

    task = cache.get('task')
    # print(json.dumps([ob.__dict__ for ob in task.result]))

    return jsonify(json.dumps(asdict(task)))

# insert task api
@app.route("/task", methods=['POST'])
def create_task():
    params = request.get_json()

    # 检查 params 是否包含 'text' 键
    if 'text' not in params:
        return jsonify({"error": "欄位 text 須必填"}), 400

    text = params.get('text')
    task = cache.get('task')

    id = 1 if task.result == [] else len(task.result) + 1
    new_task = Task(id, text, 0)
    
    task.result.append(new_task)

    cache.set('task', task)

    return jsonify(json.dumps(new_task.__dict__)), 201

# update task api
@app.route("/task", methods=['PUT'])
def update_task():
    params = request.get_json()

    # 检查 params 是否包含 'id' 键
    if 'id' not in params or params.get('id') is None:
        return jsonify({"error": "欄位 id 須必填"}), 400

    if 'status' not in params or (params.get('status') != 0 and params.get('status') != 1):
        return jsonify({"error": "欄位 status 須必填"}), 400

    id = params.get('id')
    status = params.get('status')
    text = params.get('text', None)

    task = cache.get('task')

    for item in task.result:
        if item.id == id:
            item.text = text
            item.status = status
            break
        else:
            return jsonify({"error": "無此 id"}), 400

    cache.set('task', task)

    return jsonify(json.dumps(task.result[id-1].__dict__))

# delete task api
@app.route("/task/<int:id>", methods=['DELETE'])
def delete_task(id):

    task = cache.get('task')
    
    tasks = [item for item in task.result if item.id != id]

    cache.set('task', TaskResult(tasks))

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=8000)