from dataclasses import dataclass
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.clients.firestore_client import get_firestore_client
from app.repositories import get_servers, get_channels, get_server
from app.models.entities import Server

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request, db=Depends(get_firestore_client)):
    return templates.TemplateResponse("home.jinja", {"request": request})
