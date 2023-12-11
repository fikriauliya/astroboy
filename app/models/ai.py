
from .entities import Thread


class AI:
    def __init__(self, client, system_message):
        self.client = client
        self.system_message = system_message

    def reply(self, thread: Thread) -> str:
        # convert thread to messages
        messages = [
            {"role": "system",
                "content": self.system_message},
            *_convert_thread_to_messages(thread)
        ]
        print(messages)
        reply = self.client.complete('gpt-3.5-turbo', messages)
        return reply

    def speak(self, id, message):
        self.client.speak(id, message)


def _convert_thread_to_messages(thread: Thread) -> list[dict]:
    messages = []
    for chat in thread.chats:
        messages.append(
            {"role": chat.sender.name, "content": chat.message})
    return messages
