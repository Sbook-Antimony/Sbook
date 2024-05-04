from django.contrib import admin
from .models import *

class ChattyUserAdmin(admin.ModelAdmin):
    list_display = ('sbookAccount', 'id', 'rooms',)


# Register your models here.
admin.site.register(ChattyUser, ChattyUserAdmin)
admin.site.register(ChattyRoom)
admin.site.register(ChattyTextMessage)
