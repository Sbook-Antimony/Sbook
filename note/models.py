from django.db import models

import sbook.models
# Create your models here.


class NoteUser(models.Model):
    sbookAccount = models.ForeignKey(
        sbook.models.User,
        related_name="noteAccount",
        on_delete=models.CASCADE,
    )
    
class Note(Model):
    title = models.CharField(max_length=255)
    redactor = ForeignKey(
        NoteUser,
        on_delete=CASCADE,
        related_name="notes"
    )
    

