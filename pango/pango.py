from pyoload import *
import time
import random
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
def call_me(query, session_id="you"):
    scope['name'] = query
    return "Ok, "


@chatbot.register_call("you")
def get_name(q, session_id="you"):
    conv = Conversation.instances.get(session_id)
    return conv.user.model.name if conv is not None else "you"


@chatbot.register_call("whoIs")
def who_is(query, session_id="general"):
    users = []
    for user in sbook.accounts.User.all():
        r = max(
            difflib.SequenceMatcher(
                lambda x: x == " -._",
                query,
                user.model.name,
            ).ratio(),
            difflib.SequenceMatcher(
                lambda x: x == " -._",
                query,
                user.model.username,
            ).ratio(),
        )
        if r > 0.5 and (len(users) == 0 or r > users[-1][0]):
            users.append((r, user))
            users.sort(key=lambda u: u[0], reverse=True)
        if r > 0.9:
            users = [(r, user)]
            break
    if len(users) == 0:
        return f"**Sorry** I cannot find {query}, are you sure so exists?"
    elif len(users) == 1 or users[0][0] - 0.2 > users[1][0]:
        user = users[0][1]
        return (
            f"Yeah you mean @user:{user.model.username}, his bio says:\n\n"
            + quote(user.model.bio)
        )


@chatbot.register_call("note_doc")
def notedocs(query, session_id="general"):
    return note_doc


@chatbot.register_call("note_tip")
def notetip(query, session_id="general"):
    return random.choice(note_tips)


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
        try:
            self.user = sbook.accounts.User.get(username=username)
        except sbook.accounts.User.DoesExistError:
            self.user = None
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


note_doc = """\
Here is an example of markdown code for a documentation that guides users on
using the markdown syntax in Note:

**Markdown Syntax**
--------------------

### Headers

To create a header, use the `#` symbol followed by the header text.

```
# Heading 1
## Heading 2
### Heading 3
```

### Bold and Italic Text

To create bold text, surround the text with `**` symbols.

```
**This text will be bold**
```

To create italic text, surround the text with `*` symbols.

```
*This text will be italic*
```

### Lists

To create an unordered list, use the `*` symbol followed by the list item.

```
* Item 1
* Item 2
* Item 3
```

To create an ordered list, use the `1.` symbol followed by the list item.

```
1. Item 1
2. Item 2
3. Item 3
```

### Mentions

To mention another user, use the `@` symbol followed by the username.

```
@johnDoe
```

This will create a link to the user's profile.

### Example Usage

Here is an example of how you can use the markdown syntax in Note:

```
# Welcome to Note!

This is an **example** of a note that mentions another user.

I would like to thank @johnDoe for his contribution to this project.

Here is a list of items:

* Item 1
* Item 2 @janeDoe
* Item 3

Best,
@antimonyTeam
```

This documentation will be updated regularly to include more features and
examples of the markdown syntax in Note. If you have any questions or need
further assistance, please don't hesitate to ask.

**Happy Writing!**
"""


note_tips = [
    "#Tip\nUse `*` to quote italic texts\ne.g `*hello*` -> *hello*",
    "#Tip\nUse `**` to quote bold texts\ne.g `**hello**` -> **hello**",
    "#Tip\nAdd images with `![image replacement](image url)`",
    "#Tip\nMention users with `@user:{username}` syntax",
]
