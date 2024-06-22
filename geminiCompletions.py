import os
import sys
from dotenv import load_dotenv

import google.generativeai as gai

args = sys.argv

continuous = False
prompt = ""

if len(args) < 2:
    continuous = True
    prompt = "You are an assistant named Gaia, your goal is to help the user with their tasks."
else:
    p = args[1]
    for i in range(2, len(args)):
        p += " " + args[i]
    prompt = p

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gai.configure(api_key=GOOGLE_API_KEY)
model = gai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat()


def get_response(chat_prompt: str) -> str:
    responses = chat.send_message(chat_prompt, safety_settings=safe, stream=True)
    text_response = []
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)


safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

response = get_response(prompt)
print(response)

while continuous:
    prompt = input("You: ")
    response = get_response(prompt)
    print(response)
    if prompt == "exit" or prompt == "quit":
        prompt = "Say goodbye to the user"
        response = get_response(prompt)
        print(response)
        continuous = False