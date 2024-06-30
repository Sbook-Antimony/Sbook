"""
djamago is a python library which will help you create simple chatbots
the simple way. It uses regular expressions to match queries and
provide a response with the best match
"""

import math
import re
import random

import collections

from pyoload import *
from typing import Callable

# from .contrib.spellcheck.correction import correction as text_correction
try:
    import nltk
except:
    USE_NLTK = False
else:
    USE_NLTK = True

TopicList = list[tuple[int | float, str]] | tuple[tuple[int | float, str]]


@annotate
class Pattern:
    def __init__(*_, **__):
        raise NotImplementedError()


@annotate
class Evaluator(Pattern):
    def __init__(self, func):
        self.__func__ = func

    def check(
        self, node: "Node"
    ) -> tuple[int | float, int, dict[str | re.Pattern, str]]:
        val, var = self.__func__(node)
        return (
            val,
            {
                "callback_pattern_evaluator": self,
            },
            var,
        )


@annotate
class RegEx(Pattern):
    """
    Provides the base for regex pattern matching
    """

    @multimethod
    def __init__(self: Pattern, regex: list[tuple[float | int, str]]):
        """
        Initializes a new Regular expression as Pattern
        :param regex: a list of tuples (score, regular expression)
        which will be used to match
        """
        scores, res = zip(*regexs)
        res = map(re.compile, res)
        self.regexs = tuple(zip(res, scores))

    @multimethod
    def __init__(self: Pattern, regex: str, score: int | float = 100.0):
        """
        Initializes a new Regular expression as Pattern
        :param regex: the regex
        which will be used to match
        """
        pattern = re.compile(regex)
        self.regexs = [(score, pattern)]

    def check(self: "RegEx", node: "Node") -> tuple[int | float, dict, dict]:
        """
        Compares all the RegEx's stored on initialization to the string
        and if matching, returns the score and match object associated

        :param txt: The string to test
        :returns: A tuple (score, match Object)
        """
        ms = []
        for id, (score, regex) in enumerate(self.regexs):
            if m := regex.search(node.query):
                ms.append(
                    (
                        score,
                        {
                            "callback_pattern_regex_id": id,
                        },
                        {
                            "match": m,
                        },
                    )
                )
        if len(ms) > 0:
            ms.sort(key=lambda m: m[0], reverse=True)
            return ms[0]
        else:
            return [(0, {}, {})]


@annotate
class Expression(Pattern):
    """
    Expression class to create a new expression, in the form

    """

    ENTRIES: dict[str, list[tuple]] = {}

    @classmethod
    @annotate
    def register(
        cls,
        name: str,
        vals: list[tuple[float | int, str]],
    ) -> None:
        """
        Registers a new expression
        :param name: The name under which to register the expression
        :param vals: a list of tuples in the form (score, regex)
        """
        cls.ENTRIES[name] = [(score, re.compile(txt)) for score, txt in vals]

    @staticmethod
    def parse(
        string: str,
    ) -> tuple[str | re.Pattern, int | float, tuple | re.Pattern]:
        """
        Expression.parses the passed Expression into tuples of (call, args)
        :param string: The string to Expression.parse

        :returns: The Expression.parsed expression tuple
        """
        global indent
        name = ""
        has_args = True
        i = 0
        while i < len(string):
            c = string[i]
            if c.isalnum() or c == ":":
                name += c
                i += 1
            else:
                break
        else:
            has_args = False
        if ":" in name:
            name, score = name.rsplit(":", 1)
            score = int(score)
        else:
            score = 100
        if not has_args:
            return (name, score, ())
        i, string = 0, string[i + 1 :]
        args = []
        while i < len(string):
            c = string[i]
            if c == ")":
                break
            elif c == '"':  # A string argument
                sargs = []
                nin = 0
                i += 1
                regex = ""
                while i < len(string):  # collecting string
                    if string[i] == "(":
                        nin += 1
                    elif string[i] == ")":
                        nin -= 1
                    if nin == 0 and string[i] == '"':  # end of string
                        if len(string) > i + 1 and string[i + 1] == ":":
                            # then it is followed by score
                            i += 2  # skip score
                            sscore = ""
                            while i < len(string) and string[i].isnumeric():
                                # next score digit
                                sscore += string[i]
                                i += 1
                            sscore = int(sscore)
                        else:
                            sscore = 100  # no score in expr
                            i += 1
                        if string[i] == "(":
                            scall = ""  # store whole call here
                            snin = 0
                            while i < len(string):
                                if snin == 0 and string[i] == ")":
                                    i += 1
                                    break
                                if string[i] == "(":
                                    snin += 1
                                elif string[i] == ")":
                                    snin -= 1
                                scall += string[i]
                                i += 1
                            sargs = Expression.parse("a" + scall)[2]
                            while i < len(string) and string[i] in ", ":
                                i += 1
                        break
                    else:
                        regex += string[i]
                        i += 1
                args.append((re.compile(regex), sscore, tuple(sargs)))
            elif c.isalpha():  # other call
                call = ""  # store whole call here
                nin = 0
                while i < len(string):
                    if nin == 0 and string[i] == ")":
                        i += 1
                        break
                    if string[i] == "(":
                        nin += 1
                    elif string[i] == ")":
                        nin -= 1
                    call += string[i]
                    i += 1
                args.append(Expression.parse(call))
                while i < len(string) and string[i] in ", ":
                    i += 1
        i -= 1
        return (name, score, tuple(args))

    @classmethod
    @annotate
    def _check(
        cls,
        name: str | re.Pattern,
        nscore,
        params: tuple[tuple | re.Pattern],
        string: str,
    ) -> tuple[int | float, dict, dict[str, str]]:
        tests = []
        if isinstance(name, str):
            try:
                regexs = cls.ENTRIES[name]
            except KeyError:
                raise ValueError(f"Expression {name!r} does not exist")
        elif isinstance(name, re.Pattern):
            regexs = [(100, name)]
        for id, (score, regex) in enumerate(regexs):
            vars = {}
            mat = regex.search(string)
            if not mat:
                continue
            args = mat.groups()
            args = args[: len(params)]
            if len(params) != len(args):
                continue
            match_score = 0
            for param, arg in zip(params, args):
                if isinstance(param, tuple):
                    paramname, paramscore, paramargs = param
                    vars[str(paramname)] = arg
                    pscore, _, pvars = Expression._check(
                        paramname,
                        paramscore,
                        paramargs,
                        arg,
                    )
                    for k, v in pvars.items():
                        vars[paramname + "." + k] = v
                    if pscore == -1:
                        continue
                    else:
                        match_score += pscore / 100 * score
                elif isinstance(param, re.Pattern):
                    if param.search(arg):
                        match_score += 100
                    else:
                        return -1, {}, {}
                else:
                    raise Exception()
            if len(params) == 0:
                match_score = 100
            tests.append(
                (
                    match_score / 100 * nscore,
                    {
                        "sub_pattern_id": id,
                    },
                    vars,
                )
            )

        if len(tests) == 0:
            return (-1, {}, {})
        else:
            tests.sort(key=lambda k: k[0], reverse=True)
            return tests[0]

    def __init__(self, expr: str):
        self.expr = Expression.parse(expr)

    def check(self, node: "Node") -> _check.__annotations__.get("return"):
        return Expression._check(*self.expr, node.query)


class Callback:
    __func__: Callable
    patterns: list[tuple[int | float, Pattern]]

    @overload
    def __init__(self, patterns: "list[tuple[int | float, Pattern]]"):
        self.patterns = patterns

    @overload
    def __init__(self, pattern: Pattern):
        self.patterns = [(100, pattern)]

    @annotate
    def __call__(self, func: Callable) -> "Callback":
        self.__func__ = func
        if hasattr(func, "overload"):
            self.overload = func.overload
        return self

    def __set_name__(self, obj: Type, name: str) -> None:
        obj.register(self)
        self.topic = obj

    def __get__(self, obj: "Topic") -> "Callback":
        return self

    @annotate
    def respond(self, node: "Node") -> None:
        if not hasattr(self, "__func__"):
            raise RuntimeError("Callable not decorated")
        self.__func__(node)

    @annotate
    def check(self, node: "Node") -> "list[tuple[int | float, dict, dict]]":
        matches = []
        for cpid, (pscore, pattern) in enumerate(self.patterns):
            score, param, var = pattern.check(node)
            if score >= 0:
                matches.append(
                    (
                        score / 100 * pscore,
                        param
                        | {
                            "callback_pattern_id": cpid,
                            "callback_pattern": (pscore, pattern),
                        },
                        var,
                    )
                    # (, , self, id, )
                )
        return matches


class Topic:
    _callbacks: list[Callback]
    name: str = None

    @classmethod
    @annotate
    def register(cls, callback: Callback) -> None:
        if not hasattr(cls, "_callbacks"):
            cls._callbacks = []
        cls._callbacks.append(callback)

    @classmethod
    @annotate
    def matches(cls, node: "Node") -> "list[tuple[float | int, dict, dict]]":
        matches = []
        for callback in cls._callbacks:
            for score, params, var in callback.check(node):
                matches.append(
                    (
                        score,
                        params
                        | {
                            "callback": callback,
                            "topic": cls,
                        },
                        var,
                    )
                )
        return matches

    @classmethod
    @annotate
    def respond(cls, node: "Node"):
        node.params["callback"].respond(node)


@overload
def use_nltk() -> bool:
    return USE_NLTK


@overload
def use_nltk(val: bool) -> bool:
    global USE_NLTK
    USE_NLTK = val
    if val:
        import nltk

        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("stopwords")
    return val


Token = list[str]


@annotate
class QA(Topic):
    jaccard_score = 0.5
    cosine_score = 1.5
    difflib_score = 1

    @staticmethod
    @annotate
    def tokenize(text: str) -> Token:
        if use_nltk():
            from nltk.corpus import stopwords
            from nltk.stem import WordNetLemmatizer
            from nltk.tokenize import word_tokenize

            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words("english"))
            tokens = [t for t in tokens if t not in stop_words]  # junk
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(t) for t in tokens]  # singular
            return tokens
        else:
            return text.split(" ")

    @annotate
    def jaccard_similarity(a: Token, b: Token) -> float:
        intersection = set(a) & set(b)
        union = set(a) | set(b)
        return len(intersection) / len(union) * 100

    @annotate
    def cosine_similarity(a: Token, b: Token) -> float:
        a = list(collections.Counter(a).values())
        b = list(collections.Counter(b).values())
        dot_product = sum(av * bv for av, bv in zip(a, b))
        magnitude_a = math.sqrt(sum(av**2 for av in a))
        magnitude_b = math.sqrt(sum(bv**2 for bv in b))
        return dot_product / (magnitude_a * magnitude_b) * 100

    @annotate
    def difflib_similarity(a: Token, b: Token) -> float:
        import difflib

        return (
            difflib.SequenceMatcher(
                lambda x: x == " -._",
                " ".join(a),
                " ".join(b),
            ).ratio()
            * 100
        )

    @annotate
    def levenshtein_distance(a: Token, b: Token) -> int:
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost,
                )
        return dp[m][n]

    @staticmethod
    @overload
    def similarity(a: str, b: str) -> float:
        return QA.similarity(QA.tokenize(a), QA.tokenize(b))

    @staticmethod
    @overload
    def similarity(a: Token, b: str) -> float:
        return QA.similarity(a, QA.tokenize(b))

    @staticmethod
    @overload
    def similarity(a: Token, b: Token) -> float:
        if use_nltk():
            return sum(
                (
                    QA.jaccard_similarity(a, b) * QA.jaccard_score,
                    QA.cosine_similarity(a, b) * QA.cosine_score,
                    QA.difflib_similarity(a, b) * QA.difflib_score,
                )
            ) / sum((QA.jaccard_score, QA.cosine_score, QA.difflib_score))
        else:
            return QA.difflib_similarity(a, b)

    class QA:
        questions: list[float, str]
        answers: list[str]
        tokens: list[tuple[int | float, list[str]]]

        def check(self, node: "Node") -> list[tuple[int | float, dict, dict]]:
            matches = []
            qtoken = QA.tokenize(node.query)
            for id, (score, question, token) in enumerate(self.questions):
                matches.append(
                    (
                        QA.similarity(qtoken, token) / 100 * score,
                        {
                            "qa_qa_question_id": id,
                            "qa_qa": self,
                            "qa_qa_question_question": question,
                        },
                        {
                            "question": question,
                        },
                    )
                )
            return matches

        @annotate
        def respond(self, node: "Node"):
            node.response = random.choice(self.answers)

        @overload
        def __init__(
            self,
            questions: list[tuple[float | int, str]],
            answers: list[str],
        ):
            self.questions = []
            self.answers = answers
            for score, question in questions:
                self.questions.append((score, question, QA.tokenize(question)))

        @overload
        def __init__(self, questions: list[str], answers: list[str]):
            self.questions = []
            self.answers = answers
            for question in questions:
                self.questions.append((100, question, QA.tokenize(question)))

    questions: list[int]

    @classmethod
    @annotate
    def matches(cls, node: "Node") -> list[tuple[int | float, dict, dict]]:
        matches = []
        for qa in cls.QAs:
            for score, param, var in qa.check(node):
                matches.append(
                    (
                        score,
                        param
                        | {
                            "qa": cls,
                            "topic": cls,
                        },
                        var,
                    )
                )
        return matches

    def __init_subclass__(cls):
        if hasattr(cls, "QAs"):
            return
        else:
            cls.QAs = []
        if hasattr(cls, "data"):
            data = cls.data
        elif hasattr(cls, "source_json"):
            import json

            with open(cls.source_json) as f:
                data = json.loads(f.read())
        elif hasattr(cls, "source_yaml"):
            import yaml

            with open(cls.source_yaml) as f:
                data = yaml.safe_load(f.read())
        else:
            data = []
        for questions, answers in data:
            cls.QAs.append(QA.QA(questions, answers))

    @annotate
    @classmethod
    def respond(cls, node: "Node"):
        node.params["qa_qa"].respond(node)
        cls.format_answer(node)

    @staticmethod
    def format_answer(cls, node: "Node"):
        pass


@annotate
class Node:
    __slots__ = (
        "topics",
        "parent",
        "response",
        "query",
        "score",
        "vars",
        "params",
        "raw_query",
    )

    topics: TopicList
    parent: "Node | type(None)"
    response: str
    query: str
    score: int | float
    vars: dict
    params: dict

    def __init__(
        self,
        query: str,
        raw_query: str,
        topics: TopicList = (),
        parent: "Node | type(None)" = None,
        response: str = None,
    ):
        self.topics = topics
        self.parent = parent
        if response is not None:
            self.response = response
        self.query = query
        self.raw_query = raw_query

    def __str__(self):
        return f"<djamado.Node({self.query!r}) -> {self.response!r}>"


@annotate
class Djamago:
    topics: dict[str, Topic]
    nodes: list[Node]
    name: str
    initial_node: Node

    def __init_subclass__(cls):
        cls.topics = {}

    def __init__(self, name: str = "", initial_node=None):
        self.name = name
        self.nodes = [
            initial_node
            or Node(
                topics=tuple(self.topics.keys()),
                parent=None,
                query="",
                raw_query="",
                response="",
            )
        ]

    @unannotable
    @overload
    def respond(self, query: str) -> Node:
        node = Node(
            parent=self.nodes[-1],
            raw_query=query,
            query=query.lower(),
        )
        self.respond_node(node)
        self.nodes.append(node)
        return node

    @unannotable
    @respond.overload
    def respond_node(self, node: Node) -> None:
        matches = []
        for topic in node.parent.topics:
            if isinstance(topic, tuple):
                score, topic = topic
            else:
                score = 100
            matches.extend(
                [
                    (sscore / 100 * score, param, var)
                    for (sscore, param, var) in self.topics.get(topic).matches(node)
                ]
            )
        matches.sort(key=lambda m: m[0], reverse=True)
        if len(matches) == 0:
            raise ValueError("Node did not find any match")
        score, param, var = matches[0]
        node.params = param
        node.vars = var
        node.score = score
        param["topic"].respond(node)

    @classmethod
    def topic(cls, topic: type):
        name = topic.name or topic.__name__.lower()
        cls.topics[name] = topic


__version__ = "0.0.1"
