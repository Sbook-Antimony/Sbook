import functools

from django.http import HttpResponseRedirect, HttpResponse

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
            found = sbook.models.User.objects.get(id=id)
        except sbook.models.User.DoesNotExist as e:
            raise NoteUserDoesNotExistError() from e
        else:
            return found.noteAccount
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
