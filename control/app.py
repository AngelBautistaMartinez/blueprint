from flask import Flask, request, jsonify
import datetime, os, requests

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def log_to_supabase(ip, timestamp, data=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"ip": ip, "timestamp": timestamp, "data": data}
    r = requests.post(f"{SUPABASE_URL}/rest/v1/connections", headers=headers, json=payload)
    print("Supabase insert:", r.status_code, r.text)

@app.before_request
def log_connection():
    ip = request.remote_addr
    timestamp = datetime.datetime.utcnow().isoformat()
    log_to_supabase(ip, timestamp)

@app.route("/")
def home():
    return "Hello from Flask server (Supabase logging)"

@app.route("/send", methods=["POST"])
def receive_data():
    data = request.get_json()
    ip = request.remote_addr
    timestamp = datetime.datetime.utcnow().isoformat()
    log_to_supabase(ip, timestamp, data)
    return jsonify({"status": "success", "received": data})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
