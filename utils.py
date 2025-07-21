import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

def limpiar_texto(IAResponseText):
    msg = re.sub(r"<think>.*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg

def generateMsg(incomingMsg, result_queue):
    IAresponse = cr.CLIENT.chat.completions.create(
    model= cr.AI_MODEL,
    messages=[
        {"role": "system", "content": cr.AI_PROMPT},
        {"role": "user", "content": incomingMsg}])
    
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