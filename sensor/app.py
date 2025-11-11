from flask import Flask, request, jsonify
import sqlite3
import datetime
import os
import requests

app = Flask(__name__)

DB_PATH = "/data/connections.db"
CONTROL_URL = os.getenv("CONTROL_URL")

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS connections (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip TEXT,
                 timestamp TEXT
                 )''')
    conn.commit()
    conn.close()

@app.before_request
def log_connection():
    ip = request.remote_addr
    timestamp = datetime.datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO connections (ip, timestamp) VALUES (?, ?)", (ip, timestamp))
    conn.commit()
    conn.close()

    # send info to control server
    try:
        requests.post(f"{CONTROL_URL}/log", json={"ip": ip, "timestamp": timestamp})
    except Exception as e:
        print("Failed to send to control:", e)

@app.route('/')
def home():
    return "Sensor Node Active"

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5000)
