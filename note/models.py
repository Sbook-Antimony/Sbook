from django.db import models
from django.utils.translation import gettext as _

import sbook.models as sbook
import classroom.models as classroom
# Create your models here.


class NoteUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.User,
        related_name="noteAccount",
        on_delete=models.CASCADE,
    )
    stars = models.DecimalField(default=0.0, decimal_places=5, max_digits=6)
    starred = models.BigIntegerField(default=0)

class Bookmark(models.Model):
    note = models.ForeignKey(
        "Note",
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        NoteUser,
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    position = models.BigIntegerField()
        

class Note(models.Model):
    title = models.CharField(max_length=255)
    redactors = models.ManyToManyField(
        NoteUser,
        related_name="notes",
    )
    views = models.BigIntegerField(default=0)
    stars = models.DecimalField(default=0.0, decimal_places=5, max_digits=6)
    starred = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255)
    classrooms = models.ManyToManyField(
        classroom.Classroom,
        related_name='notes',
    )
    levels = models.ManyToManyField(
        sbook.Level,
        related_name='notes',
    )
    courses = models.ManyToManyField(
        sbook.Course,
        related_name='notes',
    )

