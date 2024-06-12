from django.contrib import admin
import note.models

# Register your models here.

admin.site.register(note.models.Bookmark)
admin.site.register(note.models.NoteUser)
admin.site.register(note.models.Note)
