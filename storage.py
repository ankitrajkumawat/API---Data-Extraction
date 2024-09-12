
storage = {}


def store_content(chat_id: str, content: str):
    storage[chat_id] = content


def get_content_by_id(chat_id: str) -> str:
    return storage.get(chat_id)
