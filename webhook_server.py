import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = 'your_telegram_chat_id'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        alerts = data.get('alerts', [])
        if not alerts:
            return jsonify({"error": "No alerts found in the request"}), 400

        for alert in alerts:
            message = format_alert_message(alert)
            send_telegram_message(message)

        return '', 204
    except Exception as e:
        print(f"Error processing the webhook: {e}")
        return jsonify({"error": str(e)}), 500

def format_alert_message(alert):
    status = alert.get('status', 'N/A')
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    
    alertname = labels.get('alertname', 'N/A')
    severity = labels.get('severity', 'N/A')
    namespace = labels.get('namespace', 'N/A')
    pod = labels.get('pod', 'N/A')
    description = annotations.get('message', 'No description provided.')
    starts_at = alert.get('startsAt', 'N/A')
    ends_at = alert.get('endsAt', 'N/A')
    
    message = (
        f"*Alert:* {alertname}\n"
        f"*Status:* {status}\n"
        f"*Severity:* {severity}\n"
        f"*Namespace:* {namespace}\n"
        f"*Pod:* {pod}\n"
        f"*Description:* {description}\n"
        f"*Start Time:* {starts_at}\n"
        f"*End Time:* {ends_at}\n"
    )
    return message

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Telegram API response: {response.status_code} {response.text}")  # Log the response
    if not response.ok:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
