import time
from fastapi import APIRouter, Depends, Response
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.clients.firestore_client import get_firestore_client
from app.dependencies import init_ai
from app.models.ai import get_ai
from ..models.entities import Chat, Thread, User, Message
from app.repositories import add_thread, delete_thread, get_thread, get_threads, get_messages, add_message
from app.dependencies import get_current_user
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{thread_id}", response_class=HTMLResponse)
async def index(request: Request, thread_id: str, db=Depends(get_firestore_client)):
    thread = get_thread(db, thread_id)
    messages = get_messages(db, thread_id)
    current_user = get_current_user(request)
    return templates.TemplateResponse("_messages.jinja", {"request": request, "messages": messages, "current_user": current_user, "thread": thread})


@router.post("/", response_class=HTMLResponse)
async def create(request: Request, thread_id: str = Form(...), content: str = Form(...), db=Depends(get_firestore_client), ai=Depends(get_ai)):
    # thread = get_thread(db, thread_id)
    current_user = get_current_user(request)
    message = Message(id="",
                      channel=None,
                      thread=thread_id,
                      sender=current_user.uid,
                      content=content,
                      created_at=datetime.now()
                      )
    message = add_message(db, message)
    messages = get_messages(db, thread_id)

    reply = ai.reply(messages)

    reply_message = Message(id="",
                            channel=None,
                            thread=thread_id,
                            sender="assistant",
                            content=reply,
                            created_at=datetime.now()
                            )
    add_message(db, reply_message)

    # return empty response
    return Response(status_code=200)

    # thread = get_thread(db, thread_id)
    # messages = get_messages(db, thread_id)
    # print("messages", messages)
    # current_user = get_current_user(request)
    # return templates.TemplateResponse("_messages.jinja", {"request": request, "messages": messages, "current_user": current_user, "thread": thread})
