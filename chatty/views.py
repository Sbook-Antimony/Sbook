from chatty.accounts import *
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from . import forms


@check_login
def index(req, user):
    return render(
        req,
        "chatty-index.django",
        {
            "User": user,
            "room": req.GET.get("room", None),
        },
    )


@check_login
def send_message(req, user, roomid):
    form = forms.SendMessageForm(req.POST)
    try:
        assert form.is_valid()
        data = req.POST.get("content")
        ChattyMessage.create(user, data, ChattyRoom.from_id(roomid))
        return HttpResponseRedirect(f"/chatty/rooms/{roomid}/messages/")
    except Exception as e:
        return HttpResponse("false" + str(e))


class room(View):
    @check_login
    def get(self, req, user, roomid, *_, **__):
        try:
            room = ChattyRoom.from_id(roomid)
        except ChattyRoomDoesExistError:
            return HttpResponseNotFound("room %d not found" % roomid)
        else:
            return render(
                req,
                "room-view.django",
                {"room": room, "User": user, "is_admin": room.admin.id == user.id},
            )


class room_create(View):
    @check_login
    def get(self, req, user, *_, **__):
        return render(req, "room-create.django")

    @check_login
    def post(self, req, user, *_, **__):
        form = form.CreateRoomForm(req.POST)
        name = form.cleaned_data.get("name")
        errormsg = None
        if not form.is_valid():
            errors = form.errors.as_data()
            errormsg = (
                str(errors.get("name")[0].message)
                if len(errors.get("name")) > 0
                else False
            )
        if not errormsg:
            try:
                room = ChattyRoom.create_from_login(user, name)
            except ChattyRoomDoesExistError:
                errormsg = "name unavailable"
            else:
                return HttpResponseRedirect("/chatty/?room=%d" % room.id)
        if errormsg:
            return render(req, "chatty-signup.django", {"errors": errormsg})
