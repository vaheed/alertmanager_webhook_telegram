# Kubernetes Alertmanager Webhook Server

This project implements a webhook server that receives alerts from Kubernetes Alertmanager and forwards them to a Telegram chat. It's designed to run as a Kubernetes deployment and can be easily set up using Docker and Kubernetes.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Receives webhook alerts from Kubernetes Alertmanager
- Filters alerts based on configurable severity levels
- Formats alert messages with relevant information and emojis for better readability
- Sends formatted alerts to a specified Telegram chat
- Kubernetes-ready with deployment and service configurations
- Docker support for easy containerization and local testing
- Health check endpoint for monitoring and liveness probes

## Prerequisites

- Docker (version 19.03 or later)
- Kubernetes cluster (version 1.16 or later)
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- Telegram Chat ID (use [@userinfobot](https://t.me/userinfobot) to get your chat ID)
- Python 3.9 or later (for local development)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/k8s-alertmanager-webhook.git
   cd k8s-alertmanager-webhook
   ```

2. Set up your Telegram bot and obtain the bot token and chat ID.

3. Create a `.env` file in the project root with your Telegram credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

4. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

5. Deploy to Kubernetes:
   ```
   kubectl apply -f k8s/webhook-server.yaml
   ```

   Note: Make sure to update the `k8s/webhook-server.yaml` file with your specific configuration, such as the image name and secret names for the Telegram credentials.

## Configuration

### Severity Levels

You can adjust the `SEVERITY_CONFIG` in `webhook_server.py` to control which alert severities are forwarded to Telegram. By default, it's set to:

## Development

To run the server locally for development:

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python webhook_server.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.