from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time

from openai import OpenAI

client = OpenAI(base_url="http://192.168.50.101:1234/v1", api_key="not-needed")
IAmodel = "deepseek/deepseek-r1-0528-qwen3-8b"

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    TwilioResponse = MessagingResponse()
    incoming_msg = str(request.form.get('Body'))

    if incoming_msg.lower() == "/exit":
        TwilioResponse.message("Cerrando sesión...")
        exit()

    else:
        IAresponse = client.chat.completions.create(
        model= IAmodel,
        messages=[
            {"role": "system", "content": "Eres un asistente útil y debes responder lo más rápido posible. responde con texto plano, no uses markdown"},
            {"role": "user", "content": incoming_msg}
            ]
        )
        msg = str(IAresponse.choices[0].message.content)
        TwilioResponse.message(msg)
        print(msg)
    
    return str(TwilioResponse)

if __name__ == "__main__":
    app.run(port=8080)
