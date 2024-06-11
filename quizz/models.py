from django.db import models

import classroom.models as classroom
import sbook.models as sbook

from mdeditor.fields import MDTextField


class QuizzUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.User, related_name="quizzAccount", on_delete=models.CASCADE
    )
    stars = models.IntegerField()
    starred_users = models.ManyToManyField(
        'self',
        related_name='starred_by',
    )
    starred_quizzes = models.ManyToManyField(
        'Quizz',
        related_name='starred_by',
    )

    def __str__(self):
        return "QuizzUser(%s)" % self.sbookAccount


class QuizzAttempt(models.Model):
    quizz = models.ForeignKey(
        "Quizz",
        on_delete=models.CASCADE,
        related_name="answer_attempts",
    )
    author = models.ForeignKey(
        QuizzUser,
        on_delete=models.CASCADE,
        related_name="quizz_attempts",
    )
    answers = models.JSONField()
    remarks = MDTextField(default="")
    remarked = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"AnswerAttempt({self.id}:{self.remarked})"


class Quizz(models.Model):
    questions = models.JSONField()
    title = models.CharField(max_length=255)
    description = MDTextField()
    prolog = MDTextField()
    epilog = MDTextField()
    instructions = MDTextField()
    profile = models.ImageField(upload_to="profiles")
    is_private = models.BooleanField(default=False)
    authors = models.ManyToManyField(
        QuizzUser,
        related_name="quizzes",
    )
    classrooms = models.ManyToManyField(
        classroom.Classroom,
        related_name="quizzes"
    )
    levels = models.ManyToManyField(sbook.Level, related_name="quizzes")
    courses = models.ManyToManyField(sbook.Course, related_name="quizzes")
    series = models.ManyToManyField(sbook.Serie, related_name="quizzes")
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}:{self.title}"
