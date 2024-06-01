from django.urls import path

from . import views

urlpatterns = [
    path('', views.do_index),
    path('new', views.do_new),
    path('profiles/quizzes/<int:quizzid>.png', views.profiles.quizzes),
    path('quizzes/<int:quizzid>/preview/', views.preview_quizz),
    path('quizzes/<int:quizzid>/attempt/', views.attempt_quizz),
    path('quizzes/<int:quizzid>/attempts/', views.view_quizz_attempts),
    path('quizzes/<int:quizzid>/submit/', views.submit_quizz),
    path(
        'quizzes/<int:quizzid>/attempts/<int:attemptid>/review/',
        views.review_attempt,
    ),
    path(
        'quizzes/<int:quizzid>/attempts/<int:attemptid>/remarks/',
        views.review_attempt_review,
    ),
    path(
        'quizzes/<int:quizzid>/attempts/<int:attemptid>/review/submit/',
        views.review_attempt_submit,
    ),
]
