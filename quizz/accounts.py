import functools
import io

import json
import textwrap

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sbook.accounts import DIR

import profile_images
import sbook.accounts
import sbook.models

from quizz import models

from PIL import Image
from pathlib import Path


class Tuple(tuple):
    @property
    def length(self):
        return len(self)


class QuizzUserDoesNotExistError(ValueError):
    pass
class QuizzUserDoesExistError(ValueError):
    pass
class QuizzUser():
    model:models.QuizzUser

    @classmethod
    def from_id(cls, id):
        try:
            found = sbook.models.User.objects.get(id=id).quizzAccount.all()[0]
        except IndexError as e:
            raise NoteUserDoesNotExistError() from e
        else:
            return cls(found)


    @classmethod
    def create_from_sbook(cls, sbook):
        try:
            obj = models.QuizzUser(sbookAccount=sbook.model)
            obj.save()
        except Exception as e:
            raise QuizzUserDoesExistError() from e
        else:
            return cls(obj)

    def __init__(self, model=None):
        if model is None:
            raise QuizzUserDoesNotExistError()
        self.model = model

    @functools.cached_property
    def sbookAccount(self):
        return sbook.accounts.User(
            self.model.sbookAccount,
        )

    @functools.cached_property
    def stars(self):
        return self.model.stars

    @functools.cached_property
    def starred(self):
        return self.model.starred

    @functools.cached_property
    def id(self):
        return self.sbookAccount.id

    @functools.cached_property
    def name(self):
        return self.sbookAccount.name

    @functools.cached_property
    def quizzes(self):
        return Tuple(map(Quizz, self.model.quizzes.all()))

    @functools.cached_property
    def hasQuizzes(self):
        return len(self.quizzes) > 0

    @functools.cached_property
    def quizz_attempts(self):
        return Tuple(map(QuizzAttempt, self.model.quizz_attempts.all()))


class Question:
    @classmethod
    def from_dict(cls, js, i):
        return MCQQuestion(js, i)


class MCQQuestion(Question):
    mode = 'mcq'

    def __init__(self, data, id=0):
        self.question = data.get('question')
        self.options = data.get('options', {}).items()
        self.answer = data.get('answer')
        self.id = id

    def js(self):
        return {
            'question': self.question,
            'options': self.options,
        }

    def json(self):
        return json.dumps(self.js)


class QuizzDoesNotExistError(ValueError):
    pass


class QuizzDoesExistError(ValueError):
    pass


class Quizz:
    @classmethod
    def from_id(cls, id):
        try:
            found = models.Quizz.objects.get(id=id)
        except models.Quizz.DoesNotExist as e:
            raise QuizzDoesNotExistError() from e
        else:
            return cls(found)

    def __init__(self, model=None):
        if model is None:
            raise QuizzDoesNotExistError()
        self.model = model
        self.data = model.data

    @functools.cached_property
    def id(self):
        return self.model.id

    @functools.cached_property
    def title(self):
        return self.model.title

    @functools.cached_property
    def views(self):
        return self.model.views

    @functools.cached_property
    def stars(self):
        return self.model.stars

    @functools.cached_property
    def starred(self):
        return self.model.starred

    @functools.cached_property
    def redactors(self):
        return tuple(map(QuizzUser, self.model.redactors.all()))

    @functools.cached_property
    def description(self):
        return self.model.description

    @functools.cached_property
    def short_description(self):
        return textwrap.shorten(self.description, 30)

    @functools.cached_property
    def profile(self):
        return Image.open(
            self.profile_path,
        )

    @functools.cached_property
    def profile_path(self):
        return Path(self.model.profile.path)

    @functools.cached_property
    def profile_asBytes(self):
        buffer = io.BytesIO()
        self.profile.save(buffer, format='PNG')
        return buffer.getvalue()

    @property
    def js(self):
        return {
            "title": self.title,
            "id": self.id,
            "views": self.views,
            "stars": float(self.stars),
            "profile": f'/note/notes/{self.id}/profile.png',
            "path": f'/note/notes/{self.id}/',
            "description": self.description,
            "color": profile_images.average_color(self.profile),
        }

    @functools.cached_property
    def questions(self):
        return tuple(
            Question.from_dict(data, i)
            for i, data in enumerate(self.data.get('questions', []))
        )

    @functools.cached_property
    def questions_js(self):
        return tuple(ques.js for ques in self.questions)

    @property
    def json(self, indent=4):
        return json.dumps(self.js, indent=indent)

    @functools.cached_property
    def instructions(self):
        return self.data.get('instructions')

    @functools.cached_property
    def epilog(self):
        return self.data.get('epilog')

    @functools.cached_property
    def prolog(self):
        return self.data.get('prolog')

    @functools.cached_property
    def attempts(self):
        return tuple(map(QuizzAttempt, self.model.answer_attempts.all()))

    @functools.cached_property
    def num_attempts(self):
        return len(self.attempts)

    @functools.cached_property
    def num_attempts_remarked(self):
        i = 0
        for attempt in self.attempts:
            if attempt.model.remarked:
                i += 1
        return i

    @property
    def num_attempts_unremarked(self):
        return self.num_attempts - self.num_attempts_remarked

    @property
    def attempts_remark_status(self):
        if self.num_attempts == 0 or self.num_attempts_unremarked == 0:
            return 2
        elif self.num_attempts_remarked == 0:
            return 0
        else:
            return 1

    @functools.cached_property
    def on_submit(self):
        return self.data.get(
            'on_submit',
            '''Thanks for answering, stydy well!''',
        )


class QuestionAttempt:
    @classmethod
    def from_dict(cls, js, i, a):
        ques = Question.from_dict(js, i)
        return MCQQuestionAttempt(ques, a)

    @classmethod
    def from_question(cls, ques, a):
        print(ques, a)
        return MCQQuestionAttempt(ques, a)


class MCQQuestionAttempt(QuestionAttempt):
    mode = 'mcq'

    def __init__(self, question, ans):
        print(question, ans)
        self.answer = ans
        self.question = question


class QuizzAttemptDoesNotExistError(ValueError):
    pass


class QuizzAttemptDoesExistError(ValueError):
    pass


class QuizzAttempt:
    @classmethod
    def create(cls, author, quizz, answers):
        model = models.QuizzAttempt(
            answers=answers,
            author=author.model,
            quizz=quizz.model,
        )
        model.save()
        return cls(model)

    @classmethod
    def from_id(cls, id):
        try:
            found = models.QuizzAttempt.objects.get(id=id)
        except models.QuizzAttempt.DoesNotExist as e:
            raise QuizzAttemptDoesNotExistError() from e
        else:
            return cls(found)

    def __init__(self, model=None):
        if model is None:
            raise QuizzAttemptDoesNotExistError()
        self.model = model

    @functools.cached_property
    def author(self):
        return QuizzUser(self.model.author)

    @functools.cached_property
    def quizz(self):
        return Quizz(self.model.quizz)

    @functools.cached_property
    def answers(self):
        ret = tuple(
            QuestionAttempt.from_question(
                self.quizz.questions[i], a
            )
            for i, a in enumerate(self.model.answers)
        )
        return ret

    @functools.cached_property
    def id(self):
        return self.model.id


def check_login(func, redirect=True):
    if isinstance(func, bool):
        return functools.partial(
            check_login,
            redirect=func,
        )

    @functools.wraps(func)
    def wrapper(*args, **kw):
        req = args[0]
        if not isinstance(req, HttpRequest):
            req = args[1]
        if "user-id" in req.session:
            try:
                user = QuizzUser.from_id(req.session.get("user-id", -1))
            except QuizzUserDoesNotExistError:
                if not redirect:
                    return func(user=None, *args,**kw)
                return HttpResponseRedirect('/signin/')
            except QuizzUserDoesNotExistError:
                user = QuizzUser.create_from_sbook(
                    sbook.accounts.User.from_id(req.session.get("user-id")),
                )
            return func(user=user, *args,**kw)
        else:
            if not redirect:
                return func(user=None, *args,**kw)
            return HttpResponseRedirect('/signin/')
    return wrapper
