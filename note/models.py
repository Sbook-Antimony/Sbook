from django.db.models import *

# Create your models here.


class NoteUser(Model):
    pass
    
class Note(Model):
    redactor = ForeignKey(
        NoteUser,
        on_delete=CASCADE,
        related_name="notes"
    )
    

