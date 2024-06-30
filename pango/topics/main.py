import difflib
import random

from djamago import Callback
from djamago import Expression
from djamago import RegEx
from djamago import Topic, Evaluator
import faqs

try:
    import sbook.accounts
except Exception:
    pass

from . import quote
import faqs


class Main(Topic):
    """@Callback([
        (100, Evaluator(lambda node: (10, {})))
    ])
    def here(node, id, var):
        node.topics = (
            (100, 'main'),
        )
        node.response = random.choice([
            "You used an Evaluator"
        ])"""

    @Callback([
        (100, Expression("askingMyname"))
    ])
    def call_me(node):
        node.topics = (
            # (100, 'pango'),
            (70, 'main'),
        )
        node.response = random.choice([
            "Hy, I am pango"
        ])

    @Callback([
        (100, Expression("whoMadeMe"))
    ])
    def whomademe(node):
        node.topics = (
            (100, 'markdown'),
            (70, 'main'),
        )
        node.response = random.choice([
            (
                "I am trained by you, and your queries,"
                " but I was programmed by @ken-morel;"
            ),
        ])

    @Callback([
        (100, Expression("greetings"))
    ])
    def greetings(node):
        node.topics = (
            (100, 'main'),
            (100, "faq"),
        )
        node.response = random.choice([
            "Yeah, how are you?",
            "Good day!",
            "Greetings"
        ])

    @Callback([
        (100, Expression("username"))
    ])
    def user_name(node):
        node.topics = (
            (100, 'main'),
            (70, "faq"),
        )
        node.response = random.choice([
            (
                "I am pango, but you... I don not know,"
                " don not tell me, I won't remember it yet"
            )
        ])

    @Callback([
        (100, Expression("aboutAUser(name)"))
    ])
    def aboutAUser(node):
        users = []
        name = node.vars["name"]
        for user in sbook.accounts.User.all():
            r = max(
                difflib.SequenceMatcher(
                    lambda x: x == " -._",
                    name,
                    user.model.name,
                ).ratio(),
                difflib.SequenceMatcher(
                    lambda x: x == " -._",
                    name,
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
            node.response = (
                f"**Sorry** I cannot find {name},"
                " are you sure so exists?"
            )
        elif len(users) == 1 or users[0][0] - 0.2 > users[1][0]:
            user = users[0][1]
            node.response = (
                f"Yeah you mean @{user.model.username};, his bio says:\n\n"
                + quote(
                    user.model.bio
                )
            )
        node.topics = ((100, "main"), (100, "faq"))
