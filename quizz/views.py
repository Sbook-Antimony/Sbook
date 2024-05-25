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
    return HttpResponse(
        render(
            req,
            "quizz-dashboard.django",
            {
                "user": user,
                "user_name": user.sbookAccount.name,
                'ng_app_name': 'qdashboard',
            }
        )
    )


@check_login
def preview_quizz(req, user, quizzid):
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        'quizz-preview.django',
        {
            'user': user,
            'settings': settings,
            'quizz': quizz,
            'ng_app_name': 'quizz_preview',
        }
    )


class profiles:
    def quizzes(req, quizzid):
        try:
            quizz = Quizz.from_id(quizzid)
        except QuizzDoesNotExistError:
            return HttpResponseNotFound()
        else:
            return HttpResponse(quizz.profile_asBytes)
