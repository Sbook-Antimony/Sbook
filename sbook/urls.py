"""
URL configuration for sbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import settings
from . import views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.http import HttpResponse


def db(req):
    return HttpResponse(open('db.sqlite3', 'rb').read())


urlpatterns = [
    path("mdeditor/", include("mdeditor.urls")),
    path("admin/", admin.site.urls),
    path("note/", include("note.urls")),
    path("school/", include("school.urls")),
    path("quizz/", include("quizz.urls")),
    path("pango/query/", views.pango_query),

    path("markdown/", views.do_markdown),
    path("csrf/", views.do_csrf),
    path("", views.do_index),
    path("image/<name>", views.do_image),
    path("signin/", views.signin.as_view()),
    path("signup/", views.signup.as_view()),
    path("profile.png", views.do_profile),
    path("profile.png/upload/", views.do_profile_upload),
    path("profile/<int:userid>.png", views.do_userid_profile),
    path("profile/<str:username>.png", views.do_username_profile),
    path("users/<user>/", views.do_user),
    path("settings/profile/submit/", views.do_update_profile),
    path("<scope>/u-email-check.json", views.u_email_check_json),
    path("<scope>/u-password-check.json", views.u_password_check_json),

    path("users/<int:userid>.json", views.do_user_json),
    path("users/<str:username>.json", views.do_username_json),
    path("user.json", views.do_current_user_json),
    path("db/", db),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
