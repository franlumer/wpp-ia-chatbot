import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

chats = {} # numero : [mensajes] | Solo para la version funcional, no para POO

def limpiar_texto(IAResponseText):
    msg = re.sub(r".*</think>", " ", IAResponseText, flags= re.DOTALL)
    return msg

class Context: 
    def __init__(self):
        self.context = False
        self.chats = {}  # 1. {"role": "system", "content": PROMPT}
                            # 2. {"role": "user", "content": CONSULTA}
                            # 3. {"role": "asistant", "content": RESPUESTA}

    def add(self, incomingNum, incomingMsg = None, AIResponse = None):
        if incomingNum not in self.chats:
            self.chats[incomingNum] = [{"role": "system", "content": cr.AI_PROMPT}] # Agrega el PROMPT
            self.chats[incomingNum].append({"role": "user", "content": incomingMsg}, {"role": "assistant", "content": AIResponse}) # Agrega la consulta y la respuesta

        else:
            self.chats[incomingNum].append({"role": "user", "content": incomingMsg}, {"role": "assistant", "content": AIResponse})

    def reset(self):
        self.chats = {}

    def start(self):
        self.context = True

    def stop(self):
        self.context = False

class Message:
    def __init__(self):
        pass

    def check(self, message):
            TwilioResponse = MessagingResponse()
            match message: 
                case None:
                    TwilioResponse.message('Procesando...')
                    checkMsg(message)
                case _:
                    TwilioResponse.message(message)

    def send(self, message):
        TwilioResponse = MessagingResponse()
        TwilioResponse.message(message)
        return TwilioResponse

    def generate(self, incomingMsg, incomingNum, resultQueue):
        
        context = Context()

        match context.context:
            case True: # Logica en caso de que el contexto esté activo
                print(context.chats)

                if incomingNum in context.chats:
                    chatContext = context.chats[incomingNum]
                    
                    chatContext.append({"role": "assistant", "content": incomingMsg})

                else:
                    context.chats[incomingNum] = []

                    chatContext = context.chats[incomingNum]

                    chatContext.append([{"role": "system", "content": cr.AI_PROMPT},
                                        {"role": "user", "content": incomingMsg}])

                IAresponse = cr.CLIENT.chat.completions.create(
                model= cr.AI_MODEL,
                messages = chatContext)

                IAResponseText = IAresponse.choices[0].message.content

                chatContext.append(limpiar_texto(IAResponseText))

                resultQueue.put(limpiar_texto(IAResponseText))

            case _: # Lógica de contexto desactivado
                try: 
                    IAresponse = cr.CLIENT.chat.completions.create(
                    model= cr.AI_MODEL,
                    chats = [{"role": "system", "content": cr.AI_PROMPT},
                    {"role": "user", "content": incomingMsg}])

                except Exception as e:
                    resultQueue.put(f'Error (Completion): {e}')
        
        try:
            match context.context:
                case True:
                    context.add(incomingNum, incomingMsg, limpiar_texto(IAresponse.choices[0].message.content))
                    print(context.chats)
                case _: 
                    pass

        except Exception as e:
            print(Context.chats)
            resultQueue.put(f'Error (context): {e}')

        IAResponseText = IAresponse.choices[0].message.content
        msg = limpiar_texto(IAResponseText)
        
        resultQueue.put(msg)



















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


