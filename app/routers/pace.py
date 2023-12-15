from dataclasses import dataclass
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.templating import Jinja2Templates
from app.clients.firestore_client import get_firestore_client
from app.dependencies import get_current_user
from app.repositories import get_servers, get_channels, get_server, add_pace
from app.models.entities import Pace, Server

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/")
async def create(request: Request, channel_id: str = Form(...), feedback: str = Form(...), db=Depends(get_firestore_client)):
    current_user = get_current_user(request)

    pace = add_pace(db, Pace(id="",
                             channel=channel_id,
                             created_at=datetime.now(timezone.utc),
                             created_by=current_user.uid,
                             feedback=feedback))
    print(pace)
    return Response(status_code=200)
