from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
from pathlib import Path
import mimetypes
import yaml, json

from .accounts import *


@check_login(False)
def do_index(req, user):
    return HttpResponse(
        render(
            req,
            "index.django",
            {
                "user": user,
            }
        )
    )

class do_mynotes:
    def do_get_json(req):
        ret = []
        user = accounts.Account(req.session['user-id'])
        notes_dir = user.folder / 'notes'

        if notes_dir.exists():
            for note in notes_dir.glob('*'):
                note = Note(note)
                ret.append(note.data)
        return HttpResponse(json.dumps(ret))
    def do_get_icon(req, noteName):
        user = accounts.Account(req.session['user-id'])
        note = Note(user.folder / 'notes' / noteName)
        return HttpResponse(note.iconFile.read_bytes())

    def do_upload(req):
        return HttpResponse(plain("upload.html"))
