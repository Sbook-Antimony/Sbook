from django.db import models

import classroom.models as classroom

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    bio = models.CharField(max_length=1023)
    
    def __str__(self):
        return f"{self.name}:{self.email}"
    profile = models.ImageField()
class Serie(models.Model):
    levels = models.ManyToManyField(
        'Level',
        related_name="series",
    )
    profile = models.ImageField()
class Level(models.Model):
    position = models.IntegerField()
    name = models.CharField(max_length=32)
    profile = models.ImageField()
    
class Course(models.Model):
    name = models.CharField(max_length=32)
    profile = models.ImageField()
    levels = models.ManyToManyField(
        Level,
        related_name="courses",
    )    

        
