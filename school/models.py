import profile_images
import sbook.models as sbook

from django.db import models
from mdeditor.fields import MDTextField


class Classroom(models.Model):
    name = models.CharField(max_length=64)
    school = models.ForeignKey(
        'School',
        related_name='classrooms',
        on_delete=models.CASCADE,
    )
    profile = models.ImageField(
        upload_to="profiles/classroom",
        default=profile_images.get_random_file,
    )
    description = MDTextField()
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
    series = models.ManyToManyField(
        "sbook.Serie",
        related_name="classrooms",
    )
    teachers = models.ManyToManyField(
        sbook.User,
        related_name='teaches_classrooms'
    )
    students = models.ManyToManyField(
        sbook.User,
        related_name='teached_classrooms'
    )
    admins = models.ManyToManyField(
        sbook.User,
        related_name="admins_classrooms",
    )
    code_of_conduct = MDTextField()

    def __str__(self):
        return f"{self.id}:{self.name}"


class School(models.Model):
    profile = models.ImageField(
        upload_to="profiles/school",
        default=profile_images.get_random_file,
    )
    description = MDTextField()
    name = models.CharField(max_length=64)
    hidden = models.BooleanField()
    teachers = models.ManyToManyField(
        sbook.User,
        related_name='teaches_schools'
    )
    students = models.ManyToManyField(
        sbook.User,
        related_name='teached_schools'
    )
    admins = models.ManyToManyField(
        sbook.User,
        related_name="admins_schools",
    )
    code_of_conduct = MDTextField()
