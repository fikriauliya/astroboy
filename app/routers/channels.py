from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.clients.firestore_client import get_firestore_client
from app.dependencies import get_current_user
from app.repositories import get_channel, get_channels, get_server, get_servers, get_threads
from app.models.entities import Thread

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{channel_id}")
async def detail(request: Request, channel_id: str, db=Depends(get_firestore_client)):
    selected_channel = get_channel(db, channel_id)
    servers = get_servers(db)

    selected_server = get_server(db, selected_channel.server)
    channels = get_channels(db, selected_server.id)

    threads = get_threads(db, channel_id)
    current_user = get_current_user(request)

    print("servers", servers, "selected_server", selected_server,
          "channels", channels, "selected_channel", selected_channel, "threads", threads)

    return templates.TemplateResponse("channel.jinja", {"request": request,
                                                        "servers": servers,
                                                        "selected_server": selected_server,
                                                        "channels": channels,
                                                        "selected_channel": selected_channel,
                                                        "threads": threads,
                                                        "current_user": current_user})
