from pathlib import Path

import yaml

import sbook.models


DIR = Path(__file__).parent.parent
ACCOUNTS = DIR/'accounts'

assert ACCOUNTS.exists(), f"accounts folder {ACCOUNTS!r} does not exists"
#############################################
import functools

from django.http import HttpResponseRedirect, HttpResponse

from sbook import models


class UserDoesNotExistError(ValueError):
    pass
class UserDoesExistError(ValueError):
    pass






def check_login(func):
    @functools.wraps(func)
    def wrapper(req, *args, **kw):
        if "user-id" in req.session:
            try:
                user = User.from_id(req.session.get("user-id", -1))
            except UserDoesNotExistError:
                return HttpResponseRedirect('/signin')
            else:
                return func(req, user=user, *args,**kw)
        else:
            return HttpResponseRedirect('/signin')
    return wrapper
##########################################

class User:
    model:models.User

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
            obj = models.User(name=name, email=email, password=password, chatty=chatty.ChattyUser.create_from_login(name, email, password))
            createUserData(obj)
            obj.save()
        except models.User.DoesNotExist as e:
            raise UserDoesExistError() from e
        else:
            return cls(obj)

    def __init__(self, model=None):
        if model is None:
            raise UserDoesNotExistError()
        self.model = model

    @functools.cached_property
    def id(self):
        return self.model.id
    @functools.cached_property
    def name(self):
        return self.model.name
    @functools.cached_property
    def rooms(self):
        return [ChattyRoom(x) for x in self.model.rooms.all()]

    DEFAULT_PHOTO = "/image/default-photo.png"
    name:tuple[str]
    password:str
    data:dict
    folder:Path
    id:int
    
def createUserData(obj) -> int:
    #users = sbook.models.Account.objects.all()
    
    folder = ACCOUNTS / str(obj.id)

    folder.mkdir()

    profile = folder / "profile.png"
    profile.touch()
    profile.write_bytes(DIR / 'image' / 'default-photo.png')

    data_file = (folder/"data.yaml")
    data_file.touch()
    data_file.write_text(yaml.safe_dump(data))

    return Account(id)
