from flask import Flask, request
import threading
import queue

import utils
# --------------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    incomingMsg = request.form.get('Body')
    incomingNum = request.form.get('From')               # returns whatsapp:+5493885107546
    incomingNum = incomingNum.replace('whatsapp:+', '')  # returns 5493885107546

    match incomingMsg.lower():
        
        case '/reset':
            utils.Context.reset()
            return str(utils.Message.send('*Contexto reiniciado.*'))
        
        case '/start':
            utils.Context.start()
            return str(utils.Message.send('*Contexto iniciado.*'))
            
        case '/stop':
            utils.Context.stop()
            return(str(utils.Message.send('*Contexto detenido.*')))
        
        case _:
            resultQueue = queue.Queue()

            sesionThread = threading.Thread(target=utils.Message.generate, args=(incomingMsg, incomingNum, resultQueue))
            sesionThread.start()

            return str(utils.Message.send(resultQueue.get()))

if __name__ == "__main__":
    app.run(port=8080, debug= True)