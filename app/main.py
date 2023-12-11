
from dotenv import load_dotenv

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .dependencies import init_ai, random_id
from entities import Chat, User
from chatapp import ChatApp

from .routers.servers import router as server_router
from .routers.channels import router as channel_router
from .routers.threads import router as thread_router

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
app.include_router(server_router, prefix="/servers")
app.include_router(channel_router, prefix="/channels")
app.include_router(thread_router, prefix="/threads")

load_dotenv()
