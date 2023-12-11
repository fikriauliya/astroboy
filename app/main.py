
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .dependencies import init_ai, random_id

from .routers.servers import router as server_router
from .routers.channels import router as channel_router
from .routers.threads import router as thread_router

app = FastAPI()
app.mount("/public", StaticFiles(directory="app/public"), name="public")
app.include_router(server_router, prefix="/servers")
app.include_router(channel_router, prefix="/channels")
app.include_router(thread_router, prefix="/threads")

load_dotenv()
