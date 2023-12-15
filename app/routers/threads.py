from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.clients.firestore_client import get_firestore_client
from app.dependencies import init_ai
from ..models.entities import Chat, Message, Thread, User
from app.models.ai import AI, get_ai
from app.repositories import add_thread, delete_thread, get_thread, get_threads, add_message
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ai = init_ai()
# chat_app = ChatApp()
# chat_app.add_thread(thread_id=0, thread_name="main", first_chat=Chat(
#     id=1, sender=User(uid='sdf2iu89s', name="assistant", email="assistant@ruangguru.com"),
#     message="Hello, I am your virtual assistant. Ask me anything"))


# @router.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     thread = chat_app.get_thread(0)
#     audio_path = f"/public/{thread.chats[-1].id}.mp3"
#     return templates.TemplateResponse("index.jinja", {"request": request, "thread": thread,
#                                                       "audio_path": audio_path})


# @router.post("/chat", response_class=HTMLResponse)
# async def chat(request: Request, message: str = Form(...)):
#     new_chat = Chat(random_id(), User(1, "user"), message)
#     chat_app.add_chat(0, "main", new_chat)
#     thread = chat_app.get_thread(0)

#     reply = Chat(random_id(), User(0, "assistant"), ai.reply(thread))
#     chat_app.add_chat(0, "main", reply)

#     ai.speak(reply.id, reply.message)

#     audio_path = f"/public/{reply.id}.mp3"
#     return templates.TemplateResponse("_chat.jinja", {"request": request, "chats": [new_chat, reply],
#                                                       "audio_path": audio_path})

@router.post("/")
async def create(request: Request, channel_id: str = Form(...), content: str = Form(...), db=Depends(get_firestore_client), ai=Depends(get_ai)):
    # TODO replace with summary
    thread_name = content
    created_at = datetime.now()
    current_user = get_current_user(request)
    thread = Thread(id="", name=thread_name,
                    channel=channel_id, created_at=created_at,
                    created_by=current_user.uid)
    thread = add_thread(db, thread)
    message = Message(id="", channel=channel_id, thread=thread.id,
                      sender=current_user.uid, content=content, created_at=created_at)
    add_message(db, message)
    threads = get_threads(db, channel_id)
    reply = ai.reply([message])

    reply_message = Message(id="", channel=None, thread=thread.id,
                            sender="assistant", content=reply, created_at=datetime.now())
    add_message(db, reply_message)

    return templates.TemplateResponse("_threads.jinja", {"request": request, "threads": threads, "current_user": current_user})


@router.delete("/{thread_id}")
async def delete(request: Request, thread_id: str, db=Depends(get_firestore_client)):
    thread = get_thread(db, thread_id)
    channel_id = thread.channel
    current_user = get_current_user(request)

    if thread.created_by == current_user.uid:
        delete_thread(db, thread_id)

    threads = get_threads(db, channel_id)
    return templates.TemplateResponse("_threads.jinja", {"request": request, "threads": threads, "current_user": current_user})
