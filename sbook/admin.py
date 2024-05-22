from django.contrib import admin
from .models import User, Serie, Level, Course


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "password")


admin.site.register(User, UserAdmin)
admin.site.register(Serie)
admin.site.register(Level)
admin.site.register(Course)
