from django.urls import path

from . import views

urlpatterns = [
    path('', views.do_index),
    path('profiles/quizzes/<int:quizzid>.png', views.profiles.quizzes),
    path('quizzes/<int:quizzid>/preview/', views.preview_quizz),
    path('quizzes/<int:quizzid>/attempt/', views.attempt_quizz),
    path('quizzes/<int:quizzid>/submit/', views.submit_quizz)
]
