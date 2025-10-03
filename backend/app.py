import flask
import requests
import os
import json
from flask import request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing only)
load_dotenv()

# --- Configuration ---
app = flask.Flask(__name__)
# IMPORTANT: Allow access from your frontend domain
CORS(app) 

# Get API key from Render Environment Variables
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY") 
SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"

# CRITICAL: This MUST match the address you verified as the sender in SendGrid
# UPDATED to use your authenticated domain 'issajozi.xyz'
SENDER_EMAIL = "mlukivelem@issajozi.xyz" 
# The separate email address that will receive the form submissions
RECIPIENT_EMAIL = "shamilajoma@gmail.com" 

# --- Routes ---

@app.route('/', methods=['GET'])
def home():
    # Simple check to confirm the backend is running
    return "Backend is running"

@app.route('/submit', methods=['POST'])
def submit():
    print("Received a form submission")

    # 1. Safely parse incoming JSON data from the frontend
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
    except Exception as e:
        print(f"❌ Error parsing incoming JSON: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    # 2. Construct the SendGrid email payload
    sendgrid_payload = {
        "personalizations": [{
            # Use the RECIPIENT_EMAIL (shamilajoma@gmail.com) here
            "to": [{"email": RECIPIENT_EMAIL}], 
            "subject": "New Form Submission"
        }],
        # This 'from' email MUST be the verified sender (@issajozi.xyz)
        "from": {"email": SENDER_EMAIL}, 
        # Allow replying directly to the person who filled out the form
        "reply_to": {"email": email},
        "content": [{
            "type": "text/plain",
            "value": f"New submission:\n\nName: {name}\nEmail: {email}\nMessage: {message}"
        }]
    }

    # 3. Set Authorization Headers
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    # 4. Make the request to SendGrid with robust error handling
    try:
        response = requests.post(SENDGRID_API_URL, headers=headers, json=sendgrid_payload)

        # Check for success (SendGrid returns 202 Accepted on success)
        if response.status_code == 202:
            print("✅ Email sent successfully via SendGrid")
            return jsonify({"message": "Submitted! We'll contact you soon."}), 200
        else:
            # Log the full, detailed error message from SendGrid to the Render console
            print(f"❌ SendGrid failed with status {response.status_code}")
            print(f"❌ SendGrid error body: {response.text}")
            
            return jsonify({"error": "Email service failed. Check backend logs for details."}), 500

    except requests.exceptions.RequestException as e:
        # Log network errors (e.g., DNS resolution failure, timeout) 
        print(f"❌ Network or connection error to SendGrid: {e}")
        return jsonify({"error": "Network error with email service."}), 500

# Start the server (Render uses Gunicorn, which ignores this block) 
if __name__ == '__main__':
    # This is for local testing only
    app.run(debug=True, port=5000)
