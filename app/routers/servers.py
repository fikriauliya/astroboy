from fastapi import APIRouter
from google.cloud import firestore

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello, world!"}
