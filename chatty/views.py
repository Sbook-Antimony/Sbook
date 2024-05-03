from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.views import View
from chatty.accounts import *

from . import forms

def index(req, user):
    return render(
        req,
        'chatty-index.html',
        {
            "User": user
        }
    )
def send_message(req, user, roomid):
    form = forms.SendMessageForm(req.POST)
    try:
        assert form.is_valid()
        data = req.POST.get('content')
        ChattyMessage.create(user, data, ChattyRoom.from_id(roomid))
        return HttpResponseRedirect(f"/chatty/rooms/{roomid}/messages/")
    except Exception as e:
        return HttpResponse('false'+str(e))

class signin(View):
    def get(self, req, *args, **kw):
        return render(req, "chatty-signin.html", {'errors': False})
    def post(self, req, *args, **kw):
        form = forms.SigninForm(req.POST)
        print(dir(form.fields))
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "chatty-signin.html",
                {
                    'errors': (str(errors.get("email", "")[0].message) if len(errors.get("email")) > 0 else False)

                }
            )
        else:
            try:
                data = form.cleaned_data
                user = ChattyUser.from_login(data.get("email"), data.get("password"))
            except ChattyUserDoesNotExistError:
                return render(
                    req,
                    "chatty-signin.html",
                    {
                        "errors": "Invalid Logig: password or email incorrect"
                    }
                )
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect('/chatty')

class signup(View):
    def get(self, req, *args, **kw):
        return render(req,"chatty-signup.html", {'errors': False})
    def post(self, req, *args, **kw):
        form = forms.SignupForm(req.POST)
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "chatty-signup.html",
                {
                    'errors': (str(errors.get("email", "")[0].message) if len(errors.get("email")) > 0 else False)

                }
            )
        else:
            try:
                data = form.cleaned_data
                user = ChattyUser.create_from_login(data.get('name'), data.get("email"), data.get("password"))
            except ChattyUserDoesExistError:
                return render(
                    req,
                    "chatty-signup.html",
                    {
                        "errors": "User exists"
                    }
                )
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect('/chatty')
class room(View):
    def get(self, req, user, roomid, *_, **__):
        try:
            room = ChattyRoom.from_id(roomid)
        except:
            return HttpResponseNotFound(
                "room %d not found"%roomid
            )
        else:
            return render(
                req,
                "room-view.html",
                {
                    'room': room,
                    'User': user,
                    'is_admin': room.admin.id == user.id
                }
            )
class room_create(View):
    def get(self, req, user, *_, **__):
        return render(req, "room-create.html")
    def post(self, req, user, *_, **__):
        form = form.CreateRoomForm(req.POST)
        name = form.cleaned_data.get("name")
        errormsg = None
        if not form.is_valid():
            errors = form.errors.as_data()
            errormsg = (str(errors.get("name")[0].message) if len(errors.get("name")) > 0 else False)
        if not errormsg:
            try:
                room = ChattyRoom.create_from_login(user, name)
            except ChattyRoomDoesExistError:
                errormsg = "name unavailable"
            else:
                return HttpResponseRedirect("/chatty/rooms/%d"%room.id)
        if errormsg:
            return render(
                req,
                "chatty-signup.html",
                {
                    'errors': errormsg
                }
            )
