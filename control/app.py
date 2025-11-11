from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/data/control.db"

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip TEXT,
                 timestamp TEXT
                 )''')
    conn.commit()
    conn.close()

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.get_json()
    ip = data.get("ip")
    timestamp = data.get("timestamp")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (ip, timestamp) VALUES (?, ?)", (ip, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "logged", "ip": ip}), 200

@app.route('/')
def index():
    return "Control Node Active"

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5000)
