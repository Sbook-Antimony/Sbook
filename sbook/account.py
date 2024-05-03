from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pathlib import Path
import accounts
redirect = lambda url: loader.get_template('redirect.django').render({'url':url})
def do_config(req):
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

def do_cmd(req, cmd):
    match cmd:
        case 'set-new-profile':
            file = req.FILES.get('file')
            print(file, req.FILES)
            acc = accounts.Account(req.session.get('user-id'))
            (acc.folder / 'profile.png').write_bytes(file.read())
            return redirect('/dashboard')

def do_profile(req):
    acc = accounts.Account(req.session.get('user-id'))
    if (acc.folder / 'profile.png').exists():
        return HttpResponse((acc.folder / 'profile.png').read_bytes(), 'image/png')
