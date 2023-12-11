from fastapi import APIRouter
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import init_ai, random_id
from entities import Chat, User
from chatapp import ChatApp

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ai = init_ai()
chat_app = ChatApp()
chat_app.add_thread(0, "main", Chat(
    1, User(random_id(), "assistant"), "Hello, I am your virtual assistant. Ask me anything"))


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    thread = chat_app.get_thread(0)
    audio_path = f"/public/{thread.chats[-1].id}.mp3"
    return templates.TemplateResponse("index.jinja", {"request": request, "thread": thread,
                                                      "audio_path": audio_path})


@router.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    new_chat = Chat(random_id(), User(1, "user"), message)
    chat_app.add_chat(0, "main", new_chat)
    thread = chat_app.get_thread(0)

    reply = Chat(random_id(), User(0, "assistant"), ai.reply(thread))
    chat_app.add_chat(0, "main", reply)

    ai.speak(reply.id, reply.message)

    audio_path = f"/public/{reply.id}.mp3"
    return templates.TemplateResponse("_chat.jinja", {"request": request, "chats": [new_chat, reply],
                                                      "audio_path": audio_path})
