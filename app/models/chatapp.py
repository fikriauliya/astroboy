from .entities import Chat, Thread


class ChatApp:
    threads: dict[int, Thread]

    def __init__(self):
        self.threads = {}

    def add_thread(self, thread_id: int, thread_name: str, first_chat: Chat):
        if thread_id in self.threads:
            return
        thread = Thread(thread_id, thread_name, [first_chat])
        self.threads[thread_id] = thread

    def add_chat(self, thread_id: int, thread_name: str, chat: Chat):
        thread = self.threads.get(thread_id)
        if thread is None:
            thread = Thread(thread_id, thread_name, [])
            self.threads[thread_id] = thread
        thread.chats.append(chat)

    def get_thread(self, thread_id: int):
        return self.threads[thread_id]
