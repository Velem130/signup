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
# CRITICAL: This MUST match the address you verified in SendGrid
SENDER_EMAIL = "mlulekivelem@gmail.com" 

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
        # Return a 400 Bad Request if the JSON is malformed
        return jsonify({"error": "Invalid JSON format"}), 400

    # 2. Construct the SendGrid email payload
    sendgrid_payload = {
        "personalizations": [{
            # Change the 'to' email if you want a different recipient
            "to": [{"email": SENDER_EMAIL}],
            "subject": "New Form Submission"
        }],
        # This 'from' email is the one that MUST be verified in SendGrid
        "from": {"email": SENDER_EMAIL},
        # Allow replying to the user who filled out the form
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
        # Use json= instead of data= for automatic JSON serialization
        response = requests.post(SENDGRID_API_URL, headers=headers, json=sendgrid_payload)

        # Check for success (SendGrid returns 202 Accepted on success)
        if response.status_code == 202:
            print("✅ Email sent successfully via SendGrid")
            return jsonify({"message": "Submitted! We'll contact you soon."}), 200
        else:
            # THIS IS THE CRITICAL LOGGING STEP
            # Log the full, detailed error message from SendGrid to the Render console
            print(f"❌ SendGrid failed with status {response.status_code}")
            print(f"❌ SendGrid error body: {response.text}")
            
            # If the email failed for any reason (e.g., bad key, bad sender, etc.)
            return jsonify({"error": "Email service failed. Check backend logs for details."}), 500

    except requests.exceptions.RequestException as e:
        # Log network errors (e.g., DNS resolution failure, timeout)
        print(f"❌ Network or connection error to SendGrid: {e}")
        return jsonify({"error": "Network error with email service."}), 500

# Start the server (Render uses Gunicorn, which ignores this block)
if __name__ == '__main__':
    # This is for local testing only
    app.run(debug=True, port=5000)
