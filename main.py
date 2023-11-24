import os
from typing import Annotated, Union
from dotenv import load_dotenv

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from clients.openai_client import OpenAIClient
from ai import AI
from chatapp import ChatApp
from entities import Chat, User


app = FastAPI()
templates = Jinja2Templates(directory="templates")

load_dotenv()


def init_ai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    oai_client = OpenAIClient(OPENAI_API_KEY)
    return AI(oai_client, "You are a chat assistant")


def random_id():
    import random
    return random.randint(0, 1 << 32)


ai = init_ai()
chat_app = ChatApp()
chat_app.add_thread(0, "main", Chat(
    1, User(random_id(), "assistant"), "Hello, I am your virtual assistant."))
# chat_app.get_thread(0).add_chat(
#     Chat(random_id(), User(1, "user"), "Hello, I am a user."))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    thread = chat_app.get_thread(0)
    return templates.TemplateResponse("index.jinja", {"request": request, "thread": thread})


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    new_chat = Chat(random_id(), User(1, "user"), message)
    chat_app.add_chat(0, "main", new_chat)
    thread = chat_app.get_thread(0)

    reply = Chat(random_id(), User(0, "assistant"), ai.reply(thread))
    chat_app.add_chat(0, "main", reply)

    return templates.TemplateResponse("_chat.jinja", {"request": request, "chats": [new_chat, reply]})
