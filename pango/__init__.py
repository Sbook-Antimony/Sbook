from . import pango
from pyoload import *


@annotate
def query(username: str, query: str) -> str:
    conv = pango.Conversation.from_username(username)
    try:
        open("pango/conversations.log", "a").write(
            username + "\n" + pango.quote(query) + "\n",
        )
    except Exception:
        pass
    return conv.answer(query)
