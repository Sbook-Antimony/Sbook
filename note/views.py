from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pathlib import Path
import accounts
import mimetypes
import yaml, json

from . import *
DIR = Path(__file__).resolve().parent
redirect = lambda url: loader.get_template('redirect.django').render({'url':url})
plain = lambda f, m='rb': open(DIR / 'html' / f, m).read()

def do_header(req):
    print("note header")
    return HttpResponse(loader.get_template("note/header.django").render({}, req))
def do_index(req):
    return HttpResponse(plain('index.html'))

def do_dashboard(req):
    return HttpResponse(plain("dashboard.html"))

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
