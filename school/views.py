from django.shortcuts import render

# Create your views here.


def do_index(req):
    return render(
        req,
        'school-main.djhtml',
        {
        }
    )
