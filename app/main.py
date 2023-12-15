
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .dependencies import init_ai

from .routers.servers import router as server_router
from .routers.channels import router as channel_router
from .routers.threads import router as thread_router
from .routers.home import router as home_router
from .routers.messages import router as message_router
from .routers.stream import router as stream_router


app = FastAPI()
load_dotenv()

app.mount("/public", StaticFiles(directory="app/public"), name="public")
app.include_router(home_router)
app.include_router(server_router, prefix="/servers")
app.include_router(channel_router, prefix="/channels")
app.include_router(thread_router, prefix="/threads")
app.include_router(message_router, prefix="/messages")
app.include_router(stream_router, prefix="/streams")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return RedirectResponse(url='/')
