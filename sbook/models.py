from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    bio = models.CharField(max_length=1023)
    profile = models.ImageField(upload_to='profiles', null=True)

    def __str__(self):
        return f"{self.id}:{self.name}:{self.email}"


class Serie(models.Model):
    levels = models.ManyToManyField(
        'Level',
        related_name="series",
    )
    profile = models.ImageField(upload_to='profiles')
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.id}:{self.name}'


class Level(models.Model):
    position = models.IntegerField()
    name = models.CharField(max_length=32)
    profile = models.ImageField(upload_to='profiles')

    def __str__(self):
        return f'{self.id}:{self.position}:{self.name}'


class Course(models.Model):
    name = models.CharField(max_length=32)
    profile = models.ImageField(upload_to='profiles')
    levels = models.ManyToManyField(
        Level,
        related_name="courses",
    )
    series = models.ManyToManyField(
        Serie,
        related_name="courses",
    )
    def __str__(self):
        return f'{self.id}:{self.name}'
