import sqlite3
from flask import Flask, request, jsonify, g


app = Flask(__name__)
DATABASE = 'tasks.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('in progress', 'completed'))
            )
        ''')
        db.commit()


@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    text = data.get('text')
    status = data.get('status')
    if not text or status not in ('in progress', 'completed'):
        return jsonify({"error": "Invalid input: 'text' and 'status' ('in progress' or 'completed') required"}), 400

    db = get_db()
    cursor = db.execute('INSERT INTO task (text, status) VALUES (?, ?)', (text, status))
    db.commit()
    task_id = cursor.lastrowid
    return jsonify({"id": task_id, "text": text, "status": status}), 201


@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    status_filter = request.args.get('status')
    db = get_db()
    if status_filter in ('in progress', 'completed'):
        tasks = db.execute('SELECT * FROM task WHERE status = ?', (status_filter,)).fetchall()
    else:
        tasks = db.execute('SELECT * FROM task').fetchall()
    result = [dict(task) for task in tasks]
    return jsonify(result), 200


@app.route('/api/v1/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"error": "Missing 'status' in JSON body"}), 400
    status = data['status']
    if status not in ('in progress', 'completed'):
        return jsonify({"error": "Invalid status, must be 'in progress' or 'completed'"}), 400

    db = get_db()
    cursor = db.execute('UPDATE task SET status = ? WHERE id = ?', (status, task_id))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404

    task = db.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()
    return jsonify(dict(task)), 200


@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cursor = db.execute('DELETE FROM task WHERE id = ?', (task_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": f"Task {task_id} deleted"}), 200


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=15243)
