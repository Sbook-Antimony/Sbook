from . import views
from django.urls import path

# from django.urls import re_path

urlpatterns = [
    path("", views.do_index),
    path("classroom/<int:clsid>.json", views.do_classroom_json),
    path("classroom/profile/<int:clsid>.png", views.do_classroom_profile),
    path("classrooms.json", views.do_all_classrooms),
    path("classroom/browse", views.do_classroom_browse),
]
