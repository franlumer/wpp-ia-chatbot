from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import threading
import queue

import credentials as cr
import utils

# --------------------------------------------------------------------------------

client = cr.CLIENT
IAmodel = cr.AI_MODEL

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    incomingMsg = request.form.get('Body')
    incomingNum = request.form.get('From')

    if incomingMsg.lower() == "/exit":    
        return str(utils.sendMessage("Cerrando sesion..."))

    else:
        resultQueue = queue.Queue()

        sesionThread = threading.Thread(target=utils.generateMsg, args=(incomingMsg, resultQueue))
        sesionThread.start()

        return str(utils.sendMessage(resultQueue.get()))

if __name__ == "__main__":
    app.run(port=8080, debug= True)