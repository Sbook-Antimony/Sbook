from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.do_index),
    path("notes/<int:noteid>/profile.png", views.note_profile),
    path("notes/upload", views.note_upload.as_view()),
    path("notes/browse", views.browse_notes),
    path("notes/json", views.browse_notes_json),
    path("notes/<int:noteid>/<path>", views.note.as_view()),
    # path('my-notes/get-notes.json', views.do_mynotes.do_get_json),
    # path('my-notes/upload', views.do_mynotes.do_upload),
    # path('my-notes/<noteName>/icon.png', views.do_mynotes.do_get_icon),
]
