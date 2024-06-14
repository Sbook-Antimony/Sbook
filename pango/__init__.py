from . import pango
from pyoload import *


@annotate
def query(username: str, query: str) -> str:
    conv = pango.Conversation.from_username(username)
    return conv.answer(query)
