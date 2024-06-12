from . import views
from django.urls import path

# from django.urls import re_path

urlpatterns = [
    path('', views.do_index),
]
