from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
import tempfile
import zipfile
from pathlib import Path
import mimetypes
import yaml, json
from django.views import View
from sbook import settings
from .accounts import *
from . import forms


@check_login(True)
def do_index(req, user):
    #print(user, user.sbookAccount, user.sbookAccount.name, user.notes, type(user.notes))
    return HttpResponse(
        render(
            req,
            "note-dashboard.django",
            {
                "user": user,
                "hasNotes": user.hasNotes,
                "hasBookmarks": user.hasBookmarks,
                "user_name": user.sbookAccount.name,
            }
        )
    )

@check_login
def note_profile(req, user, noteid):
    try:
        note = Note.from_id(noteid)
    except NoteDoesNotExistError:
        return HttpResponseNotFound()
    else:
        return HttpResponse(note.profile_asBytes, "img/png")


class note_upload(View):
    @check_login    
    def get(self, req, user, *args, **kw):
        return render(
            req,
            "note-upload.django",
            {
                "user": user,
                "settings": settings,
            }
        )
    @check_login    
    def post(self, req, user, *args, **kw):
        form = forms.NoteUploadForm(req.POST)
        form = form.cleaned_data

        file = form.get('file')

        
        file = zipfile.ZipFile(file)
        temp_dir = tempfile.TemporaryDirectory()
        url = temp_dir.name

        file.extractall(url)

        meta = engine.load_meta(redactors=[user])

        dest = Note.initialize(user, meta)

        engine.compile(
            url,
            meta,
            dest
        )

        Note.create(meta, dest)


