from flask import Flask, request
import threading
import queue

import utils
# --------------------------------------------------------------------------------

app = Flask(__name__)

Message = utils.Message()
Context = utils.Context()

resultQueue = queue.Queue()

@app.route("/whatsapp", methods=["POST", "GET"])



def whatsapp_reply():
    incomingMsg = request.form.get('Body')
    incomingNum = request.form.get('From')               # returns whatsapp:+5493885107546
    incomingNum = incomingNum.replace('whatsapp:+', '')  # returns 5493885107546

    match incomingMsg.lower():
        case '/help':
            return str(Message.send(
                "/help - Muestra esta ayuda.\n"
                "/test - Verifica la conexión.\n"
                "/resetcontext - Reinicia el contexto.\n"
                "/startcontext - Inicia el contexto.\n"
                "/stopcontext - Detiene el contexto.\n"
                "/showcontext - Muestra el contexto actual.\n"
                "/contextstatus - Muestra el estado del contexto."
            ))
        
        case '/test':
            print('/test')
            resultQueue.put('*Conexión exitosa.*')
        
        case '/resetcontext':
            print('/resetcontext')
            Context.reset()
            resultQueue.put('*Contexto reiniciado.*')
        
        case '/startcontext':
            print('/startcontext')
            Context.start()
            resultQueue.put('*Contexto iniciado.*')
            
        case '/stopcontext':
            print("/stopcontext")
            Context.stop()
            resultQueue.put('*Contexto detenido.*')
        
        case '/showcontext':
            print('/showcontext')
            if not Context.chats:
                resultQueue.put('*No hay contexto guardado.*')
            else:
                resultQueue.put(Context.chats)
        
        case '/contextstatus':
            print('/contextstatus')
            print(str(Context.context))
            resultQueue.put(str(Context.context))
        
        case _:
            sesionThread = threading.Thread(target=Message.generate, args=(incomingMsg, incomingNum, resultQueue))
            sesionThread.start()

    return str(Message.send(resultQueue.get()))

if __name__ == "__main__":
    app.run(port=8080, debug= True)