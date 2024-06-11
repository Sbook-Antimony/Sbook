from .models import Course
from .models import Level
from .models import Serie
from .models import User
from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "password")
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget,
        },
    }


admin.site.register(User, UserAdmin)
admin.site.register(Serie)
admin.site.register(Level)
admin.site.register(Course)
