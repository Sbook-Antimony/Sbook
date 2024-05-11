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
from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    #re_path('djga/', include('google_analytics.urls')),
    path('admin/', admin.site.urls),
    path('csrf/', views.do_csrf),
    path('', views.do_index),
    path('image/<name>', views.do_image),
    path('signin/', views.signin.as_view()),
    path('signup/', views.signup.as_view()),
    path('dashboard/<cmd>', views.do_cmd),
    path('profile.png', views.do_profile),

    path('<scope>/u-email-check.json', views.u_email_check_json),
    path('<scope>/u-password-check.json', views.u_password_check_json),
    
    path('note/', include('note.urls')),
    path('chatty/', include('chatty.urls')),
]
