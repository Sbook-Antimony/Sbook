from .accounts import *
from django.shortcuts import render
from django.http import JsonResponse


@check_login
def do_sidebar(req, user):
    return render(
        req,
        "short-notes/side-bar.django",
        {
            "user": user,
        },
    )


@check_login
def do_json(req, user, snid):
    try:
        snote = ShortNote.from_id(snid)
    except ShortNote.DoesNotExist:
        return JsonResponse(
            {
                "ok": False,
                "status": 404,
                "short_note": None,
            }
        )
    else:
        if not snote.model.private or snote.author.id == user.id:
            return JsonResponse(
                {
                    "ok": True,
                    "status": 200,
                    "short_note": snote.js,
                }
            )
        else:
            return JsonResponse(
                {
                    "ok": True,
                    "status": 403,
                    "short_note": None,
                }
            )
