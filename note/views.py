import mimetypes
import tempfile
import yaml, json
import zipfile

from . import forms
from .accounts import *
from django.http import FileResponse
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from pathlib import Path
from sbook import settings


@check_login(True)
def do_index(req, user):
    # print(user, user.sbookAccount, user.sbookAccount.name, user.notes, type(user.notes))
    return HttpResponse(
        render(
            req,
            "note-dashboard.django",
            {
                "user": user,
                "hasNotes": user.hasNotes,
                "hasBookmarks": user.hasBookmarks,
                "user_name": user.sbookAccount.name,
            },
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
            },
        )

    @check_login
    def post(self, req, user, *args, **kw):
        form = forms.NoteUploadForm(req.POST)
        form = form.cleaned_data

        file = form.get("file")

        file = zipfile.ZipFile(file)
        temp_dir = tempfile.TemporaryDirectory()
        url = temp_dir.name

        file.extractall(url)

        meta = engine.load_meta(redactors=[user])

        dest = Note.initialize(user, meta)

        engine.compile(url, meta, dest)

        Note.create(meta, dest)


class note(View):
    @check_login
    def get(self, req, user, noteid, path, *args, **kw):
        print(req, user, noteid, path)
        try:
            note = Note.from_id(noteid)
            print("note", note)
            file = note.directory / path
            if not file.exists():
                raise FileNotFoundError(path)
        except NoteDoesNotExistError:
            return HttpResponseNotFound("Note {noteid} does not exist")
        except FileNotFoundError as e:
            return HttpResponseNotFound(str(e))
        else:
            mime = mimetypes.guess_type(file)
            print(f"{mime=}")
            if mime[0] in ("text/html", "txt/html", "text/javascript"):
                try:
                    return HttpResponse(
                        file.read_text()
                        .replace(
                            "{",
                            "\1",
                        )
                        .replace(
                            "}",
                            "\2",
                        )
                        .replace(
                            "<<<",
                            "{",
                        )
                        .replace(
                            ">>>",
                            "}",
                        )
                        .format(
                            user=user,
                            note=note,
                        )
                        .replace("\1", "{")
                        .replace("\2", "}")
                    )
                except Exception as e:
                    return HttpResponse(str(e))
            else:
                return HttpResponse(file.read_bytes())


@check_login
def browse_notes_json(req, user):
    return JsonResponse(
        list(
            map(
                lambda note: Note(note).js,
                models.Note.objects.all(),
            )
        ),
        safe=False,
    )


@check_login
def browse_notes(req, user):
    from_ = int(req.GET.get("from", "0"))
    to_ = int(req.GET.get("to", from_ + 30))

    notes = map(Note, models.Note.objects.order_by("stars")[from_:to_])

    return render(
        req,
        "note-browse.django",
        {
            "user": user,
            "notes": notes,
            "ng_app_name": "browse",
        },
    )
