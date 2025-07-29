from flask import Flask, request
import threading
import queue

import utils
# --------------------------------------------------------------------------------

app = Flask(__name__)

Message = utils.Message()
Context = utils.Context()

@app.route("/whatsapp", methods=["POST","GET"])

def whatsapp_reply():
    incomingMsg = request.form.get('Body')
    incomingNum = request.form.get('From')               # returns whatsapp:+5493885107546
    incomingNum = incomingNum.replace('whatsapp:+', '')  # returns 5493885107546

    match incomingMsg.lower():
        case '/test':
            return str(Message.send('*Conexión exitosa.*'))
        
        case '/resetcontext':
            Context.reset()
            return str(Message.send('*Contexto reiniciado.*'))
        
        case '/startcontext':
            Context.start()
            return str(Message.send('*Contexto iniciado.*'))
            
        case '/stopcontext':
            Context.stop()
            return str(Message.send('*Contexto detenido.*'))
        
        case '/showcontext':
            return (str(Message.send(str(Context.messages))))
        
        case '/contextstatus':
            print(str(Context.context))
            return (str(Message.send(str(Context.context))))
        
        case _:
            resultQueue = queue.Queue()

            sesionThread = threading.Thread(target=Message.generate, args=(incomingMsg, incomingNum, resultQueue))
            sesionThread.start()

            return str(Message.send(resultQueue.get()))

if __name__ == "__main__":
    app.run(port=8080, debug= True)