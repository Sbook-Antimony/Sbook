from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader
from django.views import View
from pathlib import Path
from sbook.accounts import *
import mimetypes
from . import forms


def do_index(req, user):
    return render(req, 'index.django')
def do_css(req, name):
    file = (DIR.parent / "css") / name
    if file.exists():
        return HttpResponse(file.read_text(), 'text/css')
    else:
        print("not found css %s" % file)
        return HttpResponseNotFound("")
def do_js(req, name):
    file = (DIR.parent / "js") / name
    if file.exists():
        return HttpResponse(file.read_text(), 'application/javascript')
    else:
        print("not found js %s" % file)
        return HttpResponseNotFound("")
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
        return render(req, "signin.django", {'errors': False})
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


def do_config(req, user):
    id = req.session.get('user-id')
    if id is None:
        return HttpResponse("no id")
    acc = accounts.Account(id)
    return HttpResponse(
        loader.get_template("account/config.django").render(
            {
                'fname': acc.firstname,
                'lname': acc.lastname,
                'account_type': acc.data.get("type") or ''
            },
            req
        )
    )

def do_cmd(req, cmd, user):
    match cmd:
        case 'set-new-profile':
            file = req.FILES.get('file')
            print(file, req.FILES)
            acc = accounts.Account(req.session.get('user-id'))
            (acc.folder / 'profile.png').write_bytes(file.read())
            return HttpResponseRedirect('/dashboard')

def do_profile(req, user):
    acc = accounts.Account(req.session.get('user-id'))
    if (acc.folder / 'profile.png').exists():
        return HttpResponse((acc.folder / 'profile.png').read_bytes(), 'image/png')
