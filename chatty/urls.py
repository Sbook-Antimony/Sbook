"""
URL configuration for chatty project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from chatty import views
from chatty.accounts import check_login as logc
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', logc(views.index)),
    path('rooms/create', logc(views.room_create.as_view())),
    path('rooms/<int:roomid>/messages/', logc(views.room.as_view())),
    path('rooms/<int:roomid>/messages/send-message/', logc(views.send_message))
]
