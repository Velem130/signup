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

SENDER_EMAIL = "mlukivelem@issajozi.xyz" 

RECIPIENT_EMAIL = "shamilajoma@gmail.com" 

# --- Routes ---

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

 
    sendgrid_payload = {
        "personalizations": [{
           
            "to": [{"email": RECIPIENT_EMAIL}], 
            "subject": "New Form Submission"
        }],
      
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

       
        if response.status_code == 202:
            print("✅ Email sent successfully via SendGrid")
            return jsonify({"message": "Submitted! We'll contact you soon."}), 200
        else:
         
            print(f"❌ SendGrid failed with status {response.status_code}")
            print(f"❌ SendGrid error body: {response.text}")
            
            return jsonify({"error": "Email service failed. Check backend logs for details."}), 500

    except requests.exceptions.RequestException as e:
       
        print(f"❌ Network or connection error to SendGrid: {e}")
        return jsonify({"error": "Network error with email service."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
