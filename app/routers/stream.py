import time
from fastapi import APIRouter, Depends, Response
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sse_starlette import EventSourceResponse, ServerSentEvent
from app.clients.firestore_client import get_firestore_client
from app.dependencies import init_ai
from ..models.entities import Chat, Thread, User, Message
from ..models.chatapp import ChatApp
from app.repositories import add_thread, delete_thread, get_thread, get_threads, get_messages, add_message
from app.dependencies import get_current_user
from datetime import datetime
import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# @router.get("/{thread_id}")
# async def stream(thread_id: str, db=Depends(get_firestore_client)):
#     def event_stream():
#         i = 0
#         while True:
#             yield f"The server time is: {time.time()}"
#             time.sleep(1)

#     return EventSourceResponse(event_stream())


@router.get("/messages/{thread_id}")
async def messages(request: Request, thread_id: str, db=Depends(get_firestore_client)):
    print("Streaming, thread:", thread_id)

    thread = get_thread(db, thread_id)
    current_user = get_current_user(request)

    queue = asyncio.Queue()

    loop = asyncio.get_event_loop()
    messages = []

    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            event_data = change.document.to_dict()
            print(change.type.name, event_data)
            message = Message(id=change.document.id,
                              channel=None,
                              thread=thread_id,
                              sender=event_data["sender"],
                              content=event_data["content"],
                              created_at=event_data["created_at"]
                              )
            asyncio.run_coroutine_threadsafe(
                queue.put((change.type.name, message)), loop)

    query = db.collection("messages").where("thread", "==", thread_id).order_by(
        "created_at", direction="ASCENDING")
    query_watch = query.on_snapshot(on_snapshot)

    async def generator():
        try:
            while True:
                event_data = await queue.get()
                event = event_data[0]
                data = event_data[1]
                if event == "ADDED":
                    messages.append(data)
                    html = templates.get_template("_messages.jinja").render(
                        request=request, messages=messages, current_user=current_user, thread=thread)
                    yield ServerSentEvent(data=html, event=event)
        except asyncio.CancelledError:
            print("Unsubscribing from query, thread:", thread_id)
            query_watch.unsubscribe()
            raise

    return EventSourceResponse(generator())
