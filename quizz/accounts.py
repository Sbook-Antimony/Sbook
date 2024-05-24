import functools
import io

import json

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sbook.accounts import ACCOUNTS
from sbook.accounts import DIR

import profile_images
import sbook.accounts
import sbook.models

from quizz import models

from PIL import Image
from pathlib import Path


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
            raise NoteUserDoesExistError() from e
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
        return tuple(map(Quizz, self.model.quizzes.all()))

    @functools.cached_property
    def hasQuizzes(self):
        return len(self.quizzes) > 0


class Question:
    @classmethod
    def from_dict(cls, js):
        return MCQQuestion(js)


class MCQQuestion(Question):
    def __init__(self, data):
        self.question = data.get('question')
        self.options = data.get('options')
        self.answer = data.get('answer')

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
            "title"      : self.title,
            "id"         : self.id   ,
            "views"      : self.views,
            "stars"      : float(self.stars),
            "profile"    : f'/note/notes/{self.id}/profile.png',
            "path"       : f'/note/notes/{self.id}/',
            "description": self.description,
            "color"      : profile_images.average_color(self.profile),
        }

    @functools.cached_property
    def questions(self):
        return tuple(Question.from_dict(data) for data in self.model.data['questions'])

    @functools.cached_property
    def questions_js(self):
        return tuple(ques.js for ques in self.questions)

    @property
    def json(self, indent=4):
        return json.dumps(self.js, indent=indent)

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
