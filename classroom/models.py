from django.db import models

import sbook.models as sbook

# Create your models here.

class Classroom(models.Model)
    name = models.CharField(max_length=255)
    profile = models.ImageField()
    description = models.CharField(max_length=255)
    levels = models.ManyToManyField(
        sbook.Level,
        related_name='classrooms',
    )
    courses = models.ManyToManyField(
        sbook.Course,
        related_name='classrooms',
    )
