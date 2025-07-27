import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

chats = {} # Clave (numero) : Valor (lista de mensajes)

def limpiar_texto(IAResponseText):
    msg = re.sub(r"<think>.*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg

def generateMsg(incomingMsg, incomingNum, result_queue):
    print(chats)
#    actualContext = [{"role": "system", "content": cr.AI_PROMPT},
#        {"role": "user", "content": incomingMsg}]
    
    try: 
        IAresponse = cr.CLIENT.chat.completions.create(
        model= cr.AI_MODEL,
        messages = chats[incomingNum])

    except Exception as e:
        IAresponse = cr.CLIENT.chat.completions.create(
        model= cr.AI_MODEL,
        messages = [{"role": "user", "content": incomingMsg}])      

    IAResponseText = IAresponse.choices[0].message.content
    msg = limpiar_texto(IAResponseText)

    addContext(incomingNum, incomingMsg, msg)
    
    result_queue.put(msg)

def checkMsg(msg):
    TwilioResponse = MessagingResponse()
    match msg: 
        case None:
            TwilioResponse.message('Procesando...')
            checkMsg(msg)
        case _:
            TwilioResponse.message(msg)

def sendMessage(message):
            TwilioResponse = MessagingResponse()
            TwilioResponse.message(message)
            return TwilioResponse

def addContext(incomingNum, incomingMsg, IAResponseText):
    if incomingNum not in chats:
        chats[incomingNum] = [{"role": "system", "content": cr.AI_PROMPT}]
    chats[incomingNum].append({"role": "user", "content": incomingMsg})
    chats[incomingNum].append({"role": "assistant", "content": IAResponseText})


# Hay que pasar context, dentro de generateMsg() como un parametro en messages=
# Debe de ser una lista de diccionarios: 
#                                       {"role": "system", "content": cr.AI_PROMPT},
#                                       {"role": "user", "content": incomingMsg}
# De alguna forma hay que crear una funcion que vaya guardando lo que se envía dentro del mensaje