from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
    FileResponse,
)
from django.template import loader
from django.views import View
from pathlib import Path
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from sbook.accounts import *
import mimetypes
import markdown
from . import forms

File = lambda url: FileResponse(open(url, "rb"), filename=url.as_uri())


def u_email_check_json(req, scope):
    email = req.GET.get("email", "")
    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse(e.message, safe=False)
    else:
        exists = User.exists(email=email)
        if exists and scope == "signup":
            return JsonResponse(f"email {email} already used", safe=False)
        elif not exists and scope == "signin":
            return JsonResponse(
                f"email {email} does not exist in our database", safe=False
            )
        else:
            return JsonResponse(False, safe=False)


def u_password_check_json(req, scope):
    password = req.GET.get("password")
    results = password_policy.test(password)
    if len(results) == 0:
        return JsonResponse(False, safe=False)
    else:
        txt = "Password requires:\n"
        for err in results:
            txt += str(err).rstrip(")").replace("(", ": ") + "\n"
        return JsonResponse(txt, safe=False)


@check_login(False)
def do_index(req, user):
    if user is not None:
        return render(
            req,
            "dashboard.django",
            {"user": user, "ng_app_name": "dashboard"},
        )
    else:
        return render(
            req,
            "index.django",
        )


def do_image(req, name):
    file = (DIR / "image") / name
    if file.exists():
        return File(file)
    else:
        print("not found image %s" % file)
        return HttpResponseNotFound("")


def do_csrf(req):
    return render(req, "csrf.django")


class signin(View):
    def get(self, req, *args, **kw):
        return render(
            req,
            "signin.django",
            {"errors": False},
        )

    def post(self, req, *args, **kw):
        data = parse_recaptcha_token(req.POST.get("signincaptcha"))
        # print(data)
        if not data.get("success"):
            # return HttpResponseRedirect("/signin/")
            pass
        form = forms.SigninForm(req.POST)
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "signin.django",
                {
                    "errors": (
                        str(errors.get("email", "")[0].message)
                        if len(errors.get("email"), []) > 0
                        else False
                    )
                },
            )
        else:
            try:
                data = form.cleaned_data
                user = User.from_login(
                    email=data.get("email"), password=data.get("password")
                )
            except UserDoesNotExistError:
                return render(
                    req,
                    "signin.django",
                    {"errors": "Invalid Login: password or email incorrect"},
                )
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect("/")


class signup(View):
    def get(self, req, *args, **kw):
        return render(req, "signup.django", {"errors": False})

    def post(self, req, *args, **kw):
        data = parse_recaptcha_token(req.POST.get("signincaptcha"))
        # print(data)
        if not data["success"]:
            # return HttpResponseRedirect("/signup/")
            pass

        form = forms.SignupForm(req.POST)
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "signup.django",
                {
                    "errors": (
                        str(errors.get("email", "")[0].message)
                        if len(errors.get("email", [])) > 0
                        else False
                    )
                },
            )
        else:
            try:
                data = form.cleaned_data
                user = User.create_from_login(
                    data.get("name"), data.get("email"), data.get("password")
                )
            except UserDoesExistError:
                return render(req, "signup.django", {"errors": "User exists"})
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect("/")


@check_login
def do_profile_upload(req, user):
    file = req.FILES.get("file")
    image = Image.open(file)
    user.profile = image.resize((500, 500))
    user.save()
    return JsonResponse({"succes": True})


@check_login(True)
def do_profile(req, user: User):
    if user is not None:
        return HttpResponse(user.profile_asBytes, "img/png")
    else:
        return File(User.DEFAULT_PROFILE_PATH)


def do_userid_profile(req, userid):
    try:
        user = User.from_id(userid)
    except UserDoesNotExistError:
        return File(User.DEFAULT_PROFILE_PATH)
    else:
        return HttpResponse(user.profile_asBytes, "img/png")


@check_login
def do_markdown(req):
    try:
        data = req.GET.get("md")
        return HttpResponse(markdown.markdown(data))
    except Exception:
        return HttpResponse("<em>Could not be renderred</em>")
