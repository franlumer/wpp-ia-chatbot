from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import re
import time

from openai import OpenAI

client = OpenAI(base_url="http://192.168.50.101:1234/v1", api_key="not-needed")
IAmodel = "deepseek/deepseek-r1-0528-qwen3-8b"

def generateMsg(incomingMsg):
    IAresponse = client.chat.completions.create(
    model= IAmodel,
    messages=[
        {"role": "system", "content": "Eres un asistente útil y debes responder lo más rápido posible."},
        {"role": "user", "content": incomingMsg}])
    
    IAResponseText = IAresponse.choices[0].message.content
    msg = re.sub(r"<think>.*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg



app = Flask(__name__)

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    TwilioResponse = MessagingResponse()

    incomingMsg = request.form.get('Body')

    if incomingMsg.lower() == "/exit":
        TwilioResponse.message("Cerrando sesion...")
        return str(TwilioResponse)

    else:
        msg = None
        msg = generateMsg(incomingMsg)
        TwilioResponse.message(msg)
        return str(TwilioResponse)
    
def checkMsg(msg):
    TwilioResponse = MessagingResponse()
    match msg: 
        case None:
            TwilioResponse.message('Procesando...')
            time.sleep(3)
            checkMsg(msg)
        case _:
            TwilioResponse.message(msg)

if __name__ == "__main__":
    app.run(port=8080, debug= True)


# queda pendiente hacer una funcion que verifique si el mensaje se sigue procesando dentro del modelo
# o si ya está disponible. en caso de que se siga procesando hay que hacer que se envíe un mensaje
# predefinido para que twilio no cierre la sesion y asi se pueda enviár el mensaje final