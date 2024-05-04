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
    re_path('djga/', include('google_analytics.urls')),
    path('admin/', admin.site.urls),
    path('csrf/', views.do_csrf),
    path('', views.do_index),
    path('css/<name>', views.do_css),
    path('js/<name>', views.do_js),
    path('image/<name>', views.do_image),
    path('login/', views.do_login),
    path('signup/', views.do_signup),
    path('dashboard/', views.do_config),
    path('dashboard/<cmd>', views.do_cmd),
    path('images/profile', views.do_profile),
    path('note/', include('note.urls')),
    path('chatty/', include('chatty.urls')),
]
