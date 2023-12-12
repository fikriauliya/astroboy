from .models.entities import Server, Channel, Thread

def get_servers(db):
    docs = db.collection("servers").stream()
    servers = [Server(doc.id, doc.get("name")) for doc in docs]
    return servers

def get_server(db, server_id):
    doc = db.collection("servers").document(server_id).get()
    return Server(doc.id, doc.get("name"))

def get_channels(db, server_id):
    docs = db.collection("channels").where("server", "==", server_id).stream()
    channels = [Channel(doc.id, doc.get("name"), doc.get("server"))
                for doc in docs]
    return channels

def get_channel(db, channel_id):
    doc = db.collection("channels").document(channel_id).get()
    return Channel(doc.id, doc.get("name"), doc.get("server"))
    
def get_threads(db, channel_id):
    docs = db.collection("threads").where(
        "channel", "==", channel_id).order_by("created_at", direction="DESCENDING").stream()
    threads = [Thread(doc.id, doc.get("name"), doc.get("channel"))
               for doc in docs]
    return threads