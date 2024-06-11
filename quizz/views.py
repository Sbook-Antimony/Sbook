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
                "user_name": user.sbookAccount.name,
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
    data = {
        "epilog": req.POST.get("epilog"),
        "prolog": req.POST.get("prolog"),
        "instructions": req.POST.get("instructions"),
        "questions": json.loads(req.POST.get("questions")),
    }
    print(req.POST.get("questions"), "-" * 50)
    quizz = models.Quizz(
        data=data,
        title=req.POST.get("title"),
        description=req.POST.get("description"),
        is_private=req.POST.get("is_private") in (True, "true"),
        profile=open("profile.png", "rb"),
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
