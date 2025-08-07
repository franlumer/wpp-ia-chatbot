import re
import credentials as cr
from twilio.twiml.messaging_response import MessagingResponse

chats = {} # numero : [mensajes] | Solo para la version funcional, no para POO

def limpiar_texto(AIResponseText):
    msg = re.sub(r".*</think>", " ", AIResponseText, flags= re.DOTALL)
    return msg

class Context: 
    def __init__(self):
        self.context = False
        self.chats = {} # 1. {"role": "system", "content": PROMPT}
                        # 2. {"role": "user", "content": CONSULTA}
                        # 3. {"role": "asistant", "content": RESPUESTA}

    def add(self, incomingNum, incomingMsg = None, AIResponse = None):
        if incomingNum not in self.chats:
            self.chats[incomingNum] = [{"role": "system", "content": cr.AI_PROMPT}]         # Crea la lista y agrega el PROMPT
            self.chats[incomingNum].append({"role": "user", "content": incomingMsg})        # Agrega la consulta
            self.chats[incomingNum].append({"role": "assistant", "content": AIResponse})    # Agrega la respuesta

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

        if context.context:
            print(context.chats)

            if incomingNum in context.chats:
                # Si el numero ya tiene contexto, se agrega el mensaje a la lista

                chatContext = context.chats[incomingNum]
                
                chatContext.append({"role": "assistant", "content": incomingMsg})

            else:
                # Si el numero no tiene contexto, se inicia la lista, se agrega el prompt y el mensaje
                context.chats[incomingNum] = []

                chatContext = context.chats[incomingNum]

                chatContext.append([{"role": "system", "content": cr.AI_PROMPT},
                                    {"role": "user", "content": incomingMsg}])

            # En caso de ya exista contexto o no se envía el mensaje y se genera la respuesta
            AIresponse = cr.CLIENT.chat.completions.create(
                        model= cr.AI_MODEL,
                        messages = chatContext)

            AIResponseText = limpiar_texto(AIresponse.choices[0].message.content)
            
            chatContext.append({"role": "assistant", "content": AIResponseText})

            resultQueue.put(AIResponseText)

        else: # Lógica de contexto desactivado
            try: 
                AIresponse = cr.CLIENT.chat.completions.create(
                model= cr.AI_MODEL,
                chats = [{"role": "system", "content": cr.AI_PROMPT},
                        {"role": "user", "content": incomingMsg}])

                AIResponseText = limpiar_texto(AIresponse.choices[0].message.content)

                resultQueue.put(AIResponseText)
                
            except Exception as e:
                resultQueue.put(f'Error (Completion): {e}')






























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


