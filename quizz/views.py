import json

from . import forms
from .accounts import *
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from sbook import settings


@check_login(True)
def do_index(req, user):
    return HttpResponse(
        render(
            req,
            "quizz-dashboard.django",
            {
                "user": user,
                "ng_app_name": "qdashboard",
            },
        )
    )


@check_login
def do_quizzes_json(req, user, userid):
    try:
        ouser = QuizzUser.from_id(userid)
    except QuizzUserDoesNotExistError:
        return JsonResponse({"ok": False, "quizzes": ()})
    else:
        return JsonResponse(
            {"ok": True, "quizzes": tuple(quizz.js for quizz in ouser.quizzes)}
        )


@check_login
def do_user_attempts_json(req, user, userid):
    try:
        ouser = QuizzUser.from_id(userid)
    except QuizzUserDoesNotExistError:
        return JsonResponse({"ok": False, "attempts": ()})
    else:
        return JsonResponse(
            {
                "ok": True,
                "attempts": tuple(attempts.js for attempts in ouser.attempts),
            }
        )


@check_login
def preview_quizz(req, user, quizzid):
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        "quizz-preview.django",
        {
            "user": user,
            "settings": settings,
            "quizz": quizz,
            "ng_app_name": "quizz_preview",
        },
    )


@check_login
def attempt_quizz(req, user, quizzid):
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        "quizz-attempt.django",
        {
            "user": user,
            "settings": settings,
            "quizz": quizz,
            "ng_app_name": "quizz_attempt",
        },
    )


@check_login
def submit_quizz(req, user, quizzid):
    if req.method == "POST":
        print(req.POST.items(), req.POST, user)
        quizz = Quizz.from_id(quizzid)
        answers = []
        for i, question in enumerate(quizz.questions):
            answers.append(req.POST.get(str(i)))
        attempt = QuizzAttempt.create(user, quizz, answers)
        return render(req, "quizz-attempted.django", {"attempt": attempt, "user": user})


@check_login
def view_quizz_attempts(req, user, quizzid):
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        "view-quizz-attempts.django",
        {
            "quizz": quizz,
            "user": user,
        },
    )


@check_login
def review_attempt(req, user, quizzid, attemptid):
    attempt = QuizzAttempt.from_id(attemptid)
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        "quizz-attempt-review.django",
        {
            "attempt": attempt,
            "quizz": quizz,
            "user": user,
        },
    )


@check_login
def review_attempt_review(req, user, quizzid, attemptid):
    attempt = QuizzAttempt.from_id(attemptid)
    quizz = Quizz.from_id(quizzid)
    return render(
        req,
        "quizz-attempt-view-remarks.django",
        {
            "attempt": attempt,
            "quizz": quizz,
            "user": user,
            "ng_app_name": "reviewReview",
        },
    )


@check_login
def review_attempt_submit(req, user, quizzid, attemptid):
    remark = req.POST.get("remark")
    score = req.POST.get("score")
    if None in (remark, score):
        return render(
            req,
            "quizz-attempt-review.django",
            {
                "messages": [
                    ("error", "partial content"),
                ],
            },
        )
    attempt = QuizzAttempt.from_id(attemptid)
    attempt.model.remark = remark
    attempt.model.score = score
    attempt.model.remarked = True
    attempt.model.save()
    return HttpResponseRedirect(
        f"/quizz/quizzes/{quizzid}/attempts/",
    )


@check_login
def do_new(req, user):
    return render(
        req,
        "quizz-new.django",
        {
            "user": user,
            "ng_app_name": "quizzNew",
        },
    )


@check_login
def do_new_submit(req, user):
    data = json.loads(req.POST.get("questions")),
    print(req.POST.get("questions"), "-" * 50)
    prof = {}
    if req.POST.get("profile_url"):
        pass
    quizz = models.Quizz(
        instructions=req.POST.get("instructions"),
        epilog=req.POST.get("epilog"),
        prolog=req.POST.get("prolog"),
        questions=data,
        title=req.POST.get("title"),
        description=req.POST.get("description"),
        is_private=req.POST.get("is_private") in (True, "true"),
        **prof
    )
    quizz.save()
    quizz.authors.set((user.id,))
    return JsonResponse(
        {
            "ok": True,
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


@annotate
def do_user_json(req, userid: int) -> Cast(JsonResponse):
    try:
        user = QuizzUser.from_id(userid)
    except QuizzUser.DoesNotExistError:
        return {
            'ok': False,
            'error': 404,
        }
    except Exception:
        return {
            'ok': False,
            'error': 0,
        }
    else:
        return {
            'ok': True,
            'user': user.js,
        }


@check_login
def do_quizz_json(req, user, quizzid):
    try:
        quizz = Quizz.from_id(quizzid)
    except Quizz.DoesNotExistError:
        return JsonResponse({
            'ok': False,
            'quizz': None,
        })
    else:
        return JsonResponse({
            'ok': True,
            'quizz': quizz.js,
        })


@check_login
def do_quizz_browse(req, user):
    return render(
        req,
        'quizz-browse.djhtml',
        {
            "user": user,
            "ng_app_name": "browse",
        }
    )


@check_login
def do_all_quizz_json(req, user):
    return JsonResponse({
        "ok": True,
        "quizzes": list(
            map(
                lambda q: q.js,
                filter(lambda q: q.accessible_by(user), Quizz.all())
            ),
        ),
    })
