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

SENDER_EMAIL = "mlukivelem@issajozi.xyz"
RECIPIENT_EMAIL = "shamilajoma@gmail.com"

@app.route('/', methods=['GET'])
def home():
    return "Backend is running"

@app.route('/submit', methods=['POST'])
def submit():
    print("Received a form submission")

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
            print(f"❌ Brevo error body: {response.text}")
            return jsonify({"error": "Email service failed. Check backend logs for details."}), 500

    except requests.exceptions.RequestException as e:
        print(f"❌ Network or connection error to Brevo: {e}")
        return jsonify({"error": "Network error with email service."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

