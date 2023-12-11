from collections import defaultdict
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str


@dataclass
class Chat:
    id: int
    sender: User
    message: str


@dataclass
class Thread:
    id: int
    name: str
    chats: list[Chat]

    def __str__(self) -> str:
        result = ""
        result += f'Thread: {self.name}\n'
        for chat in self.chats:
            lines = chat.message.split('\n')
            # prepend line with '  ' except the first line
            lines = ['  ' + line if i > 0 else line for i,
                     line in enumerate(lines)]
            message = '\n'.join(lines)

            result += f'  {chat.sender.name}: {message}\n'
        return result

    def add_chat(self, chat: Chat):
        self.chats.append(chat)


class SummarizedThread(Thread):
    def __init__(self, thread: Thread) -> None:
        self.id = thread.id
        self.name = thread.name
        # last 10 messages
        self.chats = thread.chats[-10:]
