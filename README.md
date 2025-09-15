# wpp-ia-chatbot

A personal project for building a **WhatsApp chatbot** powered by a **local AI model**, using a dedicated **Twilio** WhatsApp number.

---

## Overview

This project connects WhatsApp with a locally hosted AI model.  
Messages sent to a Twilio WhatsApp number are received via webhook, processed by the AI, and replied to automatically—keeping data private and under your full control.

---

## Features

- **Twilio WhatsApp integration**: receive and send WhatsApp messages.  
- **Local AI inference**: run your own model without external APIs.  
- **Flexible webhook support**: works with any tunnel solution (e.g. **ngrok**, Cloudflare Tunnel, etc.).  
- Modular Python code, easy to extend or customize.

---

## Requirements

- **Python 3.x**  
- A Twilio account with an activated WhatsApp number  
- Twilio credentials: `ACCOUNT_SID`, `AUTH_TOKEN`, and the WhatsApp sender number  
- Project dependencies (see `requirements.txt`)  
- (Optional) Hardware capable of running your chosen local AI model (CPU/GPU, RAM)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/franlumer/wpp-ia-chatbot.git
   cd wpp-ia-chatbot
   ```
2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables (e.g., in a .env file)**
   ```ini
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
   Add any local AI model settings as needed.
   ```

## Usage

1. Expose your local server with a tunnel of your choice
- For example, using ngrok:
```bash
ngrok http 5000
```

2. Copy the generated public HTTPS URL.
- Set the Twilio webhook to the public URL followed by your endpoint (e.g., https://<your-ngrok-url>/webhook).
- Start the application:
```bash
python main.py
```

**Send a WhatsApp message to your Twilio number and the bot will respond using the local AI model.**
