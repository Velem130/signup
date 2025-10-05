import flask
import requests
import os
from flask import request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)
CORS(app)

# --- Configuration ---
BREVO_API_KEY = os.environ.get("BREVO_API_KEY") 
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
SENDER_EMAIL = os.environ.get("EMAIL_SENDER") 
RECIPIENT_EMAIL = "shamilajoma@gmail.com" 

@app.route('/', methods=['GET'])
def home():
    return "Backend is running"

@app.route('/submit', methods=['POST'])
def submit():
    print("Received a form submission")

    # --- START CRITICAL DEBUG SECTION ---
    
    # 1. Print Debug Info
    key_is_present = 'Yes' if BREVO_API_KEY else 'No'
    key_length = len(BREVO_API_KEY) if BREVO_API_KEY else 0
    print(f"DEBUG CHECK: BREVO_API_KEY loaded? {key_is_present}")
    print(f"DEBUG CHECK: Key length: {key_length} (Expected length is ~68)")
    print(f"DEBUG CHECK: SENDER_EMAIL: {SENDER_EMAIL}")
    
    # 2. TEMPORARILY CRASH THE APP TO ENSURE LOG IS VISIBLE
    # DO NOT KEEP THIS LINE AFTER DEBUGGING!
    raise Exception("DEBUG_CRASH: Temporary crash to check API key status.")
    
    # --- END CRITICAL DEBUG SECTION ---
    
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
    except Exception as e:
        print(f"❌ Error parsing incoming JSON: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    # ... (Rest of your submission logic remains below the crash line) ...
    # ... (This code will not run until the 'raise Exception' line is removed) ...

    return jsonify({"error": "Should not reach here."}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

