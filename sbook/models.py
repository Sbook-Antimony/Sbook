from django.db import models
from mdeditor.fields import MDTextField


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    bio = MDTextField()
    profile = models.ImageField(upload_to="profiles")

    def __str__(self):
        return f"{self.id}:{self.name}:{self.email}"


class Serie(models.Model):
    profile = models.ImageField(upload_to="profiles")
    name = models.CharField(max_length=32)
    description = MDTextField()

    def __str__(self):
        return f"{self.id}:{self.name}"


class Level(models.Model):
    series = models.ManyToManyField(
        "Serie",
        related_name="levels",
    )
    position = models.IntegerField()
    name = models.CharField(max_length=32)
    profile = models.ImageField(upload_to="profiles")
    description = MDTextField()

    def __str__(self):
        return f"{self.id}:{self.position}:{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=32)
    profile = models.ImageField(upload_to="profiles")
    description = MDTextField()
    levels = models.ManyToManyField(
        Level,
        related_name="courses",
        default=[],
    )
    series = models.ManyToManyField(
        Serie,
        related_name="courses",
        default=[],
    )

    def __str__(self):
        return f"{self.id}:{self.name}"
