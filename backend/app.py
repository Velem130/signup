

from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SENDER_EMAIL = "mlulekivelem@gmail.com"
SENDER_PASSWORD = "esvnbtnnvtgbeahz"  

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    try:
        msg = MIMEText(f"New submission:\n\nName: {name}\nEmail: {email}\nMessage: {message}")
        msg["Subject"] = "New Form Submission"
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL  # Send to yourself

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
