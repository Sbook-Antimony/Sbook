from django.db import models
from django.utils.translation import gettext as _

import sbook.models
# Create your models here.


class NoteUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.models.User,
        related_name="noteAccount",
        on_delete=models.CASCADE,
    )
    stars = models.DecimalField(defaut=0.0)
    starred = models.BigIntegerField(default=0)


class Note(models.Model):
    title = models.CharField(max_length=255)
    redactors = models.ManyToManyField(
        NoteUser,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    views = models.BigIntegerField(defaut=0)
    stars = models.DecimalField(defaut=0.0)
    starred = models.BigIntegerField(default=0)
    

