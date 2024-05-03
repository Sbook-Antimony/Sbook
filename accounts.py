from pathlib import Path

import yaml

import sbook.models

DIR = Path(__file__).parent
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


class ChattyRoomDoesNotExistError(ValueError):
    pass
class ChattyRoomDoesExistError(ValueError):
    pass
class ChattyRoom:
    @classmethod
    def from_id(cls, id):
        try:
            found = models.ChattyRoom.objects.get(id=id)
        except models.ChattyRoom.DoesNotExist as e:
            raise ChattyRoomDoesNotExistError() from e
        else:
            return cls(found)
    @classmethod
    def create_from_login(cls, user, name):
        try:
            obj = models.ChattyRoom(
                name=name,
                admin=user,
                members=[user]
            )
            obj.save()
        except models.ChattyUser.DoesNotExist as e:
            raise ChattyUserDoesExistError() from e
        else:
            return cls(obj)
    def __init__(self, model=None):
        if model is None:
            raise ChattyRoomDoesNotExistError()
        self.model = model

    @functools.cached_property
    def id(self):
        return self.model.id
    @functools.cached_property
    def name(self):
        return self.model.name
    @functools.cached_property
    def members(self):
        return tuple(map(ChattyUser ,self.model.members.all()))
    @functools.cached_property
    def admin(self):
        return ChattyUser(self.model.admin)
    @functools.cached_property
    def messages(self):
        return tuple(map(ChattyMessage, self.model.messages.all()))


class ChattyMessageDoesNotExistError(ValueError):
    pass
class ChattyMessagrDoesExistError(ValueError):
    pass
class ChattyMessage:
    @classmethod
    def create(cls, user, content, room):
        msg = models.ChattyTextMessage(content=content, sender=user.model, room=room.model)
        msg.save()
        return cls(msg)
    @classmethod
    def from_id(cls, id):
        try:
            found = models.ChattyTextMessage.objects.get(id=id)
        except models.ChattyTextMessage.DoesNotExist as e:
            raise ChattyMessageDoesNotExistError() from e
        else:
            return cls(found)
    def __init__(self, model=None):
        if model is None:
            raise ChattyMessageDoesNotExistError()
        self.model = model

    @functools.cached_property
    def id(self):
        return self.model.id
    @functools.cached_property
    def sender(self):
        return ChattyUser(self.model.sender)
    @functools.cached_property
    def content(self):
        return self.model.content
    @functools.cached_property
    def room(self):
        return ChattyRoom(self.model.room)
    @functools.cached_property
    def sent_date(self):
        return (self.model.sent_date)





def check_login(func):
    @functools.wraps(func)
    def wrapper(req, *args, **kw):
        if "user-id" in req.session:
            try:
                user = ChattyUser.from_id(req.session.get("user-id", -1))
            except ChattyUserDoesNotExistError:
                return HttpResponseRedirect('/chatty/signin')
            else:
                return func(req, user=user, *args,**kw)
        else:
            return HttpResponseRedirect('/chatty/signin')
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
            obj = models.User(name=name, email=email, password=password)
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
