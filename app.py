from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    to = data.get("to")
    message = data.get("message")

    try:
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        return jsonify({"status": "success", "sid": sms.sid}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ nécessaire pour Render
    app.run(host='0.0.0.0', port=port)
