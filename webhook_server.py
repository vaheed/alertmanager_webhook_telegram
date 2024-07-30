from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = TELEGRAM_CHAT_ID
    message = data.get('message', 'No message provided')
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    if response.status_code == 200:
        return 'Message sent', 200
    else:
        return 'Failed to send message', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
