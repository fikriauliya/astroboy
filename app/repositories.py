from .models.entities import Server, Channel, Thread


def get_servers(db):
    docs = db.collection("servers").stream()
    servers = [Server(id = doc.id, name = doc.get("name")) for doc in docs]
    return servers


def get_server(db, server_id: str) -> Server:
    doc = db.collection("servers").document(server_id).get()
    return Server(id = doc.id, name = doc.get("name"))


def get_channels(db, server_id: str) -> list[Channel]:
    docs = db.collection("channels").where("server", "==", server_id).stream()
    channels = [Channel(id = doc.id, name = doc.get("name"), server = doc.get("server"))
                for doc in docs]
    return channels


def get_channel(db, channel_id: str) -> Channel:
    doc = db.collection("channels").document(channel_id).get()
    return Channel(id = doc.id, name = doc.get("name"), server = doc.get("server"))


def get_threads(db, channel_id: str) -> list[Thread]:
    docs = db.collection("threads").where(
        "channel", "==", channel_id).order_by("created_at", direction="DESCENDING").stream()
    threads = [Thread(id = doc.id, name = doc.get("name"), channel = doc.get("channel"),
                      created_at = doc.get("created_at")) for doc in docs]
    return threads


def add_thread(db, thread: Thread) -> Thread:
    _, doc_ref = db.collection("threads").add(thread.model_dump(exclude={"id"}))
    thread.id = doc_ref.id
    return thread
