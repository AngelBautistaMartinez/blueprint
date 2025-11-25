from flask import Flask, request, jsonify
import datetime, os, requests

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SERVER_ID = os.getenv("SERVER_ID", "UNKNOWN")

def log_to_supabase(ip, timestamp, data=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if data is None:
        data{}

    if "sensor_id" not in data:
        data["sensor_id"] = SERVER_ID
        data["source"] = "browser"
    
    payload = {"ip": ip, "timestamp": timestamp, "data": data}
    r = requests.post(f"{SUPABASE_URL}/rest/v1/connections", headers=headers, json=payload)
    print("Supabase insert:", r.status_code, r.text)

@app.before_request
def log_connection():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    
    timestamp = datetime.datetime.utcnow().isoformat()
    log_to_supabase(ip, timestamp)
@app.route("/")
def home():
    return "Hello"

@app.route("/send", methods=["POST"])
def receive_data():
    data = request.get_json()    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    timestamp = datetime.datetime.utcnow().isoformat()

    if data is None:
        data = {}
    data["source"] = "program"
    
    log_to_supabase(ip, timestamp, data)
    return jsonify({"status": "success", "received": data})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
