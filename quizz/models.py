from django.db import models

import sbook.models as sbook
import classroom.models as classroom


class QuizzUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.User,
        related_name='quizzAccount',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "QuizzUser(%s)" % self.sbookAccount


class Quizz(models.Model):
    data = models.JSONField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    profile = models.ImageField(upload_to='profiles')
    is_private = models.BooleanField(default=False)
    authors = models.ManyToManyField(
        QuizzUser,
        related_name='quizzes',
    )
    classrooms = models.ManyToManyField(
        classroom.Classroom,
        related_name='quizzes'
    )
    levels = models.ManyToManyField(
        sbook.Level,
        related_name='quizzes'
    )
    couses = models.ManyToManyField(
        sbook.Course,
        related_name='quizzes'
    )

    def __str__(self):
        return f'{self.id}:{self.title}'
