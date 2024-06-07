import io

from PIL import Image
from pathlib import Path

import django.http
import yaml

import profile_images
import requests

from password_strength import PasswordPolicy
from sbook import settings

import functools

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from chatty import accounts as chatty
from note import accounts as note
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
ACCOUNTS = DIR / "accounts"

assert ACCOUNTS.exists(), f"accounts folder {ACCOUNTS!r} does not exists"


password_policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters
    entropybits=30,
)


class UserDoesNotExistError(ValueError):
    pass


class UserDoesExistError(ValueError):
    pass


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
            except UserDoesNotExistError:
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


class User:
    model: models.User

    @staticmethod
    def exists(**kw):
        try:
            models.User.objects.get(**kw)
        except models.User.DoesNotExist:
            return False
        else:
            return True

    @classmethod
    def from_id(cls, id):
        try:
            found = models.User.objects.get(id=id)
        except models.User.DoesNotExist as e:
            raise UserDoesNotExistError() from e
        else:
            return cls(found)

    @classmethod
    def from_login(cls, email, password):
        try:
            found = models.User.objects.get(email=email, password=password)
        except models.User.DoesNotExist as e:
            raise UserDoesNotExistError() from e
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
                profile=profile_images.random_profile(),
            )
            print("created.. \nnow saving")
            obj.save()
            print("creating data launch")
        except models.User.DoesNotExist as e:
            raise UserDoesExistError() from e
        else:
            return cls(obj)

    def __init__(self, model=None):
        if model is None:
            raise UserDoesNotExistError()
        self.model = model
        self.directory = ACCOUNTS / str(self.id)

    @functools.cached_property
    def id(self):
        return self.model.id

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
    def name(self):
        return self.model.name

    @functools.cached_property
    def js(self):
        return {
            "name": self.model.name,
            "id": self.model.id,
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

    DEFAULT_PROFILE_PATH = DIR / "image/default-photo.png"
    name: tuple
    password: str
    data: dict
    folder: Path
    id: int
