from google.oauth2 import id_token
from google.auth.transport import requests
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
import base64
from . import forms
from pyoload import *
import pango
from django.core.files.base import ContentFile
from sbook import markdown

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
                return HttpResponseRedirect(req.GET.get("redirect", "/"))


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
            except User.DoesNotExistError:
                return render(req, "signup.django", {"errors": "User exists"})
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect("/")


@check_login
def do_profile_upload(req, user):
    max_size = 10 * 1024 * 1024
    try:
        img = req.POST.get("image")
        data = base64.b64decode(img)
        assert len(data) > max_size, f"Image too large ({len(data) > max_size})"
        image = ContentFile(data, name=req.GET.get("imagename"))
        user.model.profile = image
        user.model.save()
    except Exception as e:
        return JsonResponse({
            "succes": False,
            "error": e.__class__.__name__ + ": " + str(e),
        })
    else:
        return JsonResponse({"succes": True})


@check_login
def do_profile(req, user: User):
    return do_userid_profile(req, user.model.id)


def do_userid_profile(req, userid):
    try:
        user = User.from_id(userid)
    except User.DoesNotExistError:
        return HttpResponseNotFound()
    else:
        return HttpResponse(user.profile_asBytes, "img/png")


def do_username_profile(req, username):
    try:
        user = User.get(username=username)
    except User.DoesNotExistError:
        return File(User.DEFAULT_PROFILE_PATH)
    else:
        return HttpResponse(user.profile_asBytes, "img/png")


def do_user(req, user):
    return render(
        req,
        "user-profile.djhtml",
        {
            "id": user,
            "ng_app_name": "userProfile",
        },
    )


@check_login
def do_markdown(req, user):
    try:
        data = req.GET.get("md")
        data = base64.b64decode(data).decode("utf-8")
        return JsonResponse(
            {
                "html": markdown(data),
                "ok": True,
            }
        )
    except Exception as e:
        print(e)
        return JsonResponse(
            {
                "html": "<em>Could not be renderred</em>",
                "ok": False,
            }
        )


@annotate
def do_user_json(req, userid: int) -> Cast(JsonResponse):
    try:
        user = User.from_id(userid)
    except UserDoesNotExistError:
        return {
            "ok": False,
            "error": 404,
        }
    except Exception:
        return {
            "ok": False,
            "error": 0,
        }
    else:
        return {
            "ok": True,
            "user": user.js,
        }


@check_login
def do_current_user_json(req, user):
    return JsonResponse(
        {
            "ok": True,
            "user": user.js,
        }
    )


@annotate
def do_username_json(req, username: str) -> Cast(JsonResponse):
    try:
        user = User.get(username=username)
    except UserDoesNotExistError:
        return {
            "ok": False,
            "error": 404,
        }
    except Exception:
        return {
            "ok": False,
            "error": 0,
        }
    else:
        return {
            "ok": True,
            "user": user.js,
        }


@check_login
def do_update_profile(req, user):
    user.model.bio = req.GET.get("bio", user.model.bio)
    user.model.name = req.GET.get("name", user.model.name)

    user.model.save()
    return JsonResponse(
        {
            "ok": True,
        }
    )


@check_login(False)
def pango_query(req, user):
    query = req.GET.get("q")
    if not query:
        return JsonResponse(
            {
                "ok": False,
                "response": None,
                "msg": "No query provided",
            }
        )
    if user is not None:
        res = pango.query(user.model.username, query)
    else:
        res = pango.query("anonymy", query)
    return JsonResponse(
        {
            "ok": True,
            "response": res,
        }
    )


def __google_token_signin(req):
    # from https://developers.google.com/identity/sign-in/web/backend-auth
    """
    {
     // These six fields are included in all Google ID Tokens.
     "iss": "https://accounts.google.com",
     "sub": "110169484474386276334",
     "azp": "    .apps.googleusercontent.com",
     "aud": "    .apps.googleusercontent.com",
     "iat": "1433978353",
     "exp": "1433981953",

     // These seven fields are only included when the user has granted the "profile" and
     // "email" OAuth scopes to the application.
     "email": "testuser@gmail.com",
     "email_verified": "true",
     "name" : "Test User",
     "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
     "given_name": "Test",
     "family_name": "User",
     "locale": "en"
    }
    """
    try:
        token = req.POST.get("token")
        print("TOKEN:------------------\n", token, "\n")
        if token is None:
            raise ValueError("Invalid request token")
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.CLIENT_ID
        )
        print("TOKEN:------------------\n", idinfo, "\n")

        if idinfo['hd'] not in settings.ALLOWED_HOSTS:
            raise ValueError('Wrong domain name.')
        userid = idinfo['sub']
        return JsonResponse({
            'ok': True,
        })
    except ValueError as e:
        return JsonResponse({
            'ok': False,
            'error': str(e),
        })

def google_token_signin(req):
    pass
