from django.db import models


import school.models as school
import profile_images
import sbook.models as sbook

from mdeditor.fields import MDTextField
# from django.utils.translation import gettext as _


class NoteUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.User,
        related_name="noteAccount",
        on_delete=models.CASCADE,
    )
    starred_notes = models.ManyToManyField(
        'Note',
        related_name='starred_by'
    )

    def __str__(self):
        return f"{self.id}:{self.sbookAccount!s}"


class Bookmark(models.Model):
    note = models.ForeignKey(
        "Note",
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        NoteUser,
        related_name="bookmarks",
        on_delete=models.CASCADE,
    )
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}:{self.position}:{self.note}"


class Note(models.Model):
    title = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    views = models.BigIntegerField(default=0)
    stars = models.IntegerField(default=0)
    profile = models.ImageField(
        upload_to="media/profiles",
        default=profile_images.get_random_file,
    )
    description = MDTextField()
    content = MDTextField()
    redactors = models.ManyToManyField(
        NoteUser,
        related_name="notes",
    )
    classrooms = models.ManyToManyField(
        school.Classroom,
        related_name="notes",
    )
    levels = models.ManyToManyField(
        sbook.Level,
        related_name="notes",
    )
    courses = models.ManyToManyField(
        sbook.Course,
        related_name="notes",
    )
    series = models.ManyToManyField(
        sbook.Serie,
        related_name="notes",
    )

    def __str__(self):
        return f"{self.id}:{self.title}:{self.stars}:{self.views}"


class ShortNote(models.Model):
    title = models.CharField(max_length=255)
    content = MDTextField()
    author = models.ForeignKey(
        NoteUser,
        related_name='short_notes',
        on_delete=models.CASCADE,
    )
    description = MDTextField(default="")
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"ShortNote({self.title=}:{self.author=!s})"
