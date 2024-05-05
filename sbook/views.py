from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
from django.views import View
from pathlib import Path
from sbook.accounts import *
import mimetypes
from . import forms


def do_index(req, user=None):
    if user:
        return render(
            req,
            'dashboard.django',
            {'user': user}
        )
    else:
        return render(
            req,
            'index.django',
        )
def do_image(req, name):
    file = (DIR.parent / "image") / name
    if file.exists():
        return HttpResponse(file.read_bytes(), mimetypes.guess_type(file)[0])
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
            {'errors': False},
        )
    def post(self, req, *args, **kw):
        form = forms.SigninForm(req.POST)
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "signin.django",
                {
                    'errors': (str(errors.get("email", "")[0].message) if len(errors.get("email")) > 0 else False)

                }
            )
        else:
            try:
                data = form.cleaned_data
                user = User.from_login(data.get("email"), data.get("password"))
            except UserDoesNotExistError:
                return render(
                    req,
                    "signin.django",
                    {
                        "errors": "Invalid Login: password or email incorrect"
                    }
                )
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect('/')

class signup(View):
    def get(self, req, *args, **kw):
        return render(req,"signup.django", {'errors': False})
    def post(self, req, *args, **kw):
        form = forms.SignupForm(req.POST)
        if not form.is_valid():
            errors = form.errors.as_data()
            return render(
                req,
                "signup.django",
                {
                    'errors': (str(errors.get("email", "")[0].message) if len(errors.get("email")) > 0 else False)

                }
            )
        else:
            try:
                data = form.cleaned_data
                user = User.create_from_login(data.get('name'), data.get("email"), data.get("password"))
            except UserDoesExistError:
                return render(
                    req,
                    "signup.django",
                    {
                        "errors": "User exists"
                    }
                )
            else:
                req.session["user-id"] = user.id
                return HttpResponseRedirect('/')

def do_cmd(req, user, cmd, user):
    match cmd:
        case 'set-new-profile':
            file = req.FILES.get('file')
            
            return HttpResponseRedirect('/dashboard')

def do_profile(req, user=None):
    if user:
        return HttpResponse(user.profile_asBytes, 'image/png')
    else:
        return HttpResponse(User.DEFAULT_PROFILE.read_bytes())
