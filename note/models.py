from django.db import models


import sbook.models as sbook
import classroom.models as classroom
# from django.utils.translation import gettext as _


class NoteUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.User,
        related_name="noteAccount",
        on_delete=models.CASCADE,
    )
    stars = models.DecimalField(default=0.0, decimal_places=5, max_digits=6)
    starred = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.id}:{self.sbookAccount}:{self.stars}'

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

    def __str__(self):
        return f'{self.id}:{self.position}:{self.note}'

class Note(models.Model):
    title = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    views = models.BigIntegerField(default=0)
    stars = models.DecimalField(default=0.0, decimal_places=5, max_digits=6)
    profile = models.ImageField(upload_to='profiles', null=True)
    starred = models.BigIntegerField(default=0)
    description = models.TextField()
    redactors = models.ManyToManyField(
        NoteUser,
        related_name="notes",
    )
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

    def __str__(self):
        return f'{self.id}:{self.title}:{self.stars}:{self.views}'
