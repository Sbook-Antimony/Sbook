import profile_images

from django.db import models
from mdeditor.fields import MDTextField


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = MDTextField()
    profile = models.ImageField(
        upload_to="profiles/user",
        default=profile_images.get_random_file,
    )
    role = models.ForeignKey(
        "school.UserRole",
        related_name='users',
        default=1,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.id}:{self.name}:{self.email}"


class Serie(models.Model):
    profile = models.ImageField(
        upload_to="profiles/series",
        default=profile_images.get_random_file,
    )
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
    profile = models.ImageField(
        upload_to="profiles/levels",
        default=profile_images.get_random_file,
    )
    description = MDTextField()

    def __str__(self):
        return f"{self.id}:{self.position}:{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=32)
    profile = models.ImageField(
        upload_to="profiles/courses",
        default=profile_images.get_random_file,
    )
    description = MDTextField()
    levels = models.ManyToManyField(
        Level,
        related_name="courses",
    )
    series = models.ManyToManyField(
        Serie,
        related_name="courses",
    )

    def __str__(self):
        return f"Course({self.id}:{self.name})"


class Topic(models.Model):
    name = models.CharField(max_length=32)
    profile = models.ImageField(
        upload_to="profiles/topics",
        default=profile_images.get_random_file,
    )
    description = MDTextField()
    course = models.ManyToManyField(
        Course,
        related_name="topics",
    )

    def __str__(self):
        return f"Topic({self.id}:{self.name})"


class Event(models.Model):
    EVENT_TYPES = {
        "c:n": "note creation",
        "m:n": "note editing",
        "s:n": "note starring",
        "d:n": "note deletion",
        "vc:n": "note visibility change",
        "c:q": "quizz creation",
        "a:q": "quizz attempt",
        "d:q": "quizz deletion",
        "s:q": "quizz starring",
        "c:c": "classroom creation",
        "c:s": "school creation",
        "msg": "message",
        "c:a": "account creation",
        "m:a": "account modification",
    }.items()
    event_type = models.CharField(
        max_length=8,
        choices=EVENT_TYPES,
        editable=False,
    )
    params = models.JSONField()
