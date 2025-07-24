import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

def limpiar_texto(IAResponseText):
    msg = re.sub(r"<think>.*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg

def generateMsg(incomingMsg, result_queue):
    actualContext = [{"role": "system", "content": cr.AI_PROMPT},
        {"role": "user", "content": incomingMsg}]
    IAresponse = cr.CLIENT.chat.completions.create(
    model= cr.AI_MODEL,
    messages = actualContext)
    
    addContext(actualContext)

    IAResponseText = IAresponse.choices[0].message.content
    msg = limpiar_texto(IAResponseText)
    result_queue.put(msg)

def checkMsg(msg):
    TwilioResponse = MessagingResponse()
    match msg: 
        case None:
            TwilioResponse.message('Procesando...')
            checkMsg(msg)
        case _:
            TwilioResponse.message(msg)

def sendMessage(message, context):
            TwilioResponse = MessagingResponse()
            TwilioResponse.message(message)
            return TwilioResponse

def addContext(context, actualContext):
     context.append(actualContext)
     

# Hay que pasar context, dentro de generateMsg() como un parametro en messages=
# Debe de ser una lista de diccionarios: 
#                                       {"role": "system", "content": cr.AI_PROMPT},
#                                       {"role": "user", "content": incomingMsg}
# De alguna forma hay que crear una funcion que vaya guardando lo que se envía dentro del mensaje