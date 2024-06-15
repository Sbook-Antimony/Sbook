from .accounts import *
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render
from sbook.accounts import *
# Create your views here.


@check_login
def do_index(req, user):
    return render(
        req,
        'school-index.djhtml',
        {
            'user': user,
        }
    )


@check_login
def do_classroom_json(req, user, clsid):
    try:
        classroom = Classroom.from_id(clsid)
    except Classroom.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "status": 404,
        })
    else:
        return JsonResponse({
            "ok": True,
            "status": 200,
            "classroom": classroom.js,
        })


@check_login
def do_classroom_profile(req, user, clsid):
    try:
        classroom = Classroom.from_id(clsid)
    except Classroom.DoesNotExist:
        return HttpResponseNotFound()
    else:
        return HttpResponse(classroom.profile_asBytes)
