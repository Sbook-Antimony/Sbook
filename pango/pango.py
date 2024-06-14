from pyoload import *
import time
import uuid
import sbook.accounts
import difflib

try:
    from . import chatbot
    pango = chatbot.Chat(default_template='pango/pango.tmpl')
except ImportError:
    import chatbot
    pango = chatbot.Chat(default_template='pango.tmpl')


scope = {}


def quote(txt):
    fl, *lns = txt.splitlines()
    ret = "> " + fl
    for ln in lns:
        ret += "\n  " + ln
    return ret


@chatbot.register_call("callMe")
def call_me(query, session_id="general"):
    scope['name'] = query
    return "Ok, "


@chatbot.register_call("whoIs")
def who_is(query, session_id="general"):
    users = []
    for user in sbook.accounts.User.all():
        s = difflib.SequenceMatcher(
            lambda x: x == " ",
            "private Thread currentThread;",
            "private volatile Thread currentThread;",
        )
        r = s.ratio()
        if len(users) == 0 or r > users[-1][0] and r > 0.5:
            users.append((r, user))
            users.sort(key=lambda u: u[0], reverse=True)
        if r > 0.9:
            break
    if len(users) == 0:
        return f"**Sorry** I cannot find {query}, are you sure he exists?"
    elif len(users) == 1 or users[0][0] - 0.2 > users[1][0]:
        user = users[0][1]
        return (
            f"Yeah you mean @user:{user.model.username}, his bio says:\n\n"
            + quote(user.model.bio)
        )



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
