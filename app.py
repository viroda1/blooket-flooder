import os
import logging
from dotenv import load_dotenv
# ... (keep other imports from previous response)

load_dotenv()

# --- Environment Configuration ---
# Convert string from .env to actual types
PORT = int(os.getenv('PORT', 5000))
# Important: .env returns "True" as a string. We need to check the content.
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
THREAD_COUNT = int(os.getenv('THREAD_COUNT', 5))

# Setup Logging based on DEBUG mode
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO

logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- (Rest of your FloodEngine class remains the same) ---

@app.route('/start', methods=['POST'])
def start_flood():
    # ... (validation logic)
    
    # Use the configurable THREAD_COUNT from .env
    success = engine.start(str(config.target_url), thread_count=THREAD_COUNT)
    
    if success:
        logger.info(f"FLOOD STARTED | Threads: {THREAD_COUNT} | Target: {config.target_url}")
        return jsonify({"message": f"Attack initiated with {THREAD_COUNT} threads"}), 200
    else:
        return jsonify({"error": "Failed to start engine"}), 500

# ... (rest of the code)

if __name__ == '__main__':
    logger.info(f"--- DeepHat Engine Initializing ---")
    logger.info(f"Configuration: PORT={PORT}, DEBUG={DEBUG_MODE}, THREADS={THREAD_COUNT}")
    
    try:
        app.run(
            host='0.0.0.0', 
            port=PORT, 
            debug=DEBUG_MODE,
            # threaded=True is default in Flask, allows handling multiple API requests
            threaded=True 
        )
    except Exception as e:
        logger.critical(f"Failed to launch server: {e}")