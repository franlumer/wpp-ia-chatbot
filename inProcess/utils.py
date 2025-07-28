import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

chats = {} # numero : [mensajes]

class Context: 
    def __init__(self):
        self.messages = {}

    def add(self, incomingNum, incomingMsg = None, AIResponse = None):
        if incomingNum not in self.messages:
            self.messages[incomingNum] = [{"role": "system", "content": cr.AI_PROMPT}]
            self.messages[incomingNum].append({"role": "user", "content": incomingMsg}, {"role": "assistant", "content": AIResponse})
        else:
            self.messages[incomingNum].append({"role": "user", "content": incomingMsg}, {"role": "assistant", "content": AIResponse})

    def reset(self):
        self.messages = {}

def limpiar_texto(IAResponseText):
    msg = re.sub(r".*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg

def generateMsg(incomingMsg, incomingNum, result_queue):
    print(chats)
#    actualContext = [{"role": "system", "content": cr.AI_PROMPT},
#        {"role": "user", "content": incomingMsg}]
    
    try: 
        IAresponse = cr.CLIENT.chat.completions.create(
        model= cr.AI_MODEL,
        messages = [{"role": "system", "content": cr.AI_PROMPT},
        {"role": "user", "content": incomingMsg}])

        Context.add(incomingNum)

    except Exception as e:
        result_queue.put(f'Error: {e}')  

    try:
        Context.add(incomingNum, incomingMsg, limpiar_texto(IAresponse.choices[0].message.content))    

    except Exception as e:
        result_queue.put(f'Error: {e}')

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


