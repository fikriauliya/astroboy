from .models.entities import Server, Channel, Thread, Message


def get_servers(db):
    docs = db.collection("servers").stream()
    servers = [Server(id=doc.id, name=doc.get("name")) for doc in docs]
    return servers


def get_server(db, server_id: str) -> Server:
    doc = db.collection("servers").document(server_id).get()
    return Server(id=doc.id, name=doc.get("name"))


def get_channels(db, server_id: str) -> list[Channel]:
    docs = db.collection("channels").where("server", "==", server_id).stream()
    channels = [Channel(id=doc.id, name=doc.get("name"), server=doc.get("server"))
                for doc in docs]
    return channels


def get_channel(db, channel_id: str) -> Channel:
    doc = db.collection("channels").document(channel_id).get()
    return Channel(id=doc.id, name=doc.get("name"), server=doc.get("server"))


def get_threads(db, channel_id: str) -> list[Thread]:
    docs = db.collection("threads").where(
        "channel", "==", channel_id).order_by("created_at", direction="DESCENDING").stream()
    threads = [Thread(id=doc.id, name=doc.get("name"), channel=doc.get("channel"),
                      created_at=doc.get("created_at"), created_by=doc.get("created_by")) for doc in docs]
    return threads


def get_thread(db, thread_id: str) -> Thread:
    doc = db.collection("threads").document(thread_id).get()
    return Thread(id=doc.id, name=doc.get("name"), channel=doc.get("channel"),
                  created_at=doc.get("created_at"), created_by=doc.get("created_by"))


def add_thread(db, thread: Thread) -> Thread:
    _, doc_ref = db.collection("threads").add(
        thread.model_dump(exclude={"id"}))
    thread.id = doc_ref.id
    return thread


def delete_thread(db, thread_id: str):
    # Start a batch
    batch = db.batch()

    # Get all messages in the thread
    messages = db.collection("messages").where(
        "thread", "==", thread_id).stream()

    # Add each message to the batch for deletion
    for message in messages:
        message_ref = db.collection("messages").document(message.id)
        batch.delete(message_ref)

    # Delete the thread
    thread_ref = db.collection("threads").document(thread_id)
    batch.delete(thread_ref)

    # Commit the batch
    batch.commit()


def get_messages(db, thread_id: str):
    docs = db.collection("messages").where("thread", "==", thread_id).order_by(
        "created_at", direction="ASCENDING").stream()
    docs = [(doc.id, doc.to_dict()) for doc in docs]
    return [Message(id=doc[0],
                    thread=doc[1].get("thread"),
                    channel=doc[1].get("channel"),
                    sender=doc[1].get("sender"),
                    content=doc[1].get("content"),
                    created_at=doc[1].get("created_at")) for doc in docs]


# def get_messages_stream(db, thread_id: str):
#     docs = db.collection("messages").where("thread", "==", thread_id).order_by(
#         "created_at", direction="ASCENDING").stream()

#     # keep streaming on the docs, and yield the messages

#     for doc in docs:
#         yield Message(id=doc.id,
#                       thread=doc.get("thread"),
#                       channel=doc.get("channel"),
#                       sender=doc.get("sender"),
#                       content=content,
#                       created_at=doc.get("created_at"))


def add_message(db, message: Message) -> Message:
    _, doc_ref = db.collection("messages").add(
        message.model_dump(exclude={"id"}, exclude_none=True))
    message.id = doc_ref.id
    return message
