import functools

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

from chatty import models
import sbook.models
import sbook.accounts


class ChattyUserDoesNotExistError(ValueError):
    pass
class ChattyUserDoesExistError(ValueError):
    pass
class ChattyUser():
    model:models.ChattyUser

    @classmethod
    def from_id(cls, id):
        try:
            found = sbook.models.User.objects.get(id=id)
        except sbook.models.User.DoesNotExist as e:
            raise ChattyUserDoesNotExistError() from e
        else:
            return found.chattyAccount
    def from_chatty_id(cls, id):
        try:
            found = models.ChattyUser.objects.get(id=id)
        except models.ChattyUser.DoesNotExist as e:
            raise ChattyUserDoesNotExistError() from e
        else:
            return cls(found)

    @staticmethod
    def create_from_sbook(cls, sbook):
        try:
            obj = models.ChattyUser(sbookAccount=sbook)
            obj.save()
        except Exception as e:
            raise ChattyUserDoesExistError() from e
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
    def id(self):
        return self.sbookAccount.id

    @functools.cached_property
    def note_id(self):
        return self.model.id

    @functools.cached_property
    def name(self):
        return self.sbookAccount.name

    @functools.cached_property
    def email(self):
        return self.sbookAccount.email


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
                user = ChattyUser.from_id(req.session.get("user-id", -1))
            except ChattyUserDoesNotExistError:
                if not redirect:
                    return func(user=None, *args,**kw)
                return HttpResponseRedirect('/signin')
            else:
                return func(user=user, *args,**kw)
        else:
            if not redirect:
                return func(user=None, *args,**kw)
            return HttpResponseRedirect('/signin')
    return wrapper


