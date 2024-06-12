import io

from PIL import Image
from pathlib import Path

import django.http
import requests

from password_strength import PasswordPolicy
from sbook import settings

import functools

from django.http import HttpResponseRedirect

import markdown

from chatty import accounts as chatty
from note import accounts as note
from pyoload import *
from sbook import models


def parse_recaptcha_token(token):
    """ """
    try:
        return requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET, "response": token},
        ).json()
    except Exception:
        return {
            "success": False,
        }


DIR = Path(__file__).parent.parent

password_policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters
    entropybits=30,
)


def check_login(func, redirect=True):
    if isinstance(func, bool):
        return functools.partial(
            check_login,
            redirect=func,
        )

    @functools.wraps(func)
    def wrapper(*args, **kw):
        req = args[0]
        if not isinstance(req, django.http.HttpRequest):
            req = args[1]
        if "user-id" in req.session:
            try:
                user = User.from_id(req.session.get("user-id", -1))
            except User.DoesNotExistError:
                if not redirect:
                    return func(user=None, *args, **kw)
                return HttpResponseRedirect("/signin")
            else:
                return func(user=user, *args, **kw)
        else:
            if not redirect:
                return func(user=None, *args, **kw)
            return HttpResponseRedirect("/signin")

    return wrapper


##########################################

class ModelInder:
    __pyod_norecur__ = True

    @classmethod
    def __init_subclass__(cls):
        cls.__pyod_norecur__ = True
        annotate(cls)

    @classmethod
    def from_id(cls, id):
        try:
            found = cls.model.objects.get(id=id)
        except cls.model.DoesNotExist as e:
            raise cls.DoesNotExistError() from e
        else:
            return cls(found)

    @classmethod
    def exists(cls, **kw):
        try:
            cls.model.objects.get(**kw)
        except cls.model.DoesNotExist:
            return False
        else:
            return True

    @staticmethod
    def all(cls):
        return map(cls, cls.model.objects.all())

    def __init__(self, model):
        self.model = model

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
        self.profile.save(buffer, format="PNG")
        return buffer.getvalue()

    @functools.cached_property
    def js(self):
        raise NotImplementedError()

    @property
    def id(self):
        return self.model.id


class User(ModelInder):
    model = models.User

    class DoesNotExistError(ValueError):
        pass

    class DoesExistError(ValueError):
        pass

    @classmethod
    def from_login(cls, email, password):
        try:
            found = models.User.objects.get(email=email, password=password)
        except models.User.DoesNotExist as e:
            raise User.DoesNotExistError() from e
        else:
            return cls(found)

    @classmethod
    def create_from_login(cls, name, email, password):
        try:
            print("creating user")
            obj = models.User(
                name=name,
                email=email,
                password=password,
            )
            print("created.. \nnow saving")
            obj.save()
            print("creating data launch")
        except models.User.DoesNotExist as e:
            raise User.DoesExistError() from e
        else:
            return cls(obj)

    @functools.cached_property
    def js(self):
        print(dir(self.model.bio))
        return {
            "name": self.model.name,
            "bio": self.model.bio,
            "bio_html": markdown.markdown(self.model.bio),
            "id": self.model.id,
            "email": self.model.email,
        }

    @functools.cached_property
    def chattyAccount(self):
        cha = self.model.chattyAccount.all()
        if len(cha) == 0:
            cha = [chatty.accounts.ChattyUser.create_from_sbook(self.model)]
            # raise chatty.accounts.UserDoesNotExistError()
        return chatty.accounts.ChattyUser(cha[0])

    @functools.cached_property
    def noteAccount(self):
        cha = self.model.noteAccount.all()
        if len(cha) == 0:
            raise note.UserDoesNotExistError()
        return note.ChattyUser(cha[0])


class Classifier(ModelInder):
    def js(self):
        return {
            'type': self.__class__.__name__.lower(),
            'id': self.model.id,
            'description': self.model.description,
        } | self.js_spec()


class Serie(Classifier):
    model = models.Serie

    def js_spec(self):
        return {}


class Level(Classifier):
    model = models.Level

    def js_spec(self):
        return {
            'series': [
                serie.id for serie in self.model.series.all()
            ]
        }


class Course(Classifier):
    model = models.Course

    def js_spec(self):
        return {
            'series': [
                serie.id for serie in self.model.series.all()
            ],
            'levels': [
                level.id for level in self.model.levels.all()
            ]
        }


class Topic(Classifier):
    model = models.Topic

    def js_spec(self):
        return {
            'courses': [
                course.id for course in self.model.courses.all()
            ]
        }
