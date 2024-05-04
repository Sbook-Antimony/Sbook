from django.db import models
import chatty.models as chatty
class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()

    chatty = models.ForeignKey(chatty.ChattyUser, related_name="sbook", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}:{self.email}"
