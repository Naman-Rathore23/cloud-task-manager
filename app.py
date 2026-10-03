from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)

# In-memory storage (real app mein ye database hota, RDS/DynamoDB)
tasks = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    # ALB / ECS isi endpoint se check karta hai app zinda hai ya nahi
    return jsonify({"status": "healthy"}), 200

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values()))

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task_id = str(uuid.uuid4())
    task = {"id": task_id, "title": data["title"], "done": False}
    tasks[task_id] = task
    return jsonify(task), 201

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404
    tasks[task_id]["done"] = not tasks[task_id]["done"]
    return jsonify(tasks[task_id])

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404
    del tasks[task_id]
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    # 0.0.0.0 isliye taaki container ke bahar se (Docker/ALB se) request mile
    app.run(host="0.0.0.0", port=5000)
