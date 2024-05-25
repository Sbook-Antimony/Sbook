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


class QuizzAnswerAttempt(models.Model):
    quizz = models.ForeignKey(
        'Quizz',
        on_delete=models.CASCADE,
        related_name='answer_attempts',
    )
    author = models.ForeignKey(
        QuizzUser,
        on_delete=models.CASCADE,
        related_name='answer_attempts',
    )
    answers = models.JSONField()
    remark = models.JSONField(default=None)
    remarked = models.BooleanField(default=False)

    def __str__(self):
        return f'AnswerAttempt({self.id}:{self.remarked})'


class Quizz(models.Model):
    data = models.JSONField()
    title = models.CharField(max_length=255)
    description = models.TextField()
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
    courses = models.ManyToManyField(
        sbook.Course,
        related_name='quizzes'
    )

    def __str__(self):
        return f'{self.id}:{self.title}'
