from django.contrib import admin

# Register your models here.

from . import models

for name in dir(models):
    try:
        cls = getattr(models, name)
        sub = issubclass(cls, models.models.Model)
        if sub and cls.__module__ == 'school.models':
            admin.site.register(cls)
    except Exception:
        pass
