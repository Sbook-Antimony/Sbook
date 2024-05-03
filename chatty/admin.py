from django.contrib import admin
from .models import *

class ChattyUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "password",)


# Register your models here.
admin.site.register(ChattyUser, ChattyUserAdmin)
admin.site.register(ChattyRoom)
admin.site.register(ChattyTextMessage)
