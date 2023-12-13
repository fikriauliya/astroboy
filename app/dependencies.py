import os
from typing import Annotated, Union
from .clients.openai_client import OpenAIClient
from .models.ai import AI
from firebase_admin import auth
from app.models.entities import User


def init_ai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    oai_client = OpenAIClient(OPENAI_API_KEY)
    return AI(oai_client, "You are a chat assistant. Reply briefly, 2 sentences max")


def get_current_user(request):
    token = request.cookies.get("token")
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token["uid"]
    user = auth.get_user(uid)
    user = User(uid=uid, name=user.display_name, email=user.email)
    return user
