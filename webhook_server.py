import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the Telegram bot token and chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            print("Received invalid JSON")
            return jsonify({"error": "Invalid JSON"}), 400

        # Print the entire incoming JSON payload to the log
        print("Received webhook payload:")
        print(json.dumps(data, indent=4))

        alerts = data.get('alerts', [])
        if not alerts:
            print("No alerts found in the request")
            return jsonify({"error": "No alerts found in the request"}), 400

        for alert in alerts:
            print(f"Processing alert: {alert}")
            message = format_alert_message(alert)
            print(f"Formatted message: {message}")
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
    
    # Adding emojis based on status and severity
    status_emoji = "✅" if status == "resolved" else "🔥"
    severity_emoji = {
        "critical": "🚨",
        "warning": "⚠️",
        "info": "ℹ️"
    }.get(severity, "")
    
    message = (
        f"{status_emoji} *Alert:* {alertname}\n"
        f"*Status:* {status}\n"
        f"{severity_emoji} *Severity:* {severity}\n"
        f"*Namespace:* {namespace}\n"
        f"*Pod:* {pod}\n"
        f"*Description:* {description}\n"
        f"*Start Time:* {starts_at}\n"
        f"*End Time:* {ends_at}\n"
    )
    return message

def send_telegram_message(message):
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(TELEGRAM_API_URL, data=json.dumps(payload), headers=headers)
    print(f"Telegram API response status: {response.status_code}")
    print(f"Telegram API response text: {response.text}")
    if not response.ok:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    # Ensure the necessary environment variables are set
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
        exit(1)
        
    app.run(host='0.0.0.0', port=5000)
