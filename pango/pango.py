from pyoload import *
import time
import uuid

try:
    from . import chatbot
    pango = chatbot.Chat(default_template='pango/pango.tmpl')
except ImportError:
    import chatbot
    pango = chatbot.Chat(default_template='pango.tmpl')


scope = {}


@chatbot.register_call("callMe")
def call_me(query, session_id="general"):
    scope['name'] = query
    return "Ok, "


@annotate
class Conversation:
    id: str = "general"
    writing: bool = False
    output: str = ""
    instances = {}
    last_active: float

    @classmethod
    def from_username(cls, username):
        if username not in cls.instances:
            cls.instances[username] = cls(username)
        return cls.instances[username]

    @classmethod
    def filter(cls):
        names = list(cls.instances.keys())
        t = time.perf_counter()
        mt = 1000 * 60 * 60
        mint = t - mt
        for name in names:
            if cls.instances[name].last_active < mint:
                del cls.instances[name]

    def __init__(self, username):
        self.last_active = time.perf_counter()
        self.id = username
        pango.start_new_session(username)

    def answer(self, text):
        if text == "quit":
            del self
            return
        pango.conversation[self.id].append(text)
        while text[-1] in "!.":
            text = text[:-1]
        pango.conversation[self.id].append(
            pango.respond(text, session_id=self.id),
        )
        return pango.conversation[self.id][-1]


def main():
    c = Conversation("ken-morel")
    while True:
        print(c.answer(input("> ")))


if __name__ == '__main__':
    main()
