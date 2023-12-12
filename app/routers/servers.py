from dataclasses import dataclass
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.clients.firestore_client import get_firestore_client
from app.repositories import get_servers, get_channels
from app.models.entities import Server

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request, db=Depends(get_firestore_client)):
    servers = get_servers(db)
    return templates.TemplateResponse("servers.jinja", {"request": request, "servers": servers})


@router.get("/{server_id}")
async def detail(request: Request, server_id: str, db=Depends(get_firestore_client)):
    servers = get_servers(db)

    selected_server = db.collection("servers").document(server_id).get()
    selected_server = Server(selected_server.id, selected_server.get("name"))

    channels = get_channels(db, server_id)

    return templates.TemplateResponse("server.jinja", {"request": request,
                                                       "servers": servers,
                                                       "selected_server": selected_server,
                                                       "channels": channels})
