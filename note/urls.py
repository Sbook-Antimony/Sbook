from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.do_index),
    path('notes/<noteid>/profile.png', views.note_profile)
    #path('my-notes/get-notes.json', views.do_mynotes.do_get_json),
    #path('my-notes/upload', views.do_mynotes.do_upload),
    #path('my-notes/<noteName>/icon.png', views.do_mynotes.do_get_icon),
]
