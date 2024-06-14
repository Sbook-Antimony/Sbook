from django.shortcuts import render
from .accounts import *
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
