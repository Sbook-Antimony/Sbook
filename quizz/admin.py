from django.contrib import admin

# Register your models here.

from . import models


admin.site.register(models.Quizz)
admin.site.register(models.QuizzUser)
admin.site.register(models.QuizzAttempt)
