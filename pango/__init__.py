from djamago import *
from pyoload import *

from . import expressions
from .topics.faq import Faq
from .topics.main import Main
from .topics.markdown import Markdown


class Pango(Djamago):
    INSTANCES = {}

    @classmethod
    @annotate
    def from_username(cls, name: str) -> "Pango":
        if name not in cls.INSTANCES:
            cls.INSTANCES[name] = Pango(name)
        return cls.INSTANCES[name]

    def __init__(self, name):
        super().__init__("pango", Node(
            parent=None,
            query="",
            raw_query="",
            response="",
            topics=(
                (100, "faq"),
                (70, "main"),
            ),
        ))
        self.username = name


@annotate
def query(username: str, query: str) -> str:
    conv = Pango.from_username(username)
    try:
        open("pango/conversations.log", "a").write(
            username + "\n" + pango.quote(query) + "\n",
        )
    except Exception:
        pass

    return conv.respond(query).response


Pango.topic(Main)
Pango.topic(Markdown)
Pango.topic(Faq)
