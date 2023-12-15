from collections import defaultdict
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    uid: str
    name: str
    email: str


class Chat(BaseModel):
    id: int
    sender: User
    message: str


# TODO: don't hardcode

bot_uid = "assistant"


class Message(BaseModel):
    id: str
    channel: Optional[str] = None
    thread: Optional[str] = None
    sender: str
    content: str
    created_at: datetime

    def is_bot(self):
        return self.sender == bot_uid

# @dataclass
# class Thread:
#     id: int
#     name: str
#     chats: list[Chat]

#     def __str__(self) -> str:
#         result = ""
#         result += f'Thread: {self.name}\n'
#         for chat in self.chats:
#             lines = chat.message.split('\n')
#             # prepend line with '  ' except the first line
#             lines = ['  ' + line if i > 0 else line for i,
#                      line in enumerate(lines)]
#             message = '\n'.join(lines)

#             result += f'  {chat.sender.name}: {message}\n'
#         return result

#     def add_chat(self, chat: Chat):
#         self.chats.append(chat)


# class SummarizedThread(Thread):
#     def __init__(self, thread: Thread) -> None:
#         self.id = thread.id
#         self.name = thread.name
#         # last 10 messages
#         self.chats = thread.chats[-10:]


class Server(BaseModel):
    id: str
    name: str


class Channel(BaseModel):
    id: str
    name: str
    server: str


class Thread(BaseModel):
    id: str
    name: str
    channel: str
    created_at: datetime
    created_by: str
