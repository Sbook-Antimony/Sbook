import functools
import io

import json

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sbook.settings import BASE_DIR as DIR

import profile_images
import sbook.accounts as sbook
import sbook.models

from . import models
from sbook.accounts import ModelInter, User

NOTES = DIR / "notes"

from PIL import Image


class BookmarkDoesNotExistError(ValueError):
    pass


class BookmarkDoesExistError(ValueError):
    pass


class Bookmark(ModelInter):
    model: models.NoteUser = models.Bookmark

    class DoesNotExistError(ValueError):
        pass

    class DoesExistError(ValueError):
        pass

    @functools.cached_property
    def stars(self):
        return self.model.stars

    @functools.cached_property
    def note(self):
        return self.model.note

    @functools.cached_property
    def author(self):
        return self.author


class NoteUser(ModelInter):
    model: models.NoteUser = models.NoteUser
    parent = User

    class DoesNotExistError(ValueError):
        pass

    class DoesExistError(ValueError):
        pass

    @classmethod
    def from_id(cls, id):
        try:
            found = sbook.models.User.objects.get(id=id).noteAccount.all()[0]
        except IndexError as e:
            raise NoteUser.DoesNotExistError() from e
        else:
            return cls(found)

    @classmethod
    def from_note_id(cls, id):
        try:
            found = models.NoteUser.objects.get(id=id)
        except models.NoteUser.DoesNotExist as e:
            raise NoteUser.DoesNotExistError() from e
        else:
            return cls(found)

    @classmethod
    def create_from_sbook(cls, sbook):
        try:
            obj = models.NoteUser(sbookAccount=sbook.model)
            obj.save()
        except Exception as e:
            raise NoteUser.DoesExistError() from e
        else:
            return cls(obj)

    @classmethod
    def fromParent(cls, parent):
        return cls.get(sbookAccount__id=parent.id)

    def __init__(self, model=None):
        if model is None:
            raise NoteUser.DoesNotExistError()
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
        return self.sbookAccount.model.id

    @functools.cached_property
    def name(self):
        return self.sbookAccount.model.name

    @functools.cached_property
    def bookmarks(self):
        return tuple(map(Bookmark, self.model.bookmarks.all()))

    @functools.cached_property
    def hasBookmarks(self):
        return len(self.bookmarks) > 0

    @functools.cached_property
    def notes(self):
        return tuple(map(Note, self.model.notes.all()))

    @functools.cached_property
    def hasNotes(self):
        return len(self.notes) > 0


class Note(ModelInter):
    model = models.Note

    class DoesNotExistError(ValueError):
        pass

    class DoesExistError(ValueError):
        pass

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
        return tuple(map(NoteUser, self.model.redactors.all()))

    @functools.cached_property
    def description(self):
        return self.model.description

    @functools.cached_property
    def profile_path(self):
        print(dir(self.model.profile))
        return self.model.profile.path

    @property
    def js(self):
        return {
            "title": self.title,
            "id": self.id,
            "views": self.views,
            "stars": float(self.stars),
            "profile": f"/note/notes/{self.id}/profile.png",
            "path": f"/note/notes/{self.id}/",
            "description": self.description,
            "color": profile_images.average_color(self.profile),
        }

    @property
    def json(self, indent=4):
        return json.dumps(self.js, indent=indent)


class ShortNote(ModelInter):
    class DoesNotExist(ValueError):
        pass

    class DoesExist(ValueError):
        pass

    model = models.ShortNote

    @classmethod
    def create(cls, title, author, content=""):
        model = cls.model(
            title=title,
            author=author,
            content=content,
        )
        model.save()

    def __init__(self, model=None):
        if model is None:
            raise NoteDoesNotExistError()
        self.model = model

    @functools.cached_property
    def author(self):
        return NoteUser(self.model.author)

    @property
    def js(self):
        return {
            "title": self.model.title,
            "id": self.model.id,
            "description": self.model.description,
            "content": self.model.content,
            "author": self.author.js,
        }


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
        uid = req.session.get("user-id")
        try:
            assert uid is not None
            user = NoteUser.from_id(uid)
        except (Note.DoesNotExistError, User.DoesNotExistError, AssertionError):
            if not redirect:
                return func(user=None, *args, **kw)
            return HttpResponseRedirect("/signin/")
        except NoteUser.DoesNotExistError:
            user = NoteUser.create_from_sbook(
                sbook.accounts.User.from_id(req.session.get("user-id")),
            )
        return func(user=user, *args, **kw)

    return wrapper
