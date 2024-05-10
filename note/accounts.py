import functools

from django.http import HttpRequest, HttpResponseRedirect, HttpResponse

from note import models
import sbook.models
import sbook.accounts


class NoteUserDoesNotExistError(ValueError):
    pass
class NoteUserDoesExistError(ValueError):
    pass
class NoteUser():
    model:models.NoteUser

    @classmethod
    def from_id(cls, id):
        try:
            found = sbook.models.User.objects.get(id=id).noteAccount.all()[0]
        except (sbook.models.User.DoesNotExist, IndexError) as e:
            raise NoteUserDoesNotExistError() from e
        else:
            return found
    def from_note_id(cls, id):
        try:
            found = models.NoteUser.objects.get(id=id)
        except models.NoteUser.DoesNotExist as e:
            raise NoteUserDoesNotExistError() from e
        else:
            return cls(found)
  
    @staticmethod
    def create_from_sbook(cls, sbook):
        try:
            obj = models.NoteUser(sbookAccount=sbook)
            obj.save()
        except Exception as e:
            raise NoteUserDoesExistError() from e
        else:
            return cls(obj)

    def __init__(self, model=None):
        if model is None:
            raise ChattyUserDoesNotExistError()
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
    def chatty_id(self):
        return self.model.id

    @functools.cached_property
    def name(self):
        return self.sbookAccount.name

    @functools.cached_property
    def rooms(self):
        return [ChattyRoom(x) for x in self.model.rooms.all()]


class NoteDoesNotExistError(ValueError):
    pass
class NoteDoesExistError(ValueError):
    pass
class Note:
    @classmethod
    def from_id(cls, id):
        try:
            found = models.Note.objects.get(id=id)
        except models.Note.DoesNotExist as e:
            raise NoteDoesNotExistError() from e
        else:
            return cls(found)
    @classmethod
    def create(cls, title, author):
        model = models.Note(
            title=title,
            redactors=[author],
        
        )
    def __init__(self, model=None):
        if model is None:
            raise NoteDoesNotExistError()
        self.model = model
        self.directory = DIR / "notes" / str(model.id)

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
        return tuple(map(NoteUser, self.model.redactors.all()))


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
                user = NoteUser.from_id(req.session.get("user-id", -1))
            except NoteUserDoesNotExistError:
                if not redirect:
                    return func(user=None, *args,**kw)
                return HttpResponseRedirect('/signin/')
            else:
                return func(user=user, *args,**kw)
        else:
            if not redirect:
                return func(user=None, *args,**kw)
            return HttpResponseRedirect('/signin')
    return wrapper
