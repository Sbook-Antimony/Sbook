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
    stars = models.DecimalField(default=0.0)
    starred = models.BigIntegerField(default=0)

class Bookmark(models.model):
    note = models.ForeignKey(
        "Note",
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "NoteUser",
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    position = models.BigIntegerField()
        

class Note(models.Model):
    title = models.CharField(max_length=255)
    redactors = models.ManyToManyField(
        NoteUser,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    views = models.BigIntegerField(default=0)
    stars = models.DecimalField(default=0.0)
    starred = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255)

