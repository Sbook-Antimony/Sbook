from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from pathlib import Path
import accounts
import mimetypes
DIR = Path(__file__).resolve().parent
redirect = lambda url: loader.get_template('redirect.django').render({'url':url})

def do_index(req):
    print(req)
    return HttpResponse(loader.get_template('index.django').render())
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
    return HttpResponse(loader.get_template("csrf.django").render())
def do_login(req):
    redirect = False
    redirect_url = ""
    if req.GET.get('redirect') is not None:
        redirect = True
        redirect_url = req.GET.get('redirect')
    if req.method == 'GET':#######################
        return HttpResponse(
            loader.get_template("login.django").render(
                {
                    'error': False,
                    'redirect': redirect,
                    'redirect_url': redirect_url,
                },
                req
            )
        )
    elif req.method == 'POST':
        fname, lname, pswd = map(
            req.POST.get,
            ('firstname', 'lastname', 'password')
        )
        if None in (fname, lname, pswd) or '' in (fname, lname, pswd):
            return HttpResponse(
                loader.get_template("login.django").render(
                    {
                        'error': True,
                        'error_title': 'partial content',
                        'error_content': 'some fields were left empty',
                        'redirect': redirect,
                        'redirect_url': redirect_url,
                    },
                    req
                )
            )
        id = accounts.Account.login_info(fname, lname, pswd)
        if id == -2:
            return HttpResponse(
                loader.get_template("login.django").render(
                    {
                        'error': True,
                        'error_title': 'wrong login',
                        'error_content': 'no such user found',
                        'redirect': redirect,
                        'redirect_url': redirect_url,
                    },
                    req
                )
            )
        elif id == -1:
            return HttpResponse(
                loader.get_template("login.django").render(
                    {
                        'error': True,
                        'error_title': 'wrong login',
                        'error_content': 'seems some login data were wrong',
                        'redirect': redirect,
                        'redirect_url': redirect_url,
                    },
                    req
                )
            )
        else:
            req.session["user-id"] = id
            print("-"*20, id)
            import django.shortcuts
            return django.shortcuts.redirect(redirect or '/')


def do_signup(req):
    redirect = False
    redirect_url = ""
    if req.GET.get('redirect') is not None:
        redirect = True
        redirect_url = req.GET.get('redirect')
    if req.method == 'GET':#######################
        return HttpResponse(
            loader.get_template("signup.django").render(
                {
                    'error': False,
                    'redirect': redirect,
                    'redirect_url': redirect_url,
                },
                req
            )
        )
    elif req.method == 'POST':
        fname, lname, pswd = map(
            req.POST.get,
            ('firstname', 'lastname', 'password')
        )
        if None in (fname, lname, pswd) or '' in (fname, lname, pswd):
            return HttpResponse(
                loader.get_template("signup.django").render(
                    {
                        'error': True,
                        'error_title': 'partial content',
                        'error_content': 'some fields were left empty',
                        'redirect': redirect,
                        'redirect_url': redirect_url,
                    },
                    req
                )
            )
        id = accounts.Account.login_info(fname, lname, pswd)
        if id >= -1:
            return HttpResponse(
                loader.get_template("signup.django").render(
                    {
                        'error': True,
                        'error_title': 'wrong login',
                        'error_content': 'user already exists',
                        'redirect': redirect,
                        'redirect_url': redirect_url,
                    },
                    req
                )
            )
        elif id == -2:

            data = {}
            data['firstname'] = req.POST.get('firstname')
            data['lastname'] = req.POST.get('lastname')
            data['password'] = req.POST.get('password')
            id = accounts.create_account(data).id
            req.session["user-id"] = id #todo it is not set
            return HttpResponse("", {'Location': "/account/config"})