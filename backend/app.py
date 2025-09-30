from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend is running"

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDER_EMAIL = "mlulekivelem@gmail.com"  

@app.route('/submit', methods=['POST'])
def submit():
    print("🔔 Received a form submission")

    try:
        data = request.get_json()
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    print(f"📨 Data received: {data}")

    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not all([name, email, message]):
        return jsonify({"status": "error", "message": "Missing form fields (name, email, or message)"}), 400

    # ✅ Construct the SendGrid email payload
    sendgrid_payload = {
        "personalizations": [{
            "to": [{"email": SENDER_EMAIL}],
            "subject": "New Form Submission"
        }],
        "from": {"email": SENDER_EMAIL},
        "reply_to": {"email": email},
        "content": [{
            "type": "text/plain",
            "value": f"New submission:\n\nName: {name}\nEmail: {email}\nMessage: {message}"
        }]
    }

    try:
        # ✅ Send the email via SendGrid API
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json=sendgrid_payload
        )

        if response.status_code >= 200 and response.status_code < 300:
            print("✅ Email sent successfully via SendGrid")
            return jsonify({"status": "success"}), 200
        else:
            print(f"❌ SendGrid error: {response.status_code} {response.text}")
            return jsonify({"status": "error", "message": f"SendGrid error: {response.text}"}), 500

    except Exception as e:
        print(f"❌ Exception sending email: {e}")
        return jsonify({"status": "error", "message": f"Server Error: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
