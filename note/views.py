from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
from pathlib import Path
import mimetypes
import yaml, json

from .accounts import *


@check_login(True)
def do_index(req, user):
    #print(user, user.sbookAccount, user.sbookAccount.name, user.notes, type(user.notes))
    return HttpResponse(
        render(
            req,
            "note-dashboard.django",
            {
                "len": len,
                "user": user,
                "user_name": user.sbookAccount.name,
            }
        )
    )


