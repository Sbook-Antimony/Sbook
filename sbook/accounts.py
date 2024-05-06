from pathlib import Path
from PIL import Image
import io

import yaml
import django.http

import random_profile_image


DIR = Path(__file__).parent.parent
ACCOUNTS = DIR/'accounts'

assert ACCOUNTS.exists(), f"accounts folder {ACCOUNTS!r} does not exists"


import functools

from django.http import HttpResponseRedirect, HttpResponse

from sbook import models
from chatty import accounts as chatty

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
                    return func(user=None, *args,**kw)
                return HttpResponseRedirect('/signin')
            else:
                return func(user=user, *args,**kw)
        else:
            if not redirect:
                return func(user=None, *args,**kw)
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
            obj = models.User(name=name, email=email, password=password, chatty=chatty.ChattyUser.create_from_login(name, email, password).model)
            obj.save()
            createUserData(obj)
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
            self.directory / 'profile.png',
        )

    @functools.cached_property
    def profile_asBytes(self):
        buffer = io.BytesIO()
        self.profile.save(buffer, format='PNG')
        return buffer.getvalue()

    @functools.cached_property
    def name(self):
        return self.model.name
    
    @functools.cached_property
    def chattyAccount(self):
        cha = self.model.chattyAccount.all()
        if len(cha) == 0:
            raise chatty.accounts.UserDoesNotExistError()
        return chatty.accounts.ChattyUser(cha[0])

    @functools.cached_property
    def noteAccount(self):
        cha = self.model.noteAccount.all()
        if len(cha) == 0:
            raise note.accounts.UserDoesNotExistError()
        return note.accounts.ChattyUser(cha[0])
    DEFAULT_PROFILE_PATH = Path("/image/default-photo.png")
    name:tuple[str]
    password:str
    data:dict
    folder:Path
    id:int
    
def createUserData(obj) -> int:
    #users = sbook.models.Account.objects.all()
    assert obj.id is not None
    folder = ACCOUNTS / str(obj.id)

    folder.mkdir()

    img = random_profile_image.random_profile()
    img.save(folder / "profile.png")

    data_file = (folder/"data.yaml")
    data_file.touch()
    data_file.write_text(
        yaml.safe_dump(
            {
                "id": obj.id,
                "name": obj.name,
                "password": obj.password,
                "email": obj.email,
                "chatty": {
                    "id": obj.chatty.id,
                }
            }
        )
    )

