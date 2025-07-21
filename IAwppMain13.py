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

    if incomingMsg.lower() == "/exit":
        TwilioResponse = MessagingResponse()
        TwilioResponse.message("Cerrando sesion...")
        return str(TwilioResponse)

    else:
        result_queue = queue.Queue()
        sesionThread = threading.Thread(target=utils.generateMsg, args=(incomingMsg, result_queue))
        sesionThread.start()

        print(result_queue)






        TwilioResponse = MessagingResponse()
        #utils.checkMsg(sesionThread)
        TwilioResponse.message(result_queue.get())
        return str(TwilioResponse)      

if __name__ == "__main__":
    app.run(port=8080, debug= True)