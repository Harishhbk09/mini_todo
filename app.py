"""Mini Todo app - a tiny Flask app used to learn cloud + DevOps basics."""
import logging
import os

from flask import Flask, jsonify, request, render_template_string

# --- Config comes from environment variables (12-factor app principle) ---
APP_ENV = os.environ.get("APP_ENV", "development")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("todo")

app = Flask(__name__)

# In-memory storage: simple, but data is lost on restart (a good lesson on "state")
todos = []
next_id = 1

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mini Todo</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 480px; margin: 40px auto; padding: 0 16px; }
    li { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #ddd; }
    .done { text-decoration: line-through; color: #888; }
    small { color: #888; }
  </style>
</head>
<body>
  <h1>Mini Todo</h1>
  <small>env: {{ env }} &middot; version: {{ version }}</small>
  <form id="f"><input id="t" placeholder="What to do?" required> <button>Add</button></form>
  <ul id="list"></ul>
  <script>
    async function load() {
      const items = await (await fetch('/api/todos')).json();
      document.getElementById('list').innerHTML = items.map(t =>
        `<li><span class="${t.done ? 'done' : ''}" onclick="toggle(${t.id})">${t.title.replace(/</g,'&lt;')}</span>
         <button onclick="del(${t.id})">x</button></li>`).join('');
    }
    async function toggle(id) { await fetch('/api/todos/' + id, {method: 'PATCH'}); load(); }
    async function del(id) { await fetch('/api/todos/' + id, {method: 'DELETE'}); load(); }
    document.getElementById('f').onsubmit = async e => {
      e.preventDefault();
      const t = document.getElementById('t');
      await fetch('/api/todos', {method: 'POST', headers: {'Content-Type': 'application/json'},
                                 body: JSON.stringify({title: t.value})});
      t.value = ''; load();
    };
    load();
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, env=APP_ENV, version=APP_VERSION)


@app.get("/health")
def health():
    """Health check: cloud platforms and load balancers call this to know the app is alive."""
    return jsonify(status="ok", env=APP_ENV, version=APP_VERSION)


@app.get("/api/todos")
def list_todos():
    return jsonify(todos)


@app.post("/api/todos")
def add_todo():
    global next_id
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    todo = {"id": next_id, "title": title, "done": False}
    todos.append(todo)
    next_id += 1
    log.info("Added todo %s", todo["id"])
    return jsonify(todo), 201


@app.patch("/api/todos/<int:todo_id>")
def toggle_todo(todo_id):
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            return jsonify(t)
    return jsonify(error="not found"), 404


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    for t in todos:
        if t["id"] == todo_id:
            todos.remove(t)
            return "", 204
    return jsonify(error="not found"), 404


if __name__ == "__main__":
    # Cloud platforms tell your app which port to use via the PORT env var
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=APP_ENV == "development")
