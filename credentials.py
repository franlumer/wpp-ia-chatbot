from openai import OpenAI

AI_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b"
BASE_URL ="http://192.168.50.101:1234/v1"
API_KEY ="not-needed"
AI_PROMPT = "Eres un asistente útil y debes responder lo más rápido posible."

CLIENT = OpenAI(base_url = BASE_URL, api_key = API_KEY)
