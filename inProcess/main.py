from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import threading
import queue

import credentials
import utils
# --------------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    incomingMsg = request.form.get('Body')
    incomingNum = request.form.get('From') # returns whatsapp:+5493885107546
    incomingNum = incomingNum.replace('whatsapp:+', '') # returns 5493885107546

    match incomingMsg.lower():
        case '/exit':
            return str(utils.sendMessage("Cerrando sesion..."))
        
        case '/reset':
            utils.Context.reset()
            return str(utils.sendMessage('Contexto reiniciado.'))
            
        case _:
            resultQueue = queue.Queue()

            sesionThread = threading.Thread(target=utils.generateMsg, args=(incomingMsg, incomingNum, resultQueue))
            sesionThread.start()

            return str(utils.sendMessage(resultQueue.get()))

if __name__ == "__main__":
    app.run(port=8080, debug= True)