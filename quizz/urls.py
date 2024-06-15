from django.urls import path

from . import views

urlpatterns = [
    path("", views.do_index),
    path("new", views.do_new),
    path("new/submit/", views.do_new_submit),
    path("profiles/quizzes/<int:quizzid>.png", views.profiles.quizzes),
    path("users/<userid>/quizzes.json", views.do_quizzes_json),
    path("users/<userid>/attempts.json", views.do_user_attempts_json),
    path("users/<userid>/stars.json", views.do_user_stars_json),
    path("users/<userid>.json", views.do_user_json),
    path("user.json", views.do_current_user_json),
    path("quizzes/<int:quizzid>/preview/", views.preview_quizz),
    path("quizzes/<int:quizzid>/attempt/", views.attempt_quizz),
    path("quizzes/<int:quizzid>/attempts/", views.view_quizz_attempts),
    path("quizzes/<int:quizzid>/submit/", views.submit_quizz),
    path("quizzes/<int:quizzid>.json", views.do_quizz_json),
    path("browse", views.do_quizz_browse),
    path("quizzes.json", views.do_all_quizz_json),
    path(
        "quizzes/<int:quizzid>/attempts/<int:attemptid>/review/",
        views.review_attempt,
    ),
    path(
        "quizzes/<int:quizzid>/attempts/<int:attemptid>/remarks/",
        views.review_attempt_review,
    ),
    path(
        "quizzes/<int:quizzid>/attempts/<int:attemptid>/review/submit/",
        views.review_attempt_submit,
    ),
]
