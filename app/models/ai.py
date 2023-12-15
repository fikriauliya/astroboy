
from openai import OpenAI
import os
from .entities import Thread, Message
from dotenv import load_dotenv

model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo"


class AI:
    def __init__(self, client, system_message):
        self.client = client
        self.system_message = system_message

    def reply(self, messages: list[Message]) -> str:
        # convert thread to messages
        messages = [{"role": "assistant" if message.is_bot(
        ) else "user", "content": message.content} for message in messages]
        messages = [
            {"role": "system", "content": self.system_message}, *messages]

        reply = self.client.chat.completions.create(
            model=model, messages=messages)

        return reply.choices[0].message.content

    def speak(self, id, message):
        self.client.speak(id, message)


load_dotenv()

# TODO: refactor


def get_ai() -> AI:
    system_message = """\
        You are an AI assistant, helping student to learn machine learning & python. 
        Answer in Bahasa Indonesia concisely and clearly. 
        Don't answer questions not related to machine learning & Python.
        Reply in maximum of 2 paragraph (excluding code).
        Give code examples if necessary."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return AI(client, system_message)
