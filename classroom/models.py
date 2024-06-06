from django.db import models

import sbook.models as sbook

# Create your models here.


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    profile = models.ImageField()
    description = models.TextField()
    members = models.ManyToManyField(
        sbook.User,
        related_name="classrooms",
    )
    levels = models.ManyToManyField(
        "sbook.Level",
        related_name="classrooms",
    )
    courses = models.ManyToManyField(
        "sbook.Course",
        related_name="classrooms",
    )

    def __str__(self):
        return f"{self.id}:{self.name}"
