import os
from typing import Annotated, Union
from .clients.openai_client import OpenAIClient
from .models.ai import AI



def init_ai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    oai_client = OpenAIClient(OPENAI_API_KEY)
    return AI(oai_client, "You are a chat assistant. Reply briefly, 2 sentences max")


def random_id():
    import random
    return random.randint(0, 1 << 32)

