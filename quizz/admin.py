from . import models
from django.contrib import admin
from martor.widgets import AdminMartorWidget
from django.db.models import TextField


class MDAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {
            "widget": AdminMartorWidget,
        },
    }


admin.site.register(models.Quizz, MDAdmin)
admin.site.register(models.QuizzUser, MDAdmin)
admin.site.register(models.QuizzAttempt, MDAdmin)
