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

# --- CRITICAL STARTUP CHECK ---
if not BREVO_API_KEY:
    # If the key is missing (i.e., not loaded from the environment group)
    print("FATAL ERROR: BREVO_API_KEY is missing. Check Render environment variables or group linkage.")
    # Exit or fail gracefully to avoid crashing later in the submit function
    # We will let the service start but will log the error on the first API call
    pass 
# ------------------------------

@app.route('/', methods=['GET'])
def home():
    return "Backend is running"

@app.route('/submit', methods=['POST'])
def submit():
    print("Received a form submission")
    
    # 1. Check Key Status at runtime (Error Code 500 if missing)
    if not BREVO_API_KEY:
        error_msg = "Brevo API Key is missing. Check Render Environment Group linkage."
        print(f"❌ FATAL: {error_msg}")
        # Returning a clear 500 error instead of a generic one
        return jsonify({"error": error_msg}), 500
        
    # 2. Key is present, proceed with Brevo Call

    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
    except Exception as e:
        print(f"❌ Error parsing incoming JSON: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    # Brevo API payload
    brevo_payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": RECIPIENT_EMAIL}],
        "subject": "New Form Submission",
        "replyTo": {"email": email},
        "textContent": f"New submission:\n\nName: {name}\nEmail: {email}\nMessage: {message}"
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        response = requests.post(BREVO_API_URL, headers=headers, json=brevo_payload)

        if response.status_code == 201:
            print("✅ Email sent successfully via Brevo")
            return jsonify({"message": "Submitted! We'll contact you soon."}), 200
        else:
            print(f"❌ Brevo failed with status {response.status_code}")
            # Include the error body in the log for 401/400 errors
            print(f"❌ Brevo error body: {response.text}")
            return jsonify({"error": "Email service failed. Check backend logs for details."}), 500

    except requests.exceptions.RequestException as e:
        print(f"❌ Network or connection error to Brevo: {e}")
        return jsonify({"error": "Network error with email service."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
